from pydantic import BaseModel
from typing import Optional

class PostChangeProfileInfoRequest(BaseModel):
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    activityLevel: Optional[str] = None
    goal: Optional[str] = None
    isVegan: Optional[bool] = None
    isVegetarian: Optional[bool] = None
    isDairyInt: Optional[bool] = None
    resetDailyNutrition: Optional[bool] = False
