"""
Analytics Worker.

Processes response-generated events and updates analytics.
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
# Analytics Counters
# ==========================================================

total_requests = 0
phi3_requests = 0
llama_requests = 0

simple_requests = 0
complex_requests = 0

total_response_length = 0


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

    global total_requests
    global phi3_requests
    global llama_requests
    global simple_requests
    global complex_requests
    global total_response_length

    total_requests += 1

    if event["model"] == "phi3":
        phi3_requests += 1
    else:
        llama_requests += 1

    if event["complexity"] == "simple":
        simple_requests += 1
    else:
        complex_requests += 1

    total_response_length += event["response_length"]

    average_length = total_response_length / total_requests

    print("\n========== ANALYTICS ==========")

    print(f"Total Requests      : {total_requests}")
    print(f"Phi3 Requests       : {phi3_requests}")
    print(f"Llama Requests      : {llama_requests}")
    print(f"Simple Queries      : {simple_requests}")
    print(f"Complex Queries     : {complex_requests}")
    print(f"Average Resp Length : {average_length:.2f}")

    print("===============================\n")


# ==========================================================
# Kafka Worker (Production Only)
# ==========================================================

def start_worker():
    """
    Start the Kafka consumer.
    Used only when LOCAL_MODE=False.
    """

    consumer = KafkaConsumer(
        RESPONSE_GENERATED,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id="analytics-worker",
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    print("Analytics Worker Started...\n")

    for message in consumer:
        process_event(message.value)


# ==========================================================
# Start automatically only in Production
# ==========================================================

if not settings.LOCAL_MODE:
    start_worker()