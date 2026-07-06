import json

from kafka import KafkaProducer

from kafka_service.config import KAFKA_BOOTSTRAP_SERVERS

from core.config import settings

if not settings.LOCAL_MODE:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )


def publish_event(topic: str, event: dict):

    if settings.LOCAL_MODE:

        from core.event_bus import publish

        publish(topic, event)

        return

    producer.send(topic, event)
    producer.flush()