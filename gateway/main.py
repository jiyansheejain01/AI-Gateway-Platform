"""
FastAPI main entrypoint for the AI Gateway Platform.
Handles request routing, API versioning, and lifecycle events.
"""

import time

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

from gateway.auth import create_access_token

from kafka_service.producer import publish_event
from kafka_service.topics import RESPONSE_GENERATED

from services.router_service.routing import route_prompt
from services.memory_service.followup_classifier import is_follow_up

from services.monitoring.tracing import tracer

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor,
)

from services.monitoring.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    REDIS_CACHE_HITS,
    REDIS_CACHE_MISSES,
    SEMANTIC_CACHE_HITS,
    SEMANTIC_CACHE_MISSES,
    MODEL_REQUESTS,
    FOLLOWUP_REQUESTS,
    KAFKA_EVENTS,
)

from services.memory_service.conversation_memory import (
    load_conversation,
    save_conversation,
    clear_conversation,
)

from services.cache_service.redis_cache import (
    get_cached_response,
    cache_response,
)

from services.cache_service.semantic_cache import (
    search_similar_prompt,
    store_embedding,
)

from services.llm_service.orchestrator import (
    generate_response,
)


app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)


# ==========================================================
# Health Check
# ==========================================================

@app.get("/")
def health_check():
    return {
        "status": "AI Gateway Running"
    }


# ==========================================================
# Login
# ==========================================================

@app.post("/login")
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


# ==========================================================
# Request Models
# ==========================================================

class PromptRequest(BaseModel):
    session_id: str
    prompt: str


class SessionRequest(BaseModel):
    session_id: str


# ==========================================================
# Clear Conversation
# ==========================================================

@app.delete("/new_chat")
def new_chat(request: SessionRequest):

    clear_conversation(request.session_id)

    return {
        "message": f"Conversation '{request.session_id}' cleared successfully."
    }


# ==========================================================
# Chat Endpoint
# ==========================================================

@app.post("/chat")
def chat(request: PromptRequest):

    REQUEST_COUNT.inc()

    start_time = time.time()

    with tracer.start_as_current_span("Follow-up Detection"):

        follow_up = is_follow_up(request.prompt)

    if follow_up:
        FOLLOWUP_REQUESTS.inc()

    # ======================================================
    # Standalone Prompt -> Use Cache
    # ======================================================

    if not follow_up:

        print("Standalone prompt detected.")

        with tracer.start_as_current_span("Redis Cache Lookup"):

            cached = get_cached_response(request.prompt)

        if cached:

            print("REDIS CACHE HIT")

            REDIS_CACHE_HITS.inc()

            REQUEST_LATENCY.observe(
                time.time() - start_time
            )

            return {
                "source": "redis",
                "response": cached
            }

        print("REDIS CACHE MISS")
        REDIS_CACHE_MISSES.inc()

        with tracer.start_as_current_span("Semantic Cache Lookup"):

            semantic = search_similar_prompt(request.prompt)

        if semantic:

            print("SEMANTIC CACHE HIT")

            SEMANTIC_CACHE_HITS.inc()
            # Repopulate Redis
            cache_response(
                request.prompt,
                semantic["response"]
            )
            
            REQUEST_LATENCY.observe(
                time.time() - start_time
            )

            return {
                "source": "semantic_cache",
                "response": semantic["response"]
            }

        print("SEMANTIC CACHE MISS")
        SEMANTIC_CACHE_MISSES.inc()

        conversation = []

    # ======================================================
    # Follow-up Prompt -> Use Memory
    # ======================================================

    else:

        print("Follow-up detected.")

        with tracer.start_as_current_span("Load Conversation"):

            conversation = load_conversation(
                request.session_id
            )

        print("\n========== Conversation Loaded ==========")
        print(conversation)
        print("=========================================\n")
    # ======================================================
    # Model Router
    # ======================================================

    print("Running Model Router...")

    with tracer.start_as_current_span("Model Router"):

        route = route_prompt(request.prompt)

    MODEL_REQUESTS.labels(
        model=route["model"]
    ).inc()

    print(f"Selected Model : {route['model']}")
    print(f"Complexity     : {route['score']}")
    print(f"Category       : {route['category']}")

    # ======================================================
    # Build Conversation
    # ======================================================

    conversation.append(
        {
            "role": "user",
            "content": request.prompt
        }
    )

    print("Calling LLM...")

    with tracer.start_as_current_span("LLM Generation"):

        response = generate_response(
            route["model"],
            conversation
        )

    conversation.append(
        {
            "role": "assistant",
            "content": response["response"]
        }
    )
    print("\n===== ABOUT TO SAVE =====")
    print("Session:", request.session_id)
    print("Conversation:")
    print(conversation)
    print("=========================\n")

    with tracer.start_as_current_span("Save Conversation"):

        save_conversation(
            request.session_id,
            conversation
        )

    print("Conversation Saved.")

    # ======================================================
    # Store Cache
    # ======================================================

    with tracer.start_as_current_span("Store Redis Cache"):

        cache_response(
            request.prompt,
            response
        )

    with tracer.start_as_current_span("Store Semantic Cache"):

        store_embedding(
            request.prompt,
            response
        )
    # ======================================================
    # Kafka
    # ======================================================
    with tracer.start_as_current_span("Kafka Publish"):
        publish_event(
            RESPONSE_GENERATED,
            {
                "event_type": "response_generated",
                "prompt": request.prompt,
                "model": route["model"],
                "complexity": route["category"],
                "score": route["score"],
                "response_length": len(response["response"])
            }
        )

    KAFKA_EVENTS.inc()

    print("Kafka Event Published.")

    # ======================================================
    # Latency
    # ======================================================

    REQUEST_LATENCY.observe(
        time.time() - start_time
    )

    return {
        "source": "llm",
        "response": response
    }