# handlers/help.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import is_pro, get_user
from config import FREE_LIMIT, PRO_MONTHLY_PRICE, PRO_3MONTH_PRICE, PRO_YEARLY_PRICE


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id = update.callback_query.from_user.id
        reply   = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id = update.effective_user.id
        reply   = update.message.reply_text

    pro       = is_pro(user_id)
    user      = get_user(user_id)
    plan_text = (
        "✅ Pro (Trial)" if user and user["plan"] == "trial" else
        "✅ Pro"         if pro                               else
        "🆓 Free"
    )

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
        "<i>Pause, resume, delete, notes, thresholds,\n"
        "webhooks, keyword checks, confirm count</i>\n\n"

        "/status — Quick one-line status per monitor\n"
        "<i>Fastest way to check everything at a glance</i>\n\n"

        "/report — 7-day uptime report\n"
        "<i>Uptime %, avg response time per monitor</i>\n\n"

        "/incidents — Incident history per monitor\n"
        "<i>Timeline of past down events and durations</i>\n\n"

        "/testalert — Send a test down/up alert pair\n"
        "<i>Verify your notifications are working</i>\n\n"

        "/maintenance — Manage maintenance windows\n"
        "<i>Pause alerts during planned downtime</i>\n\n"

        "/team — Manage team notification members\n"
        "<i>Add teammates to receive your alerts (Pro)</i>\n\n"

        "/statuspage — Your public status page\n"
        "<i>Share live uptime with clients</i>\n\n"

        "/referral — Your referral link and stats\n"
        "<i>Earn bonus monitor slots by referring users</i>\n\n"

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
        "• Public status page\n"
        "• Maintenance windows (1 window)\n"
        "• Referral bonus monitor slots\n\n"

        "─────────────────────\n"
        "⭐ <b>Pro Plan</b>\n"
        "─────────────────────\n\n"

        "• Unlimited monitors\n"
        "• 1-minute check interval\n"
        "• SSL certificate expiry warnings\n"
        "• Slow response threshold alerts\n"
        "• HTTP keyword monitoring\n"
        "• Confirm count (reduce false alerts)\n"
        "• Webhook integrations (Slack, PagerDuty)\n"
        "• Team notifications (up to 5 members)\n"
        "• Unlimited maintenance windows\n"
        "• Custom status page title + no branding\n"
        "• Full weekly summary reports\n"
        "• Avg response time tracking\n\n"

        "─────────────────────\n"
        "💰 <b>Pricing</b>\n"
        "─────────────────────\n\n"

        f"📅 Monthly       <b>{PRO_MONTHLY_PRICE} Stars</b>\n"
        f"📆 3 Months    <b>{PRO_3MONTH_PRICE} Stars</b>  "
        f"<i>save {PRO_MONTHLY_PRICE * 3 - PRO_3MONTH_PRICE} Stars</i>\n"
        f"📆 Yearly        <b>{PRO_YEARLY_PRICE} Stars</b>  "
        f"<i>save {PRO_MONTHLY_PRICE * 12 - PRO_YEARLY_PRICE} Stars</i>\n\n"

        "💬 <i>Not happy? Message us within 7 days for a full refund.</i>\n\n"

        "─────────────────────\n"
        "💡 <b>Tips</b>\n"
        "─────────────────────\n\n"

        "• Use ⏸ <b>Pause</b> during planned maintenance "
        "instead of deleting — your history is preserved.\n\n"

        "• Got a down alert while fixing? Tap "
        "🔕 <b>Snooze</b> to silence repeats. "
        "Recovery alerts always fire regardless.\n\n"

        "• Add a 📝 <b>Note</b> to each monitor via /list — "
        "it appears in every down alert so you always know "
        "who to call without checking elsewhere.\n\n"

        "• 🐢 <b>Slow response threshold</b> — get alerted "
        "when a site is slow before it fully goes down. "
        "Set per monitor via /list (Pro).\n\n"

        "• 🔑 <b>Keyword monitor</b> — confirm a word or phrase "
        "appears in the page body on every check. "
        "Catches silent failures where the site returns 200 "
        "but shows an error page (Pro).\n\n"

        "• 🔢 <b>Confirm count</b> — require N consecutive "
        "failures before alerting. Eliminates false alarms "
        "from brief network blips (Pro).\n\n"

        "• 🔗 <b>Webhooks</b> — connect to Slack or PagerDuty "
        "via /list → Webhook on any monitor (Pro).\n\n"

        "• 🔐 SSL warnings fire at 30, 7, and 1 day before "
        "expiry so you're never caught off guard.\n\n"

        "• 👥 <b>Team alerts</b> — add teammates via /team "
        "so the whole team knows when something goes down, "
        "not just you (Pro).",

        parse_mode="HTML",
        reply_markup=_help_keyboard(pro)
    )


def _help_keyboard(pro: bool) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton("➕ Add Monitor", callback_data="add_monitor"),
            InlineKeyboardButton("🧪 Test Alert",  callback_data="testalert"),
        ],
        [
            InlineKeyboardButton("👥 Referral Link", callback_data="referral_info"),
        ],
    ]
    if not pro:
        rows.append([
            InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")
        ])
    return InlineKeyboardMarkup(rows)
