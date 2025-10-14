from pydantic import BaseModel

class DeleteConsumedProductRequest(BaseModel):
    productId: int