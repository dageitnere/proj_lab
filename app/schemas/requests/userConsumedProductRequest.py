from pydantic import BaseModel
from datetime import datetime

class UserConsumedProductRequest(BaseModel):
    userUuid: int
    productName: str
    amount: float  # grams