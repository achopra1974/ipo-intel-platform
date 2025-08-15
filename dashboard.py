import streamlit as st
import pandas as pd
from db import fetch_all

st.set_page_config(page_title="IPO Dashboard", layout="wide")
st.title("IPO Intelligence Dashboard")

rows = fetch_all()
df = pd.DataFrame(rows, columns=[
    "Code","Name","Open","Close","Lot","Range","MinInvest",
    "GMP","Allotment","Refund","Listing","LastUpd"
])

st.dataframe(df, use_container_width=True)

sector_filter = st.text_input("Filter by sector keyword")
if sector_filter:
    df = df[df["Name"].str.contains(sector_filter, case=False)]
    st.dataframe(df, use_container_width=True)