"""
Authentication routes.
"""

from fastapi import APIRouter

from gateway.auth import create_access_token

router = APIRouter()


@router.post("/login")
def login():

    token = create_access_token(
        {
            "username": "admin",
            "role": "admin"
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }