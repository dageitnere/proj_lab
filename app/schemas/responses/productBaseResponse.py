from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    """Base representation of a product"""
    id: int
    productName: str
    kcal: float
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
    price100g: float

ProductsListResponse = List[ProductBase]