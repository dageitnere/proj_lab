from pydantic import BaseModel

class DeleteUserProductRequest(BaseModel):
    productName: str