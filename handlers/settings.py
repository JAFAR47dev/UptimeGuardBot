# handlers/settings.py
import asyncio
import logging
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes, ConversationHandler,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, filters
)
from db.database import get_user, set_user_timezone, get_user_timezone, get_user_language
from locales.help_strings import ht

logger = logging.getLogger(__name__)

ASK_CITY   = "SETTINGS_ASK_CITY"
CONFIRM_TZ = "SETTINGS_CONFIRM_TZ"


# ---------------------------------------------------------------------------
# /settings entry point
# ---------------------------------------------------------------------------

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    lang       = get_user_language(user_id)
    current_tz = get_user_timezone(user_id)

    await reply_fn(
        ht(lang, "settings_menu", current_tz=current_tz),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                ht(lang, "btn_change_tz"),
                callback_data="settings_change_tz"
            ),
            InlineKeyboardButton(
                ht(lang, "btn_my_plan"),
                callback_data="settings_myplan"
            ),
        ]])
    )


# ---------------------------------------------------------------------------
# My Plan — bridge from settings menu
# ---------------------------------------------------------------------------

async def settings_myplan_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.myplan import myplan
    await myplan(update, context)


# ---------------------------------------------------------------------------
# Timezone entry points
# ---------------------------------------------------------------------------

async def change_tz_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()

    await query.message.reply_text(
        ht(lang, "tz_change_prompt"),
        parse_mode="HTML"
    )
    return ASK_CITY


async def tz_onboarding_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    lang = get_user_language(user_id)
    await reply_fn(ht(lang, "tz_onboarding_prompt"), parse_mode="HTML")
    return ASK_CITY


# ---------------------------------------------------------------------------
# Receive city name
# ---------------------------------------------------------------------------

async def received_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city    = update.message.text.strip()
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    result = await asyncio.get_event_loop().run_in_executor(
        None, _lookup_timezone, city
    )

    if not result:
        await update.message.reply_text(
            ht(lang, "tz_not_found", city=city),
            parse_mode="HTML"
        )
        return ASK_CITY

    context.user_data["pending_timezone"] = result["timezone"]
    context.user_data["pending_city"]     = result["city"]

    await update.message.reply_text(
        ht(lang, "tz_found",
           city=result["city"],
           country=result["country"],
           timezone=result["timezone"],
           utc_offset=result["utc_offset"]),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(ht(lang, "btn_tz_yes"), callback_data="tz_confirm"),
            InlineKeyboardButton(ht(lang, "btn_tz_no"),  callback_data="tz_retry"),
        ]])
    )
    return CONFIRM_TZ


# ---------------------------------------------------------------------------
# Confirmation callbacks
# ---------------------------------------------------------------------------

async def tz_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()

    timezone_str = context.user_data.get("pending_timezone")
    city         = context.user_data.get("pending_city", "")

    if not timezone_str:
        await query.message.reply_text(ht(lang, "tz_save_error"))
        return ConversationHandler.END

    set_user_timezone(user_id, timezone_str)
    context.user_data.pop("pending_timezone", None)
    context.user_data.pop("pending_city", None)

    await query.message.reply_text(
        ht(lang, "tz_saved", city=city, timezone=timezone_str),
        parse_mode="HTML"
    )
    return ConversationHandler.END


async def tz_retry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()

    context.user_data.pop("pending_timezone", None)
    context.user_data.pop("pending_city", None)

    await query.message.reply_text(ht(lang, "tz_retry_prompt"))
    return ASK_CITY


async def tz_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)
    set_user_timezone(user_id, "UTC")
    context.user_data.clear()
    await update.message.reply_text(ht(lang, "tz_skip_confirmed"))
    return ConversationHandler.END


async def cancel_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang    = get_user_language(user_id)
    context.user_data.clear()
    await update.message.reply_text(ht(lang, "settings_cancelled"))
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# Geocoding helper — runs in executor, no user-facing strings, untouched
# ---------------------------------------------------------------------------

def _lookup_timezone(city: str) -> dict | None:
    try:
        from geopy.geocoders import Nominatim
        import requests
        import pytz
        import time

        geolocator = Nominatim(user_agent="UptimeGuardBot/1.0")
        time.sleep(1.1)

        location = geolocator.geocode(
            city, language="en", addressdetails=True, timeout=10
        )
        if not location:
            return None

        lat = location.latitude
        lng = location.longitude

        resp = requests.get(
            "https://timeapi.io/api/timezone/coordinate",
            params={"latitude": lat, "longitude": lng},
            timeout=10
        )
        resp.raise_for_status()
        tz_name = resp.json().get("timeZone")
        if not tz_name:
            return None

        tz         = pytz.timezone(tz_name)
        now_local  = datetime.now(tz)
        offset     = now_local.strftime("%z")
        sign       = offset[0]
        hours      = int(offset[1:3])
        minutes    = int(offset[3:5])
        utc_offset = (
            f"UTC{sign}{hours}:{minutes:02d}" if minutes else f"UTC{sign}{hours}"
        )

        raw_address = location.raw.get("address", {})
        city_found  = (
            raw_address.get("city")
            or raw_address.get("town")
            or raw_address.get("village")
            or raw_address.get("county")
            or city.title()
        )

        return {
            "timezone":   tz_name,
            "city":       city_found,
            "country":    raw_address.get("country", ""),
            "utc_offset": utc_offset,
            "lat":        lat,
            "lng":        lng,
        }

    except Exception as e:
        logger.error(f"_lookup_timezone error for '{city}': {e}", exc_info=True)
        return None


# ---------------------------------------------------------------------------
# ConversationHandler export
# ---------------------------------------------------------------------------

settings_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(change_tz_entry,     pattern="^settings_change_tz$"),
        CallbackQueryHandler(tz_onboarding_entry, pattern="^settings_set_tz$"),
    ],
    states={
        ASK_CITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_city),
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