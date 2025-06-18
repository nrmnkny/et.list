# bulk_fetch_trends.py

import time
import pandas as pd
from pytrends.request import TrendReq
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from config import DB_SETTINGS

# Connect2PostgreSQL
def get_engine():
    pw = quote_plus(DB_SETTINGS["password"])
    url = f"postgresql://{DB_SETTINGS['user']}:{pw}@{DB_SETTINGS['host']}:{DB_SETTINGS['port']}/{DB_SETTINGS['database']}"
    return create_engine(url)

# Pull/Insert
def fetch_and_insert(keyword, region="US"):
    print(f"🔍 Fetching trends for: '{keyword}' in {region}")
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo=region, gprop='')
        df = pytrends.interest_over_time()

        if df.empty:
            print(f"⚠️ No data for '{keyword}'")
            return

        df = df.reset_index()
        df["keyword"] = keyword
        df["region"] = region
        df["interest_score"] = df[keyword]
        df_to_insert = df[["keyword", "region", "interest_score", "date"]]

        with get_engine().begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO search_trends (keyword, region, interest_score, date)
                    VALUES (:keyword, :region, :interest_score, :date)
                """),
                df_to_insert.to_dict(orient="records")
            )

        print(f"✅ Inserted {len(df_to_insert)} records for '{keyword}'")

    except Exception as e:
        print(f"❌ Error for '{keyword}': {e}")

# === KEYWORD LIST ===
keywords = [
    "gaming laptop",
    "air fryer",
    "wireless headphones",
    "solar light",
    "noise cancelling headphones",
]

# === Run ===
if __name__ == "__main__":
    for kw in keywords:
        fetch_and_insert(kw)
        time.sleep(5)  
