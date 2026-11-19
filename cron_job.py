import os
import tomllib
from datetime import datetime, timedelta, date
from pathlib import Path
from src.data_engine import execute_live_ingestion
from src.pdf_generator import generate_pdf_report
from src.email_service import EnterpriseEmailService

SECRETS_PATH = Path(__file__).resolve().parent / ".streamlit" / "secrets.toml"

def get_ist_date() -> date:
    """Returns the current calendar date in Indian Standard Time (IST)."""
    # Overcomes the runner's midnight system clock rollover by explicitly matching Indian timelines
    return (datetime.utcnow() + timedelta(hours=5, minutes=30)).date()

def _load_smtp_credentials() -> tuple[str, str, str]:
    """Load credentials from GitHub Actions env vars first, then fallback to local .streamlit/secrets.toml."""
    sender = os.getenv("USERNAME") or os.getenv("SENDER_EMAIL") or ""
    password = os.getenv("APP_PASSWORD") or ""
    recipients = os.getenv("TO_EMAIL") or os.getenv("RECIPIENTS") or ""

    if (not sender or not password or not recipients) and SECRETS_PATH.exists():
        with open(SECRETS_PATH, "rb") as f:
            secrets = tomllib.load(f)
        cfg = secrets.get("gmail", secrets)
        sender = sender or str(cfg.get("username", cfg.get("sender_email", "")))
        password = password or str(cfg.get("app_password", ""))
        raw_to = recipients or cfg.get("to_email", cfg.get("recipients", ""))
        if isinstance(raw_to, list):
            recipients = ", ".join(str(r).strip() for r in raw_to if str(r).strip())
        else:
            recipients = str(raw_to)

    return sender.strip(), password.strip(), recipients.strip()

def run_headless_pipeline():
    print("Starting headless global exchanges ingestion...")
    
    # Calculate the safe market target date using Indian Standard Time
    target_date = get_ist_date()
    print(f"Targeting evaluation ledger date window: {target_date.strftime('%d/%m/%Y')}")

    # Pass the calculated date to guarantee data integrity despite GitHub runner queue delays
    df = execute_live_ingestion(target_date=target_date)
    print(f"Updated master CSV with {len(df)} global indices.")

    pdf_path = generate_pdf_report(df)
    print(f"Compiled PDF report at: {pdf_path}")

    sender, password, recipients = _load_smtp_credentials()
    if sender and password and recipients:
        sent_count = EnterpriseEmailService.send_report(
            recipient_string=recipients,
            attachment_path=str(pdf_path),
            sender_email=sender,
            app_password=password,
            subject=f"Automated Executive Briefing: Global Exchanges Market Matrix [{target_date.strftime('%d/%m/%Y')}]",
        )
        print(f"Dispatched PDF briefing to {sent_count} recipient(s).")
    else:
        print("Skipping email dispatch: SMTP credentials not configured in environment/secrets.")

if __name__ == "__main__":
    run_headless_pipeline()
