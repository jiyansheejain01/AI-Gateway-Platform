"""
FastAPI application entry point.

Responsible only for:
- Creating the FastAPI app
- Registering middleware/instrumentation
- Registering routers
"""

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from gateway.routes.health import router as health_router
from gateway.routes.login import router as login_router
from gateway.routes.session import router as session_router
from gateway.routes.chat import router as chat_router


app = FastAPI(
    title="AI Gateway Platform",
    version="1.0.0",
)

# ==========================================================
# Monitoring
# ==========================================================

FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)

# ==========================================================
# Routes
# ==========================================================

app.include_router(health_router)
app.include_router(login_router)
app.include_router(session_router)
app.include_router(chat_router)