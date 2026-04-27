# handlers/team.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters,
)
from db.database import (
    add_team_member, get_team_members, remove_team_member,
    count_team_members, is_pro, PRO_TEAM_LIMIT,
    get_user_language,
)
from locales.team_strings import tt

# ---------------------------------------------------------------------------
# Conversation states
# ---------------------------------------------------------------------------

TEAM_ASK_ID    = 60
TEAM_ASK_LABEL = 61


# ---------------------------------------------------------------------------
# /team — list view + entry point
# ---------------------------------------------------------------------------

async def team_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args    = context.args or []

    if args and args[0].lower() == "add":
        return await _start_add(update, context, user_id)

    await _show_list(update, context, user_id)
    return ConversationHandler.END


async def _show_list(update, context, user_id: int):
    lang     = get_user_language(user_id)
    pro      = is_pro(user_id)
    reply_fn = (
        update.callback_query.message.reply_text
        if update.callback_query
        else update.message.reply_text
    )

    if not pro:
        await reply_fn(
            tt(lang, "team_pro_gate", limit=PRO_TEAM_LIMIT),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    tt(lang, "team_btn_upgrade"), callback_data="upgrade"
                )
            ]])
        )
        return

    members = get_team_members(user_id)
    count   = len(members)

    if not members:
        await reply_fn(
            tt(lang, "team_empty", limit=PRO_TEAM_LIMIT),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    tt(lang, "team_btn_add"), callback_data="team_add"
                )
            ]])
        )
        return

    plural  = "s" if count != 1 else ""
    text    = tt(lang, "team_list_header", count=count, limit=PRO_TEAM_LIMIT, plural=plural)
    buttons = []

    for m in members:
        display = m["label"] or f"User {m['member_user_id']}"
        text   += tt(lang, "team_list_member",
                     display=display, member_id=m["member_user_id"])
        buttons.append([InlineKeyboardButton(
            tt(lang, "team_btn_remove", display=display),
            callback_data=f"team_remove_{m['id']}"
        )])

    if count < PRO_TEAM_LIMIT:
        buttons.append([InlineKeyboardButton(
            tt(lang, "team_btn_add"), callback_data="team_add"
        )])

    text += tt(lang, "team_list_reminder")

    await reply_fn(
        text, parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ---------------------------------------------------------------------------
# Add flow
# ---------------------------------------------------------------------------

async def _start_add(update, context, user_id: int):
    lang     = get_user_language(user_id)
    pro      = is_pro(user_id)
    reply_fn = (
        update.callback_query.message.reply_text
        if update.callback_query
        else update.message.reply_text
    )

    if not pro:
        await reply_fn(
            tt(lang, "team_add_pro_gate"),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    tt(lang, "team_btn_upgrade"), callback_data="upgrade"
                )
            ]])
        )
        return ConversationHandler.END

    if count_team_members(user_id) >= PRO_TEAM_LIMIT:
        await reply_fn(tt(lang, "team_limit_reached", limit=PRO_TEAM_LIMIT))
        return ConversationHandler.END

    await reply_fn(
        tt(lang, "team_step1_prompt"),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return TEAM_ASK_ID


async def team_add_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    return await _start_add(update, context, user_id)


# ---------------------------------------------------------------------------
# Step 1 — receive user ID
# ---------------------------------------------------------------------------

async def team_received_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text    = update.message.text.strip()
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)

    try:
        member_id = int(text)
    except ValueError:
        await update.message.reply_text(
            tt(lang, "team_id_invalid"),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        return TEAM_ASK_ID

    if member_id == user_id:
        await update.message.reply_text(tt(lang, "team_id_self"))
        return TEAM_ASK_ID

    existing = get_team_members(user_id)
    if any(m["member_user_id"] == member_id for m in existing):
        await update.message.reply_text(
            tt(lang, "team_id_duplicate", member_id=member_id),
            parse_mode="HTML"
        )
        return TEAM_ASK_ID

    context.user_data["team_member_id"] = member_id

    await update.message.reply_text(
        tt(lang, "team_id_ok", member_id=member_id),
        parse_mode="HTML"
    )
    return TEAM_ASK_LABEL


# ---------------------------------------------------------------------------
# Step 2 — receive label
# ---------------------------------------------------------------------------

async def team_received_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    label     = update.message.text.strip()
    user_id   = update.effective_user.id
    lang      = get_user_language(user_id)
    member_id = context.user_data.get("team_member_id")

    if not member_id:
        await update.message.reply_text(tt(lang, "team_something_wrong"))
        return ConversationHandler.END

    if len(label) > 50:
        await update.message.reply_text(tt(lang, "team_label_too_long"))
        return TEAM_ASK_LABEL

    return await _save_member(update.message.reply_text, user_id, member_id, label, lang)


async def team_skip_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id   = update.effective_user.id
    lang      = get_user_language(user_id)
    member_id = context.user_data.get("team_member_id")

    if not member_id:
        await update.message.reply_text(tt(lang, "team_something_wrong"))
        return ConversationHandler.END

    return await _save_member(update.message.reply_text, user_id, member_id, None, lang)


async def _save_member(reply_fn, owner_id: int, member_id: int, label, lang: str):
    try:
        success = add_team_member(owner_id, member_id, label)
    except ValueError as e:
        await reply_fn(str(e))
        return ConversationHandler.END

    if not success:
        await reply_fn(
            tt(lang, "team_already_member", member_id=member_id),
            parse_mode="HTML"
        )
        return ConversationHandler.END

    display = label or f"User {member_id}"
    await reply_fn(
        tt(lang, "team_saved", display=display, member_id=member_id),
        parse_mode="HTML"
    )
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# Remove (two-step confirm)
# ---------------------------------------------------------------------------

async def team_remove_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    row_id  = int(query.data.split("_")[2])

    members = get_team_members(user_id)
    match   = next((m for m in members if m["id"] == row_id), None)

    if not match:
        await query.answer(tt(lang, "team_remove_not_found"))
        return

    display = match["label"] or f"User {match['member_user_id']}"
    await query.answer()
    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                tt(lang, "team_btn_yes_remove"),
                callback_data=f"team_confirmremove_{row_id}"
            ),
            InlineKeyboardButton(
                tt(lang, "team_btn_cancel"),
                callback_data=f"team_cancelremove_{row_id}"
            ),
        ]])
    )
    await query.message.reply_text(
        tt(lang, "team_remove_confirm", display=display),
        parse_mode="HTML"
    )


async def team_confirm_remove_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    row_id  = int(query.data.split("_")[2])

    members = get_team_members(user_id)
    match   = next((m for m in members if m["id"] == row_id), None)
    display = (match["label"] or f"User {match['member_user_id']}") if match else "Teammate"

    remove_team_member(row_id, user_id)
    await query.answer()
    await query.edit_message_text(
        tt(lang, "team_removed", display=display),
        parse_mode="HTML"
    )


async def team_cancel_remove_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()
    await query.edit_message_text(
        tt(lang, "team_remove_cancelled"),
        parse_mode="HTML"
    )


# ---------------------------------------------------------------------------
# Cancel fallback
# ---------------------------------------------------------------------------

async def team_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)
    await update.message.reply_text(tt(lang, "team_cancelled"))
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# ConversationHandler export
# ---------------------------------------------------------------------------

team_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("team", team_command),
        CallbackQueryHandler(team_add_callback, pattern="^team_add$"),
    ],
    states={
        TEAM_ASK_ID: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, team_received_id),
        ],
        TEAM_ASK_LABEL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, team_received_label),
            CommandHandler("skip", team_skip_label),
        ],
    },
    fallbacks=[CommandHandler("cancel", team_cancel)],
    allow_reentry=True,
)