from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import ContextTypes
from db.database import upgrade_user
from config import PRO_MONTHLY_PRICE, PRO_3MONTH_PRICE, PRO_YEARLY_PRICE


async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    await reply_fn(
        "⭐ <b>Upgrade to UptimeGuard Pro</b>\n\n"
        "<b>What you unlock:</b>\n"
        "✅ Unlimited monitors\n"
        "✅ 1-minute check interval\n"
        "✅ SSL certificate expiry warnings\n"
        "✅ Slow response threshold alerts\n"
        "✅ Webhook integrations (Slack, PagerDuty)\n"
        "✅ Team notifications\n"
        "✅ Public status page\n"
        "✅ Weekly summary reports\n\n"
        "─────────────────────────\n"
        f"📅 <b>Monthly</b>       {PRO_MONTHLY_PRICE} ⭐\n"
        f"📆 <b>3 Months</b>    {PRO_3MONTH_PRICE} ⭐  "
        f"<i>save {PRO_MONTHLY_PRICE * 3 - PRO_3MONTH_PRICE} Stars</i>\n"
        f"📆 <b>Yearly</b>       {PRO_YEARLY_PRICE} ⭐  "
        f"<i>save {PRO_MONTHLY_PRICE * 12 - PRO_YEARLY_PRICE} Stars</i>\n"
        "─────────────────────────\n\n"
        "💬 <i>Not happy? Message us within 7 days for a full refund.</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                f"📅 Monthly — {PRO_MONTHLY_PRICE} ⭐",
                callback_data="pay_monthly"
            )],
            [InlineKeyboardButton(
                f"📆 3 Months — {PRO_3MONTH_PRICE} ⭐  ✨ Recommended",
                callback_data="pay_3month"
            )],
            [InlineKeyboardButton(
                f"📆 Yearly — {PRO_YEARLY_PRICE} ⭐  🏆 Best Value",
                callback_data="pay_yearly"
            )],
        ])
    )


# ─────────────────────────────────────────
# Invoice senders
# ─────────────────────────────────────────

async def pay_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Legacy monthly callback — kept for backward compatibility."""
    query = update.callback_query
    await query.answer()
    await _send_invoice(
        context.bot,
        chat_id     = query.from_user.id,
        title       = "UptimeGuard Pro — Monthly",
        description = "Unlimited monitors · 1-min checks · SSL alerts · Webhooks",
        payload     = "pro_monthly",
        price       = PRO_MONTHLY_PRICE
    )


async def pay_monthly_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await _send_invoice(
        context.bot,
        chat_id     = query.from_user.id,
        title       = "UptimeGuard Pro — Monthly",
        description = "Unlimited monitors · 1-min checks · SSL alerts · Webhooks",
        payload     = "pro_monthly",
        price       = PRO_MONTHLY_PRICE
    )


async def pay_3month_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await _send_invoice(
        context.bot,
        chat_id     = query.from_user.id,
        title       = "UptimeGuard Pro — 3 Months",
        description = (
            f"Save {PRO_MONTHLY_PRICE * 3 - PRO_3MONTH_PRICE} Stars vs monthly. "
            "Unlimited monitors · 1-min checks · SSL alerts · Webhooks"
        ),
        payload     = "pro_3month",
        price       = PRO_3MONTH_PRICE
    )


async def pay_yearly_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await _send_invoice(
        context.bot,
        chat_id     = query.from_user.id,
        title       = "UptimeGuard Pro — Yearly",
        description = (
            f"Save {PRO_MONTHLY_PRICE * 12 - PRO_YEARLY_PRICE} Stars vs monthly. "
            "Unlimited monitors · 1-min checks · SSL alerts · Webhooks"
        ),
        payload     = "pro_yearly",
        price       = PRO_YEARLY_PRICE
    )


async def _send_invoice(
    bot, chat_id: int, title: str,
    description: str, payload: str, price: int
):
    """Shared invoice sender — handles errors gracefully."""
    try:
        await bot.send_invoice(
            chat_id     = chat_id,
            title       = title,
            description = description,
            payload     = payload,
            currency    = "XTR",
            prices      = [LabeledPrice(title, price)]
        )
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(
            f"Invoice send failed for {chat_id}: {e}", exc_info=True
        )
        await bot.send_message(
            chat_id = chat_id,
            text    = (
                "⚠️ Something went wrong sending the invoice.\n\n"
                "Please try again or contact support."
            )
        )


# ─────────────────────────────────────────
# Pre-checkout
# ─────────────────────────────────────────

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


# ─────────────────────────────────────────
# Payment success
# ─────────────────────────────────────────

async def payment_success(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    payload = update.message.successful_payment.invoice_payload
    stars   = update.message.successful_payment.total_amount

    import logging
    logger = logging.getLogger(__name__)

    # Determine plan duration from payload
    plan_labels = {
        "pro_monthly": "Monthly",
        "pro_3month":  "3 Months",
        "pro_yearly":  "Yearly",
    }
    plan_label = plan_labels.get(payload, "Pro")

    # Set pro_expires based on plan
    from db.database import get_conn
    from datetime import datetime
    import calendar

    def add_months(months: int) -> str:
        now   = datetime.now()
        month = now.month - 1 + months
        year  = now.year + month // 12
        month = month % 12 + 1
        day   = min(now.day, calendar.monthrange(year, month)[1])
        return datetime(year, month, day,
                        now.hour, now.minute, now.second).isoformat()

    expiry_map = {
        "pro_monthly": add_months(1),
        "pro_3month":  add_months(3),
        "pro_yearly":  add_months(12),
    }
    expiry = expiry_map.get(payload, add_months(1))

    # Upgrade user
    upgrade_user(user_id, "pro")

    # Store expiry date
    conn = get_conn()
    c    = conn.cursor()
    try:
        c.execute(
            "ALTER TABLE users ADD COLUMN pro_expires TEXT"
        )
        conn.commit()
    except Exception:
        pass  # Column already exists
    c.execute(
        "UPDATE users SET pro_expires = ? WHERE user_id = ?",
        (expiry, user_id)
    )
    conn.commit()
    conn.close()

    logger.info(
        f"Payment success: user={user_id} "
        f"plan={plan_label} stars={stars} expires={expiry}"
    )

    # Reschedule all monitors at 1-min interval
    from db.database import get_monitors
    from services.scheduler import schedule_monitor
    monitors = get_monitors(user_id)
    for m in monitors:
        schedule_monitor(context.application, m["id"], 1)

    # Format expiry for display
    try:
        expiry_display = datetime.fromisoformat(expiry).strftime("%B %d, %Y")
    except Exception:
        expiry_display = expiry

    await update.message.reply_text(
        f"🎉 <b>Welcome to UptimeGuard Pro!</b>\n\n"
        f"📦 Plan: <b>{plan_label}</b>\n"
        f"📅 Access until: <b>{expiry_display}</b>\n\n"
        f"<b>Now active:</b>\n"
        f"⚡ Monitors check every minute\n"
        f"🔐 SSL expiry warnings\n"
        f"🐢 Slow response alerts\n"
        f"🔗 Webhook integrations\n"
        f"👥 Team notifications\n"
        f"🌐 Public status page\n\n"
        f"Use /add to add unlimited monitors.",
        parse_mode="HTML"
    )
