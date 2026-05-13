# config.py
import os
from dotenv import load_dotenv
load_dotenv()

bot_username      = os.getenv("bot_username")
BOT_TOKEN         = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH", "/opt/render/project/src/data/uptime.db")
FREE_LIMIT        = 3
PRO_MONTHLY_PRICE = 500   # Telegram Stars
PRO_3MONTH_PRICE  = 1250   # ~$12.50 — saves 250 Stars
PRO_YEARLY_PRICE  = 4000   # ~$40    — saves 2,000 Stars


# Admin IDs — comma-separated in .env: ADMIN_IDS=123456789,987654321
_raw_admin_ids = os.getenv("ADMIN_IDS", "")
ADMIN_IDS: list[int] = [
    int(x.strip()) for x in _raw_admin_ids.split(",") if x.strip().isdigit()
]

# ---------------------------------------------------------------------------
# Public base URL
# Render injects RENDER_EXTERNAL_URL automatically on every deploy,
# so the subdomain is always current regardless of redeploys.
# Falls back to STATUS_PAGE_BASE_URL for local dev.
# ---------------------------------------------------------------------------
STATUS_PAGE_BASE_URL = (
    os.getenv("RENDER_EXTERNAL_URL")        # set automatically by Render
    or os.getenv("STATUS_PAGE_BASE_URL",    # local dev fallback
                 "http://localhost:8080")
).rstrip("/")

STATUS_PAGE_PORT = int(os.getenv("STATUS_PAGE_PORT", "8080"))

# Referral reward thresholds
REFERRAL_GOAL        = 3    # qualified referrals needed to unlock a reward
REFERRAL_BONUS_SLOTS = 3    # extra free monitor slots per reward tier
REFERRAL_TRIAL_DAYS  = 7    # trial extension days per reward tier