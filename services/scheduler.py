#services/scheduler.py
from db.database import (
    get_monitors, log_incident, update_monitor_status,
    get_last_incident, get_monitor
)
from services.checker import check_url, check_ssl
from notifications.alerts import send_down_alert, send_up_alert, send_ssl_warning, send_slow_alert
from urllib.parse import urlparse
import logging
from db.database import is_pro

logger = logging.getLogger(__name__)

async def run_check(context):
    """Called by JobQueue for each monitor."""
    monitor_id = context.job.data["monitor_id"]

    try:
        monitor = get_monitor(monitor_id)

        # active=0 → deleted, active=2 → paused
        # Either way stop the job cleanly
        if not monitor:
            logger.warning(
                f"run_check: monitor {monitor_id} not found in DB — "
                f"removing job."
            )
            context.job.schedule_removal()
            return

        if monitor["active"] == 0:
            logger.info(
                f"run_check: monitor {monitor_id} is deleted — "
                f"removing job."
            )
            context.job.schedule_removal()
            return

        if monitor["active"] == 2:
            logger.info(
                f"run_check: monitor {monitor_id} is paused — "
                f"skipping check, keeping job."
            )
            # Keep the job alive so resume works instantly
            # without needing to re-register it
            return

        # Active monitor — run the check
        session = context.bot_data.get("aiohttp_session")
        result  = await check_url(monitor["url"], session=session)

        log_incident(
            monitor_id,
            result["status_code"],
            result["ms"],
            result["up"],
            result["error"]
        )

        prev_status = monitor["last_status"]
        curr_status = "up" if result["up"] else "down"

        if prev_status != curr_status:
            update_monitor_status(monitor_id, curr_status)
            if not result["up"]:
                await send_down_alert(context.bot, dict(monitor), result)
            else:
                await send_up_alert(context.bot, dict(monitor), result)
        else:
            update_monitor_status(monitor_id, curr_status)

        # Slow response alert — Pro only, site must be up
        if result["up"] and result["ms"] is not None:
            threshold = monitor["response_threshold_ms"]
            if threshold and result["ms"] > threshold:
                if is_pro(monitor["user_id"]):
                    await send_slow_alert(
                        context.bot,
                        dict(monitor),
                        result["ms"],
                        threshold
                    )

    except Exception as e:
        # Never let a single monitor crash the entire scheduler loop
        logger.error(
            f"run_check: unhandled error for monitor {monitor_id}: {e}",
            exc_info=True
        )
        
async def run_ssl_check(context):
    """Daily SSL check for pro users."""
    from db.database import get_user, is_pro
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
            ssl_result["days_left"]
        )


def schedule_monitor(app, monitor_id: int, interval_minutes: int):
    """Register a repeating job for a monitor."""
    job_name = f"monitor_{monitor_id}"
    # Remove existing job if any
    current_jobs = app.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()

    app.job_queue.run_repeating(
        run_check,
        interval=interval_minutes * 60,
        first=10,  # first check after 10 seconds
        name=job_name,
        data={"monitor_id": monitor_id}
    )

def schedule_ssl_check(app, monitor_id: int):
    """Daily SSL check job."""
    job_name = f"ssl_{monitor_id}"
    current_jobs = app.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()

    app.job_queue.run_daily(
        run_ssl_check,
        time=__import__('datetime').time(hour=9, minute=0),
        name=job_name,
        data={"monitor_id": monitor_id}
    )

async def restore_and_check(context):
    """
    Called once per monitor on bot startup.
    Runs an immediate check to fix any stale last_status
    from before the restart, then starts the repeating job.
    """
    monitor_id = context.job.data["monitor_id"]
    interval   = context.job.data["interval_minutes"]
    monitor    = get_monitor(monitor_id)

    if not monitor or not monitor["active"]:
        return

    # Run immediate check
    result = await check_url(monitor["url"])
    log_incident(
        monitor_id,
        result["status_code"],
        result["ms"],
        result["up"],
        result["error"]
    )

    prev_status = monitor["last_status"]
    curr_status = "up" if result["up"] else "down"

    # Fix stale status silently — only alert if it changed
    if prev_status != curr_status and prev_status != "unknown":
        update_monitor_status(monitor_id, curr_status)
        if not result["up"]:
            await send_down_alert(context.bot, dict(monitor), result)
        else:
            await send_up_alert(context.bot, dict(monitor), result)
    else:
        # Just update status, no alert
        update_monitor_status(monitor_id, curr_status)

    # Now start the normal repeating job
    schedule_monitor(context.application, monitor_id, interval)
    schedule_ssl_check(context.application, monitor_id)

def restore_all_monitors(app):
    """
    On bot startup, schedule a one-time immediate check for every
    active monitor before starting their repeating jobs.
    This fixes any stale last_status caused by a crash or restart.
    """
    from db.database import get_conn
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id, interval_minutes FROM monitors WHERE active = 1"
    )
    rows = c.fetchall()
    conn.close()

    for i, row in enumerate(rows):
        # Stagger startup checks by 2 seconds each so we don't
        # hammer all URLs simultaneously on boot
        app.job_queue.run_once(
            restore_and_check,
            when=3 + (i * 2),
            name=f"restore_{row['id']}",
            data={
                "monitor_id": row["id"],
                "interval_minutes": row["interval_minutes"]
            }
        )
            
