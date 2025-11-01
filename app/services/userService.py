from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy import func
from passlib.context import CryptContext
from app.models.users import User
from app.schemas.requests.getLoginRequest import LoginInRequest
from app.schemas.requests.postRegisterRequest import RegisterRequest
from app.services.verificationService import start_verification

import os, re, time, jwt

_PASS_RX = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$")
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
_JWT_SECRET = os.getenv("JWT_SECRET")
_JWT_ALG = "HS256"
_TTL = 60 * 60 * 24 # Expires in 1 day

def _require_strong_password(pw: str) -> None:
    """
        Check if the password matches requirements.
    """
    if not _PASS_RX.match(pw or ""):
        raise ValueError("The password must be at least 8 characters long, contain atleast one special character, one uppercase letter and a number.")

def _verify_password(raw: str, hashed: str) -> bool:
    """
        Compare raw password with hashed password.
    """
    return _pwd.verify(raw, hashed)

def _create_access_token(sub: str, extra: dict | None = None, ttl: int = _TTL) -> str:
    """
        Generate a JWT access token with optional extra payload.
    """
    now = int(time.time())
    payload = {"sub": sub, "iat": now, "exp": now + ttl, "typ": "access"}

    if extra:
        payload.update(extra)

    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALG)

def decode_access_token(token: str) -> dict:
    """
        Decode a JWT token and return its payload.
    """
    return jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALG])

def login_user(db: Session, request: LoginInRequest) -> tuple[str, str]:
    """
        Authenticate a user by username or email.
        Returns JWT token and username if successful.
        Raises ValueError on invalid credentials or unverified email.
    """
    key = request.login.strip()
    email_key = key.lower()

    u: User | None = (
        db.query(User)
        .filter(
            or_(
                User.username == key,
                func.lower(User.email) == email_key
            )
        )
        .first()
    )

    if not u or not _verify_password(request.password, u.password):
        raise ValueError("Invalid credentials")
    if not u.emailVerified:
        raise ValueError("Email not verified")

    token = _create_access_token(sub=str(u.uuid), extra={"username": u.username, "email": u.email})
    return token, u.username


def _hash(raw: str) -> str:
    """
        Hash a raw password using bcrypt.
    """
    return _pwd.hash(raw)

def register_user(db: Session, request: RegisterRequest) -> tuple[int, str]:
    """
        Register a new user in the system.
        Ensures username and email uniqueness.
        Initiates email verification process.
    """
    exists = db.query(User).filter(or_(User.username == request.username,
                                       User.email == request.email)).first()
    if exists:
        raise ValueError("User with this username or email already exists")

    _require_strong_password(request.password)
    email = str(request.email).lower().strip()

    u = User(
        username=request.username.strip(),
        email=email,
        password=_hash(request.password),
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
