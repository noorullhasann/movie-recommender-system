#!/bin/bash

# Movie Recommender System - Quick Start Script
# This script starts both the backend and frontend servers

echo "🎬 Starting Movie Recommender System..."
echo ""

# Check if required commands exist
check_command() {
  if ! command -v $1 &> /dev/null; then
    echo "❌ Error: $1 is not installed"
    exit 1
  fi
}

check_command python3
check_command node
check_command npm

# Start backend in background
echo "🔧 Starting Backend (Flask)..."
cd backend
python3 app.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   API: http://127.0.0.1:5000"
echo ""

# Wait for backend to start
sleep 2

# Start frontend
echo "🎨 Starting Frontend (React + Vite)..."
cd ../frontend
npm start

# Cleanup
echo ""
echo "Stopping services..."
kill $BACKEND_PID
echo "✅ All services stopped"
