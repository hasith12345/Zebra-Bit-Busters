#!/bin/bash

echo "🚨 Starting Simple Virtual Queue Alert System..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed."
    exit 1
fi

# Check if Node.js is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed."
    exit 1
fi

# Install Python dependencies if needed
echo "📦 Installing Python dependencies..."
pip3 install flask flask-cors > /dev/null 2>&1

# Start Python backend in background
echo "🐍 Starting backend server (reads real queue data)..."
python3 simple_backend.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start React frontend
echo "📱 Starting display (shows large QR code when queue >= 6)..."
npm start &
FRONTEND_PID=$!

echo "✅ System started!"
echo ""
echo "🎯 How it works:"
echo "  - Reads real data from queue_monitoring.jsonl"
echo "  - Shows LARGE QR CODE when any station has 6+ customers"
echo "  - Customer alerts appear when accessing via QR code"
echo ""
echo "📱 Access: http://localhost:3000"
echo "🔌 API: http://localhost:5001/api/health"
echo ""
echo "Press Ctrl+C to stop"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping system..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM
wait