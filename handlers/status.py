from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters
)
from db.database import get_all_monitors
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

    monitors = get_all_monitors(user_id)

    if not monitors:
        await reply_fn("No monitors yet. Use /add to add your first one.")
        return

    lines = ["⚡ <b>Monitor Status</b>\n"]

    for m in monitors:
        label     = m["label"] or m["url"]
        is_paused = m["active"] == 2

        if is_paused:
            icon        = "⏸"
            status_text = "Paused"
        elif m["last_status"] == "up":
            icon        = "🟢"
            status_text = "Up"
        elif m["last_status"] == "down":
            icon        = "🔴"
            status_text = "Down"
        else:
            icon        = "⚪"
            status_text = "Pending first check"

        if m.get("last_checked"):
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
                ago = f"{mins // 60}h ago"
        else:
            ago = "not checked yet"

        lines.append(f"{icon} <b>{label}</b> — {status_text} <i>({ago})</i>")

    await reply_fn("\n".join(lines), parse_mode="HTML")
