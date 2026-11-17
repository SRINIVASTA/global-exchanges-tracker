import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

def send_report_email(pdf_path: Path, secrets_dict: dict | None = None) -> tuple[bool, str]:
    cfg = secrets_dict or {}

    sender = cfg.get("username") or cfg.get("sender_email") or os.getenv("SENDER_EMAIL")
    password = cfg.get("app_password") or os.getenv("APP_PASSWORD")
    recipients = cfg.get("to_email") or cfg.get("recipients") or os.getenv("RECIPIENTS", "")

    if isinstance(recipients, str):
        recipient_list = [r.strip() for r in recipients.split(",") if r.strip()]
    elif recipients:
        recipient_list = [str(r).strip() for r in recipients if str(r).strip()]
    else:
        recipient_list = []

    if not sender or not password or not recipient_list:
        return False, "Missing SMTP credentials (username, app_password, or to_email)."

    clean_password = str(password).replace(" ", "").strip()

    msg = EmailMessage()
    msg["Subject"] = "Global Exchanges & Indices Market Report"
    msg["From"] = str(sender).strip()
    msg["To"] = ", ".join(recipient_list)
    msg.set_content("Attached is the latest Global Stock Exchanges & Indices Filtered Ledger PDF report.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_path.name)

    try:
        with smtplib.SMTP("://gmail.com", 587) as server:
            server.starttls()
            server.login(str(sender).strip(), clean_password)
            server.send_message(msg)
        return True, f"Dispatched PDF to {len(recipient_list)} recipient(s)."
    except Exception as e:
        return False, f"SMTP Error: {e}"
