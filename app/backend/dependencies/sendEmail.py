import os, smtplib, ssl
from email.message import EmailMessage
import secrets

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

def gen_code(n=6) -> int:
    """Generate an integer verification code with n digits, not starting with 0."""
    first = secrets.randbelow(9) + 1  # ensures 1–9
    rest = "".join(str(secrets.randbelow(10)) for _ in range(n - 1))
    return int(str(first) + rest)