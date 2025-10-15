from pydantic import BaseModel

class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str | None = None