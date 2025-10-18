from pydantic import BaseModel
from typing import List, Optional

class UserProductBase(BaseModel):
    """Base representation of a user's product entry"""
    id: int
    productName: str
    kcal: float
    fat: float
    satFat: float
    carbs: float
    sugars: float
    protein: float
    dairyProt: float
    animalProt: float
    plantProt: float
    salt: float
    price1kg: float
    price100g: float


UserProductsListResponse = List[UserProductBase]