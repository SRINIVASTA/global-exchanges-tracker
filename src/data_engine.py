from datetime import datetime, date, timedelta, timezone
import pandas as pd
import yfinance as yf
from generate_local_csv import build_master_csv, MASTER_CSV

def fetch_master_list() -> pd.DataFrame:
    if not MASTER_CSV.exists():
        return build_master_csv()
    return pd.read_csv(MASTER_CSV)

def _extract_ticker_history(raw: pd.DataFrame, ticker: str, total_tickers: int, start_date: date | None, end_date: date | None) -> pd.DataFrame:
    hist = pd.DataFrame()
    try:
        if total_tickers > 1 and ticker in raw.columns.get_level_values(0):
            hist = raw[ticker].dropna(subset=["Close"])
        elif total_tickers == 1:
            hist = raw.dropna(subset=["Close"])
    except Exception:
        hist = pd.DataFrame()

    # Fallback: fetch individually if batch download missed or returned < 2 rows
    if hist.empty or len(hist) < 2:
        try:
            t_obj = yf.Ticker(ticker)
            if end_date:
                hist = t_obj.history(
                    start=str((start_date or end_date) - timedelta(days=14)),
                    end=str(end_date + timedelta(days=1)),
                    interval="1d",
                )
            else:
                hist = t_obj.history(period="15d", interval="1d")
            hist = hist.dropna(subset=["Close"])
        except Exception:
            return pd.DataFrame()

    if not hist.empty:
        # Normalize index to date and remove duplicate intraday/close entries for the same date
        hist.index = pd.to_datetime(hist.index).tz_localize(None).normalize()
        hist = hist[~hist.index.duplicated(keep="last")].sort_index()

        # Filter up to end_date while keeping prior trading day for accurate Prev_Close
        if end_date:
            hist = hist[hist.index.date <= end_date]

    return hist

def execute_live_ingestion(start_date: date | None = None, end_date: date | None = None) -> pd.DataFrame:
    df = fetch_master_list()
    tickers = df["yfinance Ticker"].dropna().astype(str).str.strip().unique().tolist()

    if end_date:
        fetch_start = (start_date or end_date) - timedelta(days=14)
        fetch_end = end_date + timedelta(days=1)
        raw = yf.download(tickers, start=str(fetch_start), end=str(fetch_end), interval="1d", group_by="ticker", progress=False)
    else:
        raw = yf.download(tickers, period="15d", interval="1d", group_by="ticker", progress=False)

    updated_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    prev_closes, last_closes, changes, pct_changes = [], [], [], []
    day_highs, day_lows, market_dates, updated_ats = [], [], [], []

    for ticker in df["yfinance Ticker"]:
        clean_ticker = str(ticker).strip()
        hist = _extract_ticker_history(raw, clean_ticker, len(tickers), start_date, end_date)

        if len(hist) >= 2:
            # If start_date is given and has earlier candles inside window, compare end vs start; otherwise compare last 2 sessions
            if start_date and end_date:
                in_window = hist[hist.index.date >= start_date]
                if len(in_window) >= 2:
                    prev_val = float(in_window["Close"].iloc[0])
                    last_val = float(in_window["Close"].iloc[-1])
                else:
                    prev_val = float(hist["Close"].iloc[-2])
                    last_val = float(hist["Close"].iloc[-1])
            else:
                prev_val = float(hist["Close"].iloc[-2])
                last_val = float(hist["Close"].iloc[-1])

            delta = last_val - prev_val
            pct = (delta / prev_val) * 100 if prev_val != 0 else 0.0

            prev_closes.append(round(prev_val, 2))
            last_closes.append(round(last_val, 2))
            changes.append(round(delta, 2))
            pct_changes.append(round(pct, 2))
            day_highs.append(round(float(hist["High"].iloc[-1]), 2))
            day_lows.append(round(float(hist["Low"].iloc[-1]), 2))
            market_dates.append(str(hist.index[-1].date()))
            updated_ats.append(updated_utc)
        else:
            # Secondary fallback via fast_info if history endpoint is empty
            try:
                fi = yf.Ticker(clean_ticker).fast_info
                last_val = float(fi["last_price"])
                prev_val = float(fi["previous_close"])
                delta = last_val - prev_val
                pct = (delta / prev_val) * 100 if prev_val != 0 else 0.0

                prev_closes.append(round(prev_val, 2))
                last_closes.append(round(last_val, 2))
                changes.append(round(delta, 2))
                pct_changes.append(round(pct, 2))
                day_highs.append(round(float(fi.get("day_high", last_val)), 2))
                day_lows.append(round(float(fi.get("day_low", last_val)), 2))
                market_dates.append(str(date.today()))
                updated_ats.append(updated_utc)
            except Exception:
                prev_closes.append(None); last_closes.append(None)
                changes.append(None); pct_changes.append(None)
                day_highs.append(None); day_lows.append(None)
                market_dates.append(None); updated_ats.append(updated_utc)

    df["Prev_Close"] = prev_closes
    df["Last_Price"] = last_closes
    df["Change"] = changes
    df["Pct_Change"] = pct_changes
    df["Day_High"] = day_highs
    df["Day_Low"] = day_lows
    df["Market_Date"] = market_dates
    df["Updated_At"] = updated_ats

    df.to_csv(MASTER_CSV, index=False)
    return df
