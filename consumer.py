import json
import os
import threading

from collections import deque
from confluent_kafka import Consumer
from flask import Flask, jsonify

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "likes"
GROUP_ID = "likes-ui"

messages = deque(maxlen=200)

app = Flask(__name__)


def consume_loop():
    consumer = Consumer(
        {
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            "group.id": GROUP_ID,
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe([TOPIC])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            continue

        raw = msg.value().decode(errors="replace")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"raw": raw}

        if isinstance(payload, dict):
            payload["partition"] = msg.partition()
        else:
            payload = {"value": payload, "partition": msg.partition()}

        messages.append(payload)
        print(
            "Consumed: order=%s partition=%s clicked_at=%s ts_ms=%s"
            % (
                payload.get("order"),
                payload.get("partition"),
                payload.get("clicked_at"),
                payload.get("ts_ms"),
            )
        )


@app.get("/messages")
def get_messages():
    return jsonify(list(messages))


if __name__ == "__main__":
    thread = threading.Thread(target=consume_loop, daemon=True)
    thread.start()
    port = int(os.getenv("CONSUMER_PORT", "5002"))
    app.run(host="0.0.0.0", port=port, debug=False)
