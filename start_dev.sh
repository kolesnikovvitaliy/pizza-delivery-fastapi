#!/bin/sh
chmod +x ./scripts/create_tmp_data_from_docker.sh \
    && ./scripts/create_tmp_data_from_docker.sh && \
docker-compose --env-file src/config/.env -f ./src/docker-compose.dev.yml up  --remove-orphans --build