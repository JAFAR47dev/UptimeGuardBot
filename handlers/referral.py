### `handlers/referral.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import (
    get_or_create_user, get_qualified_referral_count,
    get_referral_count, get_monitor_limit, is_pro
)
from config import bot_username, REFERRAL_GOAL, REFERRAL_BONUS_SLOTS


async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /referral — shows the user their referral link
    and a live count of referrals so far.
    """
    # Works from both command and callback query
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    user, _ = get_or_create_user(user_id)
    pro      = is_pro(user_id)

    # Build referral link
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    # Counts
    qualified = get_qualified_referral_count(user_id)  # completed goal tiers
    total     = get_referral_count(user_id)             # all-time referrals with ≥1 monitor

    # Progress toward next reward
    progress      = total % REFERRAL_GOAL
    remaining     = REFERRAL_GOAL - progress
    progress_bar  = _progress_bar(progress, REFERRAL_GOAL)

    # Current bonus slots (free users only)
    bonus_slots   = user.get("bonus_monitors", 0) if user else 0
    current_limit = get_monitor_limit(user_id)

    if pro:
        reward_text = (
            f"⭐ You're on Pro — referrals extend your Pro access.\n"
            f"Every <b>{REFERRAL_GOAL} referrals</b> = extra days added."
        )
    else:
        reward_text = (
            f"🆓 You're on Free — referrals unlock extra monitor slots.\n"
            f"Every <b>{REFERRAL_GOAL} referrals</b> = "
            f"+{REFERRAL_BONUS_SLOTS} monitor slot(s).\n"
            f"Current limit: <b>{current_limit} monitors</b>"
            f"{f' (+{bonus_slots} bonus)' if bonus_slots else ''}."
        )

    text = (
        f"👥 <b>Your Referral Link</b>\n\n"
        f"<code>{ref_link}</code>\n\n"
        f"Share this link. When someone signs up and adds their "
        f"first monitor, it counts as a qualified referral.\n\n"
        f"─────────────────────────\n"
        f"📊 <b>Your Stats</b>\n"
        f"─────────────────────────\n"
        f"Total referrals:     <b>{total}</b>\n"
        f"Rewards earned:      <b>{qualified // REFERRAL_GOAL if qualified else 0}</b>\n\n"
        f"Progress to next reward:\n"
        f"{progress_bar} <b>{progress}/{REFERRAL_GOAL}</b>\n"
        f"<i>{remaining} more to go</i>\n\n"
        f"─────────────────────────\n"
        f"🎁 <b>Reward</b>\n"
        f"─────────────────────────\n"
        f"{reward_text}"
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
                "🔄 Refresh Stats",
                callback_data="referral_refresh"
            )]
        ]),
        disable_web_page_preview=True
    )


async def referral_refresh_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Refresh button — reruns the same handler."""
    await referral(update, context)


def _progress_bar(current: int, total: int, length: int = 10) -> str:
    """Simple text progress bar. e.g. ▓▓▓▓░░░░░░"""
    filled = int((current / total) * length) if total > 0 else 0
    empty  = length - filled
    return "▓" * filled + "░" * empty

