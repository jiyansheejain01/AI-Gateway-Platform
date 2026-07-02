"""
Kafka consumer/worker that simulates billing for every API request.
"""

import json

from kafka import KafkaConsumer

from kafka_service.config import KAFKA_BOOTSTRAP_SERVERS
from kafka_service.topics import RESPONSE_GENERATED


consumer = KafkaConsumer(
    RESPONSE_GENERATED,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",          # Only consume new events
    group_id="billing-worker-v2",        # New consumer group
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print("Billing Worker Started...\n")

total_cost = 0.0
total_requests = 0


for message in consumer:

    event = message.value

    print("Received Event:")
    print(event)
    print("-" * 50)

    # Skip old/incomplete events
    if "model" not in event:
        print("Skipping old/incomplete event.\n")
        continue

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
    