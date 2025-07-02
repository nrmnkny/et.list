import streamlit as st
import pandas as pd
from db.utils import get_engine

st.title("Summary Statistics")

engine = get_engine()
product_count = pd.read_sql("SELECT COUNT(*) AS count FROM product_listings", engine)
avg_stock = pd.read_sql("SELECT AVG(stock_quantity) AS avg FROM inventory_snapshots", engine)

st.metric("Total Products", int(product_count.loc[0, "count"]))

if avg_stock.loc[0, "avg"] is not None:
    st.metric("Average Stock Quantity", round(avg_stock.loc[0, "avg"], 2))
else:
    st.write("No inventory data available yet.")