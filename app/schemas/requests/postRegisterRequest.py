from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class VerifyRequest(BaseModel):
    email: EmailStr

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: int = Field(ge=0, le=999999)