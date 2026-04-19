# handlers/snooze.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from notifications.alerts import snooze_monitor, snooze_expiry, SNOOZE_MINUTES
from db.database import get_monitor


async def snooze_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the 🔕 Snooze button attached to down and slow-response alerts.

    - Sets or extends the snooze by SNOOZE_MINUTES.
    - Edits the original alert message to confirm, replacing the button
      with an 'extend snooze' option so the user can keep stacking if needed.
    - Tapping again while already snoozed extends from the current expiry.
    """
    query      = update.callback_query
    monitor_id = int(query.data.split("_")[1])
    bot_data   = context.bot_data

    monitor = get_monitor(monitor_id)
    label   = (monitor["label"] or monitor["url"]) if monitor else f"Monitor {monitor_id}"

    # Apply / extend the snooze
    expiry     = snooze_monitor(bot_data, monitor_id)
    expiry_str = expiry.strftime("%H:%M")

    await query.answer(f"🔕 Snoozed until {expiry_str}", show_alert=False)

    # Replace the button with an 'extend' variant so it remains tappable
    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
                f"🔕 Snoozed until {expiry_str} — tap to extend",
                callback_data=f"snooze_{monitor_id}"
            )
        ]])
    )
