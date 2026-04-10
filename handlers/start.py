#handlers/start.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import get_or_create_user, get_all_monitors, is_pro

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user    = update.effective_user
    db_user = get_or_create_user(user.id, user.username)
    pro     = is_pro(user.id)

    # Detect new vs returning
    monitors = get_all_monitors(user.id)
    is_new   = len(monitors) == 0

    if is_new:
        await _new_user_flow(update, db_user, pro)
    else:
        await _returning_user_flow(update, db_user, pro, monitors)


async def _new_user_flow(update, db_user, pro: bool):
    """
    Shown to users with zero monitors.
    Single goal: get them to add their first monitor.
    """
    name      = update.effective_user.first_name or "there"
    plan_text = "✅ 7-day Pro trial active" if db_user["plan"] == "trial" else "🆓 Free plan"

    await update.message.reply_text(
        f"👋 Hey {name}, welcome to <b>UptimeGuard</b>!\n\n"
        f"Get instant Telegram alerts the moment your website "
        f"goes down — before your users notice.\n\n"
        f"📦 {plan_text}\n\n"
        f"👇 Add your first monitor to get started:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "➕ Add My First Monitor", callback_data="add_monitor"
            )],
            [InlineKeyboardButton(
                "📖 How it works", callback_data="how_it_works"
            )]
        ])
    )


async def _returning_user_flow(update, db_user, pro: bool, monitors: list):
    """
    Shown to users who already have monitors.
    Shows live snapshot + quick actions.
    """
    up_count     = sum(1 for m in monitors if m["last_status"] == "up")
    down_count   = sum(1 for m in monitors if m["last_status"] == "down")
    paused_count = sum(1 for m in monitors if m["active"] == 2)
    total        = len(monitors)

    if down_count > 0:
        health_icon = "🔴"
        health_text = f"{down_count} monitor(s) currently DOWN"
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

    await update.message.reply_text(
        f"{health_icon} <b>UptimeGuard</b>\n\n"
        f"📦 Plan: <b>{plan_label}</b>\n"
        f"📡 Monitors: <b>{total}</b> total • "
        f"<b>{up_count}</b> up • "
        f"<b>{down_count}</b> down • "
        f"<b>{paused_count}</b> paused\n\n"
        f"Status: <b>{health_text}</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚡ Status",  callback_data="quick_status"),
                InlineKeyboardButton("📋 List",    callback_data="quick_list"),
            ],
            [
                InlineKeyboardButton("➕ Add Monitor", callback_data="add_monitor"),
                InlineKeyboardButton("📊 Report",      callback_data="quick_report"),
            ],
            [InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")]
            if not pro else
            []
        ])
    )


async def how_it_works_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "📖 <b>How UptimeGuard works</b>\n\n"
        "1️⃣ Add a URL with /add\n"
        "2️⃣ We ping it every 5 min (free) or 1 min (Pro)\n"
        "3️⃣ If it goes down you get an instant alert here\n"
        "4️⃣ When it recovers you get another alert\n\n"
        "Pro also includes:\n"
        "🔐 SSL expiry warnings\n"
        "🐢 Slow response alerts\n"
        "📊 Weekly summary reports\n\n"
        "👇 Ready to add your first monitor?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("➕ Add Monitor", callback_data="add_monitor")
        ]])
    )


async def quick_status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline /status trigger from start menu."""
    query = update.callback_query
    await query.answer()
    # Reuse the status handler logic by faking an update
    from handlers.monitors import status
    await status(query, context)


async def quick_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    from handlers.monitors import list_monitors
    await list_monitors(query, context)


async def quick_report_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    from handlers.reports import report
    await report(query, context)