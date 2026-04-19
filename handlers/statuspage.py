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
)
from config import STATUS_PAGE_BASE_URL

# Conversation state
ASK_TITLE = 20   # outside range used by monitors.py


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _page_url(slug: str) -> str:
    base = STATUS_PAGE_BASE_URL.rstrip("/")
    return f"{base}/status/{slug}"


# ---------------------------------------------------------------------------
# /statuspage — main entry point
# ---------------------------------------------------------------------------

async def statuspage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /statuspage          → show existing page or create one
    /statuspage delete   → delete the page
    /statuspage title    → (Pro) set a custom title (starts conversation)
    """
    user_id = update.effective_user.id
    args    = context.args or []
    pro     = is_pro(user_id)

    # ── sub-command: delete ──────────────────────────────────────────────
    if args and args[0].lower() == "delete":
        page = get_status_page_by_user(user_id)
        if not page:
            await update.message.reply_text("You don't have a status page to delete.")
            return

        delete_status_page(user_id)
        await update.message.reply_text(
            "🗑 <b>Status page deleted.</b>\n\n"
            "The URL is now inactive. Use /statuspage to create a new one.",
            parse_mode="HTML"
        )
        return

    # ── sub-command: title (Pro) ─────────────────────────────────────────
    if args and args[0].lower() == "title":
        if not pro:
            await update.message.reply_text(
                "🔒 <b>Custom titles are a Pro feature.</b>\n\n"
                "Upgrade to set a custom title and remove the "
                "'Powered by UptimeGuard' footer.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")
                ]])
            )
            return ConversationHandler.END

        page = get_status_page_by_user(user_id)
        if not page:
            await update.message.reply_text(
                "You don't have a status page yet. "
                "Run /statuspage first to create one, then set a title."
            )
            return ConversationHandler.END

        await update.message.reply_text(
            "✏️ Send me the new title for your status page.\n\n"
            "Example: <code>Acme Corp — Service Status</code>\n\n"
            "Send /cancel to abort.",
            parse_mode="HTML"
        )
        return ASK_TITLE

    # ── default: show or create ──────────────────────────────────────────
    page = get_status_page_by_user(user_id)

    if page:
        url   = _page_url(page["slug"])
        title = page["title"] or "Status Page"
        pro_line = (
            "\n\n✅ <b>Pro:</b> branding removed, custom title active."
            if pro else
            "\n\n🆓 <b>Free plan:</b> 'Powered by UptimeGuard' footer shown.\n"
            "Upgrade to Pro to remove branding and set a custom title."
        )

        await update.message.reply_text(
            f"📡 <b>Your Status Page</b>\n\n"
            f"🏷 Title: <b>{title}</b>\n"
            f"🔗 URL:\n<code>{url}</code>"
            f"{pro_line}\n\n"
            f"<b>Commands:</b>\n"
            f"/statuspage delete — remove your page\n"
            + (f"/statuspage title — change the title\n" if pro else ""),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔗 Open Status Page", url=url)
            ]])
        )
        return

    # No page yet — create one
    slug = create_status_page(user_id)
    url  = _page_url(slug)

    pro_extras = (
        "\n✅ Branding removed — your page looks fully custom.\n"
        "Use /statuspage title to set a custom title."
        if pro else
        "\n🆓 Free plan: 'Powered by UptimeGuard' footer is shown.\n"
        "Upgrade to Pro to remove it and set a custom title."
    )

    await update.message.reply_text(
        f"✅ <b>Status page created!</b>\n\n"
        f"🔗 Share this URL with your clients:\n"
        f"<code>{url}</code>"
        f"{pro_extras}\n\n"
        f"The page updates live and auto-refreshes every 60 seconds.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔗 Open Status Page", url=url)
        ]])
    )


# ---------------------------------------------------------------------------
# Conversation: set custom title (Pro)
# ---------------------------------------------------------------------------

async def received_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title   = update.message.text.strip()
    user_id = update.effective_user.id

    if len(title) > 80:
        await update.message.reply_text(
            "⚠️ Title must be 80 characters or less. Try a shorter one:"
        )
        return ASK_TITLE

    update_status_page_title(user_id, title)

    page = get_status_page_by_user(user_id)
    url  = _page_url(page["slug"]) if page else ""

    await update.message.reply_text(
        f"✅ <b>Title updated!</b>\n\n"
        f"🏷 New title: <b>{title}</b>\n"
        f"🔗 <code>{url}</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔗 Open Status Page", url=url)
        ]]) if url else None
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# Callback: create page from inline button
# ---------------------------------------------------------------------------

async def create_statuspage_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    page = get_status_page_by_user(user_id)
    if not page:
        slug = create_status_page(user_id)
    else:
        slug = page["slug"]

    url = _page_url(slug)
    pro = is_pro(user_id)

    pro_line = (
        "✅ Pro: no branding, custom title via /statuspage title"
        if pro else
        "🆓 Free: 'Powered by UptimeGuard' footer shown."
    )

    await query.message.reply_text(
        f"✅ <b>Status page ready!</b>\n\n"
        f"🔗 <code>{url}</code>\n\n"
        f"{pro_line}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔗 Open Status Page", url=url)
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
