from pydantic import BaseModel
from datetime import datetime

class GetUserStatisticsByDateRequest(BaseModel):
    userUuid: int
    startDate: datetime
    endDate: datetime
