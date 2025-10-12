from pydantic import BaseModel
from typing import List


class ProductsNamesResponse(BaseModel):
    """Response for endpoints that return only product names"""
    products: List[str]
