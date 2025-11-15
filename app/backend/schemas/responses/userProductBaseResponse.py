from pydantic import BaseModel
from typing import List, Optional

class UserProductBase(BaseModel):
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
    URL: Optional[str] = None

UserProductsListResponse = List[UserProductBase]