"""
Audit Worker.

Logs security-sensitive events.
Works with both:
- Kafka (production)
- Local EventBus (LOCAL_MODE)
"""

import json
from datetime import datetime

from kafka import KafkaConsumer

from core.config import settings
from kafka_service.config import KAFKA_BOOTSTRAP_SERVERS
from kafka_service.topics import RESPONSE_GENERATED


# ==========================================================
# Shared Business Logic
# ==========================================================

def process_event(event: dict):
    """
    Process one response-generated event.
    Can be called by:
    - Kafka consumer
    - Local EventBus
    """

    print("Received Event:")
    print(event)
    print("-" * 50)

    required_fields = [
        "model",
        "complexity",
        "score",
        "prompt",
    ]

    if not all(field in event for field in required_fields):
        print("Skipping old/incomplete event.\n")
        return

    log = (
        f"{datetime.now()} | "
        f"Model={event['model']} | "
        f"Complexity={event['complexity']} | "
        f"Score={event['score']} | "
        f"Prompt={event['prompt']}\n"
    )

    with open("audit.log", "a", encoding="utf-8") as file:
        file.write(log)

    print("Audit Log Saved.\n")


# ==========================================================
# Kafka Worker (Production Only)
# ==========================================================

def start_worker():
    """
    Start Kafka consumer.
    Used only in production.
    """

    consumer = KafkaConsumer(
        RESPONSE_GENERATED,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        group_id="audit-worker-v2",
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    print("Audit Worker Started...\n")

    for message in consumer:
        process_event(message.value)


# ==========================================================
# Auto-start only in Production
# ==========================================================

if not settings.LOCAL_MODE:
    start_worker()