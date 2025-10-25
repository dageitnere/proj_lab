from pydantic import BaseModel

class PostUserProductRequest(BaseModel):
    productName: str
    kcal: int
    fat: float
    satFat: float
    carbs: float
    sugars: float
    protein: float
    dairyProt: float
    animalProt: float
    plantProt: float
    salt: float
    price1kg: float
    vegan: bool = False
    vegetarian: bool = False
    dairyFree: bool = False