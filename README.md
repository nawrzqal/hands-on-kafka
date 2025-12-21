# Hands-on Kafka (Dockerized)

Simple local demo: click "Like" in a Streamlit UI, send a Kafka message, and watch three consumers log the messages and their partitions.

## What Runs

Docker Compose starts these services:
- Kafka broker (KRaft mode)
- Kafdrop UI
- Producer API (Flask)
- Producer UI (Streamlit)
- 3 Consumer instances (logs only)
- Topic initializer (creates `likes` with 3 partitions)

## Quick Start

```bat
run_docker.bat
create_likes_topic.bat
```

Open:
- Producer UI: http://localhost:8501
- Kafdrop: http://localhost:9000

## View Logs

Consumers:
```bash
docker-compose logs -f consumer-1 consumer-2 consumer-3
```

Kafka:
```bash
docker-compose logs -f kafka
```

Kafka + Consumers:
```bash
docker-compose logs -f kafka consumer-1 consumer-2 consumer-3
```

## Example Consumer Log

```
Consumed: order=1 partition=1 clicked_at=2025-12-20T21:45:01 ts_ms=1734721501000
```

## Files

- `docker-compose.yml` - All services in one file
- `Dockerfile` - Image for producer/consumer/ui services
- `requirements.txt` - Python dependencies for the image
- `producer.py` - Producer API (`/like`)
- `consumer.py` - Consumer (logs messages + exposes `/messages`)
- `producer_ui.py` - Streamlit UI with "Like" button
- `run_docker.bat` - Build + run + follow consumer logs

## Stop Everything

```bash
docker-compose down
```
