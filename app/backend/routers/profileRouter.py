from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.backend.database import get_db
from app.backend.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.backend.services.profileService import get_user_profile_data

profile = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")

@profile.get("/", response_class=HTMLResponse)
def profile_page(request: Request, userUuid: int = Depends(get_uuid_from_token),  db: Session = Depends(get_db)):
    accountInfo = get_user_profile_data(db, userUuid)
    return templates.TemplateResponse("profile.html", {"request": request, "accountInfo": accountInfo})