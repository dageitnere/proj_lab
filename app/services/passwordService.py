import os, time, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.services.emailService import send_email
from app.models.users import User

# Security constants
_JWT_SECRET = os.getenv("JWT_SECRET")
_ALG = "HS256"
_TTL = 60 * 30  # 30 minutes
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _create_reset_token(sub: str, ttl: int = _TTL) -> str:
    """Create a short-lived JWT reset token for the given user ID."""
    now = int(time.time())
    return jwt.encode({"sub": sub, "typ": "reset", "iat": now, "exp": now + ttl}, _JWT_SECRET, algorithm=_ALG)

def _decode(tok: str) -> dict:
    """Decode a JWT token and return its payload."""
    return jwt.decode(tok, _JWT_SECRET, algorithms=[_ALG])

def start_reset(db: Session, email: str) -> None:
    """
    Start password reset flow:
    - Find user by email
    - Generate JWT reset token
    - Send reset link via email
    """
    u = db.query(User).filter(User.email == email.lower().strip()).first()
    if not u:
        return  # Silent fail for privacy
    tok = _create_reset_token(str(u.uuid))
    reset_url = f"http://localhost:8000/auth/reset-password?token={tok}"

    send_email(
        to=str(u.email),
        subject="Password reset",
        body=f"Open this link to set a new password (valid 30 min): {reset_url}"
    )

def confirm_reset(db: Session, token: str, new_password: str) -> None:
    """
    Confirm password reset using a valid JWT token.

    Args:
        token: JWT reset token from email link.
        new_password: The user's new plaintext password.
    """
    try:
        p = _decode(token)
        if p.get("typ") != "reset":
            raise ValueError
        uid = int(p["sub"])
    except Exception:
        raise ValueError("Invalid or expired token")

    u = db.query(User).get(uid)
    if not u:
        raise ValueError("User not found")

    # Update and save the new password
    u.password = _pwd.hash(new_password)
    db.commit()