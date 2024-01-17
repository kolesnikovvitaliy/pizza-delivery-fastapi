#!/bin/sh
docker-compose --env-file src/config/.env -f ./src/docker-compose.dev.yml up  --remove-orphans --build