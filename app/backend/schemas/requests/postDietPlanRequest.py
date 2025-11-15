from pydantic import BaseModel
from typing import List, Dict, Any
from app.backend.schemas.responses.generateMenuResponse import ProductItem

class PostDietPlanRequest(BaseModel):
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
    plan: List[ProductItem]
    vegan: bool
    vegetarian: bool
    dairyFree: bool
    restrictions: List[Dict[str, Any]]