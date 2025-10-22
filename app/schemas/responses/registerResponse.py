from pydantic import BaseModel

class RegisterResponse(BaseModel):
    ok: bool
    uuid: int | None = None
    username: str | None = None

class VerifyResponse(BaseModel):
    ok: bool