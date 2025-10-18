from pydantic import BaseModel
from typing import List

class RecipeProductItem(BaseModel):
    productName: str
    grams: float
    kcal: float

class GenerateRecipesRequest(BaseModel):
    userMenuId: int  # The menu we want to generate recipes for
    products: List[RecipeProductItem]
