#handlers/start.py
import logging
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from db.database import (
    get_or_create_user, get_all_monitors, is_pro,
    get_referral_count, get_qualified_referral_count,
    mark_referral_qualified, check_and_apply_referral_reward,
    record_referral, get_monitor_limit,
    get_user_language, set_user_language,
)
from config import ADMIN_IDS, FREE_LIMIT, REFERRAL_GOAL, REFERRAL_BONUS_SLOTS
from locales.start_strings import t, resolve_lang

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Referral helpers
# ---------------------------------------------------------------------------

def _get_referral_link(bot_username: str, user_id: int) -> str:
    return f"https://t.me/{bot_username}?start=ref_{user_id}"


def _referral_progress_bar(qualified: int, goal: int = REFERRAL_GOAL) -> str:
    filled = min(qualified, goal)
    empty  = goal - filled
    return "🟩" * filled + "⬜" * empty + f"  {filled}/{goal}"


# ---------------------------------------------------------------------------
# Admin notification
# ---------------------------------------------------------------------------

async def _notify_admins_new_user(bot, user, lang: str):
    """Fire-and-forget alert to all admins when a new user joins."""
    if not ADMIN_IDS:
        return
    username_str = f"@{user.username}" if user.username else "no username"
    text = t(
        "en",   # admin messages always in English
        "admin_new_user",
        full_name=user.full_name,
        username=username_str,
        user_id=user.id,
        lang=lang,
        time=datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
    )
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=text, parse_mode="HTML")
        except Exception as e:
            logger.warning(f"Could not notify admin {admin_id}: {e}")


# ---------------------------------------------------------------------------
# Skip-timezone callback
# ---------------------------------------------------------------------------

async def skip_tz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from db.database import set_user_timezone
    set_user_timezone(update.callback_query.from_user.id, "UTC")
    await update.callback_query.answer("Using UTC for now.")
    await update.callback_query.edit_message_reply_markup(reply_markup=None)


# ---------------------------------------------------------------------------
# /start entry point
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user            = update.effective_user
    db_user, is_new = get_or_create_user(user.id, user.username)
    pro             = is_pro(user.id)

    # Language resolution:
    # - New users: seed from Telegram language_code
    # - Existing users: always use their saved language (may have been
    #   manually overridden via /settings → Language picker)
    raw_lang = user.language_code or "en"
    if is_new:
        lang = resolve_lang(raw_lang)
        set_user_language(user.id, lang)
    else:
        lang = get_user_language(user.id)

    # Admin notification for brand-new users (includes detected language)
    if is_new:
        context.application.create_task(
            _notify_admins_new_user(context.bot, user, raw_lang)
        )

    # Handle referral deep-link — ?start=ref_<referrer_id>
    if context.args and context.args[0].startswith("ref_"):
        try:
            referrer_id = int(context.args[0].split("_")[1])
            if referrer_id != user.id:
                record_referral(referrer_id, user.id)
        except (IndexError, ValueError):
            pass

    monitors = get_all_monitors(user.id)

    if not monitors:
        await _new_user_flow(update, context, db_user, pro, is_new, lang)

        # Timezone prompt — only for users who haven't set it yet
        from db.database import get_user_timezone
        current_tz = get_user_timezone(user.id)
        if not current_tz or current_tz == "UTC":
            await update.message.reply_text(
                t(lang, "tz_prompt_title") + t(lang, "tz_prompt_body"),
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        t(lang, "btn_set_tz"),
                        callback_data="settings_set_tz"
                    ),
                    InlineKeyboardButton(
                        t(lang, "btn_skip_tz"),
                        callback_data="skip_tz"
                    )
                ]])
            )
        return

    await _returning_user_flow(update, context, db_user, pro, monitors, lang)


# ---------------------------------------------------------------------------
# New user flow
# ---------------------------------------------------------------------------

async def _new_user_flow(update, context, db_user, pro: bool, is_new: bool, lang: str):
    user    = update.effective_user
    name    = user.first_name or "there"
    user_id = user.id

    bot_username = (await context.bot.get_me()).username
    ref_link     = _get_referral_link(bot_username, user_id)

    plan_text = (
        t(lang, "plan_trial") if db_user["plan"] == "trial"
        else t(lang, "plan_free")
    )
    checklist = t(lang, "checklist")
    greeting  = (
        t(lang, "welcome_greeting", name=name) if is_new
        else t(lang, "welcome_back", name=name)
    )

    body = t(
        lang, "welcome_body",
        plan_text=plan_text,
        checklist=checklist,
        goal=REFERRAL_GOAL,
        bonus=REFERRAL_BONUS_SLOTS,
        ref_link=ref_link,
    )

    await update.message.reply_text(
        greeting + body,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(lang, "btn_add_first"),    callback_data="add_monitor")],
            [InlineKeyboardButton(t(lang, "btn_how_it_works"), callback_data="how_it_works")],
            [InlineKeyboardButton(t(lang, "btn_invite"),       callback_data="referral_info")],
        ])
    )


# ---------------------------------------------------------------------------
# Returning user flow
# ---------------------------------------------------------------------------

async def _returning_user_flow(update, context, db_user, pro: bool, monitors: list, lang: str):
    user_id      = update.effective_user.id
    up_count     = sum(1 for m in monitors if m["last_status"] == "up")
    down_count   = sum(1 for m in monitors if m["last_status"] == "down")
    paused_count = sum(1 for m in monitors if m["active"] == 2)
    total        = len(monitors)

    if down_count > 0:
        health_icon = "🔴"
        health_text = t(lang, "health_down", count=down_count)
    elif paused_count == total:
        health_icon = "⏸"
        health_text = t(lang, "health_paused")
    else:
        health_icon = "🟢"
        health_text = t(lang, "health_ok")

    if db_user["plan"] == "trial":
        plan_label = t(lang, "plan_trial_label")
    elif pro:
        plan_label = t(lang, "plan_pro_label")
    else:
        plan_label = t(lang, "plan_free_label")

    # Slot usage line (free users only)
    slots_line = ""
    if not pro:
        limit        = get_monitor_limit(user_id)
        active_count = sum(1 for m in monitors if m["active"] == 1)
        bonus        = db_user["bonus_monitors"] or 0
        bonus_str    = t(lang, "slots_bonus_str", bonus=bonus) if bonus else ""
        slots_line   = t(lang, "slots_line", active=active_count, limit=limit, bonus_str=bonus_str)

    # Referral progress bar (free users only)
    referral_line = ""
    if not pro:
        qualified     = get_qualified_referral_count(user_id)
        bar           = _referral_progress_bar(qualified)
        referral_line = t(lang, "referral_bar", bar=bar)

    # Nudge if no checks have run yet
    all_unknown = all(m["last_status"] == "unknown" for m in monitors)
    nudge_line  = t(lang, "nudge_testalert") if all_unknown else ""

    header = t(
        lang, "returning_header",
        icon=health_icon,
        plan_label=plan_label,
        slots_line=slots_line,
        total=total,
        up=up_count,
        down=down_count,
        paused=paused_count,
        health_text=health_text,
        referral_line=referral_line,
        nudge_line=nudge_line,
    )

    buttons = [
        [
            InlineKeyboardButton(t(lang, "btn_status"), callback_data="quick_status"),
            InlineKeyboardButton(t(lang, "btn_list"),   callback_data="quick_list"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_add_monitor"), callback_data="add_monitor"),
            InlineKeyboardButton(t(lang, "btn_report"),      callback_data="quick_report"),
        ],
    ]
    if not pro:
        buttons.append([InlineKeyboardButton(t(lang, "btn_upgrade"),     callback_data="upgrade")])
        buttons.append([InlineKeyboardButton(t(lang, "btn_invite_earn"), callback_data="referral_info")])

    await update.message.reply_text(
        header,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

async def how_it_works_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()
    await query.message.reply_text(
        t(lang, "how_it_works"),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(t(lang, "btn_add_monitor"), callback_data="add_monitor")
        ]])
    )


async def referral_info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    lang    = get_user_language(user_id)
    await query.answer()

    bot_username = (await context.bot.get_me()).username
    ref_link     = _get_referral_link(bot_username, user_id)
    qualified    = get_qualified_referral_count(user_id)
    bar          = _referral_progress_bar(qualified)
    remaining    = max(0, REFERRAL_GOAL - (qualified % REFERRAL_GOAL))
    tiers_earned = qualified // REFERRAL_GOAL

    if qualified > 0 and qualified % REFERRAL_GOAL == 0:
        reward_text = t(lang, "referral_reward_hit", tiers=tiers_earned)
    else:
        reward_text = t(lang, "referral_remaining", remaining=remaining, bonus=REFERRAL_BONUS_SLOTS)

    db_user    = get_or_create_user(user_id)[0]
    bonus      = db_user["bonus_monitors"] or 0
    bonus_line = t(lang, "referral_bonus_line", bonus=bonus) if bonus else ""

    text = (
        t(lang, "referral_title")
        + t(lang, "referral_progress", bar=bar)
        + reward_text
        + bonus_line
        + t(lang, "referral_link_line", ref_link=ref_link, bonus=REFERRAL_BONUS_SLOTS, goal=REFERRAL_GOAL)
    )

    await query.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(t(lang, "btn_add_monitor"), callback_data="add_monitor")
        ]])
    )


# ---------------------------------------------------------------------------
# Quick-action callbacks — pass full update so handlers detect callback_query
# ---------------------------------------------------------------------------

async def quick_status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    from handlers.monitors import status
    await status(update, context)


async def quick_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    from handlers.monitors import list_monitors
    await list_monitors(update, context)


async def quick_report_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    from handlers.reports import report
    await report(update, context)


async def referral_info_callback_alias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Alias kept for any existing callback registrations."""
    await referral_info_callback(update, context)