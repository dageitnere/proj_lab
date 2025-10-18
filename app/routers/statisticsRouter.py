# app/routers/userStatisticsRouter.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.schemas.requests.getUserStatisticsByDateRequest import GetUserStatisticsByDateRequest
from app.services.statisticsService import get_daily_statistics, get_average_last_7_days, get_average_last_30_days, \
    get_average_by_date
from app.schemas.responses.userStatisticsResponse import UserStatisticsResponse

statistics = APIRouter()

@statistics.get("/daily", response_model=UserStatisticsResponse)
def getDailyStatistics(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_daily_statistics(db, userUuid)


@statistics.get("/average/7days", response_model=UserStatisticsResponse)
def getAverageLast7Days(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_average_last_7_days(db, userUuid)


@statistics.get("/average/30days", response_model=UserStatisticsResponse)
def getAverageLast30Days(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_average_last_30_days(db, userUuid)

@statistics.get("/averageByDate")
def getAverageByDate(request: GetUserStatisticsByDateRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_average_by_date(db, request, userUuid)
