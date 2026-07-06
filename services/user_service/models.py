"""
Database models for users, teams, and API keys.
"""
from sqlalchemy import Column, Integer, String

from services.user_service.database import Base


from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from services.user_service.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    username = Column(
        String,
        unique=True,
        nullable=False,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
    )

    password_hash = Column(
        String,
        nullable=False,
    )

    role = Column(
        String,
        default="developer",
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )