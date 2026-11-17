import streamlit as st
import pandas as pd
from src.data_engine import fetch_master_list, execute_live_ingestion
from src.pdf_generator import generate_pdf_report
from src.email_service import send_report_email

st.set_page_config(page_title="Global Exchanges Tracker", layout="wide")
st.title("Global Stock Exchanges & Indices Workspace")

if "df" not in st.session_state:
    st.session_state.df = fetch_master_list()

# Sidebar Controls (Verification-First Workflow)
st.sidebar.header("Control Panel")

if st.sidebar.button("Execute Live Ingestion", type="primary", use_container_width=True):
    with st.spinner("Fetching global market data via yfinance..."):
        st.session_state.df = execute_live_ingestion()
        generate_pdf_report(st.session_state.df)
    st.sidebar.success("Master CSV & PDF updated!")

if st.sidebar.button("Dispatch PDF Report", use_container_width=True):
    pdf_file = generate_pdf_report(st.session_state.df)
    gmail_cfg = dict(st.secrets["gmail"]) if "gmail" in st.secrets else {}
    ok, status_msg = send_report_email(pdf_file, gmail_cfg)
    if ok:
        st.sidebar.success(status_msg)
    else:
        st.sidebar.error(status_msg)

st.sidebar.divider()
st.sidebar.subheader("Market Filters")
df = st.session_state.df

countries = st.sidebar.multiselect("Country", df["Country"].unique(), default=df["Country"].unique())
filtered = df[df["Country"].isin(countries)]

exchanges = st.sidebar.multiselect("Exchange", filtered["Exchange"].unique(), default=filtered["Exchange"].unique())
filtered = filtered[filtered["Exchange"].isin(exchanges)]

search_query = st.text_input("Search Index or Ticker", placeholder="e.g., BSE 500, NIFTY, S&P, STI...")
if search_query:
    mask = (
        filtered["Index / Benchmark Name"].str.contains(search_query, case=False, na=False)
        | filtered["yfinance Ticker"].str.contains(search_query, case=False, na=False)
    )
    filtered = filtered[mask]

# Summary Metrics
if "Pct_Change" in filtered.columns and not filtered["Pct_Change"].dropna().empty:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tracked Indices", len(filtered))
    m2.metric("Gainers", int((filtered["Pct_Change"] > 0).sum()))
    m3.metric("Losers", int((filtered["Pct_Change"] < 0).sum()))
    last_sync = filtered["Updated_At"].dropna().iloc[0]
    m4.metric("Last Sync", last_sync)

def style_delta(val):
    if pd.isna(val):
        return ""
    color = "#16a34a" if val > 0 else ("#dc2626" if val < 0 else "gray")
    return f"color: {color}; font-weight: bold;"

styled = filtered.style
if "Change" in filtered.columns and "Pct_Change" in filtered.columns:
    styled = styled.map(style_delta, subset=["Change", "Pct_Change"])

st.dataframe(styled, use_container_width=True, hide_index=True)
