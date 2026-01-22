#!/bin/bash

echo "=========================================="
echo "Daily Questions App - Stopping..."
echo "=========================================="
echo ""

# Kill backend
echo "🛑 Stopping Backend Server..."
pkill -f "uvicorn app.main:app"

# Kill frontend
echo "🛑 Stopping Frontend Server..."
pkill -f "npm run dev"

sleep 1

echo ""
echo "✅ Application Stopped Successfully!"
echo "=========================================="

# Made with Bob
