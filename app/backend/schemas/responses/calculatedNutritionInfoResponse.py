from pydantic import BaseModel

class CalculatedNutritionInfoResponse(BaseModel):
    calculatedKcal: float
    calculatedCarbs: float
    calculatedProtein: float
    calculatedFat: float
    calculatedSatFat: float
    calculatedSugar: float
    calculatedSalt: float
    isVegetarian: bool
    isVegan: bool
    isDairyInt: bool