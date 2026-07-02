"""
Kafka consumer/worker that logs security-sensitive events,
policy violations, and access audits.
"""

import json
from datetime import datetime

from kafka import KafkaConsumer

from kafka_service.config import KAFKA_BOOTSTRAP_SERVERS
from kafka_service.topics import RESPONSE_GENERATED


consumer = KafkaConsumer(
    RESPONSE_GENERATED,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",          # Only consume new events
    group_id="audit-worker-v2",          # New consumer group
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print("Audit Worker Started...\n")


for message in consumer:

    event = message.value

    print("Received Event:")
    print(event)
    print("-" * 50)

    # Skip old/incomplete events
    required_fields = [
        "model",
        "complexity",
        "score",
        "prompt"
    ]

    if not all(field in event for field in required_fields):
        print("Skipping old/incomplete event.\n")
        continue

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