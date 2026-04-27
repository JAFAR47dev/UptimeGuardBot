# handlers/maintenance.py
import re
from datetime import date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters,
)
from db.database import (
    add_maintenance_window, get_maintenance_windows,
    delete_maintenance_window, count_maintenance_windows,
    is_pro, FREE_MAINTENANCE_LIMIT, get_user_language,
)
from locales.utility_strings import ut

# ---------------------------------------------------------------------------
# Conversation states
# ---------------------------------------------------------------------------

(
    MW_ASK_LABEL,
    MW_ASK_DAYS,
    MW_ASK_START,
    MW_ASK_END,
    MW_ASK_CONFIRM,
) = range(40, 45)

# ---------------------------------------------------------------------------
# Day preset → days_of_week string
# ---------------------------------------------------------------------------

PRESETS = {
    "days_weekdays": "0,1,2,3,4",
    "days_everyday": "0,1,2,3,4,5,6",
    "days_weekends": "5,6",
    "days_oneoff":   None,
}


def _days_label(days_of_week: str, lang: str) -> str:
    """Localised human-readable label for a days_of_week DB value."""
    if not days_of_week:
        return ut(lang, "mw_days_label_oneoff")
    days = [int(d) for d in days_of_week.split(",")]
    if days == list(range(7)):
        return ut(lang, "mw_days_label_everyday")
    if days == list(range(5)):
        return ut(lang, "mw_days_label_weekdays")
    if days == [5, 6]:
        return ut(lang, "mw_days_label_weekends")
    # Fallback for custom sets — keep English day abbreviations as they're universal
    day_abbr = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return ", ".join(day_abbr[d] for d in sorted(days))


def _time_valid(t: str) -> bool:
    return bool(re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", t))


def _reply_fn(update):
    """Return the appropriate reply function regardless of update type."""
    if update.callback_query:
        return update.callback_query.message.reply_text
    return update.message.reply_text


# ---------------------------------------------------------------------------
# /maintenance — list + entry point
# ---------------------------------------------------------------------------

async def maintenance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args    = context.args or []

    if args and args[0].lower() == "add":
        return await _start_add(update, context, user_id)

    await _show_list(update, context, user_id)
    return ConversationHandler.END


async def _show_list(update, context, user_id: int):
    lang    = get_user_language(user_id)
    windows = get_maintenance_windows(user_id)
    pro     = is_pro(user_id)

    if not windows:
        plan_note = (
            ut(lang, "mw_list_plan_pro")
            if pro else
            ut(lang, "mw_list_plan_free",
               limit=FREE_MAINTENANCE_LIMIT,
               used_str="")
        )
        await _reply_fn(update)(
            ut(lang, "mw_list_empty", plan_note=plan_note),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(ut(lang, "mw_btn_add"), callback_data="mw_add")
            ]])
        )
        return

    text    = ut(lang, "mw_list_header")
    buttons = []

    for w in windows:
        days_str = _days_label(w["days_of_week"], lang)
        text += ut(
            lang, "mw_list_row",
            label=w["label"],
            start=w["start_time"],
            end=w["end_time"],
            days=days_str,
        )
        buttons.append([InlineKeyboardButton(
            ut(lang, "mw_btn_delete", label=w["label"]),
            callback_data=f"mw_del_{w['id']}"
        )])

    buttons.append([InlineKeyboardButton(ut(lang, "mw_btn_add"), callback_data="mw_add")])

    if pro:
        plan_note = ut(lang, "mw_list_plan_pro")
    else:
        used_str  = (
            ut(lang, "mw_list_used")
            if len(windows) >= FREE_MAINTENANCE_LIMIT
            else ut(lang, "mw_list_available")
        )
        plan_note = ut(lang, "mw_list_plan_free",
                       limit=FREE_MAINTENANCE_LIMIT,
                       used_str=used_str)

    text += f"<i>{plan_note}</i>"

    await _reply_fn(update)(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ---------------------------------------------------------------------------
# Add flow — entry
# ---------------------------------------------------------------------------

async def _start_add(update, context, user_id: int):
    lang  = get_user_language(user_id)
    pro   = is_pro(user_id)
    count = count_maintenance_windows(user_id)

    if not pro and count >= FREE_MAINTENANCE_LIMIT:
        await _reply_fn(update)(
            ut(lang, "mw_limit_reached", limit=FREE_MAINTENANCE_LIMIT),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(ut(lang, "mw_btn_upgrade"), callback_data="upgrade")
            ]])
        )
        return ConversationHandler.END

    await _reply_fn(update)(
        ut(lang, "mw_step1_prompt"),
        parse_mode="HTML"
    )
    return MW_ASK_LABEL


async def mw_add_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    return await _start_add(update, context, user_id)


# ---------------------------------------------------------------------------
# Step 1 — label
# ---------------------------------------------------------------------------

async def mw_received_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    label   = update.message.text.strip()
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)

    if len(label) > 60:
        await update.message.reply_text(ut(lang, "mw_step1_too_long"))
        return MW_ASK_LABEL

    context.user_data["mw_label"] = label

    await update.message.reply_text(
        ut(lang, "mw_step2_prompt"),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(ut(lang, "mw_days_weekdays"), callback_data="days_weekdays")],
            [InlineKeyboardButton(ut(lang, "mw_days_everyday"), callback_data="days_everyday")],
            [InlineKeyboardButton(ut(lang, "mw_days_weekends"), callback_data="days_weekends")],
            [InlineKeyboardButton(ut(lang, "mw_days_oneoff"),   callback_data="days_oneoff")],
        ])
    )
    return MW_ASK_DAYS


# ---------------------------------------------------------------------------
# Step 2 — days
# ---------------------------------------------------------------------------

async def mw_received_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()

    data         = query.data
    days_of_week = PRESETS.get(data)
    context.user_data["mw_days"]       = days_of_week
    context.user_data["mw_oneoff"]     = (data == "days_oneoff")

    days_label = _days_label(days_of_week, lang) if days_of_week else ut(lang, "mw_days_label_oneoff")
    context.user_data["mw_days_label"] = days_label

    await query.message.reply_text(
        ut(lang, "mw_step2_selected", days_label=days_label),
        parse_mode="HTML"
    )
    return MW_ASK_START


# ---------------------------------------------------------------------------
# Step 3 — start time
# ---------------------------------------------------------------------------

async def mw_received_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text    = update.message.text.strip()
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)

    if not _time_valid(text):
        await update.message.reply_text(
            ut(lang, "mw_step3_invalid"), parse_mode="HTML"
        )
        return MW_ASK_START

    context.user_data["mw_start"] = text

    await update.message.reply_text(
        ut(lang, "mw_step4_prompt", start=text),
        parse_mode="HTML"
    )
    return MW_ASK_END


# ---------------------------------------------------------------------------
# Step 4 — end time → confirmation
# ---------------------------------------------------------------------------

async def mw_received_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text    = update.message.text.strip()
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)

    if not _time_valid(text):
        await update.message.reply_text(
            ut(lang, "mw_step4_invalid"), parse_mode="HTML"
        )
        return MW_ASK_END

    start = context.user_data["mw_start"]
    if text == start:
        await update.message.reply_text(ut(lang, "mw_step4_same_time"))
        return MW_ASK_END

    context.user_data["mw_end"] = text

    label      = context.user_data["mw_label"]
    days_label = context.user_data["mw_days_label"]
    is_oneoff  = context.user_data.get("mw_oneoff", False)

    overnight  = ut(lang, "mw_overnight_note") if text < start else ""
    date_line  = (
        ut(lang, "mw_date_oneoff")
        if is_oneoff else
        ut(lang, "mw_date_repeats", days_label=days_label)
    )

    await update.message.reply_text(
        ut(lang, "mw_confirm_prompt",
           label=label,
           start=start,
           end=text,
           overnight=overnight,
           date_line=date_line),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(ut(lang, "mw_btn_save"),   callback_data="mw_confirm_yes"),
            InlineKeyboardButton(ut(lang, "mw_btn_cancel"), callback_data="mw_confirm_no"),
        ]])
    )
    return MW_ASK_CONFIRM


# ---------------------------------------------------------------------------
# Confirmation
# ---------------------------------------------------------------------------

async def mw_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()

    if query.data == "mw_confirm_no":
        await query.edit_message_text(ut(lang, "mw_cancelled"))
        return ConversationHandler.END

    label      = context.user_data["mw_label"]
    start      = context.user_data["mw_start"]
    end        = context.user_data["mw_end"]
    days       = context.user_data["mw_days"]
    is_oneoff  = context.user_data.get("mw_oneoff", False)
    days_label = context.user_data["mw_days_label"]

    active_until = date.today().isoformat() if is_oneoff else None

    add_maintenance_window(
        user_id=user_id,
        label=label,
        start_time=start,
        end_time=end,
        days_of_week=days,
        active_until=active_until,
    )
    context.user_data.clear()

    await query.edit_message_text(
        ut(lang, "mw_saved",
           label=label,
           start=start,
           end=end,
           days_label=days_label),
        parse_mode="HTML"
    )
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# Delete callback
# ---------------------------------------------------------------------------

async def mw_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    win_id  = int(query.data.split("_")[2])
    await query.answer()

    windows = get_maintenance_windows(user_id)
    match   = next((w for w in windows if w["id"] == win_id), None)

    if not match:
        await query.edit_message_text(ut(lang, "mw_delete_not_found"))
        return

    delete_maintenance_window(win_id, user_id)
    await query.edit_message_text(
        ut(lang, "mw_deleted", label=match["label"]),
        parse_mode="HTML"
    )


# ---------------------------------------------------------------------------
# Cancel fallback
# ---------------------------------------------------------------------------

async def mw_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)
    context.user_data.clear()
    await update.message.reply_text(ut(lang, "mw_cancel_fallback"))
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