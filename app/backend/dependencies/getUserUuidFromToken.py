from app.backend.services.userService import decode_access_token
from fastapi import Request, HTTPException, status


def get_uuid_from_token(request: Request) -> int:
    """
    Extract and decode the user ID (UUID) from the access token stored in cookies.

    Args:
        request (Request): The incoming FastAPI request object, used to access cookies.

    Returns:
        int: The user ID (UUID) extracted from the token payload.

    Raises:
        HTTPException: If the access token is missing or invalid.
    """
    # Retrieve the JWT access token from the request cookies
    token = request.cookies.get("access_token")

    # If no token is found, raise an HTTP 401 (Unauthorized) error
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token"
        )

    # Decode the token to extract its payload (e.g., {"sub": "<user_id>", ...})
    payload = decode_access_token(token)

    # Return the user ID ("sub" field) as an integer
    return int(payload["sub"])
