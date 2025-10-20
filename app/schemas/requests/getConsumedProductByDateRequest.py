from pydantic import BaseModel
from datetime import datetime

class GetConsumedProductByDateRequest(BaseModel):
    date: datetime

