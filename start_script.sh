#!/bin/bash

# switch to the docker images venv
cd ./docker_images

# launch the docker images
docker-compose -f ./docker-compose-zookeper-kafka-postgres.yml up -d

# change directory to the kafka_venv
cd ../kafka_venv

# activate the poetry venv
poetry shell

