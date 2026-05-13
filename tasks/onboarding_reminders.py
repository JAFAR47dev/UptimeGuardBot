"""
tasks/onboarding_reminders.py
─────────────────────────────
Automated onboarding reminder system for UptimeGuardBot.

How it works:
  - A PTB JobQueue job runs every hour (configurable via CHECK_INTERVAL_SECONDS).
  - Each run queries only users who: have not added a monitor AND still have
    unsent reminders. Active users are excluded at the DB query level.
  - Per-user timing is checked in Python against joined_at.
  - Each reminder is sent at most once. The sent flag is written to the DB
    before the Telegram send, preventing duplicate sends even if the bot
    crashes mid-loop.
  - If a user has blocked the bot, the exception is caught and logged.
    The reminder is still marked sent so we don't retry blocked users.

Reminder schedule:
  #1 — 24 hours after joining       (condition: reminder_1 not sent)
  #2 — 3 days after joining         (condition: reminder_1 sent, reminder_2 not sent)
  #3 — 7 days after joining         (condition: reminder_2 sent, reminder_3 not sent)

Integration:
  Call `register_onboarding_jobs(app)` from bot.py inside post_init,
  after the application is built.
"""

import logging
from datetime import datetime, timedelta

from telegram.error import Forbidden, TelegramError

from db.database import get_pending_reminder_users, mark_reminder_sent

logger = logging.getLogger(__name__)

# How often the job wakes up to check for due reminders.
# Hourly is fine — reminder timing is day-level, not minute-level.
CHECK_INTERVAL_SECONDS = 3600  # 1 hour

# Reminder timing thresholds
_REMINDER_SCHEDULE = [
    # (reminder_num, hours_after_join, prerequisite_sent_flag)
    # prerequisite_sent_flag: the reminder_N_sent key that must be 1 before this fires
    (1, 24,   None),              # Reminder 1: 24h after join, no prerequisite
    (2, 72,   "reminder_1_sent"), # Reminder 2: 3 days after join, only if #1 was sent
    (3, 168,  "reminder_2_sent"), # Reminder 3: 7 days after join, only if #2 was sent
]

# Message texts — plain (no HTML/Markdown) so no parse_mode is needed
_REMINDER_MESSAGES = {
    1: (
        "Most people only notice their website is down after users complain.\n\n"
        "UptimeGuardBot alerts you instantly when your:\n"
        "• website\n"
        "• API\n"
        "• VPS/server\n\n"
        "goes offline.\n\n"
        "You can set up your first monitor in under 1 minute:\n"
        "➜ /add"
    ),
    2: (
        "Quick reminder:\n\n"
        "You can monitor your website/API directly from Telegram "
        "and get instant downtime alerts.\n\n"
        "Setup takes less than a minute:\n"
        "➜ /add\n\n"
        "Useful if you manage:\n"
        "• websites\n"
        "• VPS servers\n"
        "• client projects"
    ),
    3: (
        "UptimeGuardBot now supports faster downtime detection and cleaner alerts.\n\n"
        "If you haven't tried it yet, you can add your first monitor here:\n"
        "➜ /add"
    ),
}


async def _send_reminder(bot, user_id: int, reminder_num: int) -> bool:
    """
    Attempt to send a single reminder message.

    Returns True on success, False if the user has blocked the bot.
    Other Telegram errors are re-raised so the caller can log them.

    IMPORTANT: mark_reminder_sent() is called BEFORE the Telegram send.
    This ensures that even if the send fails or the bot restarts mid-loop,
    we never send the same reminder twice.
    """
    mark_reminder_sent(user_id, reminder_num)

    try:
        await bot.send_message(
            chat_id=user_id,
            text=_REMINDER_MESSAGES[reminder_num],
        )
        logger.info(
            f"Onboarding reminder #{reminder_num} sent to user {user_id}"
        )
        return True

    except Forbidden:
        # User has blocked the bot — log once and move on.
        # The sent flag is already set so this user won't be retried.
        logger.warning(
            f"Onboarding reminder #{reminder_num} skipped for user {user_id}: "
            f"bot was blocked"
        )
        return False

    except TelegramError as e:
        logger.error(
            f"Onboarding reminder #{reminder_num} failed for user {user_id}: {e}"
        )
        return False


async def check_onboarding_reminders(context) -> None:
    """
    JobQueue callback — runs every CHECK_INTERVAL_SECONDS.

    For each inactive user (has_added_monitor = 0) with unsent reminders:
      1. Compute hours elapsed since joined_at.
      2. Walk the reminder schedule in order.
      3. For each reminder, check: time threshold met AND prerequisite sent.
      4. If both conditions pass, send the reminder (marks it sent first).

    Active users are excluded at the DB query level — this loop never
    touches users who have already added a monitor.
    """
    bot      = context.bot
    now      = datetime.now()
    users    = get_pending_reminder_users()

    if not users:
        return

    logger.debug(f"Onboarding reminder check: {len(users)} inactive user(s) to evaluate")

    for user in users:
        user_id   = user["user_id"]
        joined_at = user.get("joined_at")

        if not joined_at:
            continue  # Should not happen, but guard against missing data

        try:
            joined_dt = datetime.fromisoformat(joined_at)
        except ValueError:
            logger.warning(f"Invalid joined_at for user {user_id}: {joined_at!r}")
            continue

        hours_since_join = (now - joined_dt).total_seconds() / 3600

        for reminder_num, threshold_hours, prerequisite_key in _REMINDER_SCHEDULE:
            sent_key = f"reminder_{reminder_num}_sent"

            # Skip if already sent
            if user.get(sent_key):
                continue

            # Skip if not enough time has passed
            if hours_since_join < threshold_hours:
                continue

            # Skip if prerequisite reminder hasn't been sent yet
            if prerequisite_key and not user.get(prerequisite_key):
                continue

            # All conditions met — send this reminder
            await _send_reminder(bot, user_id, reminder_num)

            # Update local copy so subsequent reminders in the same loop
            # iteration see the correct prerequisite state
            user[sent_key] = 1
            break  # Send at most one reminder per user per check cycle


def register_onboarding_jobs(app) -> None:
    """
    Register the reminder checker with the PTB JobQueue.
    Call this from post_init in bot.py after the app is built.

    The first run is delayed by one full interval so the bot has time
    to fully start before doing any DB work.
    """
    app.job_queue.run_repeating(
        check_onboarding_reminders,
        interval=CHECK_INTERVAL_SECONDS,
        first=CHECK_INTERVAL_SECONDS,   # don't run immediately on startup
        name="onboarding_reminders",
    )
    logger.info(
        f"Onboarding reminder job registered "
        f"(interval={CHECK_INTERVAL_SECONDS}s)"
    )
