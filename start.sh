#!/bin/bash

echo "=========================================="
echo "Daily Questions App - Startup Script"
echo "=========================================="
echo ""

# Kill any existing processes
echo "🛑 Stopping any running instances..."
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
sleep 2

# Start backend
echo ""
echo "🚀 Starting Backend Server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 3

# Start frontend
echo ""
echo "🚀 Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "✅ Application Started Successfully!"
echo "=========================================="
echo ""
echo "📍 Backend:  http://localhost:8000"
echo "📍 Frontend: http://localhost:5173"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop the application, run: ./stop.sh"
echo "Or press Ctrl+C and run: pkill -f uvicorn && pkill -f 'npm run dev'"
echo "=========================================="

# Made with Bob
