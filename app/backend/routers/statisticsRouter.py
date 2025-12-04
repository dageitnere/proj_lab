from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.backend.database import get_db
from fastapi.responses import HTMLResponse
from app.backend.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.backend.schemas.requests.getUserStatisticsByDateRequest import GetUserStatisticsByDateRequest
from app.backend.services.statisticsService import get_daily_statistics, get_average_last_7_days, get_average_last_30_days, get_average_by_date
from app.backend.schemas.responses.userStatisticsResponse import UserStatisticsResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/frontend/templates")

statistics = APIRouter()

@statistics.get("/form",response_class=HTMLResponse)
def showStatisticsPage(request: Request):
    return templates.TemplateResponse("statistics.html", {"request": request})

@statistics.get("/daily", response_model=UserStatisticsResponse)
def getDailyStatistics(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_daily_statistics(db, userUuid)

@statistics.get("/average/7days", response_model=UserStatisticsResponse)
def getAverageLast7Days(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_average_last_7_days(db, userUuid)

@statistics.get("/average/30days", response_model=UserStatisticsResponse)
def getAverageLast30Days(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_average_last_30_days(db, userUuid)

@statistics.post("/averageByDate", response_model=UserStatisticsResponse)
def getAverageByDate(request: GetUserStatisticsByDateRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_average_by_date(db, request, userUuid)
