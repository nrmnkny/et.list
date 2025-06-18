import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import DB_SETTINGS

def get_engine():
    encoded_password = quote_plus(DB_SETTINGS["password"])
    url = f"postgresql://{DB_SETTINGS['user']}:{encoded_password}@{DB_SETTINGS['host']}:{DB_SETTINGS['port']}/{DB_SETTINGS['database']}"
    return create_engine(url)

@st.cache_data(ttl=600)
def load_data():
    engine = get_engine()
    query = "SELECT * FROM product_listings;"
    return pd.read_sql(query, engine)

# UI
st.set_page_config(page_title="🛍 Product Dashboard", layout="wide")
st.title("Product Listings Overview")

df = load_data()

# Metrics
st.metric("Total Products", len(df))
st.metric("Average Price", f"${df['price'].mean():.2f}")

# Filters
col1, col2 = st.columns(2)
with col1:
    categories = df['category'].dropna().unique().tolist()
    selected_categories = st.multiselect("Filter by Category", categories, default=categories)
with col2:
    vendors = df['vendor'].dropna().unique().tolist()
    selected_vendors = st.multiselect("Filter by Vendor", vendors, default=vendors)

filtered = df[
    df['category'].isin(selected_categories) &
    df['vendor'].isin(selected_vendors)
]

# Price Distribution
st.subheader(" Price Distribution")
fig = px.bar(
    filtered,
    x='title',
    y='price',
    color='category',
    hover_data=['vendor'],
    title="Product Prices",
    labels={'title': 'Product', 'price': 'Price ($)'}
)
st.plotly_chart(fig, use_container_width=True)

# Product Table
st.subheader(" Product Table")
filtered['Product Link'] = filtered['product_url'].apply(lambda x: f"[🔗 Link]({x})")
st.write(
    filtered[['title', 'category', 'vendor', 'price', 'currency', 'Product Link']].rename(columns={
        'title': 'Title',
        'price': 'Price',
        'currency': 'Currency',
        'vendor': 'Vendor',
        'category': 'Category'
    }),
    unsafe_allow_html=True
)
