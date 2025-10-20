#!/bin/bash
# Startup script for GCS Bucket Viewer

set -e

echo "🚀 Starting GCS Bucket Viewer..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your GCS configuration."
    exit 1
fi

# Check if credentials file exists
CREDS_FILE=$(grep GOOGLE_APPLICATION_CREDENTIALS .env | cut -d '=' -f2)
if [ ! -f "$CREDS_FILE" ]; then
    echo "⚠️  Warning: GCS credentials file not found at $CREDS_FILE"
    echo "Please ensure your service account JSON file is in the correct location."
fi

# Install Python dependencies if needed
echo "📦 Installing Python dependencies..."
uv sync

# Install Node dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing Node dependencies..."
    cd frontend && npm install && cd ..
fi

# Start backend in background
echo "🐍 Starting FastAPI backend on port 8000..."
uv run python -m src.api &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "⚡ Starting Svelte frontend on port 5173..."
cd frontend && npm run dev &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM

echo ""
echo "✅ Application is running!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop..."

# Wait for processes
wait
