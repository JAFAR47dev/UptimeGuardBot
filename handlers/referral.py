# handlers/referral.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import (
    get_or_create_user, get_qualified_referral_count,
    get_referral_count, get_monitor_limit, is_pro,
    get_user_language,
)
from config import bot_username, REFERRAL_GOAL, REFERRAL_BONUS_SLOTS
from locales.payment_strings import pt_


def _progress_bar(current: int, total: int, length: int = 10) -> str:
    """Simple text progress bar. e.g. ▓▓▓▓░░░░░░"""
    filled = int((current / total) * length) if total > 0 else 0
    empty  = length - filled
    return "▓" * filled + "░" * empty


async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /referral — shows the user their referral link and live stats.
    Works from both command and callback query.
    """
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    lang     = get_user_language(user_id)
    user, _  = get_or_create_user(user_id)
    pro      = is_pro(user_id)

    ref_link  = f"https://t.me/{bot_username}?start=ref_{user_id}"
    qualified = get_qualified_referral_count(user_id)
    total     = get_referral_count(user_id)
    progress  = total % REFERRAL_GOAL
    remaining = REFERRAL_GOAL - progress
    bar       = _progress_bar(progress, REFERRAL_GOAL)
    rewards   = qualified // REFERRAL_GOAL if qualified else 0

    if pro:
        reward_text = pt_(lang, "referral_reward_pro", goal=REFERRAL_GOAL)
    else:
        bonus_slots   = user.get("bonus_monitors", 0) if user else 0
        current_limit = get_monitor_limit(user_id)
        bonus_str     = (
            pt_(lang, "referral_bonus_str", bonus=bonus_slots)
            if bonus_slots else ""
        )
        reward_text = pt_(
            lang, "referral_reward_free",
            goal=REFERRAL_GOAL,
            bonus=REFERRAL_BONUS_SLOTS,
            limit=current_limit,
            bonus_str=bonus_str,
        )

    text = pt_(
        lang, "referral_page",
        ref_link=ref_link,
        total=total,
        rewards=rewards,
        bar=bar,
        progress=progress,
        goal=REFERRAL_GOAL,
        remaining=remaining,
        reward_text=reward_text,
    )

    await reply_fn(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "📋 Copy Link",
                switch_inline_query=ref_link
            )],
            [InlineKeyboardButton(
                pt_(lang, "btn_refresh"),
                callback_data="referral_refresh"
            )],
        ]),
        disable_web_page_preview=True,
    )


async def referral_refresh_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Refresh button — reruns the same handler."""
    await referral(update, context)