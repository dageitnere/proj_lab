from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.backend.database import get_db
from app.backend.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.backend.schemas.requests.postRegisterRequest import CompleteRegistrationRequest
from app.backend.services.profileService import get_user_profile_data, complete_info_submit

profile = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")

@profile.get("/", response_class=HTMLResponse)
def profilePage(request: Request, userUuid: int = Depends(get_uuid_from_token),  db: Session = Depends(get_db)):
    accountInfo = get_user_profile_data(db, userUuid)
    return templates.TemplateResponse("profile.html", {"request": request, "accountInfo": accountInfo})

@profile.get("/complete", response_class=HTMLResponse)
def completeForm(request: Request):
    return templates.TemplateResponse("finishRegistration.html", {"request": request})

@profile.post("/completeInfo")
def completeInfoSubmit(completeRequest: CompleteRegistrationRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return complete_info_submit(db, completeRequest, userUuid)

# profile.post("/changeInfo")
# def changeProfileInfo(request: ChangeProfileInfoRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
#     return change_profile_info(db, request, userUuid)