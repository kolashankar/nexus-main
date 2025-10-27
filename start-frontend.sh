#!/bin/bash
# Start Karma Nexus Frontend Server

cd "$(dirname "$0")/frontend"

echo "Starting Karma Nexus Frontend Server..."
echo "========================================"
echo ""

# Start development server
npm run dev
