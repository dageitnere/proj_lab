from pydantic import BaseModel
from typing import Optional

class AddUserProductRequest(BaseModel):
    userUuid: int
    productName: str
    kcal: int
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
    vegan: float
    vegetarian: float
    dairyFree: float