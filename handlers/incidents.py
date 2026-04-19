# handlers/incidents.py
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import get_all_monitors, get_monitor, get_incident_rows, is_pro

# ---------------------------------------------------------------------------
# Plan limits
# ---------------------------------------------------------------------------

FREE_INCIDENT_DAYS = 7
PRO_INCIDENT_DAYS  = 90
MAX_INCIDENTS_SHOWN = 20   # cap per monitor to keep messages readable


# ---------------------------------------------------------------------------
# Core logic — pair consecutive rows into outage groups
# ---------------------------------------------------------------------------

def _build_outage_groups(rows: list) -> list:
    """
    Walk incident rows oldest-first and collect discrete outage groups.

    Each group is a dict:
        started_at  : datetime   — first down row
        ended_at    : datetime | None — first subsequent up row (None = ongoing)
        duration_m  : int | None — minutes down (None = ongoing)
        error       : str | None — error from the first down row
    """
    groups  = []
    current = None   # tracks an open (unresolved) outage

    for row in rows:
        ts    = datetime.fromisoformat(row["checked_at"])
        is_up = bool(row["is_up"])

        if not is_up and current is None:
            # Outage starts
            current = {
                "started_at": ts,
                "ended_at":   None,
                "duration_m": None,
                "error":      row["error_msg"] or (
                    f"HTTP {row['status_code']}" if row["status_code"] else "Unknown error"
                ),
            }

        elif is_up and current is not None:
            # Outage ends
            current["ended_at"]   = ts
            current["duration_m"] = max(1, int((ts - current["started_at"]).total_seconds() / 60))
            groups.append(current)
            current = None

    # Still-open outage at the end of the window
    if current is not None:
        now = datetime.now()
        current["duration_m"] = max(1, int((now - current["started_at"]).total_seconds() / 60))
        groups.append(current)

    return groups


def _fmt_dt(dt: datetime) -> str:
    """Apr 3, 2:17 AM"""
    return dt.strftime("%-d %b, %-I:%M %p").replace("AM", "AM").replace("PM", "PM")


def _fmt_duration(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes} min{'s' if minutes != 1 else ''}"
    h = minutes // 60
    m = minutes % 60
    return f"{h}h {m}m" if m else f"{h}h"


# ---------------------------------------------------------------------------
# Message renderer
# ---------------------------------------------------------------------------

def _render(monitor, groups: list, days: int, ongoing: bool, pro: bool) -> str:
    label = monitor["label"] or monitor["url"]
    lines = [f"📋 <b>Incident Log — {label}</b>"]
    lines.append(f"<i>Last {days} days</i>\n")

    if not groups:
        lines.append("✅ No incidents recorded in this period.")
        if not pro:
            lines.append(
                f"\n<i>Free plan shows {FREE_INCIDENT_DAYS} days. "
                "Upgrade to Pro for 90-day history.</i>"
            )
        return "\n".join(lines)

    # Most recent first
    shown  = list(reversed(groups))[:MAX_INCIDENTS_SHOWN]
    hidden = max(0, len(groups) - MAX_INCIDENTS_SHOWN)

    for g in shown:
        started_str  = _fmt_dt(g["started_at"])
        is_ongoing   = g["ended_at"] is None
        duration_str = _fmt_duration(g["duration_m"])
        error        = g["error"] or "Unknown error"

        if is_ongoing:
            lines.append(
                f"🔴 <b>Ongoing</b> — started {started_str}\n"
                f"   ⏱ Running for {duration_str}\n"
                f"   ❌ {error}"
            )
        else:
            lines.append(
                f"⚫ <b>Down {duration_str}</b> — {started_str}\n"
                f"   ❌ {error}"
            )

    if hidden:
        lines.append(f"\n<i>…and {hidden} older incident{'s' if hidden != 1 else ''} not shown.</i>")

    total_down_m = sum(g["duration_m"] or 0 for g in groups)
    lines.append(
        f"\n📊 <b>{len(groups)} incident{'s' if len(groups) != 1 else ''}</b> · "
        f"<b>{_fmt_duration(total_down_m)}</b> total downtime"
    )

    if not pro:
        lines.append(
            f"\n<i>Free plan shows {FREE_INCIDENT_DAYS} days. "
            "Upgrade to Pro for 90-day history.</i>"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Shared display helper
# ---------------------------------------------------------------------------

async def _show_incidents(reply_fn, monitor, days: int, pro: bool):
    rows   = get_incident_rows(monitor["id"], days)
    groups = _build_outage_groups(rows)
    ongoing = any(g["ended_at"] is None for g in groups)
    text   = _render(monitor, groups, days, ongoing, pro)

    await reply_fn(text, parse_mode="HTML")


# ---------------------------------------------------------------------------
# /incidents command
# ---------------------------------------------------------------------------

async def incidents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id  = update.effective_user.id
    pro      = is_pro(user_id)
    days     = FREE_INCIDENT_DAYS if not pro else PRO_INCIDENT_DAYS

    # Pro users can pass a custom day range: /incidents 30
    if pro and context.args:
        try:
            requested = int(context.args[0])
            days = max(1, min(requested, PRO_INCIDENT_DAYS))
        except ValueError:
            pass

    monitors = get_all_monitors(user_id)
    active   = [m for m in monitors if m["active"] in (1, 2)]

    if not active:
        await update.message.reply_text(
            "You have no monitors yet. Use /add to add your first one."
        )
        return

    if len(active) == 1:
        await _show_incidents(
            update.message.reply_text,
            active[0],
            days,
            pro,
        )
        return

    # Multiple monitors — show picker
    buttons = [
        [InlineKeyboardButton(
            m["label"] or m["url"],
            callback_data=f"incidents_{m['id']}_{days}"
        )]
        for m in active
    ]
    await update.message.reply_text(
        "📋 <b>Incident Log</b>\n\nWhich monitor do you want to view?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ---------------------------------------------------------------------------
# Callback — monitor selected from picker
# ---------------------------------------------------------------------------

async def incidents_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # callback_data: "incidents_<monitor_id>_<days>"
    parts      = query.data.split("_")
    monitor_id = int(parts[1])
    days       = int(parts[2]) if len(parts) > 2 else FREE_INCIDENT_DAYS

    monitor = get_monitor(monitor_id)
    if not monitor or monitor["user_id"] != user_id:
        await query.message.reply_text("⚠️ Monitor not found.")
        return

    pro = is_pro(user_id)
    await _show_incidents(
        query.message.reply_text,
        monitor,
        days,
        pro,
    )
