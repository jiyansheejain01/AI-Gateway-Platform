"""
Database session management.

Supports:
- SQLite (LOCAL_MODE)
- PostgreSQL (Production)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.logging import logger


# ==========================================================
# Database Engine
# ==========================================================

if settings.LOCAL_MODE:

    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    logger.info(
        "Using SQLite (LOCAL_MODE)",
        database=settings.SQLITE_PATH,
    )

else:

    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
    )

    logger.info(
        "Using PostgreSQL",
        host=settings.POSTGRES_HOST,
        database=settings.POSTGRES_DB,
    )


# ==========================================================
# Session
# ==========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# ==========================================================
# Connection Test
# ==========================================================

try:

    with engine.connect():
        logger.info("Database connection successful")

except Exception as e:

    logger.error(
        "Failed to connect to database",
        error=str(e),
    )

    raise