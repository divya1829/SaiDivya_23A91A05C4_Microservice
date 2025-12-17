#!/usr/bin/env sh
set -e

# Start cron daemon
cron

# Start FastAPI app
exec uvicorn app.app:app --host 0.0.0.0 --port 8080
