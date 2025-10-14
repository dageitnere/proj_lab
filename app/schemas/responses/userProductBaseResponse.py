from pydantic import BaseModel
from typing import List, Optional

class UserProductBase(BaseModel):
    """Base representation of a user's product entry"""
    id: int
    userUuid: int
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


UserProductsListResponse = List[UserProductBase]