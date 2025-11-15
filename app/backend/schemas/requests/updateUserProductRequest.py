from pydantic import BaseModel
from typing import Optional


class UpdateUserProductRequest(BaseModel):
    oldProductName: str  # Required to identify product
    productName: Optional[str] = None
    kcal: Optional[float] = None
    fat: Optional[float] = None
    satFat: Optional[float] = None
    carbs: Optional[float] = None
    sugars: Optional[float] = None
    protein: Optional[float] = None
    dairyProtein: Optional[bool] = None
    animalProtein: Optional[bool] = None
    plantProtein: Optional[bool] = None
    salt: Optional[float] = None
    price1kg: Optional[float] = None
    vegan: Optional[bool] = None
    vegetarian: Optional[bool] = None
    dairyFree: Optional[bool] = None
    URL: Optional[str] = None