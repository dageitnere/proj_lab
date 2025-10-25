from pydantic import BaseModel
from typing import List


class ProductsNamesResponse(BaseModel):
    products: List[str]
