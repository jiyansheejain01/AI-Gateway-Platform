"""
Chat Service.

Contains the complete business logic for processing chat requests.
"""

import time

from core.logging import logger

from kafka_service.producer import publish_event
from kafka_service.topics import RESPONSE_GENERATED

from services.router_service.routing import route_prompt
from services.memory_service.followup_classifier import is_follow_up

from services.monitoring.tracing import tracer

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


def process_chat(
    session_id: str,
    prompt: str,
    current_user: dict,
) -> dict:
    """
    Process a chat request.
    """

    REQUEST_COUNT.inc()
    print("STEP 1: Entered process_chat")

    start_time = time.time()

    # ======================================================
    # Authenticated User
    # ======================================================

    user_id = current_user["sub"]
    tenant = current_user["tenant"]
    role = current_user["role"]
    permissions = current_user["permissions"]

    logger.info(
        "Authenticated request",
        user_id=user_id,
        tenant=tenant,
        role=role,
    )

    # ======================================================
    # Follow-up Detection
    # ======================================================

    with tracer.start_as_current_span("Follow-up Detection"):
        follow_up = is_follow_up(prompt)
        print("STEP 2: Follow-up detection complete")

    if follow_up:
        FOLLOWUP_REQUESTS.inc()

    # ======================================================
    # Standalone Prompt -> Use Cache
    # ======================================================

    if not follow_up:

        logger.info("Standalone prompt detected")

        with tracer.start_as_current_span("Redis Cache Lookup"):
            cached = get_cached_response(prompt)

        if cached:

            logger.info("Redis cache hit")

            REDIS_CACHE_HITS.inc()

            REQUEST_LATENCY.observe(
                time.time() - start_time
            )

            return {
                "source": "redis",
                "response": cached
            }

        logger.info("Redis cache miss")

        REDIS_CACHE_MISSES.inc()

        with tracer.start_as_current_span("Semantic Cache Lookup"):
            semantic = search_similar_prompt(prompt)

        if semantic:

            logger.info("Semantic cache hit")

            SEMANTIC_CACHE_HITS.inc()

            # Repopulate Redis
            cache_response(
                prompt,
                semantic["response"]
            )

            REQUEST_LATENCY.observe(
                time.time() - start_time
            )

            return {
                "source": "semantic_cache",
                "response": semantic["response"]
            }

        logger.info("Semantic cache miss")

        SEMANTIC_CACHE_MISSES.inc()

        conversation = []

    # ======================================================
    # Follow-up Prompt -> Use Memory
    # ======================================================

    else:

        logger.info("Follow-up detected")

        with tracer.start_as_current_span("Load Conversation"):

            conversation = load_conversation(
                tenant,
                user_id,
                session_id,
            )

        logger.info(
            "Conversation loaded",
            session_id=session_id,
            messages=len(conversation),
        )

    # ======================================================
    # Model Router
    # ======================================================

    logger.info("Running model router")

    with tracer.start_as_current_span("Model Router"):

        route = route_prompt(prompt)
        print("STEP 3: Model routing complete")

    MODEL_REQUESTS.labels(
        model=route["model"]
    ).inc()

    logger.info(
        "Model selected",
        model=route["model"],
        score=route["score"],
        category=route["category"],
    )

    # ======================================================
    # Build Conversation
    # ======================================================

    conversation.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    logger.info("Calling LLM")

    with tracer.start_as_current_span("LLM Generation"):
        print("STEP 4: About to call LLM")
        response = generate_response(
            route["model"],
            conversation
        )
        print("STEP 5: LLM returned")
        

    conversation.append(
        {
            "role": "assistant",
            "content": response["response"]
        }
    )

    logger.info(
        "Saving conversation",
        session_id=session_id,
        messages=len(conversation),
    )

    with tracer.start_as_current_span("Save Conversation"):
        print("STEP 6: Saving conversation")
        save_conversation(
            tenant,
            user_id,
            session_id,
            conversation,
        )

    logger.info("Conversation saved")

    # ======================================================
    # Store Cache
    # ======================================================

    with tracer.start_as_current_span("Store Redis Cache"):

        cache_response(
            prompt,
            response
        )

    with tracer.start_as_current_span("Store Semantic Cache"):

        store_embedding(
            prompt,
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
                "prompt": prompt,
                "model": route["model"],
                "complexity": route["category"],
                "score": route["score"],
                "response_length": len(response["response"]),
            },
        )

    KAFKA_EVENTS.inc()

    logger.info("Kafka event published")

    # ======================================================
    # Latency
    # ======================================================

    REQUEST_LATENCY.observe(
        time.time() - start_time
    )

    print("STEP 7: Returning response")
    return {
        "source": "llm",
        "response": response,
    }