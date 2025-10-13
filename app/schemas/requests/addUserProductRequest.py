from pydantic import BaseModel
from typing import Optional

class AddUserProductRequest(BaseModel):
    userUuid: int
    produkts: str
    kcal: Optional[int] = None
    tauki: Optional[float] = None
    piesatTauki: Optional[float] = None
    oglh: Optional[float] = None
    cukuri: Optional[float] = None
    olbv: Optional[float] = None
    pienaOlbv: Optional[float] = None
    dzivOlbv: Optional[float] = None
    auguOlbv: Optional[float] = None
    sals: Optional[int] = None
    cena1kg: Optional[float] = None
    cena100g: Optional[float] = None
    vegan: Optional[bool] = False
    vegetarian: Optional[bool] = False
    dairyFree: Optional[bool] = False