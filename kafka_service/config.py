KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

RESPONSE_TOPIC = "response-generated""""
Kafka configuration.

All Kafka settings are loaded from the centralized
application configuration.
"""

from core.config import settings

KAFKA_BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS

RESPONSE_TOPIC = settings.RESPONSE_TOPIC