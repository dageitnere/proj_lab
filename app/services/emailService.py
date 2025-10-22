import os, smtplib, ssl
from email.message import EmailMessage

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_email(to: str, subject: str, body: str):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        raise RuntimeError("Missing GMAIL_USER or GMAIL_APP_PASSWORD")

    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls(context=context)
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)