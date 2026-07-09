"""
Centralized logging configuration.

Every module should import `logger` from here instead of using print().
"""

import logging
import sys

import structlog

from core.config import settings


logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(
        getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    ),
)

logger = structlog.get_logger()