from pydantic import BaseModel
from typing import Optional

class AddUserProductRequest(BaseModel):
    userUuid: int
    produkts: str
    kcal: int
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
    vegan: float
    vegetarian: float
    dairyFree: float