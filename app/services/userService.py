from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy import func
from passlib.context import CryptContext
from app.models.users import User
from app.schemas.requests.getLoginRequest import LoginInRequest
from app.schemas.requests.postRegisterRequest import RegisterRequest
from app.services.verificationService import start_verification

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

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALG])

def login_user(db: Session, request: LoginInRequest) -> tuple[str, str]:
    key = request.login.strip()
    email_key = key.lower()

    u: User | None = (
        db.query(User)
        .filter(
            or_(
                User.username == key,                 # username exact
                func.lower(User.email) == email_key   # email case-insensitive
            )
        )
        .first()
    )

    if not u or not _verify_password(request.password, u.password):
        raise ValueError("Invalid credentials")
    if not u.emailVerified:
        raise ValueError("Email not verified")

    token = _create_access_token(sub=str(u.uuid), extra={"username": u.username})
    return token, u.username


def _hash(raw: str) -> str:
    return _pwd.hash(raw)

def register_user(db: Session, request: RegisterRequest) -> tuple[int, str]:
    # unique check
    exists = db.query(User).filter(or_(User.username == request.username,
                                       User.email == request.email)).first()
    if exists:
        raise ValueError("User with this username or email already exists")

    email = str(request.email).lower().strip()

    u = User(
        username=request.username.strip(),
        email=email,
        password=_hash(request.password),

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

    start_verification(db, u.email)

    return u.uuid, u.username
