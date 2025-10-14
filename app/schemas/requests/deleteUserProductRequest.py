from pydantic import BaseModel

class DeleteUserProductRequest(BaseModel):
    produkts: str
    userUuid: int