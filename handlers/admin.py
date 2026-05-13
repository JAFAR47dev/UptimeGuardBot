import asyncio
import calendar
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, TelegramError
from telegram.ext import (
    ContextTypes, ConversationHandler,
    MessageHandler, CallbackQueryHandler,
    CommandHandler, filters
)
from db.database import (
    get_conn, upgrade_user, downgrade_user,
    get_user, get_or_create_user
)
from config import ADMIN_IDS

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────
# Conversation states
# ─────────────────────────────────────────
BROADCAST_ALL_MSG    = "BROADCAST_ALL_MSG"
BROADCAST_TARGET_IDS = "BROADCAST_TARGET_IDS"
BROADCAST_TARGET_MSG = "BROADCAST_TARGET_MSG"
PLAN_TARGET_IDS      = "PLAN_TARGET_IDS"
PLAN_CHOOSE          = "PLAN_CHOOSE"
PLAN_PRO_TYPE        = "PLAN_PRO_TYPE"   # new: pick monthly/3month/yearly


# ─────────────────────────────────────────
# Pro plan type → (display label, months)
# ─────────────────────────────────────────
_PRO_TYPES = {
    "pro_monthly": ("Monthly",  1),
    "pro_3month":  ("3-Month",  3),
    "pro_yearly":  ("Yearly",  12),
}


def _add_months(months: int) -> str:
    now   = datetime.now()
    month = now.month - 1 + months
    year  = now.year + month // 12
    month = month % 12 + 1
    day   = min(now.day, calendar.monthrange(year, month)[1])
    return datetime(year, month, day,
                    now.hour, now.minute, now.second).isoformat()


# ─────────────────────────────────────────
# Admin guard
# ─────────────────────────────────────────

def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.callback_query:
            user_id = update.callback_query.from_user.id
        else:
            user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            logger.warning(f"Admin access denied: user {user_id} tried {func.__name__}")
            return ConversationHandler.END
        return await func(update, context)
    return wrapper


# ─────────────────────────────────────────
# /admin — main panel
# ─────────────────────────────────────────

@admin_only
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 <b>UptimeGuard Admin Panel</b>\n\nWhat would you like to do?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📣 Broadcast to All Users",        callback_data="admin_broadcast_all")],
            [InlineKeyboardButton("🎯 Broadcast to Specific Users",   callback_data="admin_broadcast_target")],
            [InlineKeyboardButton("⚙️ Upgrade / Downgrade User Plan", callback_data="admin_plan")],
            [InlineKeyboardButton("📊 Bot Stats",                     callback_data="admin_stats")],
        ])
    )


# ─────────────────────────────────────────
# 1. Broadcast to all users
# ─────────────────────────────────────────

@admin_only
async def broadcast_all_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    total = _get_total_users()
    await query.message.reply_text(
        f"📣 <b>Broadcast to All Users</b>\n\n"
        f"This will send your message to <b>{total} users</b>.\n\n"
        f"Send the message now. Supports HTML formatting.\n\nOr /cancel to go back.",
        parse_mode="HTML"
    )
    return BROADCAST_ALL_MSG


@admin_only
async def received_broadcast_all_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message  = update.message.text.strip()
    user_ids = _get_all_user_ids()
    await update.message.reply_text(f"📤 Sending to {len(user_ids)} users...")
    sent, failed = await _blast(context.bot, user_ids, message)
    await update.message.reply_text(
        f"✅ <b>Broadcast complete.</b>\n\n"
        f"📨 Sent: <b>{sent}</b>\n"
        f"❌ Failed: <b>{failed}</b>\n"
        f"<i>(Failed = user blocked bot)</i>",
        parse_mode="HTML"
    )
    return ConversationHandler.END


# ─────────────────────────────────────────
# 2. Broadcast to specific users
# ─────────────────────────────────────────

@admin_only
async def broadcast_target_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "🎯 <b>Broadcast to Specific Users</b>\n\n"
        "Send the Telegram IDs to message.\n"
        "Separate multiple IDs with commas:\n\n"
        "<code>123456789, 987654321</code>\n\nOr /cancel to go back.",
        parse_mode="HTML"
    )
    return BROADCAST_TARGET_IDS


@admin_only
async def received_broadcast_target_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ids = _parse_ids(update.message.text.strip())
    if not ids:
        await update.message.reply_text(
            "⚠️ No valid IDs found.\nSend numeric Telegram IDs separated by commas."
        )
        return BROADCAST_TARGET_IDS
    context.user_data["target_ids"] = ids
    await update.message.reply_text(
        f"✅ Targeting <b>{len(ids)}</b> user(s).\n\n"
        f"Now send the message to deliver.\nSupports HTML formatting.\n\nOr /cancel to go back.",
        parse_mode="HTML"
    )
    return BROADCAST_TARGET_MSG


@admin_only
async def received_broadcast_target_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message  = update.message.text.strip()
    user_ids = context.user_data.get("target_ids", [])
    if not user_ids:
        await update.message.reply_text("Something went wrong. Use /admin to try again.")
        return ConversationHandler.END
    await update.message.reply_text(f"📤 Sending to {len(user_ids)} user(s)...")
    sent, failed = await _blast(context.bot, user_ids, message)
    await update.message.reply_text(
        f"✅ <b>Broadcast complete.</b>\n\n📨 Sent: <b>{sent}</b>\n❌ Failed: <b>{failed}</b>",
        parse_mode="HTML"
    )
    context.user_data.clear()
    return ConversationHandler.END


# ─────────────────────────────────────────
# 3. Upgrade / downgrade plan
# ─────────────────────────────────────────

@admin_only
async def plan_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "⚙️ <b>Upgrade / Downgrade User Plan</b>\n\n"
        "Send the Telegram ID(s) to modify.\n"
        "Separate multiple with commas:\n\n"
        "<code>123456789, 987654321</code>\n\nOr /cancel to go back.",
        parse_mode="HTML"
    )
    return PLAN_TARGET_IDS


@admin_only
async def received_plan_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ids = _parse_ids(update.message.text.strip())
    if not ids:
        await update.message.reply_text(
            "⚠️ No valid IDs found.\nSend numeric Telegram IDs separated by commas."
        )
        return PLAN_TARGET_IDS

    context.user_data["plan_target_ids"] = ids

    lines = [f"👤 <b>Targeting {len(ids)} user(s):</b>\n"]
    for uid in ids:
        user = get_user(uid)
        plan = user["plan"] if user else "not found"
        lines.append(f"• <code>{uid}</code> → current: <b>{plan}</b>")
    lines.append("\nChoose the new plan:")

    await update.message.reply_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⭐ Pro",    callback_data="setplan_pro"),
                InlineKeyboardButton("🆓 Free",   callback_data="setplan_free"),
            ],
            [
                InlineKeyboardButton("🎁 Trial",  callback_data="setplan_trial"),
                InlineKeyboardButton("🚫 Banned", callback_data="setplan_banned"),
            ],
        ])
    )
    return PLAN_CHOOSE


@admin_only
async def received_plan_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    plan  = query.data.replace("setplan_", "")
    await query.answer()

    # Pro needs a second step to pick the subscription length
    if plan == "pro":
        context.user_data["plan_choice"] = "pro"
        await query.message.reply_text(
            "⭐ <b>Select Pro plan type:</b>\n\n"
            "This determines the expiry date and what shows in the user's /settings.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📅 Monthly (1 month)",   callback_data="pro_monthly")],
                [InlineKeyboardButton("📆 3-Month (3 months)",  callback_data="pro_3month")],
                [InlineKeyboardButton("📆 Yearly (12 months)",  callback_data="pro_yearly")],
            ])
        )
        return PLAN_PRO_TYPE

    # All other plans apply immediately
    await _apply_plan(query, context, plan, pro_type=None)
    return ConversationHandler.END


@admin_only
async def received_pro_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query    = update.callback_query
    pro_type = query.data   # "pro_monthly", "pro_3month", or "pro_yearly"
    await query.answer()
    await _apply_plan(query, context, "pro", pro_type=pro_type)
    return ConversationHandler.END


async def _apply_plan(query, context, plan: str, pro_type: str | None):
    """Write plan changes to DB, reschedule monitors, notify users."""
    user_ids = context.user_data.get("plan_target_ids", [])

    if not user_ids:
        await query.message.reply_text("Something went wrong. Use /admin to try again.")
        context.user_data.clear()
        return

    results = []
    for uid in user_ids:
        try:
            get_or_create_user(uid)

            if plan == "free":
                downgrade_user(uid)
            elif plan == "pro" and pro_type:
                label, months  = _PRO_TYPES[pro_type]
                expiry         = _add_months(months)
                upgrade_user(uid, "pro", pro_expires=expiry, pro_plan_type=label)
            else:
                # trial / banned — no expiry tracking needed
                upgrade_user(uid, plan)

            # Reschedule monitors
            try:
                from db.database import get_monitors
                from services.scheduler import schedule_monitor
                interval = 1 if plan == "pro" else 5
                for m in get_monitors(uid):
                    schedule_monitor(context.application, m["id"], interval)
            except Exception:
                pass

            # Notify the user
            if plan == "pro" and pro_type:
                label, months = _PRO_TYPES[pro_type]
                expiry_display = datetime.fromisoformat(
                    _add_months(months)
                ).strftime("%B %d, %Y")
                user_msg = (
                    f"🎉 Your UptimeGuard plan has been upgraded to "
                    f"<b>Pro ({label})</b>!\n\n"
                    f"📅 Access until: <b>{expiry_display}</b>\n\n"
                    f"Your monitors now check every minute."
                )
            else:
                user_msg = {
                    "trial":  "🎁 Your <b>Pro trial</b> has been activated on UptimeGuard!",
                    "free":   "ℹ️ Your UptimeGuard plan has been changed to <b>Free</b>.\n\nMonitor checks are now every 5 minutes.",
                    "banned": "🚫 Your UptimeGuard account has been suspended.",
                }.get(plan)

            if user_msg:
                try:
                    await context.bot.send_message(
                        chat_id=uid, text=user_msg, parse_mode="HTML"
                    )
                except Exception:
                    pass

            suffix = f" ({_PRO_TYPES[pro_type][0]})" if (plan == "pro" and pro_type) else ""
            results.append(f"✅ <code>{uid}</code> → <b>{plan}{suffix}</b>")

        except Exception as e:
            results.append(f"❌ <code>{uid}</code> → failed: {e}")
            logger.error(f"Admin plan change failed for {uid}: {e}")

    await query.message.reply_text(
        "⚙️ <b>Plan update complete.</b>\n\n" + "\n".join(results),
        parse_mode="HTML"
    )
    context.user_data.clear()


# ─────────────────────────────────────────
# 4. Bot stats
# ─────────────────────────────────────────

@admin_only
async def bot_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    stats = _get_stats()

    await query.message.reply_text(
        f"📊 <b>UptimeGuard Bot Stats</b>\n\n"

        f"─────────────────────────\n"
        f"👥 <b>Users</b>\n"
        f"─────────────────────────\n"
        f"Total users:         <b>{stats['total_users']}</b>\n"
        f"Active users:        <b>{stats['active_users']}</b>\n"
        f"New today:           <b>{stats['new_today']}</b>\n"
        f"New this week:       <b>{stats['new_week']}</b>\n\n"

        f"─────────────────────────\n"
        f"📦 <b>Plans</b>\n"
        f"─────────────────────────\n"
        f"Pro users:           <b>{stats['pro_users']}</b>\n"
        f"Trial users:         <b>{stats['trial_users']}</b>\n"
        f"Free users:          <b>{stats['free_users']}</b>\n"
        f"Banned users:        <b>{stats['banned_users']}</b>\n\n"

        f"─────────────────────────\n"
        f"📡 <b>Monitors</b>\n"
        f"─────────────────────────\n"
        f"Total monitors:      <b>{stats['total_monitors']}</b>\n"
        f"Active monitors:     <b>{stats['active_monitors']}</b>\n"
        f"Paused monitors:     <b>{stats['paused_monitors']}</b>\n"
        f"Monitors per user:   <b>{stats['monitors_per_user']}</b>\n\n"

        f"─────────────────────────\n"
        f"🔴 <b>Incidents</b>\n"
        f"─────────────────────────\n"
        f"Total incidents:     <b>{stats['total_incidents']}</b>\n"
        f"Incidents today:     <b>{stats['incidents_today']}</b>\n"
        f"Incidents this week: <b>{stats['incidents_week']}</b>\n"
        f"Currently down:      <b>{stats['currently_down']}</b>\n\n"

        f"─────────────────────────\n"
        f"⚡ <b>Performance</b>\n"
        f"─────────────────────────\n"
        f"Avg response time:   <b>{stats['avg_response_ms']}ms</b>\n"
        f"Checks today:        <b>{stats['checks_today']}</b>\n"
        f"SSL warnings sent:   <b>{stats['ssl_warnings']}</b>",

        parse_mode="HTML"
    )


# ─────────────────────────────────────────
# DB helpers
# ─────────────────────────────────────────

def _get_all_user_ids() -> list[int]:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT user_id FROM users")
    rows = c.fetchall()
    conn.close()
    return [r["user_id"] for r in rows]


def _get_total_users() -> int:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count


def _get_stats() -> dict:
    conn = get_conn()
    c    = conn.cursor()

    def q(sql, params=()):
        c.execute(sql, params)
        return c.fetchone()[0]

    stats = {
        "total_users":   q("SELECT COUNT(*) FROM users"),
        "active_users":  q("SELECT COUNT(DISTINCT user_id) FROM monitors WHERE active = 1"),
        "new_today":     q("SELECT COUNT(*) FROM users WHERE activated_at >= datetime('now', '-1 day')"),
        "new_week":      q("SELECT COUNT(*) FROM users WHERE activated_at >= datetime('now', '-7 days')"),
        "pro_users":     q("SELECT COUNT(*) FROM users WHERE plan = 'pro'"),
        "trial_users":   q("SELECT COUNT(*) FROM users WHERE plan = 'trial'"),
        "free_users":    q("SELECT COUNT(*) FROM users WHERE plan = 'free'"),
        "banned_users":  q("SELECT COUNT(*) FROM users WHERE plan = 'banned'"),
        "total_monitors":  q("SELECT COUNT(*) FROM monitors"),
        "active_monitors": q("SELECT COUNT(*) FROM monitors WHERE active = 1"),
        "paused_monitors": q("SELECT COUNT(*) FROM monitors WHERE active = 2"),
        "currently_down":  q("SELECT COUNT(*) FROM monitors WHERE last_status = 'down' AND active = 1"),
        "total_incidents": q("SELECT COUNT(*) FROM incidents"),
        "incidents_today": q("SELECT COUNT(*) FROM incidents WHERE checked_at >= datetime('now', '-1 day') AND is_up = 0"),
        "incidents_week":  q("SELECT COUNT(*) FROM incidents WHERE checked_at >= datetime('now', '-7 days') AND is_up = 0"),
        "avg_response_ms": q("SELECT COALESCE(ROUND(AVG(response_ms)), 0) FROM incidents WHERE is_up = 1 AND checked_at >= datetime('now', '-1 day')"),
        "checks_today":    q("SELECT COUNT(*) FROM incidents WHERE checked_at >= datetime('now', '-1 day')"),
        "ssl_warnings":    q("SELECT COUNT(*) FROM incidents WHERE checked_at >= datetime('now', '-30 days') AND error_msg LIKE '%SSL%'"),
    }

    total_u = stats["total_users"]
    total_m = stats["active_monitors"]
    stats["monitors_per_user"] = round(total_m / total_u, 1) if total_u > 0 else 0

    conn.close()
    return stats


# ─────────────────────────────────────────
# Broadcast helper
# ─────────────────────────────────────────

async def _blast(bot, user_ids: list[int], message: str) -> tuple[int, int]:
    sent   = 0
    failed = 0
    for i in range(0, len(user_ids), 25):
        batch = user_ids[i:i + 25]
        for uid in batch:
            try:
                await bot.send_message(chat_id=uid, text=message, parse_mode="HTML")
                sent += 1
            except BadRequest as e:
                logger.warning(f"Broadcast HTML rejected for {uid} ({e}) — retrying as plain text")
                try:
                    await bot.send_message(chat_id=uid, text=message)
                    sent += 1
                except Exception as retry_err:
                    logger.warning(f"Broadcast plain text failed for {uid}: {retry_err}")
                    failed += 1
            except TelegramError as e:
                logger.warning(f"Broadcast TelegramError for {uid}: {e}")
                failed += 1
            except Exception as e:
                logger.error(f"Broadcast unexpected error for {uid}: {e}", exc_info=True)
                failed += 1
        if i + 25 < len(user_ids):
            await asyncio.sleep(1)
    return sent, failed


# ─────────────────────────────────────────
# ID parser
# ─────────────────────────────────────────

def _parse_ids(raw: str) -> list[int]:
    parts = raw.replace("\n", ",").split(",")
    ids   = []
    for p in parts:
        p = p.strip()
        try:
            ids.append(int(p))
        except ValueError:
            continue
    return ids


# ─────────────────────────────────────────
# Cancel
# ─────────────────────────────────────────

async def _cancel(update, context):
    await update.message.reply_text("❌ Cancelled.")
    context.user_data.clear()
    return ConversationHandler.END


# ─────────────────────────────────────────
# Conversation handler
# ─────────────────────────────────────────

admin_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(broadcast_all_entry,    pattern="^admin_broadcast_all$"),
        CallbackQueryHandler(broadcast_target_entry, pattern="^admin_broadcast_target$"),
        CallbackQueryHandler(plan_entry,             pattern="^admin_plan$"),
        CallbackQueryHandler(bot_stats,              pattern="^admin_stats$"),
    ],
    states={
        BROADCAST_ALL_MSG: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_broadcast_all_msg)
        ],
        BROADCAST_TARGET_IDS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_broadcast_target_ids)
        ],
        BROADCAST_TARGET_MSG: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_broadcast_target_msg)
        ],
        PLAN_TARGET_IDS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, received_plan_ids)
        ],
        PLAN_CHOOSE: [
            CallbackQueryHandler(received_plan_choice, pattern="^setplan_")
        ],
        PLAN_PRO_TYPE: [
            CallbackQueryHandler(received_pro_type, pattern="^pro_")
        ],
    },
    fallbacks=[CommandHandler("cancel", _cancel)],
    per_message=False,
    per_chat=True,
)
