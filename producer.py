from confluent_kafka import Producer
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

KAFKA_HOST = "localhost:9092"
TOPIC = "fancy-topic"

config = {
    "bootstrap.servers": KAFKA_HOST,
}

producer = Producer(config)

def on_delivery(err, msg):
    if err:
        logging.error(f"Delivery failed: {err}")
    else:
        logging.info(
            f"Sent message: {msg.value().decode()}, partition: {msg.partition()}, offset: {msg.offset()}"
        )

i = 0
while True:
    value = f"message #{i}"
    producer.produce(
        TOPIC,
        key=str(i),
        value=value,
        callback=on_delivery
    )
    producer.flush()
    i += 1
    time.sleep(1)
