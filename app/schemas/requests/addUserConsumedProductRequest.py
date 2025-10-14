from pydantic import BaseModel
from datetime import datetime

class AddUserConsumedProductRequest(BaseModel):
    userUuid: int
    productName: str
    amount: float  # grams