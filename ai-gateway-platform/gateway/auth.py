"""
Authentication utilities.
Handles JWT creation and validation.
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jose import JWTError, jwt

from core.config import settings


def create_access_token(
    user_id: int,
    username: str,
    role: str,
    tenant: str = "default",
    permissions: list[str] | None = None,
) -> str:
    """
    Create a signed JWT access token.
    """

    if permissions is None:
        permissions = ["chat"]

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "tenant": tenant,
        "permissions": permissions,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "jti": str(uuid4()),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.
    """

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
        )

        return payload

    except JWTError as e:
        print("=" * 60)
        print("JWT VALIDATION ERROR")
        print(type(e).__name__)
        print(str(e))
        print("=" * 60)
        return None