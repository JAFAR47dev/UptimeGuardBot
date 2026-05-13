from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.database import get_user, get_monitors, count_monitors, get_monitor_limit


async def myplan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user_id  = update.callback_query.from_user.id
        reply_fn = update.callback_query.message.reply_text
        await update.callback_query.answer()
    else:
        user_id  = update.effective_user.id
        reply_fn = update.message.reply_text

    user = get_user(user_id)

    if not user:
        await reply_fn(
            "⚠️ Could not find your account.\n\n"
            "Send /start to get started."
        )
        return

    plan          = (user.get("plan") or "free").lower()
    trial_expires = user.get("trial_expires")
    pro_expires   = user.get("pro_expires")
    pro_plan_type = user.get("pro_plan_type") or "Monthly"
    bonus_slots   = user.get("bonus_monitors") or 0

    monitors_used  = count_monitors(user_id)
    monitor_limit  = get_monitor_limit(user_id)
    limit_display  = "Unlimited" if monitor_limit >= 999_999 else str(monitor_limit)

    # ── Free plan ────────────────────────────────────────────────

    if plan == "free":
        bonus_line = (
            f"\n🎁 Referral bonus: <b>+{bonus_slots} slot(s)</b>"
            if bonus_slots else ""
        )
        await reply_fn(
            "📦 <b>Your Plan: Free</b>\n\n"
            f"📡 Monitors: <b>{monitors_used} / {limit_display}</b>{bonus_line}\n"
            f"⏱ Check interval: <b>5 minutes</b>\n\n"
            "What you're missing on Free:\n"
            "❌ 1-minute check intervals\n"
            "❌ SSL expiry warnings\n"
            "❌ Slow response threshold alerts\n"
            "❌ Webhook integrations\n"
            "❌ Team notifications\n"
            "❌ Unlimited monitors\n\n"
            "👇 Upgrade to never miss an outage.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "⭐ Upgrade to Pro",
                    callback_data="upgrade"
                )],
                [InlineKeyboardButton(
                    "👥 Earn free slots via referral",
                    callback_data="referral_info"
                )]
            ])
        )
        return

    # ── Trial plan ───────────────────────────────────────────────

    if plan == "trial":
        days_left, expiry_str = _parse_expiry(trial_expires)

        if days_left is not None and days_left <= 0:
            await reply_fn(
                "⏰ <b>Your Trial Has Expired</b>\n\n"
                "Your 7-day Pro trial has ended.\n"
                "Your monitors are still running but "
                "check intervals have returned to 5 minutes.\n\n"
                "Upgrade to keep 1-minute checks and all Pro features.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")
                ]])
            )
            return

        days_label = (
            f"{days_left} day{'s' if days_left != 1 else ''} remaining"
            if days_left is not None else "Unknown"
        )

        urgency = ""
        if days_left is not None:
            if days_left <= 1:
                urgency = "\n\n⚠️ <b>Your trial ends tomorrow!</b> Lock in Pro now."
            elif days_left <= 3:
                urgency = f"\n\n⏳ Only {days_left} days left in your trial."

        await reply_fn(
            f"🎁 <b>Your Plan: Pro Trial</b>\n\n"
            f"📅 Expires: <b>{expiry_str}</b>\n"
            f"⏳ Time left: <b>{days_label}</b>\n\n"
            f"📡 Monitors: <b>{monitors_used} / {limit_display}</b>\n"
            f"⏱ Check interval: <b>1 minute</b>\n\n"
            "All Pro features are active:\n"
            "✅ 1-minute check intervals\n"
            "✅ SSL expiry warnings\n"
            "✅ Slow response threshold alerts\n"
            "✅ Webhook integrations\n"
            "✅ Team notifications\n"
            "✅ Unlimited monitors"
            f"{urgency}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "⭐ Upgrade Before Trial Ends",
                    callback_data="upgrade"
                )
            ]])
        )
        return

    # ── Pro plan ─────────────────────────────────────────────────

    if plan == "pro":
        days_left, expiry_str = _parse_expiry(pro_expires)

        if days_left is None:
            expiry_line = "📅 Access: <b>Active</b>"
        else:
            days_label  = f"{days_left} day{'s' if days_left != 1 else ''} remaining"
            expiry_line = (
                f"📅 Renews: <b>{expiry_str}</b>\n"
                f"⏳ Time left: <b>{days_label}</b>"
            )

        renewal_note = ""
        if days_left is not None and days_left <= 7:
            renewal_note = (
                f"\n\n⚠️ <b>Your Pro access expires in {days_left} day"
                f"{'s' if days_left != 1 else ''}.</b>\n"
                "Renew now to avoid losing 1-minute checks."
            )

        await reply_fn(
            f"⭐ <b>Your Plan: Pro ({pro_plan_type})</b>\n\n"
            f"{expiry_line}\n\n"
            f"📡 Monitors: <b>{monitors_used} / {limit_display}</b>\n"
            f"⏱ Check interval: <b>1 minute</b>\n\n"
            "Active features:\n"
            "✅ 1-minute check intervals\n"
            "✅ SSL expiry warnings\n"
            "✅ Slow response threshold alerts\n"
            "✅ Webhook integrations\n"
            "✅ Team notifications\n"
            "✅ Unlimited monitors"
            f"{renewal_note}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "🔄 Renew Pro",
                    callback_data="upgrade"
                )
            ]]) if (days_left is not None and days_left <= 30) else None
        )
        return

    # ── Banned ───────────────────────────────────────────────────

    if plan == "banned":
        await reply_fn(
            "🚫 Your account has been suspended.\n\n"
            "If you believe this is a mistake, please contact support."
        )
        return

    # ── Fallback ─────────────────────────────────────────────────

    await reply_fn("⚠️ Could not determine your plan.\n\nContact support.")


# ─────────────────────────────────────────
# Helper
# ─────────────────────────────────────────

def _parse_expiry(expiry_str: str | None) -> tuple[int | None, str]:
    if not expiry_str:
        return None, "Not set"
    try:
        expiry_dt = datetime.fromisoformat(expiry_str) if isinstance(expiry_str, str) else expiry_str
        delta     = expiry_dt - datetime.now()
        days_left = max(delta.days, 0)
        display   = expiry_dt.strftime("%d %b %Y")
        return days_left, display
    except Exception:
        return None, "Unknown"

