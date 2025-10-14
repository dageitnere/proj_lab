from pydantic import BaseModel
from datetime import date

class GetConsumedProductByDateRequest(BaseModel):
    userUuid: int
    date: date

