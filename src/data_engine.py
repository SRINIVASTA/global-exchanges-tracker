from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf
from generate_local_csv import build_master_csv, MASTER_CSV

def fetch_master_list() -> pd.DataFrame:
    if not MASTER_CSV.exists():
        return build_master_csv()
    return pd.read_csv(MASTER_CSV)

def execute_live_ingestion() -> pd.DataFrame:
    df = fetch_master_list()
    tickers = df["yfinance Ticker"].dropna().unique().tolist()

    raw = yf.download(tickers, period="5d", interval="1d", group_by="ticker", progress=False)
    updated_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    prev_closes, last_closes, changes, pct_changes = [], [], [], []
    day_highs, day_lows, market_dates, updated_ats = [], [], [], []

    for ticker in df["yfinance Ticker"]:
        try:
            hist = raw[ticker].dropna(subset=["Close"]) if len(tickers) > 1 else raw.dropna(subset=["Close"])
            if len(hist) >= 2:
                prev_val = float(hist["Close"].iloc[-2])
                last_val = float(hist["Close"].iloc[-1])
                delta = last_val - prev_val
                pct = (delta / prev_val) * 100

                prev_closes.append(round(prev_val, 2))
                last_closes.append(round(last_val, 2))
                changes.append(round(delta, 2))
                pct_changes.append(round(pct, 2))
                day_highs.append(round(float(hist["High"].iloc[-1]), 2))
                day_lows.append(round(float(hist["Low"].iloc[-1]), 2))
                market_dates.append(str(hist.index[-1].date()))
                updated_ats.append(updated_utc)
            else:
                prev_closes.append(None); last_closes.append(None)
                changes.append(None); pct_changes.append(None)
                day_highs.append(None); day_lows.append(None)
                market_dates.append(None); updated_ats.append(updated_utc)
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
