from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.requests.getLoginRequest import LoginIn
from app.schemas.responses.loginResponse import LoginOut
from app.services.userService import login_user

router = APIRouter(tags=["auth"])
tpl = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return tpl.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_model=LoginOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    try:
        token, username = login_user(db, body)
        return JSONResponse({"access_token": token, "token_type": "bearer", "username": username})
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
