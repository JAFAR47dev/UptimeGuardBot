import asyncio
import logging
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, filters
)
from db.database import get_user, set_user_timezone, get_user_timezone

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────
# Conversation state
# ─────────────────────────────────────────
ASK_CITY    = "SETTINGS_ASK_CITY"
CONFIRM_TZ  = "SETTINGS_CONFIRM_TZ"


# ─────────────────────────────────────────
# /settings entry point
# ─────────────────────────────────────────

async def settings_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Works from both /settings command and callback query."""
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    current_tz = get_user_timezone(user_id)

    await reply_fn(
        f"⚙️ <b>Settings</b>\n\n"
        f"🌍 Timezone: <b>{current_tz}</b>\n\n"
        f"What would you like to update?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🌍 Change Timezone",
                    callback_data="settings_change_tz"
                ),
                InlineKeyboardButton(
                    "📦 My Plan",
                    callback_data="settings_myplan"
                ),
            ]
        ])
    )


# ─────────────────────────────────────────
# My Plan — bridge from settings menu
# ─────────────────────────────────────────

async def settings_myplan_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Delegates to myplan handler when tapped from the settings menu."""
    from handlers.myplan import myplan
    await myplan(update, context)


# ─────────────────────────────────────────
# Timezone setup — entry
# ─────────────────────────────────────────

async def change_tz_entry(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Entry point — from /settings button or direct from onboarding."""
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "🌍 <b>Set Your Timezone</b>\n\n"
        "Type the name of your city and I'll detect your timezone.\n\n"
        "Examples:\n"
        "• <code>London</code>\n"
        "• <code>New York</code>\n"
        "• <code>Dubai</code>\n"
        "• <code>Mumbai</code>\n"
        "• <code>Tokyo</code>\n\n"
        "Send /cancel to go back.",
        parse_mode="HTML"
    )
    return ASK_CITY


async def tz_onboarding_entry(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Called directly from start.py for new users.
    Same flow but entry is a message not a callback.
    """
    reply_fn = (
        update.callback_query.message.reply_text
        if update.callback_query
        else update.message.reply_text
    )
    if update.callback_query:
        await update.callback_query.answer()

    await reply_fn(
        "🌍 <b>One quick thing — what city do you live in?</b>\n\n"
        "This lets me send your weekly reports and alerts "
        "at the right time for your timezone.\n\n"
        "Just type your city name:\n"
        "<code>Lagos</code> · <code>London</code> · "
        "<code>New York</code> · <code>Dubai</code>\n\n"
        "Send /skip to use UTC for now.",
        parse_mode="HTML"
    )
    return ASK_CITY


# ─────────────────────────────────────────
# Receive city name
# ─────────────────────────────────────────

async def received_city(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    city    = update.message.text.strip()
    user_id = update.effective_user.id

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    result = await asyncio.get_event_loop().run_in_executor(
        None, _lookup_timezone, city
    )

    if not result:
        await update.message.reply_text(
            f"❌ <b>Couldn't find \"{city}\".</b>\n\n"
            "Try a larger nearby city, or spell it in English.\n\n"
            "Examples: <code>New York</code>, <code>Moscow</code>, "
            "<code>London</code>, <code>Dubai</code>",
            parse_mode="HTML"
        )
        return ASK_CITY

    timezone_str = result["timezone"]
    city_found   = result["city"]
    country      = result["country"]
    utc_offset   = result["utc_offset"]

    context.user_data["pending_timezone"] = timezone_str
    context.user_data["pending_city"]     = city_found

    await update.message.reply_text(
        f"📍 <b>Found it!</b>\n\n"
        f"City: <b>{city_found}</b>\n"
        f"Country: <b>{country}</b>\n"
        f"Timezone: <b>{timezone_str}</b>\n"
        f"UTC offset: <b>{utc_offset}</b>\n\n"
        f"Is this correct?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Yes, save it", callback_data="tz_confirm"),
                InlineKeyboardButton("❌ No, try again", callback_data="tz_retry"),
            ]
        ])
    )
    return CONFIRM_TZ


# ─────────────────────────────────────────
# Confirmation callbacks
# ─────────────────────────────────────────

async def tz_confirmed(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query   = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    timezone_str = context.user_data.get("pending_timezone")
    city         = context.user_data.get("pending_city", "")

    if not timezone_str:
        await query.message.reply_text(
            "Something went wrong. Use /settings to try again."
        )
        return ConversationHandler.END

    set_user_timezone(user_id, timezone_str)
    context.user_data.pop("pending_timezone", None)
    context.user_data.pop("pending_city", None)

    await query.message.reply_text(
        f"✅ <b>Timezone saved!</b>\n\n"
        f"📍 {city}\n"
        f"🌍 {timezone_str}\n\n"
        f"Your weekly reports and scheduled alerts will now "
        f"arrive at the right local time for you.",
        parse_mode="HTML"
    )
    return ConversationHandler.END


async def tz_retry(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    context.user_data.pop("pending_timezone", None)
    context.user_data.pop("pending_city", None)

    await query.message.reply_text(
        "No problem. Type your city name again:",
        parse_mode="HTML"
    )
    return ASK_CITY


async def tz_skip(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """/skip inside the timezone conversation — keep UTC."""
    user_id = update.effective_user.id
    set_user_timezone(user_id, "UTC")
    context.user_data.clear()

    await update.message.reply_text(
        "OK, using UTC for now.\n\n"
        "You can update this anytime via /settings."
    )
    return ConversationHandler.END


async def cancel_settings(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    context.user_data.clear()
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END


# ─────────────────────────────────────────
# Geocoding helper — runs in executor
# ─────────────────────────────────────────

def _lookup_timezone(city: str) -> dict | None:
    """
    Synchronous function — must be called via run_in_executor.

    1. geopy Nominatim geocodes the city name to lat/lng
    2. timezonefinder converts lat/lng to an IANA timezone string
    3. Returns a dict with timezone, display city, country, UTC offset

    Returns None if the city cannot be found or geocoding fails.
    """
    try:
        from geopy.geocoders import Nominatim
        from timezonefinder import TimezoneFinder
        import pytz
        import time

        geolocator = Nominatim(user_agent="UptimeGuardBot/1.0")

        # Respect Nominatim's 1 req/sec policy
        time.sleep(1.1)

        location = geolocator.geocode(
            city,
            language="en",
            addressdetails=True,
            timeout=10
        )

        if not location:
            return None

        lat = location.latitude
        lng = location.longitude

        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lat=lat, lng=lng)

        if not tz_name:
            return None

        tz        = pytz.timezone(tz_name)
        now_local = datetime.now(tz)
        offset    = now_local.strftime("%z")
        sign      = offset[0]
        hours     = int(offset[1:3])
        minutes   = int(offset[3:5])
        if minutes:
            utc_offset = f"UTC{sign}{hours}:{minutes:02d}"
        else:
            utc_offset = f"UTC{sign}{hours}"

        raw_address = location.raw.get("address", {})
        city_found  = (
            raw_address.get("city")
            or raw_address.get("town")
            or raw_address.get("village")
            or raw_address.get("county")
            or city.title()
        )
        country = raw_address.get("country", "")

        return {
            "timezone":   tz_name,
            "city":       city_found,
            "country":    country,
            "utc_offset": utc_offset,
            "lat":        lat,
            "lng":        lng,
        }

    except Exception as e:
        logger.error(f"_lookup_timezone error for '{city}': {e}", exc_info=True)
        return None


# ─────────────────────────────────────────
# Conversation handler
# ─────────────────────────────────────────

settings_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(change_tz_entry,      pattern="^settings_change_tz$"),
        CallbackQueryHandler(tz_onboarding_entry,  pattern="^settings_set_tz$"),
    ],
    states={
        ASK_CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                received_city
            ),
        ],
        CONFIRM_TZ: [
            CallbackQueryHandler(tz_confirmed, pattern="^tz_confirm$"),
            CallbackQueryHandler(tz_retry,     pattern="^tz_retry$"),
        ],
        ConversationHandler.TIMEOUT: [
            MessageHandler(filters.ALL, lambda u, c: ConversationHandler.END),
            CallbackQueryHandler(lambda u, c: ConversationHandler.END),
        ],
    },
    fallbacks=[
        CommandHandler("skip",   tz_skip),
        CommandHandler("cancel", cancel_settings),
    ],
    per_message=False,
    per_chat=True,
    conversation_timeout=300,
)
