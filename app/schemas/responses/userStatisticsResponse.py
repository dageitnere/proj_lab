from pydantic import BaseModel
from typing import Optional

class UserStatisticsResponse(BaseModel):
    averageKcal: float
    averageFat: float
    averageSatFat: float
    averageCarbs: float
    averageSugar: float
    averageProtein: float
    averageDairyProtein: float
    averageAnimalProtein: float
    averagePlantProtein: float
    averageSalt: float
    averageCost: float
    averageProducts: float
    period: Optional[str] = None
