from pydantic import BaseModel
from datetime import datetime

class AddUserConsumedProductRequest(BaseModel):
    productName: str
    amount: float  # grams