"""
Database session management and connection pooling
for the User Service.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.logging import logger


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


try:
    with engine.connect():
        logger.info("Connected to PostgreSQL")

except Exception as e:
    logger.error(
        "Failed to connect to PostgreSQL",
        error=str(e),
    )
    raise