import os, smtplib, ssl
from email.message import EmailMessage

# Gmail credentials must be stored as environment variables
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_email(to: str, subject: str, body: str):
    """
    Send a plain-text email via Gmail SMTP.

    Args:
        to (str): Recipient email address.
        subject (str): Email subject line.
        body (str): Plain-text email body.

    Raises:
        RuntimeError: If Gmail credentials are missing.
    """
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        raise RuntimeError("Missing GMAIL_USER or GMAIL_APP_PASSWORD")

    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    # Secure SMTP connection
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls(context=context)
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)