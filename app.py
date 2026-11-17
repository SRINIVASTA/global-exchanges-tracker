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
    st.session_state.pipeline_executed = (
        "Last_Price" in st.session_state.df.columns
        and not st.session_state.df["Last_Price"].dropna().empty
    )

# ==========================================
# MAIN DATA PREPARATION
# ==========================================
df = st.session_state.df.copy()

if "Last_Price" in df.columns and "Prev_Close" in df.columns:
    df["Previous Close"] = df["Prev_Close"]
    df["Last Closing Price"] = df["Last_Price"]
    df["Price Difference"] = (df["Last Closing Price"] - df["Previous Close"]).round(2)
    df["% Difference"] = ((df["Price Difference"] / df["Previous Close"]) * 100).round(2)

# ==========================================
# SIDEBAR: PIPELINE & DATE CONTROLS
# ==========================================
with st.sidebar:
    st.header("⚙️ Pipeline Execution Control")
    if st.button("🚀 Execute Live Ingestion", type="primary", use_container_width=True):
        with st.spinner("Ingesting multi-exchange telemetry via yfinance..."):
            st.session_state.df = execute_live_ingestion(
                start_date=st.session_state.get("start_date"),
                end_date=st.session_state.get("end_date"),
            )
            st.session_state.pipeline_executed = True
        st.rerun()

    st.divider()
    st.subheader("📅 Date Horizon Filters")
    default_end = date.today()
    default_start = default_end - timedelta(days=5)
    start_date = st.date_input("Start Date", value=default_start, format="DD-MM-YYYY", key="start_date")
    end_date = st.date_input("End Date", value=default_end, format="DD-MM-YYYY", key="end_date")

    st.divider()
    st.subheader("📧 Document Delivery Terminal")
    pdf_slot = st.empty()
    email_slot = st.empty()

# ==========================================
# MAIN DESKTOP WORKSPACE
# ==========================================
st.title("📊 Global Exchanges Market Performance Enterprise Workspace")
st.caption("Automated ingestion pipeline mapping tracking deltas across India (BSE/NSE), USA, China, Singapore & global exchanges with interactive absolute price variance analysis dashboards.")

if not st.session_state.pipeline_executed:
    st.warning("⚠️ **Hub Pipeline Standby:** Displaying structural index tracking registry. Live metrics will map below after running execution pipeline.")

tab_ledger, tab_analytics = st.tabs(["📋 Master Ledger Workspace", "📈 Cross-Sectional Analytics"])

with tab_ledger:
    # 4 Dedicated Registry Filters: Country, Exchange, Index / Benchmark Name, yfinance Ticker
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        selected_countries = st.multiselect(
            "Country",
            options=df["Country"].dropna().unique().tolist(),
            default=[],
        )
    with f2:
        exchange_pool = df[df["Country"].isin(selected_countries)] if selected_countries else df
        selected_exchanges = st.multiselect(
            "Exchange",
            options=exchange_pool["Exchange"].dropna().unique().tolist(),
            default=[],
        )
    with f3:
        index_pool = exchange_pool[exchange_pool["Exchange"].isin(selected_exchanges)] if selected_exchanges else exchange_pool
        selected_indices = st.multiselect(
            "Index / Benchmark Name",
            options=index_pool["Index / Benchmark Name"].dropna().unique().tolist(),
            default=[],
        )
    with f4:
        ticker_pool = index_pool[index_pool["Index / Benchmark Name"].isin(selected_indices)] if selected_indices else index_pool
        selected_tickers = st.multiselect(
            "yfinance Ticker",
            options=ticker_pool["yfinance Ticker"].dropna().unique().tolist(),
            default=[],
        )

    filtered_df = df.copy()
    if selected_countries:
        filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]
    if selected_exchanges:
        filtered_df = filtered_df[filtered_df["Exchange"].isin(selected_exchanges)]
    if selected_indices:
        filtered_df = filtered_df[filtered_df["Index / Benchmark Name"].isin(selected_indices)]
    if selected_tickers:
        filtered_df = filtered_df[filtered_df["yfinance Ticker"].isin(selected_tickers)]

    if "% Difference" in filtered_df.columns and not filtered_df["% Difference"].dropna().empty:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Tracked Indices", len(filtered_df))
        k2.metric("Advancing (🟢)", int((filtered_df["% Difference"] > 0).sum()))
        k3.metric("Declining (🔴)", int((filtered_df["% Difference"] < 0).sum()))
        last_sync = (
            str(filtered_df["Updated_At"].dropna().iloc[0])
            if "Updated_At" in filtered_df.columns and not filtered_df["Updated_At"].dropna().empty
            else "N/A"
        )
        k4.metric("Last Sync Timestamp", last_sync)

    base_cols = ["Country", "Exchange", "Index / Benchmark Name", "yfinance Ticker"]
    calc_cols = [
        c for c in ["Previous Close", "Last Closing Price", "Price Difference", "% Difference", "Day_High", "Day_Low", "Market_Date", "Updated_At"]
        if c in filtered_df.columns
    ]
    display_df = filtered_df[base_cols + calc_cols]

    def color_variance(val):
        if pd.isna(val):
            return ""
        color = "#16a34a" if val > 0 else ("#dc2626" if val < 0 else "gray")
        return f"color: {color}; font-weight: bold;"

    styled_df = display_df.style
    if "Price Difference" in display_df.columns and "% Difference" in display_df.columns:
        styled_df = styled_df.map(color_variance, subset=["Price Difference", "% Difference"])

    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=560)

# ==========================================
# POPULATE SIDEBAR PDF DOWNLOAD & EMAIL FOR FILTERED DATA ONLY
# ==========================================
filtered_pdf_path = generate_pdf_report(filtered_df)
with open(filtered_pdf_path, "rb") as f:
    filtered_pdf_bytes = f.read()

pdf_slot.download_button(
    label=f"📥 Download Filtered PDF ({len(filtered_df)} rows)",
    data=filtered_pdf_bytes,
    file_name="Filtered_Exchanges_Report.pdf",
    mime="application/pdf",
    use_container_width=True,
)

if email_slot.button("📤 Dispatch Filtered PDF via Email", use_container_width=True):
    gmail_cfg = dict(st.secrets["gmail"]) if "gmail" in st.secrets else {}
    ok, status_msg = send_report_email(filtered_pdf_path, gmail_cfg)
    if ok:
        st.sidebar.success(status_msg)
    else:
        st.sidebar.error(status_msg)

with tab_analytics:
    if "% Difference" not in filtered_df.columns or filtered_df["% Difference"].dropna().empty:
        st.info("Run **🚀 Execute Live Ingestion** from the sidebar to unlock Cross-Sectional Analytics charts.")
    else:
        chart_df = filtered_df.dropna(subset=["% Difference"]).sort_values("% Difference", ascending=False)
        st.subheader("Percentage Variance (%) Across Filtered Indices")
        st.bar_chart(chart_df.set_index("Index / Benchmark Name")["% Difference"], use_container_width=True)

        st.subheader("Country-Level Average Performance (%)")
        country_perf = chart_df.groupby("Country", as_index=True)["% Difference"].mean().sort_values(ascending=False)
        st.bar_chart(country_perf, use_container_width=True)
