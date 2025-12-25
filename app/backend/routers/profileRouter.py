from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.backend.database import get_db
from app.backend.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.backend.schemas.requests.postChangeDailyNutritionRequest import PostChangeDailyNutritionRequest
from app.backend.schemas.requests.postChangeProfileInfoRequest import PostChangeProfileInfoRequest
from app.backend.schemas.requests.postRegisterRequest import CompleteRegistrationRequest
from app.backend.services.profileService import get_user_profile_data, complete_info_submit, change_profile_info, \
    change_daily_nutrition, calculate_daily_nutrition, calculated_nutrition_info

profile = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")

@profile.get("/", response_class=HTMLResponse)
def profilePage(request: Request, userUuid: int = Depends(get_uuid_from_token),  db: Session = Depends(get_db)):
    accountInfo = get_user_profile_data(db, userUuid)
    return templates.TemplateResponse("profile.html", {"request": request, "accountInfo": accountInfo})

# Returns user profile data as JSON for the React frontend
@profile.get("/getProfileInfo")
def getProfileInfo(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_user_profile_data(db, userUuid)

@profile.get("/complete", response_class=HTMLResponse)
def completeForm(request: Request):
    return templates.TemplateResponse("finishRegistration.html", {"request": request})

@profile.post("/completeInfo")
def completeInfoSubmit(completeRequest: CompleteRegistrationRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return complete_info_submit(db, completeRequest, userUuid)

@profile.post("/changeInfo")
def changeProfileInfo(request: PostChangeProfileInfoRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return change_profile_info(db, request, userUuid)

@profile.post("/changeDailyNutrition")
def changeDailyNutrition(request: PostChangeDailyNutritionRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return change_daily_nutrition(db, request, userUuid)

@profile.post("/calculateDailyNutrition")
def calculateDailyNutrition(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return calculate_daily_nutrition(db, userUuid)

@profile.get("/getCalculatedNutritionInfo")
def calculatedNutritionInfo(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return calculated_nutrition_info(db, userUuid)