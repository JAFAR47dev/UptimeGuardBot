# notifications/alerts.py
import logging
from datetime import datetime, timedelta
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Snooze helpers
# ---------------------------------------------------------------------------

SNOOZE_MINUTES = 30


def _snooze_store(bot_data: dict) -> dict:
    if "snoozes" not in bot_data:
        bot_data["snoozes"] = {}
    return bot_data["snoozes"]


def is_snoozed(bot_data: dict, monitor_id: int) -> bool:
    store  = _snooze_store(bot_data)
    expiry = store.get(monitor_id)
    if not expiry:
        return False
    if datetime.now() < expiry:
        return True
    del store[monitor_id]
    return False


def snooze_monitor(bot_data: dict, monitor_id: int) -> datetime:
    store   = _snooze_store(bot_data)
    current = store.get(monitor_id)
    base    = current if (current and current > datetime.now()) else datetime.now()
    expiry  = base + timedelta(minutes=SNOOZE_MINUTES)
    store[monitor_id] = expiry
    return expiry


def clear_snooze(bot_data: dict, monitor_id: int):
    _snooze_store(bot_data).pop(monitor_id, None)


def snooze_expiry(bot_data: dict, monitor_id: int):
    store  = _snooze_store(bot_data)
    expiry = store.get(monitor_id)
    if expiry and datetime.now() < expiry:
        return expiry
    return None


# ---------------------------------------------------------------------------
# Webhook delivery
# ---------------------------------------------------------------------------

WEBHOOK_TIMEOUT = 8


async def send_webhook(monitor: dict, event: str, result: dict):
    """
    POST a JSON payload to the monitor's webhook_url.
    Fires regardless of snooze/maintenance.
    Failures are logged and swallowed — never affects the alert loop.
    """
    webhook_url = (monitor.get("webhook_url") or "").strip()
    if not webhook_url:
        return

    label = monitor["label"] or monitor["url"]
    now   = datetime.now().isoformat(timespec="seconds")

    if event == "down":
        error   = result.get("error") or f"HTTP {result.get('status_code')}"
        summary = f"🔴 DOWN: {label} — {error}"
        payload = {
            "text":        summary,
            "event":       "down",
            "monitor_id":  monitor["id"],
            "label":       label,
            "url":         monitor["url"],
            "error":       result.get("error"),
            "status_code": result.get("status_code"),
            "response_ms": result.get("ms"),
            "note":        (monitor.get("note") or "").strip() or None,
            "timestamp":   now,
        }
    else:
        summary = f"🟢 RECOVERED: {label} — back online in {result.get('ms')}ms"
        payload = {
            "text":        summary,
            "event":       "up",
            "monitor_id":  monitor["id"],
            "label":       label,
            "url":         monitor["url"],
            "error":       None,
            "status_code": result.get("status_code"),
            "response_ms": result.get("ms"),
            "note":        (monitor.get("note") or "").strip() or None,
            "timestamp":   now,
        }

    try:
        timeout = aiohttp.ClientTimeout(total=WEBHOOK_TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            ) as resp:
                if resp.status >= 400:
                    logger.warning(
                        f"Webhook for monitor {monitor['id']} returned "
                        f"HTTP {resp.status}: {webhook_url}"
                    )
    except Exception as e:
        logger.warning(f"Webhook delivery failed for monitor {monitor['id']}: {e}")


# ---------------------------------------------------------------------------
# Internal fan-out helper
# ---------------------------------------------------------------------------

async def _send_to_recipients(
    bot: Bot,
    recipients: list[int],
    owner_id: int,
    text: str,
    owner_markup=None,
):
    """
    Send `text` to every recipient.
    The snooze keyboard is only attached for the owner — teammates
    receive the plain alert with no action buttons.
    """
    for uid in recipients:
        try:
            markup = owner_markup if uid == owner_id else None
            await bot.send_message(
                chat_id=uid,
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )
        except Exception as e:
            # Teammate may not have started the bot yet — log and continue
            logger.warning(f"Could not deliver alert to user {uid}: {e}")


def _snooze_keyboard(monitor_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            f"🔕 Snooze {SNOOZE_MINUTES} mins",
            callback_data=f"snooze_{monitor_id}"
        )
    ]])


# ---------------------------------------------------------------------------
# Telegram alert senders
# ---------------------------------------------------------------------------

async def send_down_alert(bot: Bot, monitor: dict, result: dict):
    from db.database import get_alert_recipients

    owner_id   = monitor["user_id"]
    monitor_id = monitor["id"]
    label      = monitor["label"] or monitor["url"]
    error      = result.get("error") or f"Status {result.get('status_code')}"
    note       = (monitor.get("note") or "").strip()
    note_line  = f"\n📝 <b>Note:</b> <i>{note}</i>" if note else ""

    text = (
        f"🔴 <b>DOWN: {label}</b>\n\n"
        f"🌐 {monitor['url']}\n"
        f"❌ Error: <code>{error}</code>\n"
        f"🕐 Detected: just now"
        f"{note_line}\n\n"
        f"I'll notify you when it recovers."
    )

    recipients = get_alert_recipients(owner_id)
    await _send_to_recipients(
        bot, recipients, owner_id, text,
        owner_markup=_snooze_keyboard(monitor_id)
    )


async def send_up_alert(bot: Bot, monitor: dict, result: dict):
    from db.database import get_alert_recipients

    owner_id = monitor["user_id"]
    label    = monitor["label"] or monitor["url"]

    text = (
        f"🟢 <b>RECOVERED: {label}</b>\n\n"
        f"🌐 {monitor['url']}\n"
        f"⚡ Response: {result['ms']}ms\n"
        f"✅ Site is back online."
    )

    recipients = get_alert_recipients(owner_id)
    await _send_to_recipients(bot, recipients, owner_id, text)


async def send_ssl_warning(bot: Bot, user_id: int, url: str, days_left: int):
    from db.database import get_alert_recipients

    text = (
        f"⚠️ <b>SSL Certificate Expiring Soon</b>\n\n"
        f"🌐 {url}\n"
        f"📅 Expires in <b>{days_left} days</b>\n\n"
        f"Renew your SSL certificate to avoid downtime."
    )

    recipients = get_alert_recipients(user_id)
    await _send_to_recipients(bot, recipients, user_id, text)


async def send_slow_alert(bot: Bot, monitor: dict, response_ms: int, threshold_ms: int):
    from db.database import get_alert_recipients

    owner_id   = monitor["user_id"]
    monitor_id = monitor["id"]
    label      = monitor["label"] or monitor["url"]
    note       = (monitor.get("note") or "").strip()
    note_line  = f"\n📝 <b>Note:</b> <i>{note}</i>" if note else ""

    text = (
        f"🐢 <b>SLOW RESPONSE: {label}</b>\n\n"
        f"🌐 {monitor['url']}\n"
        f"⚡ Response time: <b>{response_ms}ms</b>\n"
        f"⚠️ Your threshold: {threshold_ms}ms"
        f"{note_line}\n\n"
        f"Your site is up but responding slowly."
    )

    recipients = get_alert_recipients(owner_id)
    await _send_to_recipients(
        bot, recipients, owner_id, text,
        owner_markup=_snooze_keyboard(monitor_id)
    )
