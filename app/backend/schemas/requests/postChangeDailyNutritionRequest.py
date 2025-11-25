from pydantic import BaseModel
from typing import Optional

class PostChangeDailyNutritionRequest(BaseModel):
    calculatedKcal: Optional[float] = None
    calculatedCarbs: Optional[float] = None
    calculatedProtein: Optional[float] = None
    calculatedFat: Optional[float] = None
    calculatedSatFat: Optional[float] = None
    calculatedSugar: Optional[float] = None
    calculatedSalt: Optional[float] = None
