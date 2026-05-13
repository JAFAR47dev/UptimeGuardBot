import logging
import datetime
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, PreCheckoutQueryHandler,
    MessageHandler, filters,
)
from config import BOT_TOKEN, STATUS_PAGE_PORT
from db.database import init_db
from services.scheduler import restore_all_monitors
from handlers.start import (
    start,
    skip_tz_callback,
    how_it_works_callback,
    quick_status_callback,
    quick_list_callback,
    quick_report_callback,
    referral_info_callback,
)
from handlers.help import help_command
from handlers.monitors import (
    add_conversation, threshold_conversation,
    note_conversation, webhook_conversation,
    keyword_conversation, confirm_conversation,
    list_monitors, delete_callback,
    confirm_delete_callback, cancel_delete_callback,
    pause_callback, resume_callback, status,
)
from handlers.snooze import snooze_callback
from handlers.testalert import testalert_command, testalert_callback
from handlers.maintenance import maintenance_conversation, mw_delete_callback
from handlers.incidents import incidents_command, incidents_callback
from handlers.team import (
    team_conversation,
    team_remove_callback,
    team_confirm_remove_callback,
    team_cancel_remove_callback,
)
from handlers.reports import report
from handlers.payments import (
    upgrade,
    pay_callback,
    pay_monthly_callback,
    pay_3month_callback,
    pay_yearly_callback,
    precheckout,
    payment_success
)
from handlers.statuspage import statuspage_conversation
from tasks.trial_expiry import check_expired_trials
from tasks.weekly_report import send_weekly_reports
from services.checker import create_shared_session
from web.server import start_web_server, stop_web_server
from handlers.referral import referral, referral_refresh_callback
from handlers.admin import admin_panel, admin_conversation
from handlers.myplan import myplan
from handlers.settings import (
    settings_command,
    settings_conversation,
    settings_myplan_callback,
    language_btn_callback,
    language_set_callback,
)
from tasks.onboarding_reminders import register_onboarding_jobs


logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def post_init(app):
    await start_web_server(app, port=STATUS_PAGE_PORT)
    app.bot_data["aiohttp_session"] = await create_shared_session()
    restore_all_monitors(app)
    register_onboarding_jobs(app)
    # Ensure no stale webhook is registered — polling and webhooks conflict
    await app.bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook cleared — running in polling mode")


async def post_shutdown(app):
    await stop_web_server(app)
    session = app.bot_data.get("aiohttp_session")
    if session and not session.closed:
        await session.close()


def main():
    init_db()

    builder = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .post_stop(post_shutdown)
    )

    app = builder.build()

    app.job_queue.run_daily(
        check_expired_trials,
        time=datetime.time(hour=9, minute=0),
        name="trial_expiry_check",
    )

    app.job_queue.run_daily(
        send_weekly_reports,
        time=datetime.time(hour=9, minute=0),
        days=(1,),
        name="weekly_reports",
    )

    # -----------------------------------------------------------------------
    # Handlers
    # ConversationHandlers first — entry_point patterns must not overlap with
    # global callbacks registered below.
    # -----------------------------------------------------------------------

    # Conversations
    app.add_handler(maintenance_conversation)
    app.add_handler(threshold_conversation)
    app.add_handler(note_conversation)
    app.add_handler(webhook_conversation)
    app.add_handler(keyword_conversation)
    app.add_handler(confirm_conversation)
    app.add_handler(team_conversation)
    app.add_handler(add_conversation)
    app.add_handler(statuspage_conversation)
    app.add_handler(admin_conversation)
    app.add_handler(settings_conversation)

    # Commands
    app.add_handler(CommandHandler("start",       start))
    app.add_handler(CommandHandler("list",        list_monitors))
    app.add_handler(CommandHandler("report",      report))
    app.add_handler(CommandHandler("upgrade",     upgrade))
    app.add_handler(CommandHandler("status",      status))
    app.add_handler(CommandHandler("help",        help_command))
    app.add_handler(CommandHandler("testalert",   testalert_command))
    app.add_handler(CommandHandler("incidents",   incidents_command))
    app.add_handler(CommandHandler("team",        team_conversation.entry_points[0].callback))
    app.add_handler(CommandHandler("maintenance", maintenance_conversation.entry_points[0].callback))
    app.add_handler(CommandHandler("statuspage",  statuspage_conversation.entry_points[0].callback))
    app.add_handler(CommandHandler("referral",    referral))
    app.add_handler(CommandHandler("admin",       admin_panel))
    app.add_handler(CommandHandler("settings",    settings_command))

    # Delete — long prefixes before short ones
    app.add_handler(CallbackQueryHandler(confirm_delete_callback, pattern="^confirmdelete_"))
    app.add_handler(CallbackQueryHandler(cancel_delete_callback,  pattern="^canceldelete_"))
    app.add_handler(CallbackQueryHandler(delete_callback,         pattern="^del_"))
    app.add_handler(CallbackQueryHandler(
        referral_refresh_callback, pattern="^referral_refresh$"
    ))

    # Settings & plan
    app.add_handler(CallbackQueryHandler(settings_command,         pattern="^settings$"))
    app.add_handler(CallbackQueryHandler(settings_myplan_callback, pattern="^settings_myplan$"))
    app.add_handler(CallbackQueryHandler(myplan,                   pattern="^myplan$"))

    # Language picker — exact match before prefix
    app.add_handler(CallbackQueryHandler(language_btn_callback, pattern="^settings_lang$"))
    app.add_handler(CallbackQueryHandler(language_set_callback, pattern="^setlang_"))

    app.add_handler(CallbackQueryHandler(skip_tz_callback, pattern="^skip_tz$"))

    # Monitor actions
    app.add_handler(CallbackQueryHandler(pause_callback,  pattern="^pause_"))
    app.add_handler(CallbackQueryHandler(resume_callback, pattern="^resume_"))
    app.add_handler(CallbackQueryHandler(snooze_callback, pattern="^snooze_"))

    # Test alert — specific before generic
    app.add_handler(CallbackQueryHandler(testalert_callback, pattern="^testalert_"))
    app.add_handler(CallbackQueryHandler(testalert_callback, pattern="^testalert$"))

    # Incidents picker
    app.add_handler(CallbackQueryHandler(incidents_callback, pattern="^incidents_"))

    # Maintenance delete
    app.add_handler(CallbackQueryHandler(mw_delete_callback, pattern="^mw_del_"))

    # Team — confirmremove/cancelremove before remove_ (prefix safety)
    app.add_handler(CallbackQueryHandler(team_confirm_remove_callback, pattern="^team_confirmremove_"))
    app.add_handler(CallbackQueryHandler(team_cancel_remove_callback,  pattern="^team_cancelremove_"))
    app.add_handler(CallbackQueryHandler(team_remove_callback,         pattern="^team_remove_"))

    # Start menu
    app.add_handler(CallbackQueryHandler(help_command,          pattern="^help$"))
    app.add_handler(CallbackQueryHandler(how_it_works_callback, pattern="^how_it_works$"))
    app.add_handler(CallbackQueryHandler(quick_status_callback, pattern="^quick_status$"))
    app.add_handler(CallbackQueryHandler(quick_list_callback,   pattern="^quick_list$"))
    app.add_handler(CallbackQueryHandler(quick_report_callback, pattern="^quick_report$"))
    app.add_handler(CallbackQueryHandler(referral_info_callback, pattern="^referral_info$"))

    # Status page
    app.add_handler(CallbackQueryHandler(
        statuspage_conversation.entry_points[1].callback,
        pattern="^create_statuspage$",
    ))

    # Payments
    app.add_handler(CallbackQueryHandler(pay_callback,         pattern="^pay_pro$"))
    app.add_handler(CallbackQueryHandler(upgrade,              pattern="^upgrade$"))
    app.add_handler(CallbackQueryHandler(pay_monthly_callback, pattern="^pay_monthly$"))
    app.add_handler(CallbackQueryHandler(pay_3month_callback,  pattern="^pay_3month$"))
    app.add_handler(CallbackQueryHandler(pay_yearly_callback,  pattern="^pay_yearly$"))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, payment_success))

    # -----------------------------------------------------------------------
    # Always use polling — the aiohttp status page server already owns the
    # port so PTB's built-in webhook server can't run alongside it.
    # Polling works fine on Render since the process runs continuously.
    # -----------------------------------------------------------------------
    logger.info("Starting polling")
    app.run_polling()


if __name__ == "__main__":
    main()