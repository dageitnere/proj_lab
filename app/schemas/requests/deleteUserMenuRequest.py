from pydantic import BaseModel

class DeleteUserMenuRequest(BaseModel):
    menuName: str
    userUuid: int