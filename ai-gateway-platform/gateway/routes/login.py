"""
Authentication routes.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from core.security import verify_password
from gateway.auth import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from services.user_service.crud import authenticate_user
from services.user_service.database import get_db
from services.user_service.schemas import (
    Token,
    UserLogin,
    RefreshTokenRequest,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return a JWT.
    """

    user = authenticate_user(
        db,
        credentials.username,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not verify_password(
        credentials.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(
    user.id,
    user.username,
    user.role,
    )

    refresh_token = create_refresh_token(
        user.id,
        user.username,
        user.role,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post(
    "/refresh",
)
def refresh_token(request: RefreshTokenRequest):

    payload = decode_refresh_token(request.refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    access_token = create_access_token(
        user_id=int(payload["sub"]),
        username=payload["username"],
        role=payload["role"],
        tenant=payload["tenant"],
        permissions=payload["permissions"],
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }