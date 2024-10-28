#!/bin/bash

echo "clearing any existing containers..."
docker stop $(docker ps -a -q)
echo "Beginning rabbitMQ docker image..."

docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

echo "Session ended"
