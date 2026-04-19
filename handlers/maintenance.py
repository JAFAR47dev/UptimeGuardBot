# handlers/maintenance.py
import re
from datetime import datetime, timedelta, date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters,
)
from db.database import (
    add_maintenance_window, get_maintenance_windows,
    delete_maintenance_window, count_maintenance_windows,
    is_pro, FREE_MAINTENANCE_LIMIT,
)

# ---------------------------------------------------------------------------
# Conversation states
# ---------------------------------------------------------------------------

(
    MW_ASK_LABEL,
    MW_ASK_DAYS,
    MW_ASK_START,
    MW_ASK_END,
    MW_ASK_CONFIRM,
) = range(40, 45)   # well outside other handler ranges

# ---------------------------------------------------------------------------
# Day helpers
# ---------------------------------------------------------------------------

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Maps callback_data suffix → weekday int
DAY_MAP = {name.lower(): i for i, name in enumerate(DAY_NAMES)}

PRESETS = {
    "days_weekdays":  "0,1,2,3,4",
    "days_everyday":  "0,1,2,3,4,5,6",
    "days_weekends":  "5,6",
    "days_oneoff":    None,   # sentinel — will use active_until
}


def _days_label(days_of_week: str) -> str:
    """Human-readable label for a days_of_week string."""
    if not days_of_week:
        return "One-off (today only)"
    days = [int(d) for d in days_of_week.split(",")]
    if days == list(range(7)):
        return "Every day"
    if days == list(range(5)):
        return "Weekdays (Mon–Fri)"
    if days == [5, 6]:
        return "Weekends (Sat–Sun)"
    return ", ".join(DAY_NAMES[d] for d in sorted(days))


def _time_valid(t: str) -> bool:
    """Accept HH:MM in 24-hour format."""
    return bool(re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", t))


# ---------------------------------------------------------------------------
# /maintenance — list + entry point
# ---------------------------------------------------------------------------

async def maintenance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /maintenance         → list windows
    /maintenance add     → start add conversation
    """
    user_id = update.effective_user.id
    args    = context.args or []

    if args and args[0].lower() == "add":
        return await _start_add(update, context, user_id)

    await _show_list(update, context, user_id)
    return ConversationHandler.END


async def _show_list(update, context, user_id: int):
    windows = get_maintenance_windows(user_id)
    pro     = is_pro(user_id)

    if not windows:
        reply_fn = (
            update.callback_query.message.reply_text
            if update.callback_query
            else update.message.reply_text
        )
        await reply_fn(
            "🔧 <b>Maintenance Windows</b>\n\n"
            "You have no scheduled maintenance windows.\n\n"
            "Use /maintenance add to create one.\n\n"
            f"{'⭐ Pro: unlimited windows.' if pro else f'🆓 Free: {FREE_MAINTENANCE_LIMIT} window.'}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("➕ Add Window", callback_data="mw_add")
            ]])
        )
        return

    text    = "🔧 <b>Maintenance Windows</b>\n\n"
    buttons = []

    for w in windows:
        days_str = _days_label(w["days_of_week"])
        text += (
            f"📅 <b>{w['label']}</b>\n"
            f"   🕐 {w['start_time']} – {w['end_time']}\n"
            f"   📆 {days_str}\n\n"
        )
        buttons.append([InlineKeyboardButton(
            f"🗑 Delete — {w['label']}",
            callback_data=f"mw_del_{w['id']}"
        )])

    buttons.append([InlineKeyboardButton("➕ Add Window", callback_data="mw_add")])

    plan_note = (
        "⭐ Pro: unlimited windows."
        if pro
        else f"🆓 Free: {FREE_MAINTENANCE_LIMIT} window. {'Used.' if len(windows) >= FREE_MAINTENANCE_LIMIT else 'Available.'}"
    )
    text += f"<i>{plan_note}</i>"

    reply_fn = (
        update.callback_query.message.reply_text
        if update.callback_query
        else update.message.reply_text
    )
    await reply_fn(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


# ---------------------------------------------------------------------------
# Add flow — entry
# ---------------------------------------------------------------------------

async def _start_add(update, context, user_id: int):
    pro   = is_pro(user_id)
    count = count_maintenance_windows(user_id)

    if not pro and count >= FREE_MAINTENANCE_LIMIT:
        reply_fn = (
            update.callback_query.message.reply_text
            if update.callback_query
            else update.message.reply_text
        )
        await reply_fn(
            f"⚠️ Free plan allows <b>{FREE_MAINTENANCE_LIMIT} maintenance window</b>.\n\n"
            "Upgrade to Pro for unlimited windows.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")
            ]])
        )
        return ConversationHandler.END

    reply_fn = (
        update.callback_query.message.reply_text
        if update.callback_query
        else update.message.reply_text
    )
    await reply_fn(
        "🔧 <b>Add Maintenance Window</b>\n\n"
        "Step 1 of 4 — Give this window a label.\n\n"
        "Example: <i>Nightly backup</i> or <i>Deploy window</i>\n\n"
        "Send /cancel to abort.",
        parse_mode="HTML"
    )
    return MW_ASK_LABEL


async def mw_add_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """➕ Add Window button."""
    query   = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    return await _start_add(update, context, user_id)


# ---------------------------------------------------------------------------
# Step 1 — label
# ---------------------------------------------------------------------------

async def mw_received_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    label = update.message.text.strip()

    if len(label) > 60:
        await update.message.reply_text(
            "⚠️ Label must be 60 characters or less. Try a shorter one:"
        )
        return MW_ASK_LABEL

    context.user_data["mw_label"] = label

    await update.message.reply_text(
        "📆 <b>Step 2 of 4 — When does this window repeat?</b>\n\n"
        "Choose a preset or send /cancel to abort.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Mon – Fri",   callback_data="days_weekdays")],
            [InlineKeyboardButton("Every day",   callback_data="days_everyday")],
            [InlineKeyboardButton("Sat & Sun",   callback_data="days_weekends")],
            [InlineKeyboardButton("One-off (today only)", callback_data="days_oneoff")],
        ])
    )
    return MW_ASK_DAYS


# ---------------------------------------------------------------------------
# Step 2 — days
# ---------------------------------------------------------------------------

async def mw_received_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data  = query.data   # e.g. "days_weekdays"

    days_of_week = PRESETS.get(data)   # None for one-off
    context.user_data["mw_days"]    = days_of_week
    context.user_data["mw_oneoff"]  = (data == "days_oneoff")

    days_label = _days_label(days_of_week) if days_of_week else "One-off (today only)"
    context.user_data["mw_days_label"] = days_label

    await query.message.reply_text(
        f"✅ <b>{days_label}</b> selected.\n\n"
        "🕐 <b>Step 3 of 4 — Start time?</b>\n\n"
        "Send in 24-hour format. Example: <code>02:00</code>\n\n"
        "Send /cancel to abort.",
        parse_mode="HTML"
    )
    return MW_ASK_START


# ---------------------------------------------------------------------------
# Step 3 — start time
# ---------------------------------------------------------------------------

async def mw_received_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not _time_valid(text):
        await update.message.reply_text(
            "⚠️ Please use 24-hour format. Example: <code>02:00</code> or <code>23:30</code>",
            parse_mode="HTML"
        )
        return MW_ASK_START

    context.user_data["mw_start"] = text

    await update.message.reply_text(
        f"✅ Start: <b>{text}</b>\n\n"
        "🕐 <b>Step 4 of 4 — End time?</b>\n\n"
        "Send in 24-hour format. Example: <code>04:00</code>\n"
        "<i>Overnight windows are supported, e.g. 23:00 – 01:00.</i>\n\n"
        "Send /cancel to abort.",
        parse_mode="HTML"
    )
    return MW_ASK_END


# ---------------------------------------------------------------------------
# Step 4 — end time → confirmation
# ---------------------------------------------------------------------------

async def mw_received_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text  = update.message.text.strip()

    if not _time_valid(text):
        await update.message.reply_text(
            "⚠️ Please use 24-hour format. Example: <code>04:00</code>",
            parse_mode="HTML"
        )
        return MW_ASK_END

    start = context.user_data["mw_start"]
    if text == start:
        await update.message.reply_text(
            "⚠️ End time must be different from start time. Try again:"
        )
        return MW_ASK_END

    context.user_data["mw_end"] = text

    label      = context.user_data["mw_label"]
    days_label = context.user_data["mw_days_label"]
    is_oneoff  = context.user_data.get("mw_oneoff", False)

    overnight_note = ""
    if text < start:
        overnight_note = "\n<i>⏰ Overnight window — wraps past midnight.</i>"

    date_line = (
        f"📆 Repeats: <b>{days_label}</b>"
        if not is_oneoff
        else f"📆 <b>One-off</b> — active today only"
    )

    await update.message.reply_text(
        f"✅ <b>Confirm Maintenance Window</b>\n\n"
        f"🏷 Label: <b>{label}</b>\n"
        f"🕐 Time: <b>{start} – {text}</b>{overnight_note}\n"
        f"{date_line}\n\n"
        f"During this window, no alerts will fire for any of your monitors.\n"
        f"Checks still run and history is still recorded.\n\n"
        f"Save this window?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Save",   callback_data="mw_confirm_yes"),
            InlineKeyboardButton("❌ Cancel", callback_data="mw_confirm_no"),
        ]])
    )
    return MW_ASK_CONFIRM


# ---------------------------------------------------------------------------
# Confirmation
# ---------------------------------------------------------------------------

async def mw_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "mw_confirm_no":
        await query.edit_message_text("❌ Cancelled. No window was saved.")
        return ConversationHandler.END

    label      = context.user_data["mw_label"]
    start      = context.user_data["mw_start"]
    end        = context.user_data["mw_end"]
    days       = context.user_data["mw_days"]       # None = one-off
    is_oneoff  = context.user_data.get("mw_oneoff", False)

    active_until = date.today().isoformat() if is_oneoff else None

    add_maintenance_window(
        user_id=user_id,
        label=label,
        start_time=start,
        end_time=end,
        days_of_week=days,
        active_until=active_until,
    )

    days_label = context.user_data["mw_days_label"]
    await query.edit_message_text(
        f"✅ <b>Maintenance window saved!</b>\n\n"
        f"🏷 <b>{label}</b>\n"
        f"🕐 {start} – {end}\n"
        f"📆 {days_label}\n\n"
        f"No alerts will fire during this window.\n"
        f"Use /maintenance to view or delete windows.",
        parse_mode="HTML"
    )
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# Delete callback
# ---------------------------------------------------------------------------

async def mw_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    win_id  = int(query.data.split("_")[2])   # "mw_del_<id>"
    await query.answer()

    # Verify ownership before delete
    windows = get_maintenance_windows(user_id)
    match   = next((w for w in windows if w["id"] == win_id), None)

    if not match:
        await query.edit_message_text("⚠️ Window not found or already deleted.")
        return

    delete_maintenance_window(win_id, user_id)
    await query.edit_message_text(
        f"🗑 <b>{match['label']}</b> has been deleted.\n\n"
        "Use /maintenance to manage your windows.",
        parse_mode="HTML"
    )


# ---------------------------------------------------------------------------
# Cancel fallback
# ---------------------------------------------------------------------------

async def mw_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# ConversationHandler export
# ---------------------------------------------------------------------------

maintenance_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("maintenance", maintenance_command),
        CallbackQueryHandler(mw_add_callback, pattern="^mw_add$"),
    ],
    states={
        MW_ASK_LABEL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, mw_received_label),
        ],
        MW_ASK_DAYS: [
            CallbackQueryHandler(mw_received_days, pattern="^days_"),
        ],
        MW_ASK_START: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, mw_received_start),
        ],
        MW_ASK_END: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, mw_received_end),
        ],
        MW_ASK_CONFIRM: [
            CallbackQueryHandler(mw_confirm, pattern="^mw_confirm_"),
        ],
    },
    fallbacks=[CommandHandler("cancel", mw_cancel)],
    allow_reentry=True,
)
