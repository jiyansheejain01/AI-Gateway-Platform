import json

from kafka import KafkaProducer

from kafka_service.config import KAFKA_BOOTSTRAP_SERVERS


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


def publish_event(topic: str, event: dict):

    producer.send(topic, event)
    producer.flush()

    print(f"Published event to {topic}")