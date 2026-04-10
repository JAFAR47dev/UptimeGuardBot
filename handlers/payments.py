##handlers/payments.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import ContextTypes
from db.database import upgrade_user
from config import PRO_MONTHLY_PRICE

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("⭐ Pay with Telegram Stars", callback_data="pay_pro")
    ]])
    await update.message.reply_text(
        "⭐ <b>Upgrade to Pro</b>\n\n"
        "✅ Unlimited monitors\n"
        "✅ 1-minute check interval\n"
        "✅ SSL expiry warnings\n"
        "✅ Avg response time tracking\n"
        "✅ Weekly summary reports\n\n"
        f"💰 <b>{PRO_MONTHLY_PRICE} Telegram Stars / month</b>",
        parse_mode="HTML",
        reply_markup=keyboard
    )

async def pay_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_invoice(
        chat_id=query.from_user.id,
        title="UptimeGuard Pro",
        description="Unlimited monitors, 1-min checks, SSL alerts",
        payload="pro_monthly",
        currency="XTR",
        prices=[LabeledPrice("Pro Monthly", PRO_MONTHLY_PRICE)]
    )

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def payment_success(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    upgrade_user(user_id, "pro")

    # Re-schedule all monitors at 1-min interval
    from db.database import get_monitors
    from services.scheduler import schedule_monitor
    monitors = get_monitors(user_id)
    for m in monitors:
        schedule_monitor(context.application, m["id"], 1)

    await update.message.reply_text(
        "🎉 <b>Welcome to Pro!</b>\n\n"
        "Your monitors are now checked every minute.\n"
        "SSL expiry warnings are active.\n\n"
        "Use /add to add unlimited monitors.",
        parse_mode="HTML"
    )
