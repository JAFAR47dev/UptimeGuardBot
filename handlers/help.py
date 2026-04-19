# handlers/help.py
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
        "<i>Pause, resume, delete, notes, thresholds</i>\n\n"

        "/status — Quick one-line status per monitor\n"
        "<i>Fastest way to check everything at a glance</i>\n\n"

        "/report — 7-day uptime report\n"
        "<i>Uptime %, avg response time per monitor</i>\n\n"

        "/testalert — Send a test down/up alert pair\n"
        "<i>Verify your notifications are working</i>\n\n"

        "/statuspage — Generate a public status page URL\n"
        "<i>Share live uptime with clients</i>\n\n"

        "/upgrade — Upgrade to Pro\n\n"

        "/help — This message\n\n"

        "─────────────────────\n"
        "📦 <b>Free Plan</b>\n"
        "─────────────────────\n\n"

        f"• Up to {FREE_LIMIT} monitors\n"
        "• 5-minute check interval\n"
        "• Down + recovery alerts\n"
        "• 7-day uptime history\n"
        "• Monitor notes\n"
        "• Alert snooze\n"
        "• Public status page\n\n"

        "─────────────────────\n"
        "⭐ <b>Pro Plan</b>\n"
        "─────────────────────\n\n"

        "• Unlimited monitors\n"
        "• 1-minute check interval\n"
        "• SSL certificate expiry warnings\n"
        "• Slow response threshold alerts\n"
        "• Full weekly summary reports\n"
        "• Avg response time tracking\n"
        "• Custom status page title + no branding\n\n"

        f"💰 <b>{PRO_MONTHLY_PRICE} Telegram Stars / month</b>\n\n"

        "─────────────────────\n"
        "💡 <b>Tips</b>\n"
        "─────────────────────\n\n"

        "• Use ⏸ <b>Pause</b> during planned maintenance "
        "instead of deleting — your history is preserved.\n\n"
        "• Got a down alert while fixing an issue? Tap "
        "🔕 <b>Snooze 30 mins</b> to silence repeats. "
        "Tap again to extend. Recovery alerts always fire.\n\n"
        "• Add a 📝 <b>Note</b> to each monitor via /list — "
        "it appears in every down alert so you always know "
        "who to call without checking elsewhere.\n\n"
        "• Pro users: set a 🐢 <b>slow response threshold</b> "
        "per monitor via /list — get alerted before "
        "customers notice sluggishness.\n\n"
        "• SSL warnings fire at 30, 7, and 1 day before "
        "expiry so you never get caught off guard.",

        parse_mode="HTML",
        reply_markup=_help_keyboard(pro)
    )


def _help_keyboard(pro: bool) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton("➕ Add Monitor",    callback_data="add_monitor"),
         InlineKeyboardButton("🧪 Test Alert",     callback_data="testalert")],
    ]
    if not pro:
        rows.append([
            InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")
        ])
    return InlineKeyboardMarkup(rows)
