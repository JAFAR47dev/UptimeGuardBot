#handlers/monitors.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters
)

from db.database import (
    add_monitor, get_monitors, delete_monitor,
    count_monitors, is_pro, get_uptime_percent
)

from db.database import (
    add_monitor, get_all_monitors, delete_monitor,
    count_monitors, is_pro, get_uptime_percent,
    pause_monitor, resume_monitor, url_exists,
    set_response_threshold, clear_response_threshold,
    get_monitor
)
from services.scheduler import schedule_monitor, schedule_ssl_check
from config import FREE_LIMIT
from services.checker import is_valid_url_format, verify_url_reachable
from db.database import url_exists
import time

# { user_id: last_add_attempt_timestamp }
_add_cooldowns: dict[int, float] = {}
ADD_COOLDOWN_SECONDS = 10


def _is_rate_limited(user_id: int) -> tuple[bool, int]:
    """
    Returns (is_limited, seconds_remaining).
    Enforces a per-user cooldown on /add entry.
    """
    now  = time.monotonic()
    last = _add_cooldowns.get(user_id, 0)
    diff = now - last
    if diff < ADD_COOLDOWN_SECONDS:
        remaining = int(ADD_COOLDOWN_SECONDS - diff)
        return True, remaining
    return False, 0


def _stamp_cooldown(user_id: int):
    """Record that user just triggered /add."""
    _add_cooldowns[user_id] = time.monotonic()
    
ASK_URL, ASK_LABEL = range(2)

# --- /add flow ---
async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle both command and callback query entry points
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    # Rate limit check
    limited, remaining = _is_rate_limited(user_id)
    if limited:
        await reply_fn(
            f"⏳ Please wait <b>{remaining}s</b> before adding another monitor.",
            parse_mode="HTML"
        )
        return ConversationHandler.END

    # Plan limit check
    count = count_monitors(user_id)
    pro   = is_pro(user_id)
    if not pro and count >= FREE_LIMIT:
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")
        ]])
        await reply_fn(
            f"⚠️ Free plan allows <b>{FREE_LIMIT} monitors</b>.\n\n"
            f"Upgrade to Pro for unlimited monitors.",
            parse_mode="HTML",
            reply_markup=keyboard
        )
        return ConversationHandler.END

    # Stamp cooldown only after passing all checks
    _stamp_cooldown(user_id)

    await reply_fn(
        "🌐 Send me the URL to monitor.\n\n"
        "Example: <code>https://mysite.com</code>",
        parse_mode="HTML"
    )
    return ASK_URL
    

async def received_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url     = update.message.text.strip()
    user_id = update.effective_user.id

    # Normalise — add https if no scheme given
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # 1. Format check
    if not is_valid_url_format(url):
        await update.message.reply_text(
            "⚠️ That doesn't look like a valid URL.\n\n"
            "Please send a full URL like:\n"
            "<code>https://mysite.com</code>",
            parse_mode="HTML"
        )
        return ASK_URL  # stay in same state, let them try again

    # 2. Duplicate check
    if url_exists(user_id, url):
        await update.message.reply_text(
            f"⚠️ You're already monitoring <code>{url}</code>\n\n"
            f"Use /list to see your active monitors.",
            parse_mode="HTML"
        )
        return ConversationHandler.END

    # 3. Reachability check — show typing indicator while we probe
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    probe = await verify_url_reachable(url)
    if not probe["reachable"]:
        await update.message.reply_text(
            f"❌ <b>Could not reach that URL.</b>\n\n"
            f"Error: {probe['error']}\n\n"
            f"Double-check the URL and try again, or send a different URL.",
            parse_mode="HTML"
        )
        return ASK_URL  # let them retry rather than killing the conversation

    # All good — store and move to label step
    context.user_data["new_url"] = url
    await update.message.reply_text(
        "✅ URL looks good!\n\n"
        "🏷 Give it a label (or /skip to use the URL as label):"
    )
    return ASK_LABEL
    
async def received_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    label   = update.message.text.strip()
    url     = context.user_data["new_url"]
    user_id = update.effective_user.id
    pro     = is_pro(user_id)
    interval = 1 if pro else 5

    monitor_id = add_monitor(user_id, url, label, interval)
    schedule_monitor(context.application, monitor_id, interval)
    schedule_ssl_check(context.application, monitor_id)

    await update.message.reply_text(
        f"✅ <b>Monitor added!</b>\n\n"
        f"🏷 Label: {label}\n"
        f"🌐 URL: {url}\n"
        f"⏱ Check interval: every {interval} min\n\n"
        f"I'll alert you instantly if it goes down.",
        parse_mode="HTML"
    )
    return ConversationHandler.END

async def skip_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url     = context.user_data["new_url"]
    user_id = update.effective_user.id
    pro     = is_pro(user_id)
    interval = 1 if pro else 5

    monitor_id = add_monitor(user_id, url, url, interval)
    schedule_monitor(context.application, monitor_id, interval)
    schedule_ssl_check(context.application, monitor_id)

    await update.message.reply_text(
        f"✅ <b>Monitor added!</b>\n\n"
        f"🌐 {url}\n"
        f"⏱ Every {interval} min\n\n"
        f"You'll be alerted instantly on downtime.",
        parse_mode="HTML"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

# --- /list ---

async def list_monitors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id  = update.effective_user.id
    monitors = get_all_monitors(user_id)  # includes paused

    if not monitors:
        await update.message.reply_text(
            "You have no monitors yet.\n\nUse /add to add one."
        )
        return

    text = "📋 <b>Your Monitors:</b>\n\n"
    for m in monitors:
        is_paused = m["active"] == 2
        if is_paused:
            status_icon = "⏸"
        elif m["last_status"] == "up":
            status_icon = "🟢"
        elif m["last_status"] == "down":
            status_icon = "🔴"
        else:
            status_icon = "⚪"

        label      = m["label"] or m["url"]
        uptime     = get_uptime_percent(m["id"]) if not is_paused else "—"
        uptime_str = f"{uptime}%" if uptime != "—" else "—"
        threshold  = m["response_threshold_ms"]
        threshold_str = f"{threshold}ms" if threshold else "not set"

        text += (
            f"{status_icon} <b>{label}</b>"
            f"{' (paused)' if is_paused else ''}\n"
            f"   🌐 {m['url']}\n"
            f"   📊 Uptime (7d): {uptime_str}\n"
        )
        if is_pro(user_id):
            text += f"   🐢 Slow alert: {threshold_str}\n"
        text += "\n"

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=_build_list_keyboard(monitors, is_pro(user_id))
    )


def _build_list_keyboard(monitors: list, pro: bool) -> InlineKeyboardMarkup:
    """Build per-monitor action buttons."""
    buttons = []
    for m in monitors:
        label     = (m["label"] or m["url"])[:18]
        is_paused = m["active"] == 2

        row = []
        if is_paused:
            row.append(InlineKeyboardButton(
                f"▶️ Resume {label}", callback_data=f"resume_{m['id']}"
            ))
        else:
            row.append(InlineKeyboardButton(
                f"⏸ Pause {label}", callback_data=f"pause_{m['id']}"
            ))

        row.append(InlineKeyboardButton(
            "🗑", callback_data=f"del_{m['id']}"
        ))

        if pro:
            row.append(InlineKeyboardButton(
                "🐢 Threshold", callback_data=f"threshold_{m['id']}"
            ))

        buttons.append(row)
    return InlineKeyboardMarkup(buttons)
    
async def pause_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    user_id    = query.from_user.id

    pause_monitor(monitor_id, user_id)

    # Stop the scheduler job
    for job in context.application.job_queue.get_jobs_by_name(
        f"monitor_{monitor_id}"
    ):
        job.schedule_removal()

    await query.answer("Monitor paused.")
    await query.edit_message_text(
        "⏸ <b>Monitor paused.</b>\n\n"
        "Your history is preserved. Use /list to resume.",
        parse_mode="HTML"
    )


async def resume_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    user_id    = query.from_user.id

    resume_monitor(monitor_id, user_id)

    # Restart scheduler
    monitor  = get_monitor(monitor_id)
    interval = monitor["interval_minutes"]
    schedule_monitor(context.application, monitor_id, interval)
    schedule_ssl_check(context.application, monitor_id)

    await query.answer("Monitor resumed.")
    await query.edit_message_text(
        "▶️ <b>Monitor resumed.</b>\n\n"
        "Checks are running again.",
        parse_mode="HTML"
    )

async def delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """First tap — ask for confirmation."""
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    monitor    = get_monitor(monitor_id)

    if not monitor:
        await query.answer("Monitor not found.")
        return

    label = monitor["label"] or monitor["url"]

    await query.answer()
    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ Yes, delete it",
                    callback_data=f"confirmdelete_{monitor_id}"
                ),
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data=f"canceldelete_{monitor_id}"
                )
            ]
        ])
    )
    await query.message.reply_text(
        f"⚠️ <b>Delete {label}?</b>\n\n"
        f"🌐 {monitor['url']}\n\n"
        f"This will permanently remove the monitor "
        f"and all its history. This cannot be undone.\n\n"
        f"<i>Tip: use ⏸ Pause instead to keep your history.</i>",
        parse_mode="HTML"
    )


async def confirm_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Second tap — actually delete."""
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    user_id    = query.from_user.id
    monitor    = get_monitor(monitor_id)
    label      = (monitor["label"] or monitor["url"]) if monitor else "Monitor"

    delete_monitor(monitor_id, user_id)

    # Stop scheduler job
    for job in context.application.job_queue.get_jobs_by_name(
        f"monitor_{monitor_id}"
    ):
        job.schedule_removal()

    # Stop SSL job too
    for job in context.application.job_queue.get_jobs_by_name(
        f"ssl_{monitor_id}"
    ):
        job.schedule_removal()

    await query.answer("Monitor deleted.")
    await query.edit_message_text(
        f"🗑 <b>{label}</b> has been deleted.",
        parse_mode="HTML"
    )


async def cancel_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User changed their mind — dismiss the confirmation."""
    query = update.callback_query
    await query.answer("Cancelled.")
    await query.edit_message_text(
        "❌ Delete cancelled. Monitor is still active.",
        parse_mode="HTML"
    )
        

add_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("add", add_start),
        CallbackQueryHandler(add_start, pattern="^add_monitor$")
    ],
    states={
        ASK_URL:   [MessageHandler(filters.TEXT & ~filters.COMMAND, received_url)],
        ASK_LABEL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_label),
            CommandHandler("skip", skip_label)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

ASK_THRESHOLD = 10  # new state, outside existing range(2)

async def threshold_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point — ask user for threshold value."""
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    user_id    = query.from_user.id

    if not is_pro(user_id):
        await query.answer("Pro feature only.", show_alert=True)
        return

    monitor = get_monitor(monitor_id)
    label   = monitor["label"] or monitor["url"]
    current = monitor["response_threshold_ms"]
    current_str = f"{current}ms" if current else "not set"

    context.user_data["threshold_monitor_id"] = monitor_id
    await query.message.reply_text(
        f"🐢 <b>Set Slow Response Threshold</b>\n\n"
        f"Monitor: <b>{label}</b>\n"
        f"Current threshold: <b>{current_str}</b>\n\n"
        f"Send the threshold in milliseconds.\n"
        f"Example: <code>2000</code> = alert if response &gt; 2s\n\n"
        f"Or send /clear to remove the threshold.",
        parse_mode="HTML"
    )
    await query.answer()
    return ASK_THRESHOLD


async def received_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text       = update.message.text.strip()
    user_id    = update.effective_user.id
    monitor_id = context.user_data.get("threshold_monitor_id")

    if not monitor_id:
        await update.message.reply_text("Something went wrong. Use /list to try again.")
        return ConversationHandler.END

    try:
        threshold_ms = int(text)
        if threshold_ms < 100:
            await update.message.reply_text(
                "⚠️ Threshold must be at least 100ms. Try again:"
            )
            return ASK_THRESHOLD
        if threshold_ms > 30000:
            await update.message.reply_text(
                "⚠️ Threshold must be under 30000ms (30s). Try again:"
            )
            return ASK_THRESHOLD
    except ValueError:
        await update.message.reply_text(
            "⚠️ Please send a number in milliseconds. Example: <code>2000</code>",
            parse_mode="HTML"
        )
        return ASK_THRESHOLD

    set_response_threshold(monitor_id, user_id, threshold_ms)
    await update.message.reply_text(
        f"✅ <b>Threshold set to {threshold_ms}ms.</b>\n\n"
        f"You'll be alerted whenever response time exceeds this.",
        parse_mode="HTML"
    )
    return ConversationHandler.END


async def clear_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id    = update.effective_user.id
    monitor_id = context.user_data.get("threshold_monitor_id")
    if monitor_id:
        clear_response_threshold(monitor_id, user_id)
    await update.message.reply_text("✅ Threshold removed.")
    return ConversationHandler.END


threshold_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(threshold_callback, pattern="^threshold_")
    ],
    states={
        ASK_THRESHOLD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_threshold),
            CommandHandler("clear", clear_threshold)
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id  = update.effective_user.id
    monitors = get_all_monitors(user_id)

    if not monitors:
        await update.message.reply_text(
            "No monitors yet. Use /add to add your first one."
        )
        return

    lines = ["⚡ <b>Monitor Status</b>\n"]

    for m in monitors:
        label     = m["label"] or m["url"]
        is_paused = m["active"] == 2

        if is_paused:
            icon   = "⏸"
            status_text = "Paused"
        elif m["last_status"] == "up":
            icon   = "🟢"
            status_text = "Up"
        elif m["last_status"] == "down":
            icon   = "🔴"
            status_text = "Down"
        else:
            icon   = "⚪"
            status_text = "Pending first check"

        # Last checked — show relative time
        if m["last_checked"]:
            from datetime import datetime
            last = datetime.fromisoformat(m["last_checked"])
            diff = datetime.now() - last
            mins = int(diff.total_seconds() // 60)
            if mins < 1:
                ago = "just now"
            elif mins == 1:
                ago = "1 min ago"
            elif mins < 60:
                ago = f"{mins} mins ago"
            else:
                hrs = mins // 60
                ago = f"{hrs}h ago"
        else:
            ago = "not checked yet"

        lines.append(f"{icon} <b>{label}</b> — {status_text} <i>({ago})</i>")

    await update.message.reply_text(
        "\n".join(lines),
        parse_mode="HTML"
    )