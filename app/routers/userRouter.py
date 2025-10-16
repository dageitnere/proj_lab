from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.requests.getLoginRequest import LoginInRequest
from app.schemas.responses.loginResponse import LoginOut
from app.services.userService import login_user
from app.schemas.requests.getRegisterRequest import RegisterInRequest
from app.schemas.responses.registerResponse import RegisterOut
from app.services.userService import register_user

router = APIRouter(tags=["auth"])
tpl = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return tpl.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_model=LoginOut)
def login(body: LoginInRequest, db: Session = Depends(get_db)):
    try:
        token, username = login_user(db, body)
        return JSONResponse({"access_token": token, "token_type": "bearer", "username": username})
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return tpl.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_model=RegisterOut)
def register(body: RegisterInRequest, db: Session = Depends(get_db)):
    try:
        uuid, username = register_user(db, body)
        return JSONResponse({"ok": True, "uuid": uuid, "username": username})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))