#config.py
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN        = os.getenv("BOT_TOKEN")
DB_PATH          = os.getenv("DB_PATH", "uptime.db")
FREE_LIMIT       = 3
PRO_MONTHLY_PRICE = 500   # Telegram Stars
