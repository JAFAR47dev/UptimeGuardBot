from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import is_pro
from config import FREE_LIMIT, PRO_MONTHLY_PRICE

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle both direct command and callback query
    if update.callback_query:
        user_id = update.callback_query.from_user.id
        reply   = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id = update.effective_user.id
        reply   = update.message.reply_text

    pro       = is_pro(user_id)
    plan_text = "✅ Pro" if pro else "🆓 Free"

    await reply(
        f"📖 <b>UptimeGuard Help</b>\n"
        f"Your plan: <b>{plan_text}</b>\n\n"

        "─────────────────────\n"
        "⚙️ <b>Commands</b>\n"
        "─────────────────────\n\n"

        "/start — Home screen with live snapshot\n\n"

        "/add — Add a new URL to monitor\n"
        "<i>Example: https://mystore.com</i>\n\n"

        "/list — All your monitors with actions\n"
        "<i>Pause, resume, delete, set thresholds</i>\n\n"

        "/status — Quick one-line status per monitor\n"
        "<i>Fastest way to check everything at a glance</i>\n\n"

        "/report — 7-day uptime report\n"
        "<i>Uptime %, avg response time per monitor</i>\n\n"

        "/upgrade — Upgrade to Pro\n\n"

        "/help — This message\n\n"

        "─────────────────────\n"
        "📦 <b>Free Plan</b>\n"
        "─────────────────────\n\n"

        f"• Up to {FREE_LIMIT} monitors\n"
        "• 5-minute check interval\n"
        "• Down + recovery alerts\n"
        "• 7-day uptime history\n\n"

        "─────────────────────\n"
        "⭐ <b>Pro Plan</b>\n"
        "─────────────────────\n\n"

        "• Unlimited monitors\n"
        "• 1-minute check interval\n"
        "• SSL certificate expiry warnings\n"
        "• Slow response threshold alerts\n"
        "• Full weekly summary reports\n"
        "• Avg response time tracking\n\n"

        f"💰 <b>{PRO_MONTHLY_PRICE} Telegram Stars / month</b>\n\n"

        "─────────────────────\n"
        "💡 <b>Tips</b>\n"
        "─────────────────────\n\n"

        "• Use ⏸ <b>Pause</b> during planned maintenance "
        "instead of deleting — your history is preserved.\n\n"
        "• Pro users: set a 🐢 <b>slow response threshold</b> "
        "per monitor via /list — get alerted before "
        "customers notice sluggishness.\n\n"
        "• SSL warnings fire at 30, 7, and 1 day before "
        "expiry so you never get caught off guard.",

        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Monitor", callback_data="add_monitor")],
            [InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")]
        ]) if not pro else InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Monitor", callback_data="add_monitor")]
        ])
    )