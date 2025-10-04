#!/bin/bash

# Virtual Queue System Startup Script
# This script starts both the Python backend and React frontend

echo "🚀 Starting Virtual Queue System..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Start Python backend in background
echo "🐍 Starting Python backend server..."
python3 queue_backend.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start React frontend
echo "⚛️ Starting React frontend..."
npm start &
FRONTEND_PID=$!

echo "✅ Virtual Queue System started!"
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:5001"
echo ""
echo "📋 Available endpoints:"
echo "  - GET  /api/stations           - Get all station data"
echo "  - POST /api/virtual-queue/join - Join virtual queue"
echo "  - GET  /api/virtual-queue/status/<token> - Check queue status"
echo "  - GET  /api/health             - Health check"
echo ""
echo "Press Ctrl+C to stop both services"

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Stopping Virtual Queue System..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend server stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend server stopped"
    fi
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait