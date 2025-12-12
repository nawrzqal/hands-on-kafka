from confluent_kafka import Consumer
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

KAFKA_HOST = "localhost:9092"
TOPIC = "fancy-topic"

config = {
    "bootstrap.servers": KAFKA_HOST,
    "group.id": "fancy-group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(config)
consumer.subscribe([TOPIC])

logging.info("Consumer is running...")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        logging.error(msg.error())
        continue

    logging.info(
        f"Received message: {msg.value().decode()}, key: {msg.key().decode() if msg.key() else None}, partition: {msg.partition()}, offset: {msg.offset()}"
    )
