"""
User registration routes.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from core.security import hash_password
from services.user_service.crud import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from services.user_service.database import get_db
from services.user_service.schemas import (
    UserRegister,
    UserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    # Check if username already exists
    if get_user_by_username(db, user.username):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    # Check if email already exists
    if get_user_by_email(db, user.email):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    # Hash the password
    password_hash = hash_password(user.password)

    # Create user
    new_user = create_user(
        db=db,
        username=user.username,
        email=user.email,
        password_hash=password_hash,
    )

    return new_user