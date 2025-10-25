from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Literal
from fastapi.responses import RedirectResponse
from app.database import get_db
from app.schemas.responses.loginResponse import LoginOut
from app.schemas.responses.registerResponse import VerifyResponse
from app.schemas.responses.registerResponse import RegisterResponse
from app.schemas.requests.postRegisterRequest import VerifyRequest, VerifyCodeRequest, CompleteRegistrationRequest
from app.schemas.requests.postRegisterRequest import RegisterRequest
from app.schemas.requests.getLoginRequest import LoginInRequest
from app.schemas.requests.postForgetRequest import ForgotRequest, ForgotConfirmRequest
from app.services.passwordService import start_reset, confirm_reset
from app.services.profileService import complete_registration
from app.services.userService import login_user, decode_access_token
from app.services.verificationService import start_verification, confirm_verification
from app.services.userService import register_user

user = APIRouter(tags=["auth"])
tpl = Jinja2Templates(directory="app/templates")
COOKIE = "access_token"
SECURE = False   # todo true kad pabeigts
SAMESITE: Literal["lax", "strict", "none"] = "lax"

@user.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return tpl.TemplateResponse("login.html", {"request": request})

@user.post("/login", response_model=LoginOut)
def login(request: LoginInRequest, db: Session = Depends(get_db)):
    try:
        token, username = login_user(db, request)
        resp = JSONResponse({"ok": True, "username": username})
        resp.set_cookie(
            key=COOKIE, value=token, httponly=True, secure=SECURE,
            samesite=SAMESITE, max_age=60 * 60 * 24, path="/"
        )
        return resp
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@user.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return tpl.TemplateResponse("register.html", {"request": request})

@user.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        uuid, username = register_user(db, request)
        return JSONResponse({"ok": True, "uuid": uuid, "username": username})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user.post("/logout")
def logout():
    resp = JSONResponse({"ok": True, "message": "logged out"})
    resp.delete_cookie(COOKIE, path="/")
    return resp

@user.get("/verify", response_class=HTMLResponse)
def verify_page(request: Request):
    if request.cookies.get("access_token"):
        return RedirectResponse("/mainPage")
    return tpl.TemplateResponse("verify.html", {"request": request})

@user.post("/verification/start", response_model=VerifyResponse)
def verification_start(request: VerifyRequest, db: Session = Depends(get_db)):
    start_verification(db, str(request.email))
    return JSONResponse({"ok": True})

@user.post("/verification/confirm", response_model=VerifyResponse)
def verification_confirm(request: VerifyCodeRequest, db: Session = Depends(get_db)):
    try:
        confirm_verification(db, str(request.email), request.code)
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user.get("/forgot-password", response_class=HTMLResponse)
def forgot_page(request: Request):
    if request.cookies.get("access_token"):
        return RedirectResponse("/mainPage")
    return tpl.TemplateResponse("forgotPassword.html", {"request": request})

@user.post("/forgot-password/start", response_model=VerifyResponse)
def forgot_start(request: ForgotRequest, db: Session = Depends(get_db)):
    start_reset(db, str(request.email))
    return JSONResponse({"ok": True})

@user.get("/reset-password", response_class=HTMLResponse)
def reset_page(request: Request):
    if request.cookies.get("access_token"):
        return RedirectResponse("/mainPage")
    return tpl.TemplateResponse("resetPassword.html", {"request": request})

@user.post("/reset-password/confirm", response_model=VerifyResponse)
def reset_confirm(request: ForgotConfirmRequest, db: Session = Depends(get_db)):
    try:
        confirm_reset(db, request.token, request.new_password)
        return JSONResponse({"ok": True})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user.get("/complete", response_class=HTMLResponse)
def complete_page(request: Request):
    tok = request.cookies.get("access_token")
    if not tok:
        return RedirectResponse("/auth/login")
    return tpl.TemplateResponse("finishRegistration.html", {"request": request})

@user.post("/complete")
def complete_submit(body: CompleteRegistrationRequest, request: Request, db: Session = Depends(get_db)):
    tok = request.cookies.get("access_token")
    if not tok:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        sub = int(decode_access_token(tok)["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        complete_registration(db, sub, body)
        return JSONResponse({"ok": True})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))