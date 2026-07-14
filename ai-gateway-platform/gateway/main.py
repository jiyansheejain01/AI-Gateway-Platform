"""
FastAPI application entry point.

Responsible only for:
- Creating the FastAPI app
- Registering middleware/instrumentation
- Registering routers
"""

print("MAIN 1")
from fastapi import FastAPI

print("MAIN 2")
from fastapi.middleware.cors import CORSMiddleware

print("MAIN 3")
from prometheus_fastapi_instrumentator import Instrumentator

print("MAIN 4")
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

print("MAIN 5")
from gateway.routes.health import router as health_router

print("MAIN 6")
from gateway.routes.login import router as login_router

print("MAIN 7")
from gateway.routes.session import router as session_router

print("MAIN 8")
from gateway.routes.chat import router as chat_router

print("MAIN 9")
from gateway.routes.register import router as register_router

print("MAIN 10")
from gateway.routes import conversations

print("MAIN 11")
from core.config import settings

print("MAIN 12")
from core.event_bus import subscribe

print("MAIN 13")
from kafka_service.topics import RESPONSE_GENERATED

print("MAIN 14")
from services.analytics_worker.worker import process_event as analytics_handler

print("MAIN 15")
from services.audit_worker.worker import process_event as audit_handler

print("MAIN 16")
from services.billing_worker.worker import process_event as billing_handler

print("MAIN 17")
from services.user_service.database import Base, engine

print("MAIN 18")
from services.user_service.models import User

print("ALL IMPORTS COMPLETE")

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

