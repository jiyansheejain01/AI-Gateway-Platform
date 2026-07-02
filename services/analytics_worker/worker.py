import json

from kafka import KafkaConsumer

from kafka_service.config import KAFKA_BOOTSTRAP_SERVERS
from kafka_service.topics import RESPONSE_GENERATED


consumer = KafkaConsumer(
    RESPONSE_GENERATED,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    group_id="analytics-worker",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print("Analytics Worker Started...\n")


total_requests = 0
phi3_requests = 0
llama_requests = 0

simple_requests = 0
complex_requests = 0

total_response_length = 0


for message in consumer:

    event = message.value

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