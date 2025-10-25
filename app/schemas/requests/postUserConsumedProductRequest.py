from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostUserConsumedProductRequest(BaseModel):
    productName: str
    amount: float
    date: Optional[datetime] = None