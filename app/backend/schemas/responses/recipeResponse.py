from pydantic import BaseModel
from typing import List, Optional

class RecipeItem(BaseModel):
    mealType: str
    name: str
    description: Optional[str] = None
    instructions: str
    pictureBase64: Optional[str] = None
    calories: Optional[float] = None
    recipeBatch: int


class GenerateRecipesResponse(BaseModel):
    status: str
    recipes: Optional[List[RecipeItem]] = None
    executionTime: Optional[float] = None
    message: Optional[str] = None
