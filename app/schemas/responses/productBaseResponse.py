from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    """Base representation of a product"""
    id: Optional[int]
    produkts: str
    kcal: Optional[float]
    tauki: Optional[float]
    piesatTauki: Optional[float]
    oglh: Optional[float]
    cukuri: Optional[float]
    olbv: Optional[float]
    pienaOlbv: Optional[float]
    dzivOlbv: Optional[float]
    auguOlbv: Optional[float]
    sals: Optional[float]
    cena1kg: Optional[float]
    cena100g: Optional[float]

ProductsListResponse = List[ProductBase]