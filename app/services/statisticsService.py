from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.userConsumedProducts import UserConsumedProduct
from fastapi import HTTPException, status
from sqlalchemy import and_
from typing import List
from app.schemas.responses.userStatisticsResponse import UserStatisticsResponse
from app.schemas.requests.getUserStatisticsByDateRequest import GetUserStatisticsByDateRequest

def _sum_consumed(products: List[UserConsumedProduct]) -> dict:
    """Helper: sum all numeric fields for a list of products"""
    sums = {
        "averageKcal": 0.0,
        "averageFat": 0.0,
        "averageSatFat": 0.0,
        "averageCarbs": 0.0,
        "averageSugar": 0.0,
        "averageProtein": 0.0,
        "averageDairyProtein": 0.0,
        "averageAnimalProtein": 0.0,
        "averagePlantProtein": 0.0,
        "averageSalt": 0.0,
        "averageCost": 0.0,
        "averageProducts": len(products)
    }
    for p in products:
        sums["averageKcal"] += p.kcal
        sums["averageFat"] += p.fat
        sums["averageSatFat"] += p.satFat
        sums["averageCarbs"] += p.carbs
        sums["averageSugar"] += p.sugar
        sums["averageProtein"] += p.protein
        sums["averageDairyProtein"] += p.dairyProtein
        sums["averageAnimalProtein"] += p.animalProtein
        sums["averagePlantProtein"] += p.plantProtein
        sums["averageSalt"] += p.salt
        sums["averageCost"] += p.cost
    return sums


def get_daily_statistics(db: Session, userUuid: int) -> UserStatisticsResponse:
    today = datetime.now().date()
    products = db.query(UserConsumedProduct).filter(
        and_(
            UserConsumedProduct.userUuid == userUuid,
            UserConsumedProduct.date >= datetime.combine(today, datetime.min.time()),
            UserConsumedProduct.date <= datetime.combine(today, datetime.max.time())
        )
    ).all()

    if not products:
        # Return zeros instead of raising exception
        averages = {
            "averageKcal": 0.0,
            "averageFat": 0.0,
            "averageSatFat": 0.0,
            "averageCarbs": 0.0,
            "averageSugar": 0.0,
            "averageProtein": 0.0,
            "averageDairyProtein": 0.0,
            "averageAnimalProtein": 0.0,
            "averagePlantProtein": 0.0,
            "averageSalt": 0.0,
            "averageCost": 0.0,
            "averageProducts": 0
        }
        averages["period"] = "Today"
        return UserStatisticsResponse(**averages)

    averages = _sum_consumed(products)
    averages["period"] = "Today"
    return UserStatisticsResponse(**averages)


def get_average_last_7_days(db: Session, userUuid: int) -> UserStatisticsResponse:
    start_date = datetime.now() - timedelta(days=7)
    products = db.query(UserConsumedProduct).filter(
        and_(
            UserConsumedProduct.userUuid == userUuid,
            UserConsumedProduct.date >= start_date
        )
    ).all()

    if not products:
        # Return zeros instead of raising exception
        averages = {
            "averageKcal": 0.0,
            "averageFat": 0.0,
            "averageSatFat": 0.0,
            "averageCarbs": 0.0,
            "averageSugar": 0.0,
            "averageProtein": 0.0,
            "averageDairyProtein": 0.0,
            "averageAnimalProtein": 0.0,
            "averagePlantProtein": 0.0,
            "averageSalt": 0.0,
            "averageCost": 0.0,
            "averageProducts": 0
        }
        averages["period"] = "Last 7 days"
        return UserStatisticsResponse(**averages)

    sums = _sum_consumed(products)
    # divide all by 7 for daily averages
    averages = {k: round((v / 7), 2) for k, v in sums.items()}
    averages["period"] = "Last 7 days"
    return UserStatisticsResponse(**averages)


def get_average_last_30_days(db: Session, userUuid: int) -> UserStatisticsResponse:
    start_date = datetime.now() - timedelta(days=30)
    products = db.query(UserConsumedProduct).filter(
        and_(
            UserConsumedProduct.userUuid == userUuid,
            UserConsumedProduct.date >= start_date
        )
    ).all()

    if not products:
        # Return zeros instead of raising exception
        averages = {
            "averageKcal": 0.0,
            "averageFat": 0.0,
            "averageSatFat": 0.0,
            "averageCarbs": 0.0,
            "averageSugar": 0.0,
            "averageProtein": 0.0,
            "averageDairyProtein": 0.0,
            "averageAnimalProtein": 0.0,
            "averagePlantProtein": 0.0,
            "averageSalt": 0.0,
            "averageCost": 0.0,
            "averageProducts": 0
        }
        averages["period"] = "Last 30 days"
        return UserStatisticsResponse(**averages)

    sums = _sum_consumed(products)
    # divide all by 30 for daily averages
    averages = {k: round((v / 30), 2) for k, v in sums.items()}
    averages["period"] = "Last 30 days"
    return UserStatisticsResponse(**averages)


def get_average_by_date(db: Session, request: GetUserStatisticsByDateRequest, userUuid: int) -> UserStatisticsResponse:

    # Validate range
    if request.startDate > request.endDate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be after end date."
        )

    end_of_day = datetime.combine(request.endDate.date(), datetime.max.time())

    # Fetch all products consumed in that range
    products = db.query(UserConsumedProduct).filter(
        and_(
            UserConsumedProduct.userUuid == userUuid,
            UserConsumedProduct.date >= datetime.combine(request.startDate.date(), datetime.min.time()),
            UserConsumedProduct.date <= end_of_day
        )
    ).all()

    if not products:
        # Return zeros instead of raising exception
        averages = {
            "averageKcal": 0.0,
            "averageFat": 0.0,
            "averageSatFat": 0.0,
            "averageCarbs": 0.0,
            "averageSugar": 0.0,
            "averageProtein": 0.0,
            "averageDairyProtein": 0.0,
            "averageAnimalProtein": 0.0,
            "averagePlantProtein": 0.0,
            "averageSalt": 0.0,
            "averageCost": 0.0,
            "averageProducts": 0
        }
        averages["period"] = f"{request.startDate.date()} - {request.endDate.date()}"
        return UserStatisticsResponse(**averages)

    # Calculate sums and averages
    sums = _sum_consumed(products)
    days_count = (request.endDate.date() - request.startDate.date()).days + 1
    averages = {k: (v / days_count) if isinstance(v, (int, float)) else v for k, v in sums.items()}
    averages["period"] = f"{request.startDate.date()} - {request.endDate.date()}"

    return UserStatisticsResponse(**averages)