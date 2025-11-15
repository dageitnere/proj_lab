from pydantic import BaseModel, HttpUrl
from typing import Optional

class PostUserProductByRimiUrlRequest(BaseModel):
    url: str
    productName: Optional[str] = None
    mass_g: Optional[float] = None
    vegan: bool = False
    vegetarian: bool = False
    dairyFree: bool = False
    dairyProtein: bool = False
    animalProtein: bool = False
    plantProtein: bool = False
