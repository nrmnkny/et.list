import streamlit as st
import pandas as pd
import plotly.express as px
from db.utils import get_engine

st.title("Inventory Trends")

engine = get_engine()
query = """
SELECT product_id, stock_quantity, captured_at
FROM inventory_snapshots
ORDER BY captured_at
"""

df = pd.read_sql(query, engine)

if df.empty:
    st.info("No inventory snapshots available.")
else:
    fig = px.line(df, x="captured_at", y="stock_quantity", color="product_id")
    st.plotly_chart(fig, use_container_width=True)