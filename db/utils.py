# db/utils.py
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import DB_SETTINGS

def get_engine():
    pw = quote_plus(DB_SETTINGS["password"])
    url = (
        f"postgresql://{DB_SETTINGS['user']}:"
        f"{pw}@{DB_SETTINGS['host']}:"
        f"{DB_SETTINGS['port']}/"
        f"{DB_SETTINGS['database']}"
    )
    return create_engine(url)
