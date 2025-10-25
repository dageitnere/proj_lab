from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Annotated

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class VerifyRequest(BaseModel):
    email: EmailStr

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: int = Field(ge=0, le=999999)

Activity = Literal["SEDENTARY","LIGHT","MODERATE","ACTIVE","VERY_ACTIVE"]
Goal = Literal["MAINTAIN","LOSE","GAIN"]
Gender = Literal["MALE","FEMALE"]

class CompleteRegistrationRequest(BaseModel):
    age: Annotated[int, Field(ge=10, le=120)]
    gender: Gender
    weight: Annotated[float, Field(gt=0)]       # kg
    height: Annotated[float, Field(gt=0)]        # cm
    isVegan: bool
    isVegetarian: bool
    isDairyInt: bool              # eats dairy? True==intolerant? If you meant “eats dairy”, rename to e.g. eatsDairy: bool
    goal: Goal
    activityFactor: Activity