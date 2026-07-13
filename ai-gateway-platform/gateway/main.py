"""
FastAPI application entry point.

Responsible only for:
- Creating the FastAPI app
- Registering middleware/instrumentation
- Registering routers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from gateway.routes.health import router as health_router
from gateway.routes.login import router as login_router
from gateway.routes.session import router as session_router
from gateway.routes.chat import router as chat_router
from gateway.routes.register import router as register_router
from gateway.routes import conversations

from core.config import settings

from core.event_bus import subscribe

from kafka_service.topics import RESPONSE_GENERATED

from services.analytics_worker.worker import process_event as analytics_handler
from services.audit_worker.worker import process_event as audit_handler
from services.billing_worker.worker import process_event as billing_handler

from services.user_service.database import Base, engine
from services.user_service.models import User

# Create database tables (temporary until Alembic is added)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Gateway Platform",
    version="1.0.0",
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.CORS_ORIGINS.split(",")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Local Event Bus
# ==========================================================

if settings.LOCAL_MODE:

    subscribe(
        RESPONSE_GENERATED,
        analytics_handler,
    )

    subscribe(
        RESPONSE_GENERATED,
        audit_handler,
    )

    subscribe(
        RESPONSE_GENERATED,
        billing_handler,
    )

# ==========================================================
# Routes
# ==========================================================

app.include_router(
    health_router,
    prefix="/api/v1",
)
"""
app.include_router(
    login_router,
    prefix="/api/v1",
)

app.include_router(
    session_router,
    prefix="/api/v1",
)

app.include_router(
    chat_router,
    prefix="/api/v1",
)

app.include_router(
    register_router,
    prefix="/api/v1",
)

app.include_router(
    conversations.router,
    prefix="/api/v1",
)
# ==========================================================
# Monitoring
# ==========================================================

FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)

""""