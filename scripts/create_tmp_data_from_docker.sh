#!/bin/sh

DOCKER_DATA_BACKEND_PATH='./.docker_data/backend'
if [ -e "$DOCKER_DATA_BACKEND_PATH" ]; then
    echo "$DOCKER_DATA_BACKEND_PATH exists."
else mkdir -p $DOCKER_DATA_BACKEND_PATH \
        && cd $DOCKER_DATA_BACKEND_PATH \
        && mkdir -p \
        postgresql \
        postgresql/data \
        postgresql/logs 
fi
