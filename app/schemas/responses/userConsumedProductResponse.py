from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserConsumedProductResponse(BaseModel):
    productName: str
    amount: float
    kcal: float
    fat: float
    satFat: float
    carbs: float
    sugar: float
    protein: float
    dairyProtein: float
    animalProtein: float
    plantProtein: float
    salt: float
    cost: float
    createdAt: datetime

UserConsumedProductListResponse = List[UserConsumedProductResponse]