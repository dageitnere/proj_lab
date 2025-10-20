from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AddUserConsumedProductRequest(BaseModel):
    productName: str
    amount: float
    date: Optional[datetime] = None