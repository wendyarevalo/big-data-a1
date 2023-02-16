#!/bin/bash

docker-compose -f coredms/docker-compose.yml up -d

echo "Waiting for cluster to be ready"
sleep 100

docker exec -it cassandra1 cqlsh -f conf_cassandra.cql

docker build -t consumer dataingest/consumer/.

docker build -t daas daas/app/.

docker-compose -f dataingest/docker-compose.yml up -d

echo "Waiting for rabbitMQ to be ready"
sleep 30

docker restart daas
docker restart dataingest-consumer-1
docker restart dataingest-consumer-2
docker restart dataingest-consumer-3
docker restart dataingest-consumer-4

echo "If you did not see any errors everything is set! Follow the steps for the producer now:)"