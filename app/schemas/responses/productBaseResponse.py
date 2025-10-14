from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    """Base representation of a product"""
    id: int
    produkts: str
    kcal: float
    tauki: float
    piesatTauki: float
    oglh: float
    cukuri: float
    olbv: float
    pienaOlbv: float
    dzivOlbv: float
    auguOlbv: float
    sals: float
    cena1kg: float
    cena100g: float

ProductsListResponse = List[ProductBase]