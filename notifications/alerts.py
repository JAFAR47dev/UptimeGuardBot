#notifications/alerts.py
from telegram import Bot
from db.database import get_monitor, get_user

async def send_down_alert(bot: Bot, monitor: dict, result: dict):
    user_id = monitor["user_id"]
    label   = monitor["label"] or monitor["url"]
    error   = result.get("error") or f"Status {result.get('status_code')}"

    text = (
        f"🔴 <b>DOWN: {label}</b>\n\n"
        f"🌐 {monitor['url']}\n"
        f"❌ Error: <code>{error}</code>\n"
        f"🕐 Detected: just now\n\n"
        f"I'll notify you when it recovers."
    )
    await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")

async def send_up_alert(bot: Bot, monitor: dict, result: dict):
    user_id = monitor["user_id"]
    label   = monitor["label"] or monitor["url"]

    text = (
        f"🟢 <b>RECOVERED: {label}</b>\n\n"
        f"🌐 {monitor['url']}\n"
        f"⚡ Response: {result['ms']}ms\n"
        f"✅ Site is back online."
    )
    await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")

async def send_ssl_warning(bot: Bot, user_id: int, url: str, days_left: int):
    text = (
        f"⚠️ <b>SSL Certificate Expiring Soon</b>\n\n"
        f"🌐 {url}\n"
        f"📅 Expires in <b>{days_left} days</b>\n\n"
        f"Renew your SSL certificate to avoid downtime."
    )
    await bot.send_message(chat_id=user_id, text=text, parse_mode="HTML")
    
async def send_slow_alert(bot, monitor: dict, response_ms: int, threshold_ms: int):
    label = monitor["label"] or monitor["url"]
    text = (
        f"🐢 <b>SLOW RESPONSE: {label}</b>\n\n"
        f"🌐 {monitor['url']}\n"
        f"⚡ Response time: <b>{response_ms}ms</b>\n"
        f"⚠️ Your threshold: {threshold_ms}ms\n\n"
        f"Your site is up but responding slowly."
    )
    await bot.send_message(
        chat_id=monitor["user_id"],
        text=text,
        parse_mode="HTML"
    )