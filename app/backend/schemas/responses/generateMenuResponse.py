from pydantic import BaseModel
from typing import List, Optional


class ProductItem(BaseModel):
    productName: str
    grams: float
    kcal: float
    cost: float
    fat: float
    satFat: float
    carbs: float
    protein: float
    dairyProtein: float
    animalProtein: float
    plantProtein: float
    sugars: float
    salt: float


class GenerateMenuResponse(BaseModel):
    status: str
    executionTime: float
    totalKcal: Optional[float] = None
    totalCost: Optional[float] = None
    totalFat: Optional[float] = None
    totalCarbs: Optional[float] = None
    totalProtein: Optional[float] = None
    totalDairyProtein: Optional[float] = None
    totalAnimalProtein: Optional[float] = None
    totalPlantProtein: Optional[float] = None
    totalSugar: Optional[float] = None
    totalSatFat: Optional[float] = None
    totalSalt: Optional[float] = None
    plan: Optional[List[ProductItem]] = None
    message: Optional[str] = None
    invalidProducts: Optional[List[str]] = None
