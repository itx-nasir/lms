#!/usr/bin/env bash
set -e

# Simple entrypoint to run DB migrations and seeds before starting the web server.
# This is intentionally simple to support environments without interactive shell access.

echo "[entrypoint] Running alembic migrations..."
if command -v alembic >/dev/null 2>&1; then
  alembic upgrade head || echo "[entrypoint] Warning: alembic upgrade failed (continuing)"
else
  echo "[entrypoint] alembic not found in PATH; skipping migrations"
fi

echo "[entrypoint] Seeding admin user (idempotent)..."
python scripts/seed_admin.py || echo "[entrypoint] Warning: seed_admin failed (continuing)"

echo "[entrypoint] Starting web server"
exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000} --timeout 120
