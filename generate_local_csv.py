from pathlib import Path
import pandas as pd

MASTER_CSV = Path(__file__).resolve().parent / "data" / "global_exchanges_master.csv"

EXCHANGE_DATA = [
    # INDIA - BSE
    ("India", "BSE", "BSE SENSEX", "^BSESN"),
    ("India", "BSE", "BSE 500", "BSE-500.BO"),
    ("India", "BSE", "BSE 200", "BSE-200.BO"),
    ("India", "BSE", "BSE 100", "BSE-100.BO"),
    ("India", "BSE", "BSE BANKEX", "BSE-BANK.BO"),
    ("India", "BSE", "BSE IT", "BSE-IT.BO"),
    ("India", "BSE", "BSE Auto", "BSE-AUTO.BO"),
    ("India", "BSE", "BSE Healthcare", "BSE-HC.BO"),
    ("India", "BSE", "BSE FMCG", "BSE-FMCG.BO"),
    ("India", "BSE", "BSE MidCap", "BSE-MIDCAP.BO"),
    ("India", "BSE", "BSE SmallCap", "BSE-SMLCAP.BO"),
    # INDIA - NSE
    ("India", "NSE", "NIFTY 50", "^NSEI"),
    ("India", "NSE", "NIFTY BANK", "^NSEBANK"),
    ("India", "NSE", "NIFTY 500", "^CRSLDX"),
    ("India", "NSE", "NIFTY IT", "^CNXIT"),
    ("India", "NSE", "NIFTY Auto", "^CNXAUTO"),
    ("India", "NSE", "NIFTY Pharma", "^CNXPHARMA"),
    ("India", "NSE", "NIFTY FMCG", "^CNXFMCG"),
    ("India", "NSE", "NIFTY Midcap 100", "^CNXMIDCAP"),
    # USA
    ("USA", "NYSE/S&P", "S&P 500", "^GSPC"),
    ("USA", "NYSE", "Dow Jones Industrial Average", "^DJI"),
    ("USA", "NASDAQ", "NASDAQ Composite", "^IXIC"),
    ("USA", "NASDAQ", "NASDAQ 100", "^NDX"),
    ("USA", "Russell", "Russell 2000", "^RUT"),
    # CHINA & HONG KONG
    ("China", "SSE", "SSE Composite", "000001.SS"),
    ("China", "SSE/SZSE", "CSI 300", "000300.SS"),
    ("China", "SZSE", "Shenzhen Component", "399001.SZ"),
    ("China", "SZSE", "ChiNext Index", "399006.SZ"),
    ("Hong Kong", "HKEX", "Hang Seng Index", "^HSI"),
    # SINGAPORE & GLOBAL
    ("Singapore", "SGX", "Straits Times Index", "^STI"),
    ("Japan", "TSE", "Nikkei 225", "^N225"),
    ("UK", "LSE", "FTSE 100", "^FTSE"),
    ("Germany", "XETRA", "DAX 40", "^GDAXI"),
]

def build_master_csv():
    MASTER_CSV.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(
        EXCHANGE_DATA,
        columns=["Country", "Exchange", "Index / Benchmark Name", "yfinance Ticker"],
    )
    df.to_csv(MASTER_CSV, index=False)
    print(f"Generated {MASTER_CSV} with {len(df)} indices.")
    return df

if __name__ == "__main__":
    build_master_csv()
