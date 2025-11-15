from pydantic import BaseModel
from typing import List

class RecipeProductItem(BaseModel):
    productName: str
    grams: float
    kcal: float

class RegenerateRecipesRequest(BaseModel):
    menuId: int

class DeleteRecipesBatchRequest(BaseModel):
    menuId: int
    batchId: int