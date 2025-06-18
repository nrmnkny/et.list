# dashboard_trend_summary.py

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import DB_SETTINGS

st.set_page_config(page_title=" Trend Summary", layout="wide")
st.title(" Google Trends: Insight Summary")

# === Connect to DB ===
def get_engine():
    pw = quote_plus(DB_SETTINGS["password"])
    url = f"postgresql://{DB_SETTINGS['user']}:{pw}@{DB_SETTINGS['host']}:{DB_SETTINGS['port']}/{DB_SETTINGS['database']}"
    return create_engine(url)

@st.cache_data(ttl=600)
def load_data():
    engine = get_engine()
    return pd.read_sql("SELECT keyword, region, interest_score, date FROM search_trends;", engine)

df = load_data()

# === Filters ===
st.sidebar.header(" Filter")
region = st.sidebar.selectbox("Region", ["All"] + sorted(df["region"].unique().tolist()))
keyword = st.sidebar.selectbox("Keyword", ["All"] + sorted(df["keyword"].unique().tolist()))

df_filtered = df.copy()
if region != "All":
    df_filtered = df_filtered[df_filtered["region"] == region]
if keyword != "All":
    df_filtered = df_filtered[df_filtered["keyword"] == keyword]

# === Trend Line Chart ===
if not df_filtered.empty:
    st.subheader(f" Search Interest Over Time ({keyword if keyword != 'All' else 'All Keywords'})")
    fig = (
        df_filtered.groupby(["date", "keyword"])["interest_score"]
        .mean()
        .unstack()
        .plot(kind="line", use_index=True, figsize=(10, 4))
        .figure
    )
    st.pyplot(fig)

    # === Metrics Summary ===
    col1, col2, col3 = st.columns(3)
    col1.metric(" Avg Interest", f"{df_filtered['interest_score'].mean():.1f}")
    col2.metric(" Peak Interest", f"{df_filtered['interest_score'].max()}")
    col3.metric(" Last Date", f"{df_filtered['date'].max().strftime('%Y-%m-%d')}")

    # === CSV Export ===
    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(" Download CSV", csv, "filtered_trends.csv", "text/csv")
else:
    st.warning("No data matches your filters.")
