# handlers/status.py
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_all_monitors, get_user_language
from locales.monitors_strings import mt


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    lang     = get_user_language(user_id)
    monitors = get_all_monitors(user_id)

    if not monitors:
        await reply_fn(mt(lang, "status_no_monitors"))
        return

    lines = [mt(lang, "status_header")]

    for m in monitors:
        label     = m.get("label") or m.get("url", "")
        is_paused = m["active"] == 2

        if is_paused:
            icon        = "⏸"
            status_text = mt(lang, "status_paused")
        elif m.get("last_status") == "up":
            icon        = "🟢"
            status_text = mt(lang, "status_up")
        elif m.get("last_status") == "down":
            icon        = "🔴"
            status_text = mt(lang, "status_down")
        else:
            icon        = "⚪"
            status_text = mt(lang, "status_pending")

        if m.get("last_checked"):
            last = datetime.fromisoformat(m["last_checked"])
            diff = datetime.now() - last
            mins = int(diff.total_seconds() // 60)
            if mins < 1:
                ago = mt(lang, "status_just_now")
            elif mins == 1:
                ago = mt(lang, "status_1min")
            elif mins < 60:
                ago = mt(lang, "status_mins", mins=mins)
            else:
                ago = mt(lang, "status_hours", h=mins // 60)
        else:
            ago = mt(lang, "status_not_checked")

        lines.append(
            mt(lang, "status_line",
               icon=icon, label=label, status_text=status_text, ago=ago)
        )

    await reply_fn("\n".join(lines), parse_mode="HTML")
