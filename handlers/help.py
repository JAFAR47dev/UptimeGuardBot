# handlers/help.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import is_pro, get_user, get_user_language
from config import FREE_LIMIT, PRO_MONTHLY_PRICE, PRO_3MONTH_PRICE, PRO_YEARLY_PRICE
from locales.help_strings import ht


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id = update.callback_query.from_user.id
        reply   = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id = update.effective_user.id
        reply   = update.message.reply_text

    lang = get_user_language(user_id)
    pro  = is_pro(user_id)
    user = get_user(user_id)

    if user and user["plan"] == "trial":
        plan_text = ht(lang, "plan_trial")
    elif pro:
        plan_text = ht(lang, "plan_pro")
    else:
        plan_text = ht(lang, "plan_free")

    save_3m = PRO_MONTHLY_PRICE * 3  - PRO_3MONTH_PRICE
    save_yr = PRO_MONTHLY_PRICE * 12 - PRO_YEARLY_PRICE

    await reply(
        ht(lang, "help_full",
           plan_text=plan_text,
           free_limit=FREE_LIMIT,
           monthly=PRO_MONTHLY_PRICE,
           three_month=PRO_3MONTH_PRICE,
           yearly=PRO_YEARLY_PRICE,
           save_3m=save_3m,
           save_yr=save_yr),
        parse_mode="HTML",
        reply_markup=_help_keyboard(pro, lang)
    )


def _help_keyboard(pro: bool, lang: str) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(ht(lang, "btn_add_monitor"), callback_data="add_monitor"),
            InlineKeyboardButton(ht(lang, "btn_test_alert"),  callback_data="testalert"),
        ],
        [
            InlineKeyboardButton(ht(lang, "btn_referral"), callback_data="referral_info"),
        ],
    ]
    if not pro:
        rows.append([
            InlineKeyboardButton(ht(lang, "btn_upgrade"), callback_data="upgrade")
        ])
    return InlineKeyboardMarkup(rows)