# Hands-on Kafka

A practical hands-on project for learning and experimenting with Apache Kafka using Python and Docker.

## Overview

This repository demonstrates a basic producer-consumer pattern with Apache Kafka. It includes a containerized Kafka setup with KRaft mode (Kafka Raft Metadata), a Flask producer API with a Streamlit UI to send "like" messages, and a Flask consumer API that prints messages to the console.

## Architecture

```
┌─────────────────────────────────────────────┐
│         Docker Compose Environment          │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ Kafka Broker (KRaft Mode)           │   │
│  │ - bitnami/kafka:3.7                 │   │
│  │ - Port 9092: External Access        │   │
│  │ - Port 29092: Internal (Docker net) │   │
│  │ - Port 9093: KRaft Controller       │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ Kafdrop (Web UI)                    │   │
│  │ - Port 9000: Dashboard              │   │
│  │ - Monitor topics and messages       │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
         ↓                          ↑
  ┌──────────────┐          ┌──────────────┐
  │   Producer   │          │   Consumer   │
  │   (Python)   │          │   (Python)   │
  └──────────────┘          └──────────────┘
```

## Project Structure

- **`producer.py`** - Flask API that sends like messages to the `likes` topic
- **`consumer.py`** - Flask API that consumes the `likes` topic and logs messages
- **`producer_ui.py`** - Streamlit UI with a "Like" button
- **`start_kafka.bat`** - Starts Kafka via Docker Compose
- **`create_likes_topic.bat`** - Creates the `likes` topic with 3 partitions
- **`start_apps.bat`** - Starts producer + 3 consumers + the producer UI
- **`docker-compose.yml`** - Docker Compose configuration for Kafka broker and Kafdrop UI
- **`README.md`** - This file

## Prerequisites

- Docker and Docker Compose
- Python 3.7+
- Python packages: `confluent-kafka`, `flask`, `streamlit`, `requests`

## Setup & Installation

### 1. Install Python Dependencies

```bash
pip install confluent-kafka flask streamlit requests
```

### 2. Start Kafka with Docker Compose

```bash
docker-compose up -d
```

Or run the batch file:

```bat
start_kafka.bat
```

This command starts:
- **Kafka Broker** on `localhost:9092` (external) and `kafka:29092` (internal)
- **Kafdrop UI** on `http://localhost:9000`

Wait about 10-15 seconds for Kafka to fully initialize.

### 3. Verify Kafka is Running

Visit **Kafdrop Dashboard**: http://localhost:9000

You should see the Kafka broker status and topics.

### 4. Create the Likes Topic (3 Partitions)

```bat
create_likes_topic.bat
```

Or run the command directly:

```bash
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic likes --partitions 3 --replication-factor 1
```

## Usage

### Quick Start (Batch File)

```bat
start_apps.bat
```

This opens:
- Producer API window
- 3 Consumer API windows (logs show consumed messages)
- Producer UI window

### Manual Start

```bash
python producer.py
python consumer.py
streamlit run producer_ui.py
```

By default:
- Producer UI: http://localhost:8501
- Producer API: http://localhost:5001
- Consumer APIs: http://localhost:5002, http://localhost:5003, http://localhost:5004

## Practicing Partitioning & Consumer Groups

This section demonstrates how to practice **partitioning** and **consumer group rebalancing** in Kafka - fundamental concepts for scaling message consumption.

### Understanding Partitions

Partitions allow Kafka to:
- **Scale horizontally** by distributing data across multiple consumers
- **Process messages in parallel** with multiple threads/processes
- **Preserve order** within a partition while allowing out-of-order across partitions

### Setup: 3 Partitions with 3 Consumers

#### Step 1: Create a Topic with 3 Partitions

```bash
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic likes --partitions 3 --replication-factor 1
```

This creates a topic named `likes` with:
- **3 partitions** (Partition 0, 1, 2) - allows 3 concurrent consumers
- **1 replication factor** - suitable for single-broker development setup

#### Step 2: Confirm the Topic in Code

Ensure the `TOPIC` constant in both `producer.py` and `consumer.py` is:

```python
TOPIC = "likes"
```

Kafka will distribute messages across 3 partitions (round-robin by default when no key is set).

#### Step 3: Run Three Consumer Instances

Start the consumer in three separate terminal windows. Each will belong to the same **consumer group** and automatically be assigned one partition:

**Terminal 1 - Consumer Instance 1:**
```bash
python consumer.py
```

**Terminal 2 - Consumer Instance 2:**
```bash
set CONSUMER_PORT=5003 && python consumer.py
```

**Terminal 3 - Consumer Instance 3:**
```bash
set CONSUMER_PORT=5004 && python consumer.py
```

Note: to run multiple instances on one machine, change the `CONSUMER_PORT` value.

#### Step 4: Run the Producer

**Terminal 4 - Producer:**
```bash
python producer.py
```

### What to Observe

When all 3 consumers and the producer are running, you'll see:

1. **Partition Distribution**: Each consumer handles exactly one partition
   - Consumer 1 processes: Partition 0
   - Consumer 2 processes: Partition 1
   - Consumer 3 processes: Partition 2

2. **Message Distribution**: Messages are distributed across partitions (round-robin by default when no key is set).

3. **Parallel Processing**: Each consumer independently processes messages from its partition, demonstrating horizontal scaling.

Example output across three terminals:

```
# Consumer 1 (Partition 0)
Consumed: order=1 partition=0 clicked_at=2025-12-20 21:45:01 ts_ms=1734721501000
Consumed: order=4 partition=0 clicked_at=2025-12-20 21:45:04 ts_ms=1734721504000

# Consumer 2 (Partition 1)
Consumed: order=2 partition=1 clicked_at=2025-12-20 21:45:02 ts_ms=1734721502000
Consumed: order=5 partition=1 clicked_at=2025-12-20 21:45:05 ts_ms=1734721505000

# Consumer 3 (Partition 2)
Consumed: order=3 partition=2 clicked_at=2025-12-20 21:45:03 ts_ms=1734721503000
Consumed: order=6 partition=2 clicked_at=2025-12-20 21:45:06 ts_ms=1734721506000
```

### Consumer Group Rebalancing

Try stopping one consumer (Ctrl+C) while the producer and other consumers are running:

1. **When Consumer 1 stops**: Kafka automatically detects this and rebalances
   - Consumer 2 and 3 rebalance to cover all 3 partitions
   - This demonstrates Kafka's fault tolerance

2. **When you restart Consumer 1**: Kafka rebalances again
   - All 3 consumers return to their original 1:1 partition assignment

### Verify Partitions with Kafdrop

Visit **http://localhost:9000** (Kafdrop) to:
- View the `likes` topic with 3 partitions
- See which consumer group owns each partition
- Monitor message count per partition
- Check consumer group lag

### Advanced: Verify Partitions via CLI

```bash
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic likes
```

Expected output:
```
Topic: likes
  Partition: 0    Leader: 0    Replicas: [0]    Isr: [0]
  Partition: 1    Leader: 0    Replicas: [0]    Isr: [0]
  Partition: 2    Leader: 0    Replicas: [0]    Isr: [0]
```

### Key Learnings

- **Partitions = Parallelism**: More partitions = more concurrent consumers
- **Message Keys = Ordering**: Same key → same partition → ordered delivery
- **Consumer Groups = Scalability**: Consumers automatically distribute partitions
- **Offset Management**: Each partition maintains independent offsets per consumer group

## Configuration Details

### Kafka Broker (docker-compose.yml)

- **Image**: `bitnami/kafka:3.7` - Production-ready Kafka distribution
- **KRaft Mode**: Simplified cluster coordination without ZooKeeper
- **Single Node Setup**: NODE_ID=0 acting as both controller and broker
- **Listeners**:
  - `INTERNAL` (29092): Internal Docker network communication
  - `EXTERNAL` (9092): Host machine connection
  - `CONTROLLER` (9093): KRaft metadata consensus

### Kafdrop UI

- **Image**: `obsidiandynamics/kafdrop` - Web-based Kafka monitoring tool
- **Port**: 9000
- **Features**:
  - View topics and partitions
  - Monitor messages in real-time
  - Check consumer group status
  - Explore message content and metadata

### Python Configuration

**Producer Settings** (`producer.py`):
- Bootstrap servers: `localhost:9092`
- Topic: `likes`
- Message format: JSON payload with `order`, `clicked_at`, `ts_ms`

**Consumer Settings** (`consumer.py`):
- Bootstrap servers: `localhost:9092`
- Topic: `likes`
- Consumer group: `likes-ui`
- Offset reset: `earliest` (read from the beginning)
- Poll timeout: 1.0 second
- Logs: prints `order`, `partition`, `clicked_at`, `ts_ms`

## Monitoring

Access the Kafdrop dashboard at **http://localhost:9000** to:
- Visualize topics and partitions
- View consumer group lag
- Monitor message throughput
- Inspect individual message content

## Common Commands

### View Kafka Topic Info

```bash
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list
```

### Create a Topic (if needed)

```bash
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic likes --partitions 3 --replication-factor 1
```

### Stop Kafka

```bash
docker-compose down
```

### Clean Up Data

```bash
docker-compose down -v
```

This removes containers and volumes, resetting Kafka state.

## Learning Concepts

This project covers:

- **Producer-Consumer Pattern**: Asynchronous message passing
- **Topics & Partitions**: Organizing and distributing messages
- **Consumer Groups**: Coordinated consumption with offset management
- **KRaft Mode**: ZooKeeper-less Kafka cluster coordination
- **Docker Containerization**: Isolated, reproducible environment
- **Message Delivery Guarantees**: Confirmation callbacks and logging
- **Offset Management**: Message tracking and replay capability

## Troubleshooting

### Kafka connection refused

- Ensure Docker containers are running: `docker-compose ps`
- Wait 15+ seconds for Kafka to fully initialize
- Check if port 9092 is already in use

### Producer/Consumer hangs

- Verify Kafka is running: `docker-compose logs kafka`
- Check firewall settings
- Ensure `confluent-kafka` is properly installed

### Messages not appearing in consumer

- Consumer uses `earliest` offset reset, so it should read all historical messages
- Check that the topic exists: Use Kafdrop at http://localhost:9000
- Verify both producer and consumer target the same topic name (`likes` or your custom value)

## Next Steps

- Modify message content to send different data
- Add error handling and retry logic
- Implement multiple consumer groups
- Experiment with multiple partitions and replication
- Add schema validation (Avro/Protobuf)
- Deploy to a multi-broker Kafka cluster

## Resources

- [Confluent Kafka Python Documentation](https://docs.confluent.io/kafka-clients/python/current/overview.html)
- [Apache Kafka Official Documentation](https://kafka.apache.org/documentation/)
- [Bitnami Kafka Docker Image](https://hub.docker.com/r/bitnami/kafka)
- [Kafdrop Project](https://github.com/obsidiandynamics/kafdrop)

## License

This project is open source and available for educational and learning purposes.

