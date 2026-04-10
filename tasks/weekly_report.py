# tasks/weekly_report.py
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import (
    get_all_active_users, get_monitors,
    get_weekly_stats, is_pro
)

logger = logging.getLogger(__name__)

def _status_icon(uptime_pct: float) -> str:
    if uptime_pct >= 99:
        return "🟢"
    elif uptime_pct >= 95:
        return "🟡"
    else:
        return "🔴"

def _build_pro_report(monitors: list) -> str:
    """Full detail report for Pro users."""
    lines = ["📊 <b>Your Weekly Uptime Report</b>\n"]
    all_healthy = True

    for m in monitors:
        stats = get_weekly_stats(m["id"])
        label = m["label"] or m["url"]
        icon  = _status_icon(stats["uptime_pct"])

        if stats["uptime_pct"] < 100:
            all_healthy = False

        avg_ms_str = f"{stats['avg_ms']}ms" if stats["avg_ms"] else "N/A"
        lines.append(
            f"{icon} <b>{label}</b>\n"
            f"   📈 Uptime: <b>{stats['uptime_pct']}%</b>\n"
            f"   ⚡ Avg response: <b>{avg_ms_str}</b>\n"
            f"   🔴 Incidents: <b>{stats['down_count']}</b>\n"
            f"   🔍 Total checks: {stats['total_checks']}\n"
        )

    if all_healthy:
        lines.append("✅ <b>All systems healthy this week!</b>")
    else:
        lines.append("⚠️ Some monitors had incidents this week.")

    lines.append("\n<i>Next report: Monday 9AM</i>")
    return "\n".join(lines)

def _build_free_report(monitors: list) -> tuple[str, InlineKeyboardMarkup]:
    """Teaser report for free users — shows first monitor only."""
    lines = ["📊 <b>Your Weekly Uptime Report</b>\n"]

    # Show first monitor as teaser
    m     = monitors[0]
    stats = get_weekly_stats(m["id"])
    label = m["label"] or m["url"]
    icon  = _status_icon(stats["uptime_pct"])

    lines.append(
        f"{icon} <b>{label}</b>\n"
        f"   📈 Uptime: <b>{stats['uptime_pct']}%</b>\n"
        f"   ⚡ Avg response: <b>— Pro only</b>\n"
        f"   🔴 Incidents: <b>— Pro only</b>\n"
    )

    remaining = len(monitors) - 1
    if remaining > 0:
        lines.append(
            f"🔒 <i>+{remaining} more monitor(s) hidden.</i>\n"
        )

    lines.append(
        "\nUpgrade to Pro for full weekly reports with avg "
        "response time, incident counts, and all monitors."
    )

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("⭐ See Full Report → Upgrade", callback_data="upgrade")
    ]])
    return "\n".join(lines), keyboard


async def send_weekly_reports(context: ContextTypes.DEFAULT_TYPE):
    """
    Runs every Monday at 9AM.
    Sends each active user a weekly summary of their monitors.
    """
    users = get_all_active_users()
    sent  = 0
    failed = 0

    for user in users:
        user_id  = user["user_id"]
        monitors = get_monitors(user_id)

        if not monitors:
            continue

        try:
            pro = is_pro(user_id)

            if pro:
                text     = _build_pro_report(monitors)
                keyboard = None
            else:
                text, keyboard = _build_free_report(monitors)

            await context.bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode="HTML",
                reply_markup=keyboard
            )
            sent += 1

        except Exception as e:
            # User blocked bot or other error — never let one
            # failure stop the rest of the batch
            logger.warning(f"Weekly report failed for {user_id}: {e}")
            failed += 1
            continue

    logger.info(f"Weekly reports sent: {sent} ok, {failed} failed")