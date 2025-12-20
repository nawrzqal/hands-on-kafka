import itertools
import json
import os
import time
from flask import Flask, jsonify
from confluent_kafka import Producer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "likes")

producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
counter = itertools.count(1)

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"status": "ok", "topic": TOPIC})

@app.post("/like")
def like():
    payload = {
        "order": next(counter),
        "clicked_at": time.strftime("%Y-%m-%dT%H:%M:%S"), 
        "ts_ms": int(time.time() * 1000),
    }

    try:
        producer.produce(TOPIC, value=json.dumps(payload, separators=(",", ":")))
        producer.flush(1) 
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 500

    return jsonify({"status": "sent", "payload": payload})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
