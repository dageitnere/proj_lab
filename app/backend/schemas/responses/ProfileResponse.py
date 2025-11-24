from pydantic import BaseModel

class ProfileResponse(BaseModel):
    username: str
    email: str
    emailVerified: bool
    age: int
    gender: str
    weight: float
    height: float
    bmi: float
    bmr: float
    calculatedKcal: float
    calculatedCarbs: float
    calculatedProtein: float
    calculatedFat: float
    calculatedSatFat: float
    calculatedSugar: float
    calculatedSalt: float
    activityFactorDisplay: str
    goalDisplay: str
    isVegan: bool
    isVegetarian: bool
    dairyIntolerance: bool