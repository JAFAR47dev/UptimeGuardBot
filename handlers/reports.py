# handlers/reports.py
from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_monitors, get_uptime_percent, get_conn, get_user_language
from locales.reports_strings import rt


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Works from both /report command and callback query
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    lang     = get_user_language(user_id)
    monitors = get_monitors(user_id)

    if not monitors:
        await reply_fn(rt(lang, "report_no_monitors"))
        return

    text = rt(lang, "report_header")

    for m in monitors:
        label  = m.get("label") or m.get("url", "")
        uptime = get_uptime_percent(m["id"], days=7)

        conn = get_conn()
        c    = conn.cursor()
        c.execute(
            """SELECT AVG(response_ms) as avg_ms
               FROM incidents
               WHERE monitor_id = ? AND is_up = 1
               AND checked_at >= datetime('now', '-7 days')""",
            (m["id"],)
        )
        row    = c.fetchone()
        conn.close()
        avg_ms = (
            round(row["avg_ms"]) if row and row["avg_ms"]
            else rt(lang, "report_avg_na")
        )

        status_icon = "🟢" if m.get("last_status") == "up" else "🔴"
        text += rt(
            lang, "report_row",
            icon=status_icon,
            label=label,
            uptime=uptime,
            avg_ms=avg_ms,
        )

    await reply_fn(text, parse_mode="HTML")
