from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.backend.database import get_db
from app.backend.schemas.requests.getLoginRequest import LoginInRequest
from app.backend.schemas.requests.postRegisterRequest import RegisterRequest, VerifyRequest, VerifyCodeRequest
from app.backend.schemas.requests.postForgetRequest import ForgotRequest, ForgotConfirmRequest
from app.backend.services.userService import verification_start, verification_confirm, forgot_start, reset_confirm, login_user, register_user, logout_user

user = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/frontend/templates")

@user.get("/login", response_class=HTMLResponse)
def loginForm(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@user.get("/register", response_class=HTMLResponse)
def registerForm(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@user.get("/verify", response_class=HTMLResponse)
def verifyForm(request: Request):
    return templates.TemplateResponse("verify.html", {"request": request})

@user.get("/forgot-password", response_class=HTMLResponse)
def forgotForm(request: Request):
    return templates.TemplateResponse("forgotPassword.html", {"request": request})

@user.get("/reset-password", response_class=HTMLResponse)
def resetForm(request: Request):
    return templates.TemplateResponse("resetPassword.html", {"request": request})

# ----- Actions (delegate fully to services) -----
@user.post("/login")
def loginUser(request: LoginInRequest, db: Session = Depends(get_db)):
    return login_user(db, request)

@user.post("/register")
def registerUser(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(db, request)

@user.post("/logout")
def logoutUser():
    return logout_user()

@user.post("/verification/start")
def verificationStart(request: VerifyRequest, db: Session = Depends(get_db)):
    return verification_start(db, request)

@user.post("/verification/confirm")
def verificationConfirm(request: VerifyCodeRequest, db: Session = Depends(get_db)):
    return verification_confirm(db, request)

@user.post("/forgot-password/start")
def forgotStart(request: ForgotRequest, db: Session = Depends(get_db)):
    return forgot_start(db, request)

@user.post("/reset-password/confirm")
def resetConfirm(request: ForgotConfirmRequest, db: Session = Depends(get_db)):
    return reset_confirm(db, request)
