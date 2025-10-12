from pydantic import BaseModel

class DietRequest(BaseModel):
    userUuid: int
    kcal: float
    protein: float
    fat: float
    satFat: float
    carbs: float
    sugars: float
    salt: float
    vegan: bool = False
    vegetarian: bool = False
    dairyFree: bool = False
    restrictions: list[dict] = []