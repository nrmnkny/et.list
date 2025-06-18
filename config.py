# config.py
import os
from dotenv import load_dotenv

load_dotenv(override=True)
print("Looking for .env at:", os.path.abspath(".env"))


DB_SETTINGS = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME")
}
print("✅ Loaded DB_SETTINGS:", DB_SETTINGS)
