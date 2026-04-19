# handlers/team.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters,
)
from db.database import (
    add_team_member, get_team_members, remove_team_member,
    count_team_members, is_pro, PRO_TEAM_LIMIT,
)

# ---------------------------------------------------------------------------
# Conversation states — well outside all other handler ranges
# ---------------------------------------------------------------------------

TEAM_ASK_ID    = 60
TEAM_ASK_LABEL = 61


# ---------------------------------------------------------------------------
# /team — list view + entry point
# ---------------------------------------------------------------------------

async def team_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /team        → list teammates
    /team add    → start add conversation
    """
    user_id = update.effective_user.id
    args    = context.args or []

    if args and args[0].lower() == "add":
        return await _start_add(update, context, user_id)

    await _show_list(update, context, user_id)
    return ConversationHandler.END


async def _show_list(update, context, user_id: int):
    pro     = is_pro(user_id)
    reply_fn = (
        update.callback_query.message.reply_text
        if update.callback_query
        else update.message.reply_text
    )

    if not pro:
        await reply_fn(
            "👥 <b>Team Notifications</b>\n\n"
            "Team notifications are a <b>Pro</b> feature.\n\n"
            "Upgrade to add up to 5 teammates who receive the same "
            "down and recovery alerts as you.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")
            ]])
        )
        return

    members = get_team_members(user_id)
    count   = len(members)

    if not members:
        await reply_fn(
            "👥 <b>Team Notifications</b>\n\n"
            f"You have no teammates yet. You can add up to {PRO_TEAM_LIMIT}.\n\n"
            "Teammates receive the same down and recovery alerts as you, "
            "directly in their Telegram DMs.\n\n"
            "⚠️ <b>Important:</b> each teammate must send <code>/start</code> "
            "to this bot before they can receive alerts.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("➕ Add Teammate", callback_data="team_add")
            ]])
        )
        return

    text    = f"👥 <b>Team Notifications</b>\n\n"
    text   += f"<b>{count}/{PRO_TEAM_LIMIT}</b> teammate{'s' if count != 1 else ''} added.\n\n"
    buttons = []

    for m in members:
        display = m["label"] or f"User {m['member_user_id']}"
        text   += f"👤 <b>{display}</b> — ID: <code>{m['member_user_id']}</code>\n"
        buttons.append([InlineKeyboardButton(
            f"🗑 Remove {display}",
            callback_data=f"team_remove_{m['id']}"
        )])

    if count < PRO_TEAM_LIMIT:
        buttons.append([InlineKeyboardButton(
            "➕ Add Teammate", callback_data="team_add"
        )])

    text += (
        "\n⚠️ <b>Reminder:</b> teammates must send <code>/start</code> "
        "to this bot to receive alerts."
    )

    await reply_fn(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))


# ---------------------------------------------------------------------------
# Add flow
# ---------------------------------------------------------------------------

async def _start_add(update, context, user_id: int):
    pro = is_pro(user_id)
    reply_fn = (
        update.callback_query.message.reply_text
        if update.callback_query
        else update.message.reply_text
    )

    if not pro:
        await reply_fn(
            "⭐ Team notifications are a Pro feature.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")
            ]])
        )
        return ConversationHandler.END

    if count_team_members(user_id) >= PRO_TEAM_LIMIT:
        await reply_fn(
            f"⚠️ You've reached the limit of {PRO_TEAM_LIMIT} teammates.\n\n"
            "Remove an existing teammate before adding a new one."
        )
        return ConversationHandler.END

    await reply_fn(
        "👥 <b>Add Teammate — Step 1 of 2</b>\n\n"
        "Send your teammate's <b>Telegram user ID</b>.\n\n"
        "They can find their ID by messaging "
        "<a href='https://t.me/userinfobot'>@userinfobot</a>.\n\n"
        "⚠️ They must also send <code>/start</code> to this bot first, "
        "otherwise Telegram will block the alert delivery.\n\n"
        "Send /cancel to abort.",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return TEAM_ASK_ID


async def team_add_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """➕ Add Teammate button."""
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

    # Must be a plain integer
    try:
        member_id = int(text)
    except ValueError:
        await update.message.reply_text(
            "⚠️ Please send a numeric Telegram user ID.\n\n"
            "Example: <code>123456789</code>\n\n"
            "Your teammate can find their ID via "
            "<a href='https://t.me/userinfobot'>@userinfobot</a>.",
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        return TEAM_ASK_ID

    # Can't add yourself
    if member_id == user_id:
        await update.message.reply_text(
            "⚠️ You can't add yourself as a teammate."
        )
        return TEAM_ASK_ID

    # Check if already a member
    existing = get_team_members(user_id)
    if any(m["member_user_id"] == member_id for m in existing):
        await update.message.reply_text(
            f"⚠️ User <code>{member_id}</code> is already on your team.",
            parse_mode="HTML"
        )
        return TEAM_ASK_ID

    context.user_data["team_member_id"] = member_id

    await update.message.reply_text(
        f"✅ User ID <code>{member_id}</code> noted.\n\n"
        "👥 <b>Step 2 of 2</b> — Give them a label so you know who they are.\n\n"
        "Example: <i>John</i> or <i>DevOps Lead</i>\n\n"
        "Send /skip to use their user ID as the label, or /cancel to abort.",
        parse_mode="HTML"
    )
    return TEAM_ASK_LABEL


# ---------------------------------------------------------------------------
# Step 2 — receive label
# ---------------------------------------------------------------------------

async def team_received_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    label     = update.message.text.strip()
    user_id   = update.effective_user.id
    member_id = context.user_data.get("team_member_id")

    if not member_id:
        await update.message.reply_text("Something went wrong. Use /team add to try again.")
        return ConversationHandler.END

    if len(label) > 50:
        await update.message.reply_text(
            "⚠️ Label must be 50 characters or less. Try a shorter one:"
        )
        return TEAM_ASK_LABEL

    return await _save_member(update.message.reply_text, user_id, member_id, label)


async def team_skip_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id   = update.effective_user.id
    member_id = context.user_data.get("team_member_id")

    if not member_id:
        await update.message.reply_text("Something went wrong. Use /team add to try again.")
        return ConversationHandler.END

    return await _save_member(update.message.reply_text, user_id, member_id, label=None)


async def _save_member(reply_fn, owner_id: int, member_id: int, label: str | None):
    try:
        success = add_team_member(owner_id, member_id, label)
    except ValueError as e:
        await reply_fn(str(e))
        return ConversationHandler.END

    if not success:
        await reply_fn(
            f"⚠️ User <code>{member_id}</code> is already on your team.",
            parse_mode="HTML"
        )
        return ConversationHandler.END

    display = label or f"User {member_id}"
    await reply_fn(
        f"✅ <b>{display}</b> added to your team!\n\n"
        f"👤 ID: <code>{member_id}</code>\n\n"
        "They will now receive the same down and recovery alerts as you.\n\n"
        "⚠️ Make sure they've sent <code>/start</code> to this bot, "
        "otherwise Telegram will block the delivery.",
        parse_mode="HTML"
    )
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# Remove (two-step confirm)
# ---------------------------------------------------------------------------

async def team_remove_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """First tap — confirm prompt."""
    query   = update.callback_query
    user_id = query.from_user.id
    row_id  = int(query.data.split("_")[2])   # team_remove_<id>

    members = get_team_members(user_id)
    match   = next((m for m in members if m["id"] == row_id), None)

    if not match:
        await query.answer("Teammate not found.")
        return

    display = match["label"] or f"User {match['member_user_id']}"
    await query.answer()
    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "✅ Yes, remove",
                callback_data=f"team_confirmremove_{row_id}"
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data=f"team_cancelremove_{row_id}"
            ),
        ]])
    )
    await query.message.reply_text(
        f"⚠️ Remove <b>{display}</b> from your team?\n\n"
        f"They will stop receiving alerts immediately.",
        parse_mode="HTML"
    )


async def team_confirm_remove_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    row_id  = int(query.data.split("_")[2])   # team_confirmremove_<id>

    members = get_team_members(user_id)
    match   = next((m for m in members if m["id"] == row_id), None)
    display = (match["label"] or f"User {match['member_user_id']}") if match else "Teammate"

    remove_team_member(row_id, user_id)
    await query.answer("Removed.")
    await query.edit_message_text(
        f"🗑 <b>{display}</b> removed from your team.\n\n"
        "Use /team to manage your teammates.",
        parse_mode="HTML"
    )


async def team_cancel_remove_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Cancelled.")
    await query.edit_message_text(
        "❌ Cancelled. Teammate is still active.",
        parse_mode="HTML"
    )


# ---------------------------------------------------------------------------
# Cancel fallback
# ---------------------------------------------------------------------------

async def team_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
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
