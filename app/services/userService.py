from sqlalchemy.orm import Session
from sqlalchemy import or_
from passlib.context import CryptContext
from app.models.users import User
from app.schemas.requests.getLoginRequest import LoginIn

import os, time, jwt

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
_JWT_SECRET = os.getenv("JWT_SECRET")
_JWT_ALG = "HS256"
_TTL = 60 * 60 * 24

def _verify_password(raw: str, hashed: str) -> bool:
    return _pwd.verify(raw, hashed)

def _create_access_token(sub: str, extra: dict | None = None, ttl: int = _TTL) -> str:
    now = int(time.time())
    payload = {"sub": sub, "iat": now, "exp": now + ttl, "typ": "access"}

    if extra:
        payload.update(extra)

    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALG)

def login_user(db: Session, body: LoginIn) -> tuple[str, str]:
    """Return (jwt, username) or raise ValueError for invalid creds."""
    u: User | None = (
        db.query(User)
        .filter(or_(User.username == body.login, User.email == body.login))
        .first()
    )

    if not u or not _verify_password(body.password, u.password):
        raise ValueError("Invalid credentials")

    token = _create_access_token(sub=str(u.uuid), extra={"username": u.username})

    return token, u.username
