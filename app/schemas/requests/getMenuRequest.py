from pydantic import BaseModel

class GetMenuRequest(BaseModel):
    menuName: str
    userUuid: int