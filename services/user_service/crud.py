"""
CRUD operations for the User Service.
"""

from sqlalchemy.orm import Session

from services.user_service.models import User


def get_user_by_username(
    db: Session,
    username: str,
):
    """
    Retrieve a user by username.
    """

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str,
):
    """
    Retrieve a user by email.
    """

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    username: str,
    email: str,
    password_hash: str,
):
    """
    Create a new user.
    """

    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role="developer",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user