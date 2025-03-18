# dbs-benchmark

## Description
Benchmark of different databases using Python and Docker Compose.

## Databases
### SQL
- MariaDB
- PostgreSQL
### NoSQL
- MongoDB
- Cassandra
### In-memory
- Redis

## Prerequisites 
- Docker
- Conda/Venv with python==3.10.12

## Running local stack
```shell
# running the local stack as a daemon
docker compose -f docker-compose.yml up -d
```
```shell
# running the local stack in the foreground with exit on stop
docker compose -f docker-compose.yml up --abort-on-container-exit
```
```shell
# removing the containers
docker compose -f docker-compose.yml down --remove-orphans
```
```shell
# clear the data
docker compose -f docker-compose.yml down --volumes --remove-orphans && rm -rf .dev/data/
```
```shell
# full clean
docker compose -f docker-compose.yml down --volumes --remove-orphans --rmi all
```