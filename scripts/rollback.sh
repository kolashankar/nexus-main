#!/bin/bash

# Karma Nexus Rollback Script
# Usage: ./scripts/rollback.sh [backup_file]

set -e

APP_DIR="/app/karma-nexus"
BACKUP_DIR="/backups/karma-nexus"

echo "========================================"
echo "Karma Nexus Rollback Script"
echo "========================================"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# List available backups if no argument provided
if [ -z "$1" ]; then
    echo "\nAvailable backups:"
    ls -lht $BACKUP_DIR/*.tar.gz | head -10
    echo "\nUsage: ./scripts/rollback.sh [backup_file]"
    echo "Example: ./scripts/rollback.sh backup_20240101_120000.tar.gz"
    exit 1
fi

BACKUP_FILE="$1"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_FILE"

# Check if backup exists
if [ ! -f "$BACKUP_PATH" ]; then
    echo "✗ Backup file not found: $BACKUP_PATH"
    exit 1
fi

echo "\nRollback details:"
echo "  - Backup file: $BACKUP_FILE"
echo "  - Backup size: $(du -h $BACKUP_PATH | cut -f1)"
echo "  - Backup date: $(stat -c %y $BACKUP_PATH)"

# Confirm rollback
read -p "\nAre you sure you want to rollback? This will overwrite current installation (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Rollback cancelled"
    exit 0
fi

# Stop services
echo "\n[1/5] Stopping services..."
cd $APP_DIR
docker-compose down
echo "✓ Services stopped"

# Create backup of current state
echo "\n[2/5] Backing up current state..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf $BACKUP_DIR/pre_rollback_$TIMESTAMP.tar.gz -C $APP_DIR .
echo "✓ Current state backed up to: pre_rollback_$TIMESTAMP.tar.gz"

# Extract backup
echo "\n[3/5] Extracting backup..."
rm -rf $APP_DIR/*
tar -xzf $BACKUP_PATH -C $APP_DIR
echo "✓ Backup extracted"

# Restart services
echo "\n[4/5] Restarting services..."
cd $APP_DIR
docker-compose up -d --build
echo "✓ Services restarted"

# Health check
echo "\n[5/5] Running health check..."
sleep 30

max_attempts=10
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost/health > /dev/null 2>&1; then
        echo "✓ Health check passed"
        break
    fi
    attempt=$((attempt + 1))
    echo "Attempt $attempt/$max_attempts failed, retrying..."
    sleep 5
done

if [ $attempt -eq $max_attempts ]; then
    echo "✗ Health check failed after $max_attempts attempts"
    echo "Please check logs: docker-compose logs"
    exit 1
fi

echo "\n========================================"
echo "✓ Rollback completed successfully!"
echo "========================================"
echo "\nRollback details:"
echo "  - Restored from: $BACKUP_FILE"
echo "  - Current state backup: pre_rollback_$TIMESTAMP.tar.gz"
echo "\nServices status:"
docker-compose ps
