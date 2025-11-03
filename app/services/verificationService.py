import secrets, datetime as dt
from sqlalchemy.orm import Session
from app.models.users import User
from app.services.emailService import send_email

def _now_utc():
    """Return current UTC datetime."""
    return dt.datetime.now(dt.timezone.utc)

def _gen_code(n=6) -> int:
    """Generate an integer verification code with n digits, not starting with 0."""
    first = secrets.randbelow(9) + 1  # ensures 1–9
    rest = "".join(str(secrets.randbelow(10)) for _ in range(n - 1))
    return int(str(first) + rest)

def start_verification(db: Session, email: str) -> None:
    """
        Generate and send a verification code to the user's email.
        Code expires in 30 minutes.
    """
    u = db.query(User).filter(User.email == email.lower().strip()).first()

    if not u:
        return

    code = _gen_code()
    u.verificationCode = code
    u.verificationExpiresAt = _now_utc() + dt.timedelta(minutes=30)
    db.commit()
    send_email(
        to=str(u.email),
        subject="Your Diet App verification code",
        body=f"Your verification code is: {code}\nIt expires in 30 minutes."
    )

def confirm_verification(db: Session, email: str, code: int) -> User:
    """
        Confirm a user's email by validating the provided verification code.
        Raises ValueError for invalid, expired, or missing codes.
        Marks user as emailVerified on success.
    """
    u = db.query(User).filter(User.email == email.lower().strip()).first()

    if not u:
        raise ValueError("Invalid code")
    if not u.verificationCode or not u.verificationExpiresAt:
        raise ValueError("No active verification")
    if u.verificationExpiresAt < _now_utc() or u.verificationCode != code:
        raise ValueError("Invalid or expired code")

    u.emailVerified = True
    u.verificationCode = None
    u.verificationExpiresAt = None
    db.commit()
    return u
