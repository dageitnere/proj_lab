from pydantic import BaseModel, HttpUrl
from typing import Optional

class AddUserProductByRimiUrlRequest(BaseModel):
    url: str
    productName: Optional[str] = None  # if not provided, use scraped name
    mass_g: Optional[float] = None  # weight of one unit in grams, needed for price normalization
    vegan: bool = False
    vegetarian: bool = False
    dairyFree: bool = False
    dairyProtein: bool = False
    animalProtein: bool = False
    plantProtein: bool = False
