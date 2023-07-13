#!/bin/sh

# ANSI escape codes to set and reset text color.
GREEN='\033[0;32m'
NC='\033[0m' # No color (aka. RESET)

echo -n "Waiting for PostgreSQL..."

while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
  echo -n "."
  sleep 0.1
done

echo "\n${GREEN}PostgreSQL is up!${NC}\n"
exec "$@"
