# pages/4_Product_Trends.py
import streamlit as st
import pandas as pd
from db.utils import get_engine

st.title("🔍 Product Trends")

@st.cache_data(ttl=600)
def load_data():
    engine = get_engine()
    query = """
        SELECT p.product_id,
               p.title,
               p.category,
               p.vendor,
               p.price,
               p.currency,
               p.product_url,
               t.region,
               t.date,
               t.interest_score
        FROM product_listings p
        JOIN search_trends t
          ON LOWER(t.keyword) = LOWER(p.title)
          OR LOWER(t.keyword) = LOWER(p.category)
    """
    return pd.read_sql(query, engine)

# — load & bail on error —
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Database error: {e}")
    st.stop()

# — Sidebar filters —
st.sidebar.header("Filter Trends")
min_date, max_date = df["date"].min(), df["date"].max()
start_date, end_date = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

regions   = sorted(df["region"].dropna().unique())
vendors   = sorted(df["vendor"].dropna().unique())
categories= sorted(df["category"].dropna().unique())

selected_regions    = st.sidebar.multiselect("Region",   regions,   default=regions)
selected_vendors    = st.sidebar.multiselect("Vendor",   vendors,   default=vendors)
selected_categories = st.sidebar.multiselect("Category",categories,default=categories)

# — apply filters —
filtered = df[
    (df["date"]   >= pd.to_datetime(start_date)) &
    (df["date"]   <= pd.to_datetime(end_date))   &
    (df["region"].isin(selected_regions))       &
    (df["vendor"].isin(selected_vendors))       &
    (df["category"].isin(selected_categories))
]

if filtered.empty:
    st.warning("No data for those filters — try widening your net.")
    st.stop()

# — aggregate & sort —
agg = (
    filtered
    .groupby(
        ["product_id","title","category","vendor","price","currency","product_url","region"]
    )["interest_score"]
    .mean()
    .reset_index(name="avg_interest")
    .sort_values("avg_interest", ascending=False)
)

agg["Link"] = agg["product_url"].apply(lambda x: f"[🔗]({x})")

# — render —
st.dataframe(
    agg[["title","vendor","category","region","avg_interest","Link"]]
       .rename(columns={
           "title":"Title",
           "vendor":"Vendor",
           "category":"Category",
           "region":"Region",
           "avg_interest":"Avg Interest"
       }),
    use_container_width=True,
)
