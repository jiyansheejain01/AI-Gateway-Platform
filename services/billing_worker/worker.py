"""
Billing Worker.

Simulates billing for every API request.
Works with both:
- Kafka (production)
- Local EventBus (LOCAL_MODE)
"""

import json

from kafka import KafkaConsumer

from core.config import settings
from kafka_service.config import KAFKA_BOOTSTRAP_SERVERS
from kafka_service.topics import RESPONSE_GENERATED


# ==========================================================
# Billing State
# ==========================================================

total_cost = 0.0
total_requests = 0


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

    global total_cost
    global total_requests

    print("Received Event:")
    print(event)
    print("-" * 50)

    if "model" not in event:
        print("Skipping old/incomplete event.\n")
        return

    model = event["model"]

    # Simulated pricing
    if model == "phi3":
        cost = 0.00
    elif model == "llama3":
        cost = 0.00
    else:
        cost = 0.00

    total_requests += 1
    total_cost += cost

    print(f"Model               : {model}")
    print(f"Current Request Cost: ₹{cost:.2f}")
    print(f"Total Requests      : {total_requests}")
    print(f"Total Cost          : ₹{total_cost:.2f}")
    print("-" * 50)


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
        group_id="billing-worker-v2",
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    print("Billing Worker Started...\n")

    for message in consumer:
        process_event(message.value)


# ==========================================================
# Auto-start only in Production
# ==========================================================

if not settings.LOCAL_MODE:
    start_worker()