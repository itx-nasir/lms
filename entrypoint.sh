#!/usr/bin/env bash
set -euo pipefail

# Wait for database to become available (supports Postgres via DATABASE_URL)
wait_for_db() {
  if [ -z "${DATABASE_URL:-}" ]; then
    echo "DATABASE_URL not set, skipping DB wait"
    return 0
  fi

  # Only support postgres for wait-for logic here
  if [[ "$DATABASE_URL" == postgresql://* || "$DATABASE_URL" == postgres://* ]]; then
    echo "Waiting for Postgres to accept connections..."
    # extract host and port
    # DATABASE_URL expected like: postgres://user:pass@host:port/db
    host_port=$(echo "$DATABASE_URL" | sed -E 's#.*@([^/]+)/.*#\1#')
    host=$(echo "$host_port" | cut -d: -f1)
    port=$(echo "$host_port" | cut -d: -f2)
    port=${port:-5432}

    # try to connect until successful (using pg_isready if available, otherwise nc)
    until python - <<PY
import sys
import socket
try:
    s=socket.create_connection(("${host}", int(${port})), timeout=1)
    s.close()
    print('ok')
    sys.exit(0)
except Exception as e:
    print('retry')
    sys.exit(1)
PY
    do
      echo "Postgres not ready yet - sleeping 1s"
      sleep 1
    done

    echo "Postgres is available"
  else
    echo "DATABASE_URL not recognized as postgres, skipping wait"
  fi
}

# Run alembic migrations if enabled
run_migrations() {
  if [ "${RUN_MIGRATIONS:-true}" != "true" ]; then
    echo "RUN_MIGRATIONS != true, skipping alembic migrations"
    return 0
  fi

  echo "Running alembic upgrade head (if needed)"
  # alembic will be run in the project root
  alembic upgrade head || {
    echo "Alembic failed" >&2
    exit 1
  }
}

# Run seed_all if enabled
run_seed_all() {
  if [ "${RUN_SEED_ALL:-false}" != "true" ]; then
    echo "RUN_SEED_ALL != true, skipping seeding"
    return 0
  fi

  echo "Running scripts/seed_all.py"
  python scripts/seed_all.py || {
    echo "Seeding failed" >&2
    exit 1
  }
}

# Start the application using gunicorn (same as Procfile)
start_app() {
  GUNICORN_WORKERS=${GUNICORN_WORKERS:-1}
  echo "Starting gunicorn with ${GUNICORN_WORKERS} workers"
  exec gunicorn -w "${GUNICORN_WORKERS}" -k uvicorn.workers.UvicornWorker main:app
}

# Execute steps
cd /app
wait_for_db
run_migrations
run_seed_all
start_app
