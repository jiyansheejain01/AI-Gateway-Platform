import json

from kafka import KafkaProducer

from core.config import settings

from kafka_service.config import KAFKA_BOOTSTRAP_SERVERS

# ==========================================================
# Kafka Producer (Production)
# ==========================================================

producer = None

if not settings.LOCAL_MODE:

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )


# ==========================================================
# Publish Event
# ==========================================================

def publish_event(topic: str, event: dict):

    if settings.LOCAL_MODE:

        from core.event_bus import publish

        publish(topic, event)

        return

    producer.send(topic, event)
    producer.flush()

    print(f"Published event to {topic}")