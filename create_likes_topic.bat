@echo off
docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --create --topic likes --partitions 3 --replication-factor 1
