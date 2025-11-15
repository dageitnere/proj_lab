import os, re, time, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.backend.services.emailService import send_email
from app.backend.models.users import User

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
_PASS_RX = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$")

def require_strong_password(pw: str) -> None:
    if not _PASS_RX.match(pw or ""):
        raise ValueError("Password must be ≥8 chars and include 1 uppercase letter, 1 number, and 1 special symbol")

def hash_password(raw: str) -> str:
    return _pwd.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    return _pwd.verify(raw, hashed)

_JWT_SECRET = os.getenv("JWT_SECRET")
_ALG = "HS256"
_TTL = 60 * 30

def _create_reset_token(sub: str, ttl: int = _TTL) -> str:
    now = int(time.time())
    return jwt.encode({"sub": sub, "typ": "reset", "iat": now, "exp": now + ttl}, _JWT_SECRET, algorithm=_ALG)

def _decode(tok: str) -> dict:
    return jwt.decode(tok, _JWT_SECRET, algorithms=[_ALG])

def start_reset(db: Session, email: str) -> None:
    u = db.query(User).filter(User.email == email.lower().strip()).first()

    if not u:
        return

    tok = _create_reset_token(str(u.uuid))
    reset_url = f"http://localhost:8000/auth/reset-password?token={tok}"
    send_email(to=str(u.email), subject="Password reset", body=f"Open this link to set a new password (valid 30 min): {reset_url}")

def confirm_reset(db: Session, token: str, new_password: str) -> None:
    try:
        p = _decode(token)

        if p.get("typ") != "reset":
            raise ValueError

        uid = int(p["sub"])
    except Exception:
        raise ValueError("Invalid or expired token")

    require_strong_password(new_password)
    u = db.query(User).get(uid)

    if not u:
        raise ValueError("User not found")

    u.password = hash_password(new_password)
    db.commit()