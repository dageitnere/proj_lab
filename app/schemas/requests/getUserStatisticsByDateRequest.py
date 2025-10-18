from pydantic import BaseModel
from datetime import datetime

class GetUserStatisticsByDateRequest(BaseModel):
    startDate: datetime
    endDate: datetime
