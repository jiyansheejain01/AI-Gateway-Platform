"""
Authentication utilities.
Handles JWT creation and validation.
"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from uuid import uuid4

from jose import jwt

from core.config import settings


def create_access_token(
    user_id: int,
    username: str,
    role: str,
) -> str:
    """
    Create a signed JWT access token.
    """

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
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