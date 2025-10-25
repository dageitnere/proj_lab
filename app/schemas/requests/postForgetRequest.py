from pydantic import BaseModel, EmailStr, Field

class ForgotRequest(BaseModel):
    email: EmailStr

class ForgotConfirmRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)