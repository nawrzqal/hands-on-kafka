@echo off
docker exec hands-on-kafka-kafka-1 kafka-topics.sh --bootstrap-server localhost:9092 --create --topic likes --partitions 3 --replication-factor 1