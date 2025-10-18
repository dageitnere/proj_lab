from app.services.userService import decode_access_token
from fastapi import Request, HTTPException, status

def get_uuid_from_token(request: Request) -> int:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token"
        )
    payload = decode_access_token(token)
    return int(payload["sub"])