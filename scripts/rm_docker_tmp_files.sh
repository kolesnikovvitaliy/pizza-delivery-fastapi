#!/bin/sh

DOCKER_DATA_BACKEND_PATH='./.docker_data'
if [ -e "$DOCKER_DATA_BACKEND_PATH" ]; then
    sudo rm -rf $DOCKER_DATA_BACKEND_PATH
fi