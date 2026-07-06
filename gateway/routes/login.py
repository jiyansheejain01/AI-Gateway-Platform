"""
Authentication routes.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from core.security import verify_password
from gateway.auth import create_access_token
from services.user_service.crud import authenticate_user
from services.user_service.database import get_db
from services.user_service.schemas import (
    Token,
    UserLogin,
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

    token = create_access_token(
        user.id,
        user.username,
        user.role,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }