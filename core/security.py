"""
Security utilities.

Handles:
- Password hashing
- Password verification
- Authentication dependencies
"""

import bcrypt

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from gateway.auth import decode_access_token


security = HTTPBearer()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        salt,
    )

    return hashed_password.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a password.
    """

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Validate JWT and return the current user payload.
    """

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return payload