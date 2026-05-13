# handlers/monitors.py
import asyncio
import aiohttp
import logging
import time
from datetime import datetime
from urllib.parse import urlparse

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters
)
from db.database import (
    add_monitor, mark_monitor_added, get_all_monitors, delete_monitor,
    count_monitors, is_pro, get_uptime_percent,
    pause_monitor, resume_monitor, url_exists,
    set_response_threshold, clear_response_threshold,
    get_monitor, set_monitor_note, clear_monitor_note,
    set_webhook_url, clear_webhook_url,
    set_keyword, clear_keyword,
    set_confirm_count,
    FREE_CONFIRM_LIMIT, PRO_CONFIRM_LIMIT,
    get_monitor_limit,
    mark_referral_qualified, check_and_apply_referral_reward,
    get_user_language,
)
from services.scheduler import schedule_monitor, schedule_ssl_check
from config import FREE_LIMIT, REFERRAL_BONUS_SLOTS, REFERRAL_TRIAL_DAYS
from services.checker import is_valid_url_format, verify_url_reachable
from locales.monitors_strings import mt

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------

_add_cooldowns: dict[int, float] = {}
ADD_COOLDOWN_SECONDS = 10


def _is_rate_limited(user_id: int) -> tuple[bool, int]:
    now  = time.monotonic()
    last = _add_cooldowns.get(user_id, 0)
    diff = now - last
    if diff < ADD_COOLDOWN_SECONDS:
        return True, int(ADD_COOLDOWN_SECONDS - diff)
    return False, 0


def _stamp_cooldown(user_id: int):
    _add_cooldowns[user_id] = time.monotonic()


# ---------------------------------------------------------------------------
# Conversation states — strings to avoid integer collisions
# ---------------------------------------------------------------------------

ASK_URL       = "ASK_URL"
ASK_LABEL     = "ASK_LABEL"
ASK_THRESHOLD = "ASK_THRESHOLD"
ASK_NOTE      = "ASK_NOTE"
ASK_WEBHOOK   = "ASK_WEBHOOK"
ASK_KEYWORD   = "ASK_KEYWORD"
ASK_CONFIRM   = "ASK_CONFIRM"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

async def conversation_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    try:
        reply_fn = (
            update.callback_query.message.reply_text
            if update.callback_query
            else update.message.reply_text
        )
        await reply_fn(
            "⏰ <b>Session expired.</b>\n\n"
            "Your setup session timed out after 5 minutes of inactivity.\n\n"
            "Use the command again to start over.",
            parse_mode="HTML"
        )
    except Exception:
        pass
    return ConversationHandler.END


async def unexpected_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.answer(
            "⚠️ Please complete the current step first.", show_alert=True
        )
    elif update.message:
        await update.message.reply_text(
            "⚠️ I'm waiting for a specific response.\n\nSend /cancel to exit this flow."
        )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    if update.message:
        await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# Referral reward notification
# ---------------------------------------------------------------------------

async def _send_referral_reward_message(bot, referrer_id: int, reward: dict):
    try:
        if reward["type"] == "slots":
            text = (
                f"🎉 <b>Referral reward unlocked!</b>\n\n"
                f"One of your invited friends just added their first monitor.\n\n"
                f"You've earned <b>+{REFERRAL_BONUS_SLOTS} free monitor slots</b>!\n\n"
                f"Keep sharing your referral link to earn more. "
                f"Use /start to see your updated limit."
            )
        else:
            text = (
                f"🎉 <b>Referral reward unlocked!</b>\n\n"
                f"One of your invited friends just added their first monitor.\n\n"
                f"You've earned <b>+{REFERRAL_TRIAL_DAYS} days</b> added to your plan!\n\n"
                f"Keep sharing to earn more."
            )
        await bot.send_message(chat_id=referrer_id, text=text, parse_mode="HTML")
    except Exception as e:
        logger.warning(f"Could not send referral reward to {referrer_id}: {e}")


# ---------------------------------------------------------------------------
# Post-add follow-up job (fires 30s after first monitor is added)
# ---------------------------------------------------------------------------

async def _post_add_followup(context):
    monitor_id = context.job.data["monitor_id"]
    chat_id    = context.job.data["chat_id"]
    user_id    = context.job.data["user_id"]
    try:
        monitor     = get_monitor(monitor_id)
        if not monitor:
            return
        label       = monitor.get("label") or monitor.get("url", "")
        last_status = monitor.get("last_status") or "unknown"
        lang        = get_user_language(user_id)

        if last_status == "up":
            msg = mt(lang, "followup_up", label=label)
        elif last_status == "down":
            msg = mt(lang, "followup_down", label=label)
        else:
            return   # Still unknown — don't send noise

        await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")
    except Exception as e:
        logger.warning(f"_post_add_followup error: {e}")


# ---------------------------------------------------------------------------
# /add conversation
# ---------------------------------------------------------------------------

async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.callback_query:
            user_id  = update.callback_query.from_user.id
            reply_fn = update.callback_query.message.reply_text
            await update.callback_query.answer()
        else:
            user_id  = update.effective_user.id
            reply_fn = update.message.reply_text

        lang = get_user_language(user_id)

        limited, remaining = _is_rate_limited(user_id)
        if limited:
            await reply_fn(
                mt(lang, "add_rate_limit", remaining=remaining),
                parse_mode="HTML"
            )
            return ConversationHandler.END

        count = count_monitors(user_id)
        pro   = is_pro(user_id)
        limit = get_monitor_limit(user_id)

        if not pro and count >= limit:
            bonus     = limit - FREE_LIMIT
            bonus_str = mt(lang, "add_limit_bonus_str", bonus=bonus) if bonus else ""
            await reply_fn(
                mt(lang, "add_limit_reached", limit=limit, bonus_str=bonus_str),
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        mt(lang, "btn_upgrade_pro"),
                        callback_data="upgrade"
                    )
                ]])
            )
            return ConversationHandler.END

        _stamp_cooldown(user_id)
        await reply_fn(mt(lang, "add_ask_url"), parse_mode="HTML")
        return ASK_URL

    except Exception as e:
        logger.error(f"add_start error: {e}", exc_info=True)
        return ConversationHandler.END


async def received_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url     = update.message.text.strip()
        user_id = update.effective_user.id
        lang    = get_user_language(user_id)

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        if not is_valid_url_format(url):
            await update.message.reply_text(
                mt(lang, "add_invalid_url"), parse_mode="HTML"
            )
            return ASK_URL

        if url_exists(user_id, url):
            await update.message.reply_text(
                mt(lang, "add_duplicate_url", url=url), parse_mode="HTML"
            )
            return ConversationHandler.END

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )
        probe = await verify_url_reachable(url)
        if not probe["reachable"]:
            await update.message.reply_text(
                mt(lang, "add_unreachable", error=probe["error"]),
                parse_mode="HTML"
            )
            return ASK_URL

        context.user_data["new_url"] = url
        await update.message.reply_text(mt(lang, "add_url_ok"))
        return ASK_LABEL

    except Exception as e:
        logger.error(f"received_url error: {e}", exc_info=True)
        user_id = update.effective_user.id
        lang    = get_user_language(user_id)
        await update.message.reply_text(mt(lang, "add_something_wrong"))
        return ASK_URL


async def received_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        label   = update.message.text.strip()
        url     = context.user_data.get("new_url")
        user_id = update.effective_user.id
        lang    = get_user_language(user_id)

        if not url:
            await update.message.reply_text(mt(lang, "add_something_wrong"))
            return ConversationHandler.END

        pro      = is_pro(user_id)
        interval = 1 if pro else 5
        is_first = count_monitors(user_id) == 0

        monitor_id = add_monitor(user_id, url, label, interval)
        mark_monitor_added(user_id) 
        schedule_monitor(context.application, monitor_id, interval)
        schedule_ssl_check(context.application, monitor_id)

        if is_first:
            referrer_id = mark_referral_qualified(user_id)
            if referrer_id:
                reward = check_and_apply_referral_reward(referrer_id)
                if reward:
                    await _send_referral_reward_message(context.bot, referrer_id, reward)

        context.user_data.clear()

        limit      = get_monitor_limit(user_id)
        active_now = count_monitors(user_id)
        slots_line = (
            mt(lang, "add_slots_line", active=active_now, limit=limit)
            if not pro else ""
        )

        await update.message.reply_text(
            mt(lang, "add_success",
               label=label, url=url, interval=interval, slots_line=slots_line),
            parse_mode="HTML"
        )

        if is_first:
            context.application.job_queue.run_once(
                _post_add_followup,
                when=30,
                data={
                    "monitor_id": monitor_id,
                    "chat_id":    update.effective_chat.id,
                    "user_id":    user_id,
                },
                name=f"followup_{monitor_id}"
            )

        return ConversationHandler.END

    except Exception as e:
        logger.error(f"received_label error: {e}", exc_info=True)
        user_id = update.effective_user.id
        lang    = get_user_language(user_id)
        await update.message.reply_text(mt(lang, "add_something_wrong"))
        return ASK_LABEL


async def skip_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url     = context.user_data.get("new_url")
        user_id = update.effective_user.id
        lang    = get_user_language(user_id)

        if not url:
            await update.message.reply_text(mt(lang, "add_something_wrong"))
            return ConversationHandler.END

        pro      = is_pro(user_id)
        interval = 1 if pro else 5
        is_first = count_monitors(user_id) == 0

        monitor_id = add_monitor(user_id, url, url, interval)
        mark_monitor_added(user_id) 
        schedule_monitor(context.application, monitor_id, interval)
        schedule_ssl_check(context.application, monitor_id)

        if is_first:
            referrer_id = mark_referral_qualified(user_id)
            if referrer_id:
                reward = check_and_apply_referral_reward(referrer_id)
                if reward:
                    await _send_referral_reward_message(context.bot, referrer_id, reward)

        context.user_data.clear()

        await update.message.reply_text(
            mt(lang, "add_success_nolabel", url=url, interval=interval),
            parse_mode="HTML"
        )

        if is_first:
            context.application.job_queue.run_once(
                _post_add_followup,
                when=30,
                data={
                    "monitor_id": monitor_id,
                    "chat_id":    update.effective_chat.id,
                    "user_id":    user_id,
                },
                name=f"followup_{monitor_id}"
            )

        return ConversationHandler.END

    except Exception as e:
        logger.error(f"skip_label error: {e}", exc_info=True)
        return ConversationHandler.END


add_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("add", add_start),
        CallbackQueryHandler(add_start, pattern="^add_monitor$"),
    ],
    states={
        ASK_URL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_url)
        ],
        ASK_LABEL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_label),
            CommandHandler("skip", skip_label),
        ],
        ConversationHandler.TIMEOUT: [
            MessageHandler(filters.ALL, conversation_timeout),
            CallbackQueryHandler(conversation_timeout),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(unexpected_input),
        MessageHandler(filters.ALL, unexpected_input),
    ],
    per_message=False,
    per_chat=True,
    conversation_timeout=300,
)


# ---------------------------------------------------------------------------
# /list
# ---------------------------------------------------------------------------

NOTE_MAX_DISPLAY = 60


async def list_monitors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    lang     = get_user_language(user_id)
    monitors = get_all_monitors(user_id)

    if not monitors:
        await reply_fn(mt(lang, "list_no_monitors"))
        return

    pro  = is_pro(user_id)
    text = mt(lang, "list_header")

    for m in monitors:
        is_paused   = m["active"] == 2
        last_status = m.get("last_status") or "unknown"

        if is_paused:
            status_icon = "⏸"
        elif last_status == "up":
            status_icon = "🟢"
        elif last_status == "down":
            status_icon = "🔴"
        else:
            status_icon = "⚪"

        label         = m.get("label") or m.get("url", "")
        uptime        = get_uptime_percent(m["id"]) if not is_paused else "—"
        uptime_str    = f"{uptime}%" if uptime != "—" else "—"
        threshold     = m.get("response_threshold_ms")
        threshold_str = f"{threshold}ms" if threshold else mt(lang, "list_threshold_none")
        note          = m.get("note") or ""
        note_display  = (note[:NOTE_MAX_DISPLAY] + "…") if len(note) > NOTE_MAX_DISPLAY else note
        webhook       = m.get("webhook_url") or ""
        keyword       = m.get("keyword") or ""
        confirm       = m.get("confirm_count") or 1
        paused_suffix = mt(lang, "list_paused_suffix") if is_paused else ""

        text += (
            f"{status_icon} <b>{label}</b>{paused_suffix}\n"
            f"   🌐 <code>{m.get('url', '')}</code>\n"
            + mt(lang, "list_uptime", uptime_str=uptime_str)
        )
        if note_display:
            text += f"   📝 <i>{note_display}</i>\n"
        if keyword:
            case_str = mt(lang, "list_keyword_cs") if m.get("keyword_case_sensitive") else ""
            text += mt(lang, "list_keyword", keyword=keyword, case_str=case_str)
        if confirm > 1:
            text += mt(lang, "list_confirms", count=confirm)
        if pro:
            text += mt(lang, "list_threshold", threshold_str=threshold_str)
        if pro and webhook:
            domain = urlparse(webhook).netloc or webhook
            text += mt(lang, "list_webhook", domain=domain)
        text += "\n"

    await reply_fn(
        text,
        parse_mode="HTML",
        reply_markup=_build_list_keyboard(monitors, pro, lang)
    )


def _build_list_keyboard(monitors: list, pro: bool, lang: str) -> InlineKeyboardMarkup:
    buttons = []
    for m in monitors:
        label     = (m.get("label") or m.get("url", ""))[:18]
        is_paused = m["active"] == 2
        has_note  = bool(m.get("note"))
        has_wh    = bool(m.get("webhook_url"))
        has_kw    = bool(m.get("keyword"))

        # Row 1 — pause/resume + delete
        row1 = []
        if is_paused:
            row1.append(InlineKeyboardButton(
                mt(lang, "btn_resume", label=label),
                callback_data=f"resume_{m['id']}"
            ))
        else:
            row1.append(InlineKeyboardButton(
                mt(lang, "btn_pause", label=label),
                callback_data=f"pause_{m['id']}"
            ))
        row1.append(InlineKeyboardButton(
            mt(lang, "btn_delete"), callback_data=f"del_{m['id']}"
        ))
        buttons.append(row1)

        # Row 2 — note | keyword | confirm (all users)
        row2 = [
            InlineKeyboardButton(
                mt(lang, "btn_edit_note") if has_note else mt(lang, "btn_add_note"),
                callback_data=f"note_{m['id']}"
            ),
            InlineKeyboardButton(
                mt(lang, "btn_edit_keyword") if has_kw else mt(lang, "btn_add_keyword"),
                callback_data=f"keyword_{m['id']}"
            ),
            InlineKeyboardButton(
                mt(lang, "btn_confirmations"),
                callback_data=f"confirm_{m['id']}"
            ),
        ]
        buttons.append(row2)

        # Row 3 — Pro-only: threshold + webhook
        if pro:
            row3 = [
                InlineKeyboardButton(
                    mt(lang, "btn_threshold"),
                    callback_data=f"threshold_{m['id']}"
                ),
                InlineKeyboardButton(
                    mt(lang, "btn_edit_webhook") if has_wh else mt(lang, "btn_add_webhook"),
                    callback_data=f"webhook_{m['id']}"
                ),
            ]
            buttons.append(row3)

    return InlineKeyboardMarkup(buttons)


# ---------------------------------------------------------------------------
# Pause / Resume
# ---------------------------------------------------------------------------

async def pause_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    user_id    = query.from_user.id

    pause_monitor(monitor_id, user_id)
    for job in context.application.job_queue.get_jobs_by_name(f"monitor_{monitor_id}"):
        job.schedule_removal()

    await query.answer("Monitor paused.")
    await query.edit_message_text(
        "⏸ <b>Monitor paused.</b>\n\nYour history is preserved. Use /list to resume.",
        parse_mode="HTML"
    )


async def resume_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    user_id    = query.from_user.id

    resume_monitor(monitor_id, user_id)
    monitor  = get_monitor(monitor_id)
    interval = monitor["interval_minutes"]
    schedule_monitor(context.application, monitor_id, interval)
    schedule_ssl_check(context.application, monitor_id)

    await query.answer("Monitor resumed.")
    await query.edit_message_text(
        "▶️ <b>Monitor resumed.</b>\n\nChecks are running again.",
        parse_mode="HTML"
    )


# ---------------------------------------------------------------------------
# Delete (two-step)
# ---------------------------------------------------------------------------

async def delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    monitor    = get_monitor(monitor_id)

    if not monitor:
        await query.answer("Monitor not found.")
        return

    label = monitor.get("label") or monitor.get("url", "")
    await query.answer()
    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "✅ Yes, delete it",
                callback_data=f"confirmdelete_{monitor_id}"
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data=f"canceldelete_{monitor_id}"
            ),
        ]])
    )
    await query.message.reply_text(
        f"⚠️ <b>Delete {label}?</b>\n\n"
        f"🌐 <code>{monitor.get('url', '')}</code>\n\n"
        "This will permanently remove the monitor and all its history.\n\n"
        "<i>Tip: use ⏸ Pause instead to keep your history.</i>",
        parse_mode="HTML"
    )


async def confirm_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    user_id    = query.from_user.id
    monitor    = get_monitor(monitor_id)
    label      = (monitor.get("label") or monitor.get("url", "")) if monitor else "Monitor"

    delete_monitor(monitor_id, user_id)
    for job in context.application.job_queue.get_jobs_by_name(f"monitor_{monitor_id}"):
        job.schedule_removal()
    for job in context.application.job_queue.get_jobs_by_name(f"ssl_{monitor_id}"):
        job.schedule_removal()

    await query.answer("Monitor deleted.")
    await query.edit_message_text(
        f"🗑 <b>{label}</b> has been deleted.", parse_mode="HTML"
    )


async def cancel_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Cancelled.")
    await query.edit_message_text(
        "❌ Delete cancelled. Monitor is still active.", parse_mode="HTML"
    )


# ---------------------------------------------------------------------------
# Threshold conversation
# ---------------------------------------------------------------------------

async def threshold_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query      = update.callback_query
        monitor_id = int(query.data.split("_")[1])
        user_id    = query.from_user.id

        if not is_pro(user_id):
            await query.answer("Pro feature only.", show_alert=True)
            return ConversationHandler.END

        monitor = get_monitor(monitor_id)
        if not monitor or monitor["user_id"] != user_id:
            await query.answer("Monitor not found.", show_alert=True)
            return ConversationHandler.END

        label       = monitor.get("label") or monitor.get("url", "")
        current     = monitor.get("response_threshold_ms")
        current_str = f"{current}ms" if current else "not set"
        context.user_data["threshold_monitor_id"] = monitor_id

        await query.answer()
        await query.message.reply_text(
            f"🐢 <b>Set Slow Response Threshold</b>\n\n"
            f"Monitor: <b>{label}</b>\n"
            f"Current threshold: <b>{current_str}</b>\n\n"
            "Send the threshold in milliseconds.\n"
            "Example: <code>2000</code> = alert if response &gt; 2s\n\n"
            "Send /clear to remove the threshold, or /cancel to abort.",
            parse_mode="HTML"
        )
        return ASK_THRESHOLD

    except Exception as e:
        logger.error(f"threshold_callback error: {e}", exc_info=True)
        return ConversationHandler.END


async def received_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text       = update.message.text.strip()
        user_id    = update.effective_user.id
        monitor_id = context.user_data.get("threshold_monitor_id")

        if not monitor_id:
            await update.message.reply_text("Something went wrong. Use /list to try again.")
            return ConversationHandler.END

        try:
            threshold_ms = int(text)
            if threshold_ms < 100:
                await update.message.reply_text("⚠️ Threshold must be at least 100ms. Try again:")
                return ASK_THRESHOLD
            if threshold_ms > 30_000:
                await update.message.reply_text("⚠️ Threshold must be under 30000ms. Try again:")
                return ASK_THRESHOLD
        except ValueError:
            await update.message.reply_text(
                "⚠️ Please send a number in milliseconds. Example: <code>2000</code>",
                parse_mode="HTML"
            )
            return ASK_THRESHOLD

        set_response_threshold(monitor_id, user_id, threshold_ms)
        context.user_data.clear()
        await update.message.reply_text(
            f"✅ <b>Threshold set to {threshold_ms}ms.</b>\n\n"
            "You'll be alerted whenever response time exceeds this.",
            parse_mode="HTML"
        )
        return ConversationHandler.END

    except Exception as e:
        logger.error(f"received_threshold error: {e}", exc_info=True)
        await update.message.reply_text("⚠️ Something went wrong. Send /cancel and try again.")
        return ASK_THRESHOLD


async def clear_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id    = update.effective_user.id
    monitor_id = context.user_data.get("threshold_monitor_id")
    if monitor_id:
        clear_response_threshold(monitor_id, user_id)
    context.user_data.clear()
    await update.message.reply_text("✅ Threshold removed.")
    return ConversationHandler.END


threshold_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(threshold_callback, pattern="^threshold_")],
    states={
        ASK_THRESHOLD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_threshold),
            CommandHandler("clear", clear_threshold),
        ],
        ConversationHandler.TIMEOUT: [
            MessageHandler(filters.ALL, conversation_timeout),
            CallbackQueryHandler(conversation_timeout),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(unexpected_input),
        MessageHandler(filters.ALL, unexpected_input),
    ],
    per_message=False,
    per_chat=True,
    conversation_timeout=300,
)


# ---------------------------------------------------------------------------
# Note conversation
# ---------------------------------------------------------------------------

NOTE_MAX_LENGTH = 120


async def note_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query      = update.callback_query
        monitor_id = int(query.data.split("_")[1])
        user_id    = query.from_user.id

        monitor = get_monitor(monitor_id)
        if not monitor or monitor["user_id"] != user_id:
            await query.answer("Monitor not found.", show_alert=True)
            return ConversationHandler.END

        context.user_data["note_monitor_id"] = monitor_id
        label   = monitor.get("label") or monitor.get("url", "")
        current = monitor.get("note")

        await query.answer()
        if current:
            await query.message.reply_text(
                f"📝 <b>Edit Note</b>\n\n"
                f"Monitor: <b>{label}</b>\n"
                f"Current note:\n<i>{current}</i>\n\n"
                f"Send a new note to replace it ({NOTE_MAX_LENGTH} chars max).\n"
                "Send /clearnote to remove it, or /cancel to abort.",
                parse_mode="HTML"
            )
        else:
            await query.message.reply_text(
                f"📝 <b>Add Note</b>\n\n"
                f"Monitor: <b>{label}</b>\n\n"
                f"Send a short note ({NOTE_MAX_LENGTH} chars max).\n\n"
                "Example: <i>Client site — call John on +44 7700 if down.</i>\n\n"
                "This note will appear in all down alerts for this monitor.\n"
                "Send /cancel to abort.",
                parse_mode="HTML"
            )
        return ASK_NOTE

    except Exception as e:
        logger.error(f"note_callback error: {e}", exc_info=True)
        return ConversationHandler.END


async def received_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        note       = update.message.text.strip()
        user_id    = update.effective_user.id
        monitor_id = context.user_data.get("note_monitor_id")

        if not monitor_id:
            await update.message.reply_text("Something went wrong. Use /list to try again.")
            return ConversationHandler.END

        if len(note) > NOTE_MAX_LENGTH:
            await update.message.reply_text(
                f"⚠️ Note is too long ({len(note)} chars). "
                f"Keep it under {NOTE_MAX_LENGTH} characters and try again:"
            )
            return ASK_NOTE

        set_monitor_note(monitor_id, user_id, note)
        monitor = get_monitor(monitor_id)
        label   = (monitor.get("label") or monitor.get("url", "")) if monitor else "Monitor"
        context.user_data.clear()

        await update.message.reply_text(
            f"✅ <b>Note saved.</b>\n\n"
            f"🏷 Monitor: <b>{label}</b>\n"
            f"📝 Note: <i>{note}</i>\n\n"
            "This will appear in all down alerts for this monitor.",
            parse_mode="HTML"
        )
        return ConversationHandler.END

    except Exception as e:
        logger.error(f"received_note error: {e}", exc_info=True)
        await update.message.reply_text("⚠️ Something went wrong. Send /cancel and try again.")
        return ASK_NOTE


async def clear_note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id    = update.effective_user.id
    monitor_id = context.user_data.get("note_monitor_id")
    if monitor_id:
        clear_monitor_note(monitor_id, user_id)
        await update.message.reply_text("✅ Note removed.")
    else:
        await update.message.reply_text("No active note session. Use /list to manage notes.")
    context.user_data.clear()
    return ConversationHandler.END


note_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(note_callback, pattern="^note_")],
    states={
        ASK_NOTE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_note),
            CommandHandler("clearnote", clear_note_command),
        ],
        ConversationHandler.TIMEOUT: [
            MessageHandler(filters.ALL, conversation_timeout),
            CallbackQueryHandler(conversation_timeout),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(unexpected_input),
        MessageHandler(filters.ALL, unexpected_input),
    ],
    per_message=False,
    per_chat=True,
    conversation_timeout=300,
)


# ---------------------------------------------------------------------------
# Webhook conversation (Pro only)
# ---------------------------------------------------------------------------

WEBHOOK_MAX_LENGTH = 500


async def webhook_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query      = update.callback_query
        monitor_id = int(query.data.split("_")[1])
        user_id    = query.from_user.id

        if not is_pro(user_id):
            await query.answer("Pro feature only.", show_alert=True)
            return ConversationHandler.END

        monitor = get_monitor(monitor_id)
        if not monitor or monitor["user_id"] != user_id:
            await query.answer("Monitor not found.", show_alert=True)
            return ConversationHandler.END

        context.user_data["webhook_monitor_id"] = monitor_id
        label   = monitor.get("label") or monitor.get("url", "")
        current = monitor.get("webhook_url")

        await query.answer()
        if current:
            await query.message.reply_text(
                f"🔗 <b>Edit Webhook URL</b>\n\n"
                f"Monitor: <b>{label}</b>\n"
                f"Current: <code>{current}</code>\n\n"
                "Send a new URL to replace it, or /clearwebhook to remove it.\n\n"
                "Supports: Slack incoming webhooks, PagerDuty, or any HTTPS endpoint.\n\n"
                "Send /cancel to abort.",
                parse_mode="HTML"
            )
        else:
            await query.message.reply_text(
                f"🔗 <b>Set Webhook URL</b>\n\n"
                f"Monitor: <b>{label}</b>\n\n"
                "Send the HTTPS URL to POST alerts to.\n\n"
                "Works with:\n"
                "• Slack: <code>https://hooks.slack.com/services/…</code>\n"
                "• PagerDuty Events API v2\n"
                "• Any custom HTTPS endpoint\n\n"
                "A JSON payload is sent on every down and recovery event.\n\n"
                "Send /cancel to abort.",
                parse_mode="HTML"
            )
        return ASK_WEBHOOK

    except Exception as e:
        logger.error(f"webhook_callback error: {e}", exc_info=True)
        return ConversationHandler.END


async def received_webhook_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url        = update.message.text.strip()
        user_id    = update.effective_user.id
        monitor_id = context.user_data.get("webhook_monitor_id")

        if not monitor_id:
            await update.message.reply_text("Something went wrong. Use /list to try again.")
            return ConversationHandler.END

        if not url.startswith("https://"):
            await update.message.reply_text(
                "⚠️ Webhook URL must start with <code>https://</code>\n\n"
                "Send a valid HTTPS URL or /cancel to abort.",
                parse_mode="HTML"
            )
            return ASK_WEBHOOK

        if len(url) > WEBHOOK_MAX_LENGTH:
            await update.message.reply_text(
                f"⚠️ URL is too long. Keep it under {WEBHOOK_MAX_LENGTH} characters."
            )
            return ASK_WEBHOOK

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        reachable = False
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    resp = await asyncio.wait_for(
                        session.head(url, allow_redirects=True, ssl=True), timeout=8
                    )
                    reachable = resp.status < 500
                except Exception:
                    try:
                        resp = await asyncio.wait_for(
                            session.get(url, allow_redirects=True, ssl=True), timeout=8
                        )
                        reachable = resp.status < 500
                    except Exception:
                        reachable = False
        except Exception:
            reachable = False

        if not reachable:
            await update.message.reply_text(
                "⚠️ <b>Could not reach that URL.</b>\n\n"
                "Make sure it's a valid, publicly accessible HTTPS endpoint "
                "and try again, or send /cancel to abort.",
                parse_mode="HTML"
            )
            return ASK_WEBHOOK

        set_webhook_url(monitor_id, user_id, url)
        monitor = get_monitor(monitor_id)
        label   = (monitor.get("label") or monitor.get("url", "")) if monitor else "Monitor"
        context.user_data.clear()

        await update.message.reply_text(
            f"✅ <b>Webhook saved!</b>\n\n"
            f"🏷 Monitor: <b>{label}</b>\n"
            f"🔗 <code>{url}</code>\n\n"
            "A JSON POST will be sent to this URL on every down and recovery event.",
            parse_mode="HTML"
        )
        return ConversationHandler.END

    except Exception as e:
        logger.error(f"received_webhook_url error: {e}", exc_info=True)
        await update.message.reply_text("⚠️ Something went wrong. Send /cancel and try again.")
        return ASK_WEBHOOK


async def clear_webhook_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id    = update.effective_user.id
    monitor_id = context.user_data.get("webhook_monitor_id")
    if monitor_id:
        clear_webhook_url(monitor_id, user_id)
        await update.message.reply_text("✅ Webhook removed.")
    else:
        await update.message.reply_text("No active webhook session. Use /list to manage webhooks.")
    context.user_data.clear()
    return ConversationHandler.END


webhook_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(webhook_callback, pattern="^webhook_")],
    states={
        ASK_WEBHOOK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_webhook_url),
            CommandHandler("clearwebhook", clear_webhook_command),
        ],
        ConversationHandler.TIMEOUT: [
            MessageHandler(filters.ALL, conversation_timeout),
            CallbackQueryHandler(conversation_timeout),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(unexpected_input),
        MessageHandler(filters.ALL, unexpected_input),
    ],
    per_message=False,
    per_chat=True,
    conversation_timeout=300,
)


# ---------------------------------------------------------------------------
# Keyword conversation
# ---------------------------------------------------------------------------

KEYWORD_MAX_LENGTH = 100


async def keyword_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query      = update.callback_query
        monitor_id = int(query.data.split("_")[1])
        user_id    = query.from_user.id

        monitor = get_monitor(monitor_id)
        if not monitor or monitor["user_id"] != user_id:
            await query.answer("Monitor not found.", show_alert=True)
            return ConversationHandler.END

        context.user_data["keyword_monitor_id"] = monitor_id
        label     = monitor.get("label") or monitor.get("url", "")
        current   = monitor.get("keyword")
        case_sens = bool(monitor.get("keyword_case_sensitive", 0))

        await query.answer()
        if current:
            case_str = "case-sensitive" if case_sens else "case-insensitive"
            await query.message.reply_text(
                f"🔑 <b>Edit Keyword Check</b>\n\n"
                f"Monitor: <b>{label}</b>\n"
                f"Current keyword: <code>{current}</code> ({case_str})\n\n"
                f"Send a new keyword to replace it ({KEYWORD_MAX_LENGTH} chars max).\n\n"
                "Send /clearkeyword to remove it, or /cancel to abort.",
                parse_mode="HTML"
            )
        else:
            await query.message.reply_text(
                f"🔑 <b>Set Keyword Check</b>\n\n"
                f"Monitor: <b>{label}</b>\n\n"
                "Send a word or phrase that must appear in the response body.\n\n"
                "If the site returns 200 but the keyword is missing, "
                "it's treated as <b>down</b>.\n\n"
                "Example: <code>Welcome back</code> or <code>Dashboard</code>\n\n"
                f"Max {KEYWORD_MAX_LENGTH} characters. Matching is case-insensitive.\n\n"
                "Send /cancel to abort.",
                parse_mode="HTML"
            )
        return ASK_KEYWORD

    except Exception as e:
        logger.error(f"keyword_callback error: {e}", exc_info=True)
        return ConversationHandler.END


async def received_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyword    = update.message.text.strip()
        user_id    = update.effective_user.id
        monitor_id = context.user_data.get("keyword_monitor_id")

        if not monitor_id:
            await update.message.reply_text("Something went wrong. Use /list to try again.")
            return ConversationHandler.END

        if not keyword:
            await update.message.reply_text(
                "⚠️ Keyword can't be empty. Send a word or phrase to search for:"
            )
            return ASK_KEYWORD

        if len(keyword) > KEYWORD_MAX_LENGTH:
            await update.message.reply_text(
                f"⚠️ Keyword is too long ({len(keyword)} chars). "
                f"Keep it under {KEYWORD_MAX_LENGTH} characters and try again:"
            )
            return ASK_KEYWORD

        set_keyword(monitor_id, user_id, keyword, case_sensitive=False)
        monitor = get_monitor(monitor_id)
        label   = (monitor.get("label") or monitor.get("url", "")) if monitor else "Monitor"
        context.user_data.clear()

        await update.message.reply_text(
            f"✅ <b>Keyword check set!</b>\n\n"
            f"🏷 Monitor: <b>{label}</b>\n"
            f"🔑 Keyword: <code>{keyword}</code>\n"
            f"🔠 Matching: case-insensitive\n\n"
            "If the page loads but the keyword isn't found, "
            "you'll get an alert as if the site were down.",
            parse_mode="HTML"
        )
        return ConversationHandler.END

    except Exception as e:
        logger.error(f"received_keyword error: {e}", exc_info=True)
        await update.message.reply_text("⚠️ Something went wrong. Send /cancel and try again.")
        return ASK_KEYWORD


async def clear_keyword_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id    = update.effective_user.id
    monitor_id = context.user_data.get("keyword_monitor_id")
    if monitor_id:
        clear_keyword(monitor_id, user_id)
        await update.message.reply_text("✅ Keyword check removed.")
    else:
        await update.message.reply_text("No active keyword session. Use /list to manage keywords.")
    context.user_data.clear()
    return ConversationHandler.END


keyword_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(keyword_callback, pattern="^keyword_")],
    states={
        ASK_KEYWORD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_keyword),
            CommandHandler("clearkeyword", clear_keyword_command),
        ],
        ConversationHandler.TIMEOUT: [
            MessageHandler(filters.ALL, conversation_timeout),
            CallbackQueryHandler(conversation_timeout),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(unexpected_input),
        MessageHandler(filters.ALL, unexpected_input),
    ],
    per_message=False,
    per_chat=True,
    conversation_timeout=300,
)


# ---------------------------------------------------------------------------
# Confirmation count conversation
# ---------------------------------------------------------------------------

async def confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query      = update.callback_query
        monitor_id = int(query.data.split("_")[1])
        user_id    = query.from_user.id

        monitor = get_monitor(monitor_id)
        if not monitor or monitor["user_id"] != user_id:
            await query.answer("Monitor not found.", show_alert=True)
            return ConversationHandler.END

        context.user_data["confirm_monitor_id"] = monitor_id
        pro          = is_pro(user_id)
        label        = monitor.get("label") or monitor.get("url", "")
        current      = monitor.get("confirm_count") or 1
        max_confirms = PRO_CONFIRM_LIMIT if pro else FREE_CONFIRM_LIMIT

        await query.answer()

        option_buttons = [
            [InlineKeyboardButton(
                f"{'✅ ' if i == current else ''}{i} check{'s' if i > 1 else ''}"
                f"{' (default)' if i == 1 else ''}",
                callback_data=f"confirmset_{monitor_id}_{i}"
            )]
            for i in range(1, max_confirms + 1)
        ]

        plan_note = (
            "" if pro
            else f"\n\n🆓 Free: up to {FREE_CONFIRM_LIMIT} confirmations. "
                 f"Pro unlocks {PRO_CONFIRM_LIMIT}."
        )

        await query.message.reply_text(
            f"🌍 <b>Confirmation Checks</b>\n\n"
            f"Monitor: <b>{label}</b>\n"
            f"Current: <b>{current} check{'s' if current > 1 else ''}</b>\n\n"
            "How many consecutive failures before you get an alert?\n\n"
            "• <b>1 check</b> — alert on first failure (default)\n"
            "• <b>2+ checks</b> — only alert after N consecutive failures, "
            "filtering out transient blips"
            f"{plan_note}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(option_buttons)
        )
        return ASK_CONFIRM

    except Exception as e:
        logger.error(f"confirm_callback error: {e}", exc_info=True)
        return ConversationHandler.END


async def confirmset_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query   = update.callback_query
        user_id = query.from_user.id

        parts      = query.data.split("_")
        monitor_id = int(parts[1])
        count      = int(parts[2])

        monitor = get_monitor(monitor_id)
        if not monitor or monitor["user_id"] != user_id:
            await query.answer("Monitor not found.", show_alert=True)
            return ConversationHandler.END

        pro          = is_pro(user_id)
        max_confirms = PRO_CONFIRM_LIMIT if pro else FREE_CONFIRM_LIMIT

        if count < 1 or count > max_confirms:
            await query.answer("Invalid selection.", show_alert=True)
            return ASK_CONFIRM

        set_confirm_count(monitor_id, user_id, count)
        label = monitor.get("label") or monitor.get("url", "")
        context.user_data.clear()

        interval = monitor.get("interval_minutes") or 5
        if count == 1:
            timing_note = "You'll be alerted on the first failure."
        else:
            wait_mins   = (count - 1) * interval
            timing_note = (
                f"You'll only be alerted after {count} consecutive failures "
                f"(~{wait_mins} min delay at your check interval)."
            )

        await query.answer(f"Set to {count} check{'s' if count > 1 else ''}.")
        await query.edit_message_text(
            f"✅ <b>Confirmation checks updated.</b>\n\n"
            f"🏷 Monitor: <b>{label}</b>\n"
            f"🌍 Required failures: <b>{count}</b>\n\n"
            f"{timing_note}",
            parse_mode="HTML"
        )
        return ConversationHandler.END

    except Exception as e:
        logger.error(f"confirmset_callback error: {e}", exc_info=True)
        return ConversationHandler.END


confirm_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(confirm_callback, pattern="^confirm_\\d+$")],
    states={
        ASK_CONFIRM: [
            CallbackQueryHandler(confirmset_callback, pattern="^confirmset_"),
        ],
        ConversationHandler.TIMEOUT: [
            MessageHandler(filters.ALL, conversation_timeout),
            CallbackQueryHandler(conversation_timeout),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CallbackQueryHandler(unexpected_input),
        MessageHandler(filters.ALL, unexpected_input),
    ],
    per_message=False,
    per_chat=True,
    conversation_timeout=300,
)


# ---------------------------------------------------------------------------
# /status
# ---------------------------------------------------------------------------

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    lang     = get_user_language(user_id)
    monitors = get_all_monitors(user_id)

    if not monitors:
        await reply_fn(mt(lang, "status_no_monitors"))
        return

    lines = [mt(lang, "status_header")]

    for m in monitors:
        label     = m.get("label") or m.get("url", "")
        is_paused = m["active"] == 2

        if is_paused:
            icon        = "⏸"
            status_text = mt(lang, "status_paused")
        elif m.get("last_status") == "up":
            icon        = "🟢"
            status_text = mt(lang, "status_up")
        elif m.get("last_status") == "down":
            icon        = "🔴"
            status_text = mt(lang, "status_down")
        else:
            icon        = "⚪"
            status_text = mt(lang, "status_pending")

        if m.get("last_checked"):
            last = datetime.fromisoformat(m["last_checked"])
            diff = datetime.now() - last
            mins = int(diff.total_seconds() // 60)
            if mins < 1:
                ago = mt(lang, "status_just_now")
            elif mins == 1:
                ago = mt(lang, "status_1min")
            elif mins < 60:
                ago = mt(lang, "status_mins", mins=mins)
            else:
                ago = mt(lang, "status_hours", h=mins // 60)
        else:
            ago = mt(lang, "status_not_checked")

        lines.append(mt(lang, "status_line", icon=icon, label=label,
                        status_text=status_text, ago=ago))

    await reply_fn("\n".join(lines), parse_mode="HTML")
    
    

