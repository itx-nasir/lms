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

    DB_WAIT_TIMEOUT=${DB_WAIT_TIMEOUT:-120}
    DB_WAIT_INTERVAL=${DB_WAIT_INTERVAL:-1}

    # Use psycopg2 to attempt a real DB connection (better error messages and handles SSL/auth)
    python - <<PY
import os, sys, time
from urllib.parse import urlparse
url = os.environ.get('DATABASE_URL')
if not url:
    print('no_database_url')
    sys.exit(0)
p = urlparse(url)
host = p.hostname or 'localhost'
port = p.port or 5432
user = p.username or ''
password = p.password or ''
dbname = (p.path or '').lstrip('/')
timeout = int(os.environ.get('DB_WAIT_TIMEOUT', '120'))
interval = float(os.environ.get('DB_WAIT_INTERVAL', '1'))
deadline = time.time() + timeout
try:
    import psycopg2
    have_psycopg2 = True
except Exception:
    have_psycopg2 = False

if have_psycopg2:
    while time.time() < deadline:
        try:
            conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname, connect_timeout=5, sslmode=os.environ.get('DB_SSLMODE','prefer'))
            conn.close()
            print('ok')
            sys.exit(0)
        except Exception as e:
            msg = str(e).splitlines()[0]
            print('retry:'+msg)
            time.sleep(interval)
    print('timeout')
    sys.exit(2)
else:
    # Fallback: socket connect
    import socket
    while time.time() < deadline:
        try:
            s = socket.create_connection((host, int(port)), timeout=5)
            s.close()
            print('ok')
            sys.exit(0)
        except Exception as e:
            print('retry:'+str(e).splitlines()[0])
            time.sleep(interval)
    print('timeout')
    sys.exit(2)
PY

    rc=$?
    if [ "$rc" -eq 0 ]; then
      echo "Postgres is available"
    elif [ "$rc" -eq 2 ]; then
      echo "Timed out waiting for Postgres after ${DB_WAIT_TIMEOUT}s" >&2
      return 1
    else
      echo "Unexpected error while checking Postgres (rc=$rc)" >&2
      return 1
    fi
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
