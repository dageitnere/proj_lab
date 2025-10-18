from pydantic import BaseModel, HttpUrl
from typing import Optional

class AddUserProductByNutritionValueUrlRequest(BaseModel):
    url: str
    productName: Optional[str] = None  # if not provided, use scraped name
    massPerUnit: Optional[float] = None
    vegan: bool = False
    vegetarian: bool = False
    dairyFree: bool = False
    dairyProtein: bool = False
    animalProtein: bool = False
    plantProtein: bool = False
    price1kg: Optional[float] = None
    pricePerUnit: Optional[float] = None
