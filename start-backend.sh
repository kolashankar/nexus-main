#!/bin/bash
# Start Karma Nexus Backend Server

cd "$(dirname "$0")/backend"

echo "Starting Karma Nexus Backend Server..."
echo "======================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Start uvicorn server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
