"""
Authentication and authorization mechanisms.
Handles JWT creation and validation.
"""

from jose import jwt

from core.config import settings


def create_access_token(data: dict) -> str:
    """
    Create a signed JWT access token.
    """

    return jwt.encode(
        data,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )