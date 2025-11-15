from pydantic import BaseModel

class LoginInRequest(BaseModel):
    login: str
    password: str