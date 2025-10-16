from sqlalchemy.orm import Session
from sqlalchemy import or_
from passlib.context import CryptContext
from app.models.users import User
from app.schemas.requests.getLoginRequest import LoginInRequest
from app.schemas.requests.getRegisterRequest import RegisterInRequest

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

def login_user(db: Session, body: LoginInRequest) -> tuple[str, str]:
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

def _hash(raw: str) -> str:
    return _pwd.hash(raw)

def register_user(db: Session, body: RegisterInRequest) -> tuple[int, str]:
    # unique check
    exists = db.query(User).filter(or_(User.username == body.username,
                                       User.email == body.email)).first()
    if exists:
        raise ValueError("User with this username or email already exists")

    email = str(body.email).lower().strip()

    u = User(
        username=body.username.strip(),
        email=email,
        password=_hash(body.password),

        # todo - likt lietotajam kkur so info ievadit
        age=0,
        gender="UNSET",
        weight=0,
        height=0,
        bmi=0.0,
        bmr=0.0,
        activityFactor="UNSET",
        isVegan=False,
        isDairyInt=False,
        isVegetarian=False,
    )

    db.add(u)
    db.commit()
    db.refresh(u)
    return u.uuid, u.username
