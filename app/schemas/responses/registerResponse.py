from pydantic import BaseModel

class RegisterOut(BaseModel):
    ok: bool
    uuid: int | None = None
    username: str | None = None
