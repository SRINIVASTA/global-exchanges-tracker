from datetime import date, timedelta
import streamlit as st
import pandas as pd
from src.data_engine import fetch_master_list, execute_live_ingestion
from src.pdf_generator import generate_pdf_report
from src.email_service import send_report_email

st.set_page_config(
    page_title="Global Exchanges Market Performance Enterprise Workspace",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "df" not in st.session_state:
    st.session_state.df = fetch_master_list()

if "pipeline_executed" not in st.session_state:
    st.session_state.pipeline_executed = "Last_Price" in st.session_state.df.columns and not st.session_state.df["Last_Price"].dropna().empty

# ==========================================
# SIDEBAR: PIPELINE & FILTER CONTROLS
# ==========================================
with st.sidebar:
    st.header("⚙️ Pipeline Execution Control")
    if st.button("🚀 Execute Live Ingestion", type="primary", use_container_width=True):
        with st.spinner("Ingesting multi-exchange telemetry via yfinance..."):
            st.session_state.df = execute_live_ingestion(
                start_date=st.session_state.get("start_date"),
                end_date=st.session_state.get("end_date"),
            )
            generate_pdf_report(st.session_state.df)
            st.session_state.pipeline_executed = True
        st.success("Live ingestion complete!")

    st.divider()
    st.subheader("📅 Date Horizon Filters")
    default_end = date.today()
    default_start = default_end - timedelta(days=5)
    start_date = st.date_input("Start Date", value=default_start, format="DD-MM-YYYY", key="start_date")
    end_date = st.date_input("End Date", value=default_end, format="DD-MM-YYYY", key="end_date")

    st.divider()
    st.subheader("💰 Valuation Matrix Range")
    price_from = st.number_input("Price From (Index Level)", min_value=0.0, value=0.0, step=100.0)
    price_to = st.number_input("Price To (Index Level)", min_value=0.0, value=200000.0, step=1000.0)

    st.divider()
    st.subheader("📧 Document Delivery Terminal")
    if st.button("📤 Dispatch PDF Report", use_container_width=True):
        pdf_file = generate_pdf_report(st.session_state.df)
        gmail_cfg = dict(st.secrets["gmail"]) if "gmail" in st.secrets else {}
        ok, status_msg = send_report_email(pdf_file, gmail_cfg)
        if ok:
            st.success(status_msg)
        else:
            st.error(status_msg)

# ==========================================
# MAIN DESKTOP WORKSPACE
# ==========================================
st.title("📊 Global Exchanges Market Performance Enterprise Workspace")
st.caption("Automated ingestion pipeline mapping tracking deltas across India (BSE/NSE), USA, China, Singapore & global exchanges with interactive absolute price variance analysis dashboards.")

if not st.session_state.pipeline_executed:
    st.warning("⚠️ **Hub Pipeline Standby:** Displaying structural index tracking registry. Live metrics will map below after running execution pipeline.")

df = st.session_state.df.copy()

# Apply Valuation Matrix Range if live prices exist
if "Last_Price" in df.columns and not df["Last_Price"].dropna().empty:
    df = df[(df["Last_Price"].isna()) | ((df["Last_Price"] >= price_from) & (df["Last_Price"] <= price_to))]

tab_ledger, tab_analytics = st.tabs(["📋 Master Ledger Workspace", "📈 Cross-Sectional Analytics"])

with tab_ledger:
    col_search, col_country, col_exchange = st.columns([2, 1, 1])
    with col_search:
        search_query = st.text_input(
            "Filter Ledger (Index Name / Ticker / Country)",
            placeholder="Search e.g., BSE 500, NIFTY, S&P 500, STI, ^BSESN...",
        )
    with col_country:
        selected_countries = st.multiselect("Country", options=df["Country"].unique().tolist(), default=[])
    with col_exchange:
        selected_exchanges = st.multiselect("Exchange", options=df["Exchange"].unique().tolist(), default=[])

    filtered_df = df.copy()
    if selected_countries:
        filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]
    if selected_exchanges:
        filtered_df = filtered_df[filtered_df["Exchange"].isin(selected_exchanges)]
    if search_query:
        mask = (
            filtered_df["Index / Benchmark Name"].str.contains(search_query, case=False, na=False)
            | filtered_df["yfinance Ticker"].str.contains(search_query, case=False, na=False)
            | filtered_df["Country"].str.contains(search_query, case=False, na=False)
            | filtered_df["Exchange"].str.contains(search_query, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    if "Pct_Change" in filtered_df.columns and not filtered_df["Pct_Change"].dropna().empty:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Tracked Indices", len(filtered_df))
        k2.metric("Advancing (🟢)", int((filtered_df["Pct_Change"] > 0).sum()))
        k3.metric("Declining (🔴)", int((filtered_df["Pct_Change"] < 0).sum()))
        last_sync = filtered_df["Updated_At"].dropna().iloc
        k4.metric("Last Sync Timestamp", last_sync)

    def color_variance(val):
        if pd.isna(val):
            return ""
        color = "#16a34a" if val > 0 else ("#dc2626" if val < 0 else "gray")
        return f"color: {color}; font-weight: bold;"

    styled_df = filtered_df.style
    if "Change" in filtered_df.columns and "Pct_Change" in filtered_df.columns:
        styled_df = styled_df.map(color_variance, subset=["Change", "Pct_Change"])

    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=560)

with tab_analytics:
    if "Pct_Change" not in df.columns or df["Pct_Change"].dropna().empty:
        st.info("Run **🚀 Execute Live Ingestion** from the sidebar to unlock Cross-Sectional Analytics charts.")
    else:
        chart_df = df.dropna(subset=["Pct_Change"]).sort_values("Pct_Change", ascending=False)
        st.subheader("Percentage Variance (%) Across Global Indices")
        st.bar_chart(chart_df.set_index("Index / Benchmark Name")["Pct_Change"], use_container_width=True)

        st.subheader("Country-Level Average Performance (%)")
        country_perf = chart_df.groupby("Country", as_index=True)["Pct_Change"].mean().sort_values(ascending=False)
        st.bar_chart(country_perf, use_container_width=True)
