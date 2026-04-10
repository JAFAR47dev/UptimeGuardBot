#tasks/trial_expiry.py
import logging
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.database import get_expired_trials, downgrade_user, get_monitors
from services.scheduler import schedule_monitor

logger = logging.getLogger(__name__)

async def check_expired_trials(context: ContextTypes.DEFAULT_TYPE):
    """
    Daily job — finds expired trial users, downgrades them,
    reschedules their monitors to free interval, and sends
    a conversion message.
    """
    expired_users = get_expired_trials()

    if not expired_users:
        return

    for user in expired_users:
        user_id = user["user_id"]
        try:
            # 1. Downgrade in DB
            downgrade_user(user_id)

            # 2. Reschedule all their monitors back to 5-min interval
            monitors = get_monitors(user_id)
            for m in monitors:
                schedule_monitor(context.application, m["id"], 5)

            # 3. Send conversion message
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "⭐ Upgrade to Pro", callback_data="upgrade"
                )
            ]])

            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    "⏰ <b>Your 7-day Pro trial has ended.</b>\n\n"
                    "Your monitors are still running but have been "
                    "moved back to <b>5-minute</b> check intervals.\n\n"
                    "Upgrade to Pro to get:\n"
                    "⚡ 1-minute check intervals\n"
                    "🔐 SSL certificate expiry warnings\n"
                    "📊 Avg response time tracking\n"
                    "➕ Unlimited monitors\n\n"
                    "👇 Lock in Pro before your next outage slips through."
                ),
                parse_mode="HTML",
                reply_markup=keyboard
            )

            logger.info(f"Trial expired and downgraded: user {user_id}")

        except Exception as e:
            # User may have blocked the bot — don't let one failure
            # stop the loop for other users
            logger.warning(f"Failed to process trial expiry for {user_id}: {e}")
            continue