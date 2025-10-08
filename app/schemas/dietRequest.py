from pydantic import BaseModel

class DietRequest(BaseModel):
    kcal: float
    protein: float
    fat: float
    satFat: float
    carbs: float
    sugars: float
    salt: float
    restrictions: list[dict] = []