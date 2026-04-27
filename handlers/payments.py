# handlers/payments.py
import logging
import calendar
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import ContextTypes
from db.database import upgrade_user, get_user_language
from config import PRO_MONTHLY_PRICE, PRO_3MONTH_PRICE, PRO_YEARLY_PRICE
from locales.payment_strings import pt_

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# /upgrade — plan selection page
# ---------------------------------------------------------------------------

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    lang    = get_user_language(user_id)
    save_3m = PRO_MONTHLY_PRICE * 3 - PRO_3MONTH_PRICE
    save_yr = PRO_MONTHLY_PRICE * 12 - PRO_YEARLY_PRICE

    await reply_fn(
        pt_(lang, "upgrade_header",
            monthly=PRO_MONTHLY_PRICE,
            three_month=PRO_3MONTH_PRICE,
            yearly=PRO_YEARLY_PRICE,
            save_3m=save_3m,
            save_yr=save_yr),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                pt_(lang, "btn_monthly", price=PRO_MONTHLY_PRICE),
                callback_data="pay_monthly"
            )],
            [InlineKeyboardButton(
                pt_(lang, "btn_3month", price=PRO_3MONTH_PRICE),
                callback_data="pay_3month"
            )],
            [InlineKeyboardButton(
                pt_(lang, "btn_yearly", price=PRO_YEARLY_PRICE),
                callback_data="pay_yearly"
            )],
        ])
    )


# ---------------------------------------------------------------------------
# Invoice senders
# ---------------------------------------------------------------------------

async def _send_invoice(bot, chat_id: int, title: str,
                        description: str, payload: str, price: int, lang: str):
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
        logger.error(f"Invoice send failed for {chat_id}: {e}", exc_info=True)
        await bot.send_message(
            chat_id=chat_id,
            text=pt_(lang, "invoice_error")
        )


async def pay_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Legacy monthly callback — kept for backward compatibility."""
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()
    save_3m = PRO_MONTHLY_PRICE * 3 - PRO_3MONTH_PRICE
    await _send_invoice(
        context.bot,
        chat_id     = user_id,
        title       = pt_(lang, "invoice_title_monthly"),
        description = pt_(lang, "invoice_desc_monthly"),
        payload     = "pro_monthly",
        price       = PRO_MONTHLY_PRICE,
        lang        = lang,
    )


async def pay_monthly_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()
    await _send_invoice(
        context.bot,
        chat_id     = user_id,
        title       = pt_(lang, "invoice_title_monthly"),
        description = pt_(lang, "invoice_desc_monthly"),
        payload     = "pro_monthly",
        price       = PRO_MONTHLY_PRICE,
        lang        = lang,
    )


async def pay_3month_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()
    save = PRO_MONTHLY_PRICE * 3 - PRO_3MONTH_PRICE
    await _send_invoice(
        context.bot,
        chat_id     = user_id,
        title       = pt_(lang, "invoice_title_3month"),
        description = pt_(lang, "invoice_desc_3month", save=save),
        payload     = "pro_3month",
        price       = PRO_3MONTH_PRICE,
        lang        = lang,
    )


async def pay_yearly_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()
    save = PRO_MONTHLY_PRICE * 12 - PRO_YEARLY_PRICE
    await _send_invoice(
        context.bot,
        chat_id     = user_id,
        title       = pt_(lang, "invoice_title_yearly"),
        description = pt_(lang, "invoice_desc_yearly", save=save),
        payload     = "pro_yearly",
        price       = PRO_YEARLY_PRICE,
        lang        = lang,
    )


# ---------------------------------------------------------------------------
# Pre-checkout
# ---------------------------------------------------------------------------

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


# ---------------------------------------------------------------------------
# Payment success
# ---------------------------------------------------------------------------

def _add_months(months: int) -> str:
    now   = datetime.now()
    month = now.month - 1 + months
    year  = now.year + month // 12
    month = month % 12 + 1
    day   = min(now.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day,
                    now.hour, now.minute, now.second).isoformat()


async def payment_success(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    payload = update.message.successful_payment.invoice_payload
    stars   = update.message.successful_payment.total_amount
    lang    = get_user_language(user_id)

    expiry_map = {
        "pro_monthly": _add_months(1),
        "pro_3month":  _add_months(3),
        "pro_yearly":  _add_months(12),
    }
    plan_key_map = {
        "pro_monthly": "plan_label_monthly",
        "pro_3month":  "plan_label_3month",
        "pro_yearly":  "plan_label_yearly",
    }

    expiry     = expiry_map.get(payload, _add_months(1))
    plan_label = pt_(lang, plan_key_map.get(payload, "plan_label_monthly"))

    # Upgrade user and store expiry
    upgrade_user(user_id, "pro")

    from db.database import get_conn
    conn = get_conn()
    c    = conn.cursor()
    try:
        c.execute("ALTER TABLE users ADD COLUMN pro_expires TEXT")
        conn.commit()
    except Exception:
        pass
    c.execute(
        "UPDATE users SET pro_expires = ? WHERE user_id = ?",
        (expiry, user_id)
    )
    conn.commit()
    conn.close()

    logger.info(
        f"Payment success: user={user_id} plan={plan_label} "
        f"stars={stars} expires={expiry}"
    )

    # Reschedule monitors at 1-min interval
    from db.database import get_monitors
    from services.scheduler import schedule_monitor
    for m in get_monitors(user_id):
        schedule_monitor(context.application, m["id"], 1)

    try:
        expiry_display = datetime.fromisoformat(expiry).strftime("%B %d, %Y")
    except Exception:
        expiry_display = expiry

    await update.message.reply_text(
        pt_(lang, "payment_success",
            plan_label=plan_label,
            expiry=expiry_display),
        parse_mode="HTML"
    )