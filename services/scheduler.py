# services/scheduler.py
import logging
from urllib.parse import urlparse

from db.database import (
    log_incident, update_monitor_status,
    get_monitor, is_pro, is_in_maintenance,
    increment_failure_counter, reset_failure_counter,
)
from services.checker import check_url, check_ssl
from notifications.alerts import (
    send_down_alert, send_up_alert, send_ssl_warning, send_slow_alert,
    send_webhook, is_snoozed, clear_snooze,
)

logger = logging.getLogger(__name__)


async def run_check(context):
    """Called by JobQueue for each monitor."""
    monitor_id = context.job.data["monitor_id"]

    try:
        monitor = get_monitor(monitor_id)

        if not monitor:
            logger.warning(f"run_check: monitor {monitor_id} not found — removing job.")
            context.job.schedule_removal()
            return

        if monitor["active"] == 0:
            logger.info(f"run_check: monitor {monitor_id} deleted — removing job.")
            context.job.schedule_removal()
            return

        if monitor["active"] == 2:
            logger.info(f"run_check: monitor {monitor_id} paused — skipping.")
            return

        # Pass keyword config to checker so body is read when needed
        keyword    = monitor.get("keyword") or None
        case_sens  = bool(monitor.get("keyword_case_sensitive", 0))
        session    = context.bot_data.get("aiohttp_session")

        result = await check_url(
            monitor["url"],
            session=session,
            keyword=keyword,
            keyword_case_sensitive=case_sens,
        )

        log_incident(
            monitor_id,
            result["status_code"],
            result["ms"],
            result["up"],
            result["error"],
        )

        prev_status   = monitor["last_status"]
        curr_status   = "up" if result["up"] else "down"
        bot_data      = context.bot_data
        user_id       = monitor["user_id"]
        monitor_dict  = dict(monitor)
        confirm_count = monitor.get("confirm_count") or 1

        # Suppression flags (Telegram only — webhooks always fire)
        snoozed    = is_snoozed(bot_data, monitor_id)
        in_maint   = is_in_maintenance(user_id)
        suppressed = snoozed or in_maint

        if not result["up"]:
            # Increment consecutive failure counter
            failures = increment_failure_counter(monitor_id)

            if prev_status != "down":
                # Status just changed to down — only alert if confirmed
                if failures >= confirm_count:
                    update_monitor_status(monitor_id, "down")
                    if not suppressed:
                        await send_down_alert(context.bot, monitor_dict, result)
                    else:
                        logger.info(
                            f"run_check: monitor {monitor_id} down alert suppressed "
                            f"({'snoozed' if snoozed else 'maintenance'})."
                        )
                    # Webhook fires regardless of suppression
                    await send_webhook(monitor_dict, "down", result)
                else:
                    logger.info(
                        f"run_check: monitor {monitor_id} failure "
                        f"{failures}/{confirm_count} — waiting for confirmation."
                    )
            else:
                # Already marked down — update timestamp, no repeat alert
                update_monitor_status(monitor_id, "down")

        else:
            # Site is up
            reset_failure_counter(monitor_id)

            if prev_status != "up":
                # Recovery
                update_monitor_status(monitor_id, "up")
                clear_snooze(bot_data, monitor_id)
                await send_up_alert(context.bot, monitor_dict, result)
                await send_webhook(monitor_dict, "up", result)
            else:
                update_monitor_status(monitor_id, "up")

            # Slow response alert — Pro only, not suppressed
            threshold = monitor.get("response_threshold_ms")
            if threshold and result["ms"] and result["ms"] > threshold:
                if is_pro(user_id) and not suppressed:
                    await send_slow_alert(
                        context.bot, monitor_dict, result["ms"], threshold
                    )

    except Exception as e:
        logger.error(
            f"run_check: unhandled error for monitor {monitor_id}: {e}",
            exc_info=True,
        )


async def run_ssl_check(context):
    """Daily SSL check for pro users."""
    monitor_id = context.job.data["monitor_id"]
    monitor    = get_monitor(monitor_id)

    if not monitor or not is_pro(monitor["user_id"]):
        return

    parsed = urlparse(monitor["url"])
    if parsed.scheme != "https":
        return

    ssl_result = check_ssl(parsed.hostname)
    if ssl_result["valid"] and ssl_result["days_left"] in [30, 7, 1]:
        await send_ssl_warning(
            context.bot,
            monitor["user_id"],
            monitor["url"],
            ssl_result["days_left"],
        )


def schedule_monitor(app, monitor_id: int, interval_minutes: int):
    job_name     = f"monitor_{monitor_id}"
    current_jobs = app.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()

    app.job_queue.run_repeating(
        run_check,
        interval=interval_minutes * 60,
        first=10,
        name=job_name,
        data={"monitor_id": monitor_id},
    )


def schedule_ssl_check(app, monitor_id: int):
    job_name     = f"ssl_{monitor_id}"
    current_jobs = app.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()

    app.job_queue.run_daily(
        run_ssl_check,
        time=__import__('datetime').time(hour=9, minute=0),
        name=job_name,
        data={"monitor_id": monitor_id},
    )


async def restore_and_check(context):
    """One-shot startup check per monitor to fix stale last_status."""
    monitor_id = context.job.data["monitor_id"]
    interval   = context.job.data["interval_minutes"]
    monitor    = get_monitor(monitor_id)

    if not monitor or not monitor["active"]:
        return

    keyword   = monitor.get("keyword") or None
    case_sens = bool(monitor.get("keyword_case_sensitive", 0))

    result = await check_url(
        monitor["url"],
        keyword=keyword,
        keyword_case_sensitive=case_sens,
    )
    log_incident(
        monitor_id,
        result["status_code"],
        result["ms"],
        result["up"],
        result["error"],
    )

    prev_status  = monitor["last_status"]
    curr_status  = "up" if result["up"] else "down"
    monitor_dict = dict(monitor)

    if prev_status != curr_status and prev_status != "unknown":
        update_monitor_status(monitor_id, curr_status)
        if not result["up"]:
            await send_down_alert(context.bot, monitor_dict, result)
            await send_webhook(monitor_dict, "down", result)
        else:
            reset_failure_counter(monitor_id)
            await send_up_alert(context.bot, monitor_dict, result)
            await send_webhook(monitor_dict, "up", result)
    else:
        update_monitor_status(monitor_id, curr_status)

    schedule_monitor(context.application, monitor_id, interval)
    schedule_ssl_check(context.application, monitor_id)


def restore_all_monitors(app):
    """Stagger startup checks by 2s each to avoid thundering herd."""
    from db.database import get_conn
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT id, interval_minutes FROM monitors WHERE active = 1")
    rows = c.fetchall()
    conn.close()

    for i, row in enumerate(rows):
        app.job_queue.run_once(
            restore_and_check,
            when=3 + (i * 2),
            name=f"restore_{row['id']}",
            data={
                "monitor_id":       row["id"],
                "interval_minutes": row["interval_minutes"],
            },
        )
