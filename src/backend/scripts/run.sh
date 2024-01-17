#!/bin/sh
# run poetry activate dependencies for save in localmaсhine
# cd /app && poetry lock --no-update
poetry lock --no-update

poetry run python main.py
# Evaluating passed command:
exec "$@"
