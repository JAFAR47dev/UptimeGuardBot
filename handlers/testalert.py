# handlers/testalert.py
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import get_all_monitors

# ---------------------------------------------------------------------------
# Cooldown — one test per user per 60 seconds (in-memory, same as snooze)
# ---------------------------------------------------------------------------

TEST_COOLDOWN_SECONDS = 60


def _cooldown_store(bot_data: dict) -> dict:
    if "test_alert_cooldowns" not in bot_data:
        bot_data["test_alert_cooldowns"] = {}
    return bot_data["test_alert_cooldowns"]


def _is_on_cooldown(bot_data: dict, user_id: int) -> tuple[bool, int]:
    store     = _cooldown_store(bot_data)
    last_used = store.get(user_id)
    if not last_used:
        return False, 0
    elapsed   = (datetime.now() - last_used).total_seconds()
    remaining = int(TEST_COOLDOWN_SECONDS - elapsed)
    if remaining > 0:
        return True, remaining
    return False, 0


def _stamp_cooldown(bot_data: dict, user_id: int):
    _cooldown_store(bot_data)[user_id] = datetime.now()


# ---------------------------------------------------------------------------
# Alert builders — visually match real alerts, clearly marked as tests
# ---------------------------------------------------------------------------

def _fake_down_text(monitor: dict) -> str:
    label = monitor["label"] or monitor["url"]
    note  = (monitor.get("note") or "").strip()
    note_line = f"\n📝 <b>Note:</b> <i>{note}</i>" if note else ""
    return (
        f"🧪 <b>TEST ALERT — DOWN: {label}</b>\n\n"
        f"🌐 {monitor['url']}\n"
        f"❌ Error: <code>Simulated failure</code>\n"
        f"🕐 Detected: just now"
        f"{note_line}\n\n"
        f"I'll notify you when it recovers.\n\n"
        f"<i>This is a test alert. No action needed.</i>"
    )


def _fake_up_text(monitor: dict) -> str:
    label = monitor["label"] or monitor["url"]
    return (
        f"🧪 <b>TEST ALERT — RECOVERED: {label}</b>\n\n"
        f"🌐 {monitor['url']}\n"
        f"⚡ Response: 142ms\n"
        f"✅ Site is back online.\n\n"
        f"<i>This is a test alert. Your notifications are working correctly.</i>"
    )


# ---------------------------------------------------------------------------
# Core test fire — sends down then up with a 5s gap
# ---------------------------------------------------------------------------

async def _fire_test(context, chat_id: int, user_id: int, monitor: dict):
    """Send fake down alert, wait 5s, send fake recovery alert."""
    _stamp_cooldown(context.bot_data, user_id)

    await context.bot.send_message(
        chat_id=chat_id,
        text=_fake_down_text(monitor),
        parse_mode="HTML"
        # No snooze button — this is not a real incident
    )

    await asyncio.sleep(5)

    await context.bot.send_message(
        chat_id=chat_id,
        text=_fake_up_text(monitor),
        parse_mode="HTML"
    )


# ---------------------------------------------------------------------------
# /testalert command entry point
# ---------------------------------------------------------------------------

async def testalert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id  = update.effective_user.id
    chat_id  = update.effective_chat.id
    bot_data = context.bot_data

    on_cooldown, remaining = _is_on_cooldown(bot_data, user_id)
    if on_cooldown:
        await update.message.reply_text(
            f"⏳ Please wait <b>{remaining}s</b> before sending another test alert.",
            parse_mode="HTML"
        )
        return

    monitors = get_all_monitors(user_id)
    active   = [m for m in monitors if m["active"] == 1]

    if not active:
        await update.message.reply_text(
            "⚠️ You have no active monitors to test.\n\n"
            "Use /add to add your first monitor."
        )
        return

    if len(active) == 1:
        # Only one monitor — fire immediately, no selection needed
        await update.message.reply_text(
            f"🧪 Sending test alert for <b>{active[0]['label'] or active[0]['url']}</b>…",
            parse_mode="HTML"
        )
        await _fire_test(context, chat_id, user_id, dict(active[0]))
        return

    # Multiple monitors — let user pick
    buttons = [
        [InlineKeyboardButton(
            m["label"] or m["url"],
            callback_data=f"testalert_{m['id']}"
        )]
        for m in active
    ]
    await update.message.reply_text(
        "🧪 <b>Test Alert</b>\n\n"
        "Which monitor do you want to test?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ---------------------------------------------------------------------------
# Callback — monitor selected from the picker, or button in help/start
# ---------------------------------------------------------------------------

async def testalert_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query    = update.callback_query
    user_id  = query.from_user.id
    chat_id  = query.message.chat_id
    bot_data = context.bot_data

    await query.answer()

    on_cooldown, remaining = _is_on_cooldown(bot_data, user_id)
    if on_cooldown:
        await query.message.reply_text(
            f"⏳ Please wait <b>{remaining}s</b> before sending another test alert.",
            parse_mode="HTML"
        )
        return

    data = query.data  # "testalert_<monitor_id>" or "testalert" (no specific monitor)

    if "_" in data and data != "testalert":
        # Specific monitor chosen from picker
        monitor_id = int(data.split("_")[1])
        from db.database import get_monitor
        monitor = get_monitor(monitor_id)

        if not monitor or monitor["user_id"] != user_id:
            await query.message.reply_text("⚠️ Monitor not found.")
            return

        await query.edit_message_text(
            f"🧪 Sending test alert for <b>{monitor['label'] or monitor['url']}</b>…",
            parse_mode="HTML"
        )
        await _fire_test(context, chat_id, user_id, dict(monitor))

    else:
        # Generic trigger (e.g. from help menu) — pick first active monitor
        monitors = get_all_monitors(user_id)
        active   = [m for m in monitors if m["active"] == 1]

        if not active:
            await query.message.reply_text(
                "⚠️ You have no active monitors to test.\n\n"
                "Use /add to add your first monitor."
            )
            return

        if len(active) == 1:
            await query.edit_message_text(
                f"🧪 Sending test alert for <b>{active[0]['label'] or active[0]['url']}</b>…",
                parse_mode="HTML"
            )
            await _fire_test(context, chat_id, user_id, dict(active[0]))
            return

        # Show picker
        buttons = [
            [InlineKeyboardButton(
                m["label"] or m["url"],
                callback_data=f"testalert_{m['id']}"
            )]
            for m in active
        ]
        await query.edit_message_text(
            "🧪 <b>Test Alert</b>\n\n"
            "Which monitor do you want to test?",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
