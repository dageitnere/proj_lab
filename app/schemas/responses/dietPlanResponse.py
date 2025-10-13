from pydantic import BaseModel
from typing import List
from app.schemas.responses.generateMenuResponse import ProductItem
from datetime import datetime

class DietPlanResponse(BaseModel):
    id: str
    userUuid: str
    name: str
    totalKcal: float
    totalCost: float
    totalFat: float
    totalCarbs: float
    totalProtein: float
    totalDairyProtein: float
    totalAnimalProtein: float
    totalPlantProtein: float
    totalSugar: float
    totalSatFat: float
    totalSalt: float
    date: datetime
    plan: List[ProductItem]


DietPlanListResponse = List[DietPlanResponse]
