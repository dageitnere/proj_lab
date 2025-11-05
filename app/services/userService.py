from __future__ import annotations
from typing import Literal

import os
import time
import jwt

from fastapi import HTTPException, Request
from fastapi.responses import Response, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.users import User
from app.schemas.requests.getLoginRequest import LoginInRequest
from app.schemas.requests.postRegisterRequest import RegisterRequest, VerifyRequest, VerifyCodeRequest, CompleteRegistrationRequest
from app.schemas.requests.postForgetRequest import ForgotRequest, ForgotConfirmRequest
from app.services.passwordService import verify_password, hash_password, require_strong_password, start_reset, confirm_reset
from app.services.profileService import complete_registration
from app.services.verificationService import start_verification, confirm_verification

_JWT_SECRET = os.getenv("JWT_SECRET")
_JWT_ALG = "HS256"
_TTL = 60 * 60 * 24

def _create_access_token(sub: str, extra: dict | None = None, ttl: int = _TTL) -> str:
    now = int(time.time())
    payload = {"sub": sub, "iat": now, "exp": now + ttl, "typ": "access"}

    if extra:
        payload.update(extra)

    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALG)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALG])

def create_session_token_for_user(u: User) -> str:
    return _create_access_token(sub=str(u.uuid), extra={"username": u.username, "email": u.email},)

def extract_user_uuid_from_request(request: Request) -> int:
    tok = request.cookies.get("access_token")

    if not tok:
        raise ValueError("Missing token")

    payload = decode_access_token(tok)

    if payload.get("typ") != "access":
        raise ValueError("Invalid token type")

    return int(payload["sub"])

_COOKIE = "access_token"
_SECURE = True
_SAMESITE: Literal["lax", "strict", "none"] = "lax"
_COOKIE_MAX_AGE = 60 * 60 * 24

def build_auth_response(username: str, token: str) -> JSONResponse:
    resp = JSONResponse({"ok": True, "username": username})
    resp.set_cookie(key=_COOKIE, value=token, httponly=True, secure=_SECURE, samesite=_SAMESITE, max_age=_COOKIE_MAX_AGE, path="/",)
    return resp

def build_auth_redirect(location: str, token: str, status_code: int = 303) -> RedirectResponse:
    resp = RedirectResponse(location, status_code=status_code)
    resp.set_cookie(key=_COOKIE, value=token, httponly=True, secure=_SECURE, samesite=_SAMESITE, max_age=_COOKIE_MAX_AGE, path="/",)
    return resp

def build_logout_response() -> JSONResponse:
    resp = JSONResponse({"ok": True, "message": "logged out"})
    resp.delete_cookie(_COOKIE, path="/")

    return resp

def ok() -> JSONResponse:
    return JSONResponse({"ok": True})

def login_user(db: Session, request: LoginInRequest) -> tuple[str, str]:
    key = request.login.strip()
    email_key = key.lower()
    u: User | None = (db.query(User).filter(or_(User.username == key, func.lower(User.email) == email_key)).first() )

    if not u or not verify_password(request.password, u.password):
        raise ValueError("Invalid credentials")
    if not u.emailVerified:
        raise ValueError("Email not verified")

    token = create_session_token_for_user(u)
    return token, u.username

def register_user(db: Session, request: RegisterRequest) -> tuple[int, str]:
    exists = (db.query(User).filter(or_(User.username == request.username, User.email == request.email)).first())

    if exists:
        raise ValueError("User with this username or email already exists")

    require_strong_password(request.password)
    email = str(request.email).lower().strip()
    u = User(username=request.username.strip(), email=email, password=hash_password(request.password), age=0, gender="UNSET", weight=0, height=0, bmi=0.0, bmr=0.0, activityFactor="UNSET", isVegan=False, isDairyInt=False, isVegetarian=False, goal="MAINTAIN")
    db.add(u)
    db.commit()
    db.refresh(u)
    start_verification(db, u.email)

    return u.uuid, u.username


# -------- Action wrappers (handle errors + build responses) --------
def action_login(db: Session, body: LoginInRequest) -> Response:
    try:
        token, username = login_user(db, body)
        return build_auth_response(username, token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

def action_register(db: Session, body: RegisterRequest) -> Response:
    try:
        register_user(db, body)
        return ok()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def action_logout() -> Response:
    return build_logout_response()

def action_verification_start(db: Session, body: VerifyRequest) -> Response:
    start_verification(db, str(body.email))  # silent for privacy
    return ok()

def action_verification_confirm(db: Session, body: VerifyCodeRequest) -> Response:
    try:
        u = confirm_verification(db, str(body.email), body.code)
        tok = create_session_token_for_user(u)
        return build_auth_redirect("/auth/complete", tok, status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def action_forgot_start(db: Session, body: ForgotRequest) -> Response:
    start_reset(db, str(body.email))  # silent semantics
    return ok()

def action_reset_confirm(db: Session, body: ForgotConfirmRequest) -> Response:
    try:
        confirm_reset(db, body.token, body.new_password)
        return ok()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def action_complete_submit(db: Session, request: Request, body: CompleteRegistrationRequest) -> Response:
    try:
        sub = extract_user_uuid_from_request(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    try:
        complete_registration(db, sub, body)
        return ok()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))