# handlers/start.py
import logging
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from db.database import (
    get_or_create_user, get_all_monitors, is_pro,
    get_referral_count, get_qualified_referral_count,
    mark_referral_qualified, check_and_apply_referral_reward,
    record_referral, get_monitor_limit,
)
from config import ADMIN_IDS, FREE_LIMIT, REFERRAL_GOAL, REFERRAL_BONUS_SLOTS

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

async def _notify_admins_new_user(bot, user):
    """Fire-and-forget alert to all admins when a new user joins."""
    if not ADMIN_IDS:
        return
    username_str = f"@{user.username}" if user.username else "no username"
    text = (
        f"👤 <b>New user joined UptimeGuard</b>\n\n"
        f"Name: <b>{user.full_name}</b>\n"
        f"Username: {username_str}\n"
        f"ID: <code>{user.id}</code>\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}"
    )
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=text, parse_mode="HTML")
        except Exception as e:
            logger.warning(f"Could not notify admin {admin_id}: {e}")


# ---------------------------------------------------------------------------
# /start entry point
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user               = update.effective_user
    db_user, is_new    = get_or_create_user(user.id, user.username)
    pro                = is_pro(user.id)

    # Admin notification for brand-new users
    if is_new:
        context.application.create_task(
            _notify_admins_new_user(context.bot, user)
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
        await _new_user_flow(update, context, db_user, pro, is_new)
    else:
        await _returning_user_flow(update, context, db_user, pro, monitors)


# ---------------------------------------------------------------------------
# New user flow — sticky onboarding checklist
# ---------------------------------------------------------------------------

async def _new_user_flow(update, context, db_user, pro: bool, is_new: bool):
    user      = update.effective_user
    name      = user.first_name or "there"
    user_id   = user.id

    bot_username = (await context.bot.get_me()).username
    ref_link     = _get_referral_link(bot_username, user_id)

    if db_user["plan"] == "trial":
        plan_text = "✅ 7-day Pro trial active — all Pro features unlocked"
    else:
        plan_text = "🆓 Free plan"

    # Onboarding checklist
    checklist = (
        "📋 <b>Getting started</b>\n"
        "✅ Joined UptimeGuard\n"
        "⬜ Add your first monitor\n"
        "⬜ Receive your first alert\n\n"
    )

    greeting = (
        f"👋 Hey {name}, welcome to <b>UptimeGuard</b>!\n\n"
        if is_new else
        f"👋 Hey {name}, you're back!\n\n"
    )

    await update.message.reply_text(
        f"{greeting}"
        f"Get instant Telegram alerts the moment your website "
        f"goes down — before your users notice.\n\n"
        f"📦 {plan_text}\n\n"
        f"{checklist}"
        f"🎁 <b>Referral reward:</b> Invite {REFERRAL_GOAL} friends who add a monitor "
        f"→ earn <b>+{REFERRAL_BONUS_SLOTS} free monitor slots</b>!\n\n"
        f"Your invite link:\n<code>{ref_link}</code>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add My First Monitor", callback_data="add_monitor")],
            [InlineKeyboardButton("📖 How it works",         callback_data="how_it_works")],
            [InlineKeyboardButton("👥 Invite Friends",        callback_data="referral_info")],
        ])
    )


# ---------------------------------------------------------------------------
# Returning user flow
# ---------------------------------------------------------------------------

async def _returning_user_flow(update, context, db_user, pro: bool, monitors: list):
    user_id      = update.effective_user.id
    up_count     = sum(1 for m in monitors if m["last_status"] == "up")
    down_count   = sum(1 for m in monitors if m["last_status"] == "down")
    paused_count = sum(1 for m in monitors if m["active"] == 2)
    total        = len(monitors)

    # Alert if anything is currently down — shown prominently at top
    if down_count > 0:
        health_icon = "🔴"
        health_text = f"{down_count} monitor(s) currently DOWN ⚠️"
    elif paused_count == total:
        health_icon = "⏸"
        health_text = "All monitors paused"
    else:
        health_icon = "🟢"
        health_text = "All systems operational"

    plan_label = (
        "✅ Pro (Trial)" if db_user["plan"] == "trial" else
        "✅ Pro"         if pro                         else
        "🆓 Free"
    )

    # Monitor slot usage for free users
    limit        = get_monitor_limit(user_id)
    active_count = sum(1 for m in monitors if m["active"] == 1)
    slots_line   = ""
    if not pro:
        bonus = (db_user["bonus_monitors"] or 0)
        bonus_str = f" (+{bonus} referral bonus)" if bonus else ""
        slots_line = f"\n📦 Monitors: <b>{active_count}/{limit}</b>{bonus_str}"

    # Referral teaser for free users
    referral_line = ""
    if not pro:
        qualified = get_qualified_referral_count(user_id)
        bar       = _referral_progress_bar(qualified)
        referral_line = f"\n👥 Referrals: {bar}"

    # Nudge if user has never received a real alert (all monitors still 'unknown')
    all_unknown  = all(m["last_status"] == "unknown" for m in monitors)
    nudge_line   = (
        "\n\n💡 <i>Tip: run /testalert to confirm your notifications work.</i>"
        if all_unknown else ""
    )

    buttons = [
        [
            InlineKeyboardButton("⚡ Status",      callback_data="quick_status"),
            InlineKeyboardButton("📋 List",        callback_data="quick_list"),
        ],
        [
            InlineKeyboardButton("➕ Add Monitor", callback_data="add_monitor"),
            InlineKeyboardButton("📊 Report",      callback_data="quick_report"),
        ],
    ]
    if not pro:
        buttons.append([InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")])
        buttons.append([InlineKeyboardButton("👥 Invite Friends & Earn Rewards", callback_data="referral_info")])

    await update.message.reply_text(
        f"{health_icon} <b>UptimeGuard</b>\n\n"
        f"📦 Plan: <b>{plan_label}</b>{slots_line}\n"
        f"📡 Monitors: <b>{total}</b> total • "
        f"<b>{up_count}</b> up • "
        f"<b>{down_count}</b> down • "
        f"<b>{paused_count}</b> paused\n\n"
        f"Status: <b>{health_text}</b>"
        f"{referral_line}"
        f"{nudge_line}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

async def how_it_works_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "📖 <b>How UptimeGuard works</b>\n\n"
        "1️⃣ Add a URL with /add\n"
        "2️⃣ We ping it every 5 min (free) or 1 min (Pro)\n"
        "3️⃣ If it goes down you get an instant alert here\n"
        "4️⃣ When it recovers you get another alert\n\n"
        "<b>Pro also includes:</b>\n"
        "🔐 SSL expiry warnings\n"
        "🐢 Slow response alerts\n"
        "📊 Weekly summary reports\n"
        "🔗 Webhook integrations\n"
        "👥 Team notifications\n\n"
        "👇 Ready to add your first monitor?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("➕ Add Monitor", callback_data="add_monitor")
        ]])
    )


async def referral_info_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    bot_username = (await context.bot.get_me()).username
    ref_link     = _get_referral_link(bot_username, user_id)
    qualified    = get_qualified_referral_count(user_id)
    bar          = _referral_progress_bar(qualified)
    remaining    = max(0, REFERRAL_GOAL - (qualified % REFERRAL_GOAL))

    # How many full reward tiers earned total
    tiers_earned = qualified // REFERRAL_GOAL

    if qualified > 0 and qualified % REFERRAL_GOAL == 0:
        reward_text = (
            f"🎉 <b>Reward unlocked!</b> You've earned {tiers_earned} reward tier(s).\n"
            f"Rewards are applied automatically. Keep inviting to earn more!"
        )
    else:
        reward_text = (
            f"Invite <b>{remaining} more friend(s)</b> who add a monitor "
            f"to unlock <b>+{REFERRAL_BONUS_SLOTS} free monitor slots</b>!"
        )

    db_user = get_or_create_user(user_id)[0]
    bonus   = db_user["bonus_monitors"] or 0
    bonus_line = f"\n🎁 Bonus slots earned so far: <b>+{bonus}</b>" if bonus else ""

    await query.message.reply_text(
        f"👥 <b>Referral Programme</b>\n\n"
        f"Progress to next reward: {bar}\n\n"
        f"{reward_text}{bonus_line}\n\n"
        f"📎 Your invite link:\n<code>{ref_link}</code>\n\n"
        f"Share it with friends — they get UptimeGuard, "
        f"you get +{REFERRAL_BONUS_SLOTS} monitor slots per {REFERRAL_GOAL} who join!",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("➕ Add Monitor", callback_data="add_monitor")
        ]])
    )


# ---------------------------------------------------------------------------
# Quick-action callbacks — pass update, not query, so handlers work correctly
# ---------------------------------------------------------------------------

async def quick_status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Pass the real Update object so status() can access update.callback_query
    from handlers.monitors import status
    await status(update, context)


async def quick_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    from handlers.monitors import list_monitors
    await list_monitors(update, context)


async def quick_report_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    from handlers.reports import report
    await report(update, context)
