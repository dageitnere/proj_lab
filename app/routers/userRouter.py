from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Literal

from app.database import get_db
from app.schemas.requests.getLoginRequest import LoginInRequest
from app.schemas.responses.loginResponse import LoginOut
from app.services.userService import login_user
from app.schemas.requests.postRegisterRequest import RegisterRequest
from app.schemas.responses.registerResponse import RegisterResponse
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