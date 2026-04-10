import logging
import datetime
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, PreCheckoutQueryHandler,
    MessageHandler, filters
)
from config import BOT_TOKEN
from db.database import init_db
from services.scheduler import restore_all_monitors
from handlers.start import (
    start,
    how_it_works_callback,
    quick_status_callback,
    quick_list_callback,
    quick_report_callback
)
from handlers.help import help_command
from handlers.monitors import (
    add_conversation, threshold_conversation,
    list_monitors, delete_callback,
    confirm_delete_callback, cancel_delete_callback,
    pause_callback, resume_callback, status
)
from handlers.reports import report
from handlers.payments import upgrade, pay_callback, precheckout, payment_success
from tasks.trial_expiry import check_expired_trials
from tasks.weekly_report import send_weekly_reports
from services.checker import create_shared_session

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)


async def post_init(app):
    """Runs after bot initialises — create shared HTTP session
    and restore all active monitors from DB."""
    app.bot_data["aiohttp_session"] = await create_shared_session()
    restore_all_monitors(app)


async def post_shutdown(app):
    """Runs on shutdown — close shared HTTP session cleanly."""
    session = app.bot_data.get("aiohttp_session")
    if session and not session.closed:
        await session.close()


def main():
    init_db()

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .post_stop(post_shutdown)
        .build()
    )

    # Restore monitors from DB on startup
    # Kept for safety — post_init also calls this,
    # but this ensures jobs fire even if post_init
    # is delayed on slow cold starts
    app.job_queue.run_once(
        lambda ctx: restore_all_monitors(app),
        when=3
    )

    app.job_queue.run_daily(
        check_expired_trials,
        time=datetime.time(hour=9, minute=0),
        name="trial_expiry_check"
    )

    app.job_queue.run_daily(
        send_weekly_reports,
        time=datetime.time(hour=9, minute=0),
        days=(1,),          # 1 = Monday (0=Sun, 1=Mon ... 6=Sat)
        name="weekly_reports"
    )

    # Handlers
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("list",    list_monitors))
    app.add_handler(CommandHandler("report",  report))
    app.add_handler(CommandHandler("upgrade", upgrade))
    app.add_handler(CommandHandler("status",  status))
    app.add_handler(CommandHandler("help",    help_command))
    app.add_handler(CallbackQueryHandler(help_command,            pattern="^help$"))
    app.add_handler(CallbackQueryHandler(confirm_delete_callback, pattern="^confirmdelete_"))
    app.add_handler(CallbackQueryHandler(cancel_delete_callback,  pattern="^canceldelete_"))
    app.add_handler(CallbackQueryHandler(how_it_works_callback,   pattern="^how_it_works$"))
    app.add_handler(CallbackQueryHandler(quick_status_callback,   pattern="^quick_status$"))
    app.add_handler(CallbackQueryHandler(quick_list_callback,     pattern="^quick_list$"))
    app.add_handler(CallbackQueryHandler(quick_report_callback,   pattern="^quick_report$"))
    app.add_handler(add_conversation)
    app.add_handler(threshold_conversation)

    # Callbacks
    app.add_handler(CallbackQueryHandler(delete_callback, pattern="^del_"))
    app.add_handler(CallbackQueryHandler(pause_callback,  pattern="^pause_"))
    app.add_handler(CallbackQueryHandler(resume_callback, pattern="^resume_"))
    app.add_handler(CallbackQueryHandler(pay_callback,    pattern="^pay_pro$"))
    app.add_handler(CallbackQueryHandler(
        lambda u, c: upgrade(u, c), pattern="^upgrade$"
    ))

    # Payments
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, payment_success))

    app.run_polling()


if __name__ == "__main__":
    main()
