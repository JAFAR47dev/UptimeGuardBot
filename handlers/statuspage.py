# handlers/statuspage.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, filters,
)
from db.database import (
    get_status_page_by_user,
    create_status_page,
    delete_status_page,
    update_status_page_title,
    is_pro,
    get_user_language,
)
from config import STATUS_PAGE_BASE_URL
from locales.team_strings import tt

# Conversation state
ASK_TITLE = 20


def _page_url(slug: str) -> str:
    base = STATUS_PAGE_BASE_URL.rstrip("/")
    return f"{base}/status/{slug}"


# ---------------------------------------------------------------------------
# /statuspage — main entry point
# ---------------------------------------------------------------------------

async def statuspage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args    = context.args or []
    pro     = is_pro(user_id)
    lang    = get_user_language(user_id)

    # ── sub-command: delete ──────────────────────────────────────────────
    if args and args[0].lower() == "delete":
        page = get_status_page_by_user(user_id)
        if not page:
            await update.message.reply_text(tt(lang, "sp_no_page_to_delete"))
            return

        delete_status_page(user_id)
        await update.message.reply_text(
            tt(lang, "sp_deleted"), parse_mode="HTML"
        )
        return

    # ── sub-command: title (Pro) ─────────────────────────────────────────
    if args and args[0].lower() == "title":
        if not pro:
            await update.message.reply_text(
                tt(lang, "sp_title_pro_gate"),
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        tt(lang, "sp_btn_upgrade"), callback_data="upgrade"
                    )
                ]])
            )
            return ConversationHandler.END

        page = get_status_page_by_user(user_id)
        if not page:
            await update.message.reply_text(tt(lang, "sp_no_page_for_title"))
            return ConversationHandler.END

        await update.message.reply_text(
            tt(lang, "sp_ask_title"), parse_mode="HTML"
        )
        return ASK_TITLE

    # ── default: show or create ──────────────────────────────────────────
    page = get_status_page_by_user(user_id)

    if page:
        url      = _page_url(page["slug"])
        title    = page["title"] or "Status Page"
        pro_line = (
            tt(lang, "sp_existing_pro")
            if pro else
            tt(lang, "sp_existing_free")
        )
        title_cmd = tt(lang, "sp_existing_title_cmd") if pro else ""

        await update.message.reply_text(
            tt(lang, "sp_existing_page",
               title=title, url=url,
               pro_line=pro_line, title_cmd=title_cmd),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(tt(lang, "sp_btn_open"), url=url)
            ]])
        )
        return

    # No page yet — create one
    slug       = create_status_page(user_id)
    url        = _page_url(slug)
    pro_extras = (
        tt(lang, "sp_created_pro_extras")
        if pro else
        tt(lang, "sp_created_free_extras")
    )

    await update.message.reply_text(
        tt(lang, "sp_created", url=url, pro_extras=pro_extras),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(tt(lang, "sp_btn_open"), url=url)
        ]])
    )


# ---------------------------------------------------------------------------
# Conversation: set custom title (Pro)
# ---------------------------------------------------------------------------

async def received_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title   = update.message.text.strip()
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)

    if len(title) > 80:
        await update.message.reply_text(tt(lang, "sp_title_too_long"))
        return ASK_TITLE

    update_status_page_title(user_id, title)
    page = get_status_page_by_user(user_id)
    url  = _page_url(page["slug"]) if page else ""

    await update.message.reply_text(
        tt(lang, "sp_title_updated", title=title, url=url),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(tt(lang, "sp_btn_open"), url=url)
        ]]) if url else None
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)
    await update.message.reply_text(tt(lang, "sp_cancelled"))
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# Callback: create page from inline button
# ---------------------------------------------------------------------------

async def create_statuspage_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()

    page = get_status_page_by_user(user_id)
    slug = page["slug"] if page else create_status_page(user_id)
    url  = _page_url(slug)
    pro  = is_pro(user_id)

    pro_line = (
        tt(lang, "sp_callback_pro_line")
        if pro else
        tt(lang, "sp_callback_free_line")
    )

    await query.message.reply_text(
        tt(lang, "sp_callback_ready", url=url, pro_line=pro_line),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(tt(lang, "sp_btn_open"), url=url)
        ]])
    )


# ---------------------------------------------------------------------------
# ConversationHandler export
# ---------------------------------------------------------------------------

statuspage_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("statuspage", statuspage_command),
        CallbackQueryHandler(create_statuspage_callback, pattern="^create_statuspage$"),
    ],
    states={
        ASK_TITLE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_title),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)