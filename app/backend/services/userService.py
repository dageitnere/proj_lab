import time
import jwt
import os
import datetime as dt
from typing import Literal
from fastapi import HTTPException
from fastapi.responses import Response, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.backend.dependencies.sendEmail import send_email, gen_code
from app.backend.models.users import User
from app.backend.schemas.requests.getLoginRequest import LoginInRequest
from app.backend.schemas.requests.postRegisterRequest import RegisterRequest, VerifyRequest, VerifyCodeRequest
from app.backend.schemas.requests.postForgetRequest import ForgotRequest, ForgotConfirmRequest
from app.backend.services.passwordService import verify_password, hash_password, require_strong_password, start_reset, confirm_reset

_JWT_SECRET = os.getenv("JWT_SECRET")
_JWT_ALG = "HS256"
_TTL = 60 * 60 * 24
_COOKIE = "access_token"
_SECURE = True
_SAMESITE: Literal["lax", "strict", "none"] = "lax"
_COOKIE_MAX_AGE = 60 * 60 * 24

def _create_access_token(sub: str, extra: dict | None = None, ttl: int = _TTL) -> str:
    now = int(time.time())
    payload = {"sub": sub, "iat": now, "exp": now + ttl, "typ": "access"}

    if extra:
        payload.update(extra)

    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALG)

def _now_utc():
    """Return current UTC datetime."""
    return dt.datetime.now(dt.timezone.utc)

def _create_session_token_for_user(u: User) -> str:
    return _create_access_token(sub=str(u.uuid), extra={"username": u.username, "email": u.email},)

def _build_auth_response(username: str, token: str) -> JSONResponse:
    resp = JSONResponse({"ok": True, "username": username})
    resp.set_cookie(key=_COOKIE, value=token, httponly=True, secure=_SECURE, samesite=_SAMESITE, max_age=_COOKIE_MAX_AGE, path="/",)
    return resp

def _build_auth_redirect(location: str, token: str, status_code: int = 303) -> RedirectResponse:
    resp = RedirectResponse(location, status_code=status_code)
    resp.set_cookie(key=_COOKIE, value=token, httponly=True, secure=_SECURE, samesite=_SAMESITE, max_age=_COOKIE_MAX_AGE, path="/",)
    return resp

def _build_logout_response() -> JSONResponse:
    resp = JSONResponse({"ok": True, "message": "logged out"})
    resp.delete_cookie(_COOKIE, path="/")

    return resp

def _ok() -> JSONResponse:
    return JSONResponse({"ok": True})

def _login_user(db: Session, request: LoginInRequest) -> tuple[str, str]:
    key = request.login.strip()
    email_key = key.lower()
    u: User | None = (db.query(User).filter(or_(User.username == key, func.lower(User.email) == email_key)).first() )

    if not u or not verify_password(request.password, u.password):
        raise ValueError("Invalid credentials")
    if not u.emailVerified:
        raise ValueError("Email not verified")

    token = _create_session_token_for_user(u)
    return token, u.username

def _register_user(db: Session, request: RegisterRequest) -> None:
    exists = (db.query(User).filter(or_(User.username == request.username, User.email == request.email)).first())

    if exists:
        raise ValueError("User with this username or email already exists")

    require_strong_password(request.password)
    email = str(request.email).lower().strip()
    u = User(username=request.username.strip(), email=email, password=hash_password(request.password), age=0, gender="UNSET", weight=0, height=0, bmi=0.0, bmr=0.0, activityFactor="UNSET", isVegan=False, isDairyInt=False, isVegetarian=False, goal="MAINTAIN")
    db.add(u)
    db.commit()
    db.refresh(u)
    _start_verification(db, u.email)

def _start_verification(db: Session, email: str) -> None:
    """
        Generate and send a verification code to the user's email.
        Code expires in 30 minutes.
    """
    u = db.query(User).filter(User.email == email.lower().strip()).first()

    if not u:
        return

    code = gen_code()
    u.verificationCode = code
    u.verificationExpiresAt = _now_utc() + dt.timedelta(minutes=30)
    db.commit()
    send_email(
        to=str(u.email),
        subject="Your Diet App verification code",
        body=f"Your verification code is: {code}\nIt expires in 30 minutes."
    )

def _confirm_verification(db: Session, email: str, code: int) -> User:
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

# -------- Action wrappers (handle errors + build responses) --------
def login_user(db: Session, request: LoginInRequest) -> Response:
    try:
        token, username = _login_user(db, request)
        return _build_auth_response(username, token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

def register_user(db: Session, request: RegisterRequest) -> Response:
    try:
        _register_user(db, request)
        return _ok()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def logout_user() -> Response:
    return _build_logout_response()

def verification_start(db: Session, request: VerifyRequest) -> Response:
    _start_verification(db, str(request.email))  # silent for privacy
    return _ok()

def verification_confirm(db: Session, request: VerifyCodeRequest) -> Response:
    try:
        u = _confirm_verification(db, str(request.email), request.code)
        tok = _create_session_token_for_user(u)
        return _build_auth_redirect("/profile/complete", tok, status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def forgot_start(db: Session, request: ForgotRequest) -> Response:
    start_reset(db, str(request.email))  # silent semantics
    return _ok()

def reset_confirm(db: Session, request: ForgotConfirmRequest) -> Response:
    try:
        confirm_reset(db, request.token, request.new_password)
        return _ok()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
