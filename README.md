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
- Conda(recommended)/venv with python==3.10.12

## Installation
1. activate your conda/venv
2. check what is your path for pip. for example on unix run `which pip` - it should be located in the folder associated with your conda env
3. install required dependencies
```shell
pip install -r requirements.txt 
```

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

## Data Generator

For detailed instructions on how to use the data generator, see [README.generator.md](README.generator.md).