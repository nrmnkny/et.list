# main.py

import streamlit as st

st.set_page_config(page_title="ET.LIST Home", layout="wide")

st.title("Welcome to ATMD")
st.markdown("### A Simple ETL-powered Dashboard Platform")

st.write("""
ATMD lets you:
-  Track product interest over time using Google Trends
-  Visualize real-time product listings
-  Analyze inventory snapshots and stock levels

Use the menu on the left to navigate between dashboards.
""")

# Optional: home animation or image
st.image("https://cdn-icons-png.flaticon.com/512/4361/4361134.png", width=200)
