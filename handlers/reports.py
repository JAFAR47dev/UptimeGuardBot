# handlers/reports.py
from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_monitors, get_uptime_percent, get_conn


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Works from both /report command and callback query
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    monitors = get_monitors(user_id)

    if not monitors:
        await reply_fn("No monitors found. Use /add to start.")
        return

    text = "📊 <b>Uptime Report (Last 7 days)</b>\n\n"

    for m in monitors:
        label  = m["label"] or m["url"]
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
        avg_ms = round(row["avg_ms"]) if row and row["avg_ms"] else "N/A"

        status_icon = "🟢" if m.get("last_status") == "up" else "🔴"
        text += (
            f"{status_icon} <b>{label}</b>\n"
            f"   📈 Uptime: <b>{uptime}%</b>\n"
            f"   ⚡ Avg response: <b>{avg_ms}ms</b>\n\n"
        )

    await reply_fn(text, parse_mode="HTML")
