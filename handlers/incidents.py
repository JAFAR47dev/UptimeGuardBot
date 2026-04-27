# handlers/incidents.py
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import (
    get_all_monitors, get_monitor, get_incident_rows,
    is_pro, get_user_language,
)
from locales.reports_strings import rt

# ---------------------------------------------------------------------------
# Plan limits
# ---------------------------------------------------------------------------

FREE_INCIDENT_DAYS  = 7
PRO_INCIDENT_DAYS   = 90
MAX_INCIDENTS_SHOWN = 20


# ---------------------------------------------------------------------------
# Core logic — pair consecutive rows into outage groups
# Untouched: pure logic, no user-facing strings
# ---------------------------------------------------------------------------

def _build_outage_groups(rows: list) -> list:
    groups  = []
    current = None

    for row in rows:
        ts    = datetime.fromisoformat(row["checked_at"])
        is_up = bool(row["is_up"])

        if not is_up and current is None:
            current = {
                "started_at": ts,
                "ended_at":   None,
                "duration_m": None,
                "error":      row["error_msg"] or (
                    f"HTTP {row['status_code']}" if row["status_code"] else None
                ),
            }
        elif is_up and current is not None:
            current["ended_at"]   = ts
            current["duration_m"] = max(1, int((ts - current["started_at"]).total_seconds() / 60))
            groups.append(current)
            current = None

    if current is not None:
        now = datetime.now()
        current["duration_m"] = max(1, int((now - current["started_at"]).total_seconds() / 60))
        groups.append(current)

    return groups


def _fmt_dt(dt: datetime) -> str:
    """Apr 3, 2:17 AM — kept in English as it's a universal format."""
    return dt.strftime("%-d %b, %-I:%M %p")


def _fmt_duration(minutes: int) -> str:
    """Compact duration — kept in English (mins/h are universally understood)."""
    if minutes < 60:
        return f"{minutes} min{'s' if minutes != 1 else ''}"
    h = minutes // 60
    m = minutes % 60
    return f"{h}h {m}m" if m else f"{h}h"


# ---------------------------------------------------------------------------
# Message renderer
# ---------------------------------------------------------------------------

def _render(monitor, groups: list, days: int, pro: bool, lang: str) -> str:
    label = monitor.get("label") or monitor.get("url", "")
    lines = [
        rt(lang, "incidents_title",    label=label),
        rt(lang, "incidents_subtitle", days=days),
    ]

    if not groups:
        lines.append(rt(lang, "incidents_none"))
        if not pro:
            lines.append(
                rt(lang, "incidents_none_upsell", free_days=FREE_INCIDENT_DAYS)
            )
        return "\n".join(lines)

    # Most recent first
    shown  = list(reversed(groups))[:MAX_INCIDENTS_SHOWN]
    hidden = max(0, len(groups) - MAX_INCIDENTS_SHOWN)

    for g in shown:
        started_str  = _fmt_dt(g["started_at"])
        duration_str = _fmt_duration(g["duration_m"])
        error        = g["error"] or rt(lang, "incidents_error_unknown")
        is_ongoing   = g["ended_at"] is None

        if is_ongoing:
            lines.append(rt(
                lang, "incident_ongoing",
                started=started_str,
                duration=duration_str,
                error=error,
            ))
        else:
            lines.append(rt(
                lang, "incident_resolved",
                duration=duration_str,
                started=started_str,
                error=error,
            ))

    if hidden:
        plural = "s" if hidden != 1 else ""
        lines.append(rt(lang, "incidents_hidden", count=hidden, plural=plural))

    total_down_m = sum(g["duration_m"] or 0 for g in groups)
    count        = len(groups)
    plural       = "s" if count != 1 else ""
    lines.append(rt(
        lang, "incidents_summary",
        count=count,
        plural=plural,
        total_down=_fmt_duration(total_down_m),
    ))

    if not pro:
        lines.append(rt(lang, "incidents_upsell", free_days=FREE_INCIDENT_DAYS))

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Shared display helper
# ---------------------------------------------------------------------------

async def _show_incidents(reply_fn, monitor, days: int, pro: bool, lang: str):
    rows    = get_incident_rows(monitor["id"], days)
    groups  = _build_outage_groups(rows)
    text    = _render(monitor, groups, days, pro, lang)
    await reply_fn(text, parse_mode="HTML")


# ---------------------------------------------------------------------------
# /incidents command
# ---------------------------------------------------------------------------

async def incidents_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pro     = is_pro(user_id)
    lang    = get_user_language(user_id)
    days    = FREE_INCIDENT_DAYS if not pro else PRO_INCIDENT_DAYS

    if pro and context.args:
        try:
            requested = int(context.args[0])
            days = max(1, min(requested, PRO_INCIDENT_DAYS))
        except ValueError:
            pass

    monitors = get_all_monitors(user_id)
    active   = [m for m in monitors if m["active"] in (1, 2)]

    if not active:
        await update.message.reply_text(rt(lang, "incidents_no_monitors"))
        return

    if len(active) == 1:
        await _show_incidents(
            update.message.reply_text,
            active[0], days, pro, lang,
        )
        return

    # Multiple monitors — localised picker
    buttons = [
        [InlineKeyboardButton(
            m.get("label") or m.get("url", ""),
            callback_data=f"incidents_{m['id']}_{days}"
        )]
        for m in active
    ]
    await update.message.reply_text(
        rt(lang, "incidents_picker_title"),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# ---------------------------------------------------------------------------
# Callback — monitor selected from picker
# ---------------------------------------------------------------------------

async def incidents_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()

    parts      = query.data.split("_")
    monitor_id = int(parts[1])
    days       = int(parts[2]) if len(parts) > 2 else FREE_INCIDENT_DAYS

    monitor = get_monitor(monitor_id)
    if not monitor or monitor["user_id"] != user_id:
        await query.message.reply_text(rt(lang, "incidents_not_found"))
        return

    pro = is_pro(user_id)
    await _show_incidents(
        query.message.reply_text,
        monitor, days, pro, lang,
    )
