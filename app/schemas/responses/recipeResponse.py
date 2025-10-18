from pydantic import BaseModel
from typing import List, Optional

class RecipeItem(BaseModel):
    mealType: str
    name: str
    description: Optional[str] = None
    instructions: str
    photoUrl: Optional[str] = None
    calories: Optional[float] = None


class GenerateRecipesResponse(BaseModel):
    status: str
    recipes: Optional[List[RecipeItem]] = None
    message: Optional[str] = None
