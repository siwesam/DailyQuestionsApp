#!/bin/bash
set -e

echo "=========================================="
echo "Starting application initialization..."
echo "=========================================="

# Run database migrations
echo "Running database migrations..."
python migrations/add_ai_quote_fields.py || echo "Migration already applied or failed (continuing anyway)"

# Initialize database with questions if needed
echo "Checking database initialization..."
python init_db.py || echo "Database already initialized"

echo "=========================================="
echo "Starting FastAPI application..."
echo "=========================================="

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

# Made with Bob
