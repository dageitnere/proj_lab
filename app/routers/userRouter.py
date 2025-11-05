from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.requests.getLoginRequest import LoginInRequest
from app.schemas.requests.postRegisterRequest import RegisterRequest, VerifyRequest, VerifyCodeRequest, CompleteRegistrationRequest
from app.schemas.requests.postForgetRequest import ForgotRequest, ForgotConfirmRequest
from app.services.userService import action_login, action_register, action_logout, action_verification_start, action_verification_confirm, action_forgot_start, action_reset_confirm, action_complete_submit

user = APIRouter(tags=["auth"])
tpl = Jinja2Templates(directory="app/templates")

@user.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return tpl.TemplateResponse("login.html", {"request": request})

@user.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return tpl.TemplateResponse("register.html", {"request": request})

@user.get("/verify", response_class=HTMLResponse)
def verify_page(request: Request):
    return tpl.TemplateResponse("verify.html", {"request": request})

@user.get("/forgot-password", response_class=HTMLResponse)
def forgot_page(request: Request):
    return tpl.TemplateResponse("forgotPassword.html", {"request": request})

@user.get("/reset-password", response_class=HTMLResponse)
def reset_page(request: Request):
    return tpl.TemplateResponse("resetPassword.html", {"request": request})

@user.get("/complete", response_class=HTMLResponse)
def complete_page(request: Request):
    return tpl.TemplateResponse("finishRegistration.html", {"request": request})

# ----- Actions (delegate fully to services) -----
@user.post("/login")
def login(request: LoginInRequest, db: Session = Depends(get_db)):
    return action_login(db, request)

@user.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return action_register(db, request)

@user.post("/logout")
def logout():
    return action_logout()

@user.post("/verification/start")
def verification_start(request: VerifyRequest, db: Session = Depends(get_db)):
    return action_verification_start(db, request)

@user.post("/verification/confirm")
def verification_confirm(request: VerifyCodeRequest, db: Session = Depends(get_db)):
    return action_verification_confirm(db, request)

@user.post("/forgot-password/start")
def forgot_start(request: ForgotRequest, db: Session = Depends(get_db)):
    return action_forgot_start(db, request)

@user.post("/reset-password/confirm")
def reset_confirm(request: ForgotConfirmRequest, db: Session = Depends(get_db)):
    return action_reset_confirm(db, request)

@user.post("/complete")
def complete_submit(completeRequest: CompleteRegistrationRequest, request: Request, db: Session = Depends(get_db)):
    return action_complete_submit(db, request, completeRequest)