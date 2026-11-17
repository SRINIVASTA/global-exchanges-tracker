import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

def send_report_email(pdf_path: Path, secrets_dict: dict | None = None) -> tuple[bool, str]:
    cfg = secrets_dict or {}
    sender = cfg.get("sender_email") or os.getenv("SENDER_EMAIL")
    password = cfg.get("app_password") or os.getenv("APP_PASSWORD")
    recipients = cfg.get("recipients") or os.getenv("RECIPIENTS", "")

    if isinstance(recipients, str):
        recipient_list = [r.strip() for r in recipients.split(",") if r.strip()]
    else:
        recipient_list = list(recipients)

    if not sender or not password or not recipient_list:
        return False, "Missing SMTP credentials (sender_email, app_password, or recipients)."

    msg = EmailMessage()
    msg["Subject"] = "Global Exchanges & Indices Market Report"
    msg["From"] = sender
    msg["To"] = ", ".join(recipient_list)
    msg.set_content("Attached is the latest Global Stock Exchanges & Indices Master Ledger PDF report.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_path.name)

    with smtplib.SMTP("://gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

    return True, f"Dispatched PDF to {len(recipient_list)} recipient(s)."
