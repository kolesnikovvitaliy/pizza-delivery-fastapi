#!/bin/sh
docker-compose --env-file src/config/.env -f ./src/docker-compose.dev.yml down -v & disown
# PPPID=$(awk '{print $4}' "/proc/$PPID/stat")
sleep 15
# chmod +x ./scripts/rm_docker_tmp_files.sh \
#     && ./scripts/rm_docker_tmp_files.sh 
# kill $PPPID