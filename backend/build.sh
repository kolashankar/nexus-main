#!/bin/bash
set -e

echo "🚀 Starting Karma Nexus Backend Build..."

# Upgrade pip and build tools
echo "📦 Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

# Install requirements
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "✅ Build completed successfully!"
