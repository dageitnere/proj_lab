from pydantic import BaseModel
from typing import List


class UserMenuNamesResponse(BaseModel):
    menus: List[str]