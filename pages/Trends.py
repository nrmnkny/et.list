# dashboard_trends.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pytrends.request import TrendReq
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from config import DB_SETTINGS
import time

print(" Loaded DB_SETTINGS:", DB_SETTINGS)
st.set_page_config(page_title=" Google Trends", layout="wide")
st.title(" Google Trends Dashboard")

# Input
keyword = st.text_input("Enter a keyword (e.g. 'air fryer')", value="wireless earbuds")
region = st.selectbox("Select Region", ["US", "KE", "GB", "IN", "NG", "CA", "AU", "ZA"], index=0)

def get_engine():
    encoded_password = quote_plus(DB_SETTINGS['password'])
    url = f"postgresql://{DB_SETTINGS['user']}:{encoded_password}@{DB_SETTINGS['host']}:{DB_SETTINGS['port']}/{DB_SETTINGS['database']}"
    return create_engine(url)

if keyword:
    try:
        time.sleep(1)  # Optional delay to avoid API rate limits
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo=region, gprop='')

        df = pytrends.interest_over_time()

        if not df.empty:
            df = df.reset_index()
            st.subheader(f"Search Interest for '{keyword}' in {region}")
            fig = px.line(df, x='date', y=keyword, title='Interest Over Time', labels={keyword: 'Search Interest'})
            st.plotly_chart(fig, use_container_width=True)

            # Save to database
            if st.button(" Save to Database"):
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

                st.success(f" Saved {len(df_to_insert)} records for '{keyword}' in {region}'")
        else:
            st.warning("No trend data found. Try another keyword or region.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
