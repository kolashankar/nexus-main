#!/bin/bash

# Karma Nexus Backup Script
# Usage: ./scripts/backup.sh

set -e

APP_DIR="/app/karma-nexus"
BACKUP_DIR="/backups/karma-nexus"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATE=$(date +%Y-%m-%d)

echo "========================================"
echo "Karma Nexus Backup Script"
echo "Timestamp: $TIMESTAMP"
echo "========================================"

# Create backup directories
mkdir -p $BACKUP_DIR/database
mkdir -p $BACKUP_DIR/files
mkdir -p $BACKUP_DIR/logs

# Backup MongoDB database
echo "\n[1/5] Backing up MongoDB database..."
MONGO_CONTAINER=$(docker-compose ps -q mongodb)
if [ -z "$MONGO_CONTAINER" ]; then
    echo "✗ MongoDB container not running"
    exit 1
fi

docker exec $MONGO_CONTAINER mongodump \
    --uri="mongodb://admin:password@localhost:27017/karma_nexus?authSource=admin" \
    --out=/tmp/backup_$TIMESTAMP \
    --gzip

docker cp $MONGO_CONTAINER:/tmp/backup_$TIMESTAMP $BACKUP_DIR/database/
docker exec $MONGO_CONTAINER rm -rf /tmp/backup_$TIMESTAMP

echo "✓ Database backed up to: $BACKUP_DIR/database/backup_$TIMESTAMP"

# Backup Redis data
echo "\n[2/5] Backing up Redis data..."
REDIS_CONTAINER=$(docker-compose ps -q redis)
if [ -z "$REDIS_CONTAINER" ]; then
    echo "! Redis container not running, skipping Redis backup"
else
    docker exec $REDIS_CONTAINER redis-cli --rdb /tmp/redis_backup_$TIMESTAMP.rdb
    docker cp $REDIS_CONTAINER:/tmp/redis_backup_$TIMESTAMP.rdb $BACKUP_DIR/database/
    echo "✓ Redis backed up to: $BACKUP_DIR/database/redis_backup_$TIMESTAMP.rdb"
fi

# Backup application files
echo "\n[3/5] Backing up application files..."
tar -czf $BACKUP_DIR/files/app_backup_$TIMESTAMP.tar.gz \
    -C $APP_DIR \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='build' \
    --exclude='dist' \
    .

echo "✓ Application files backed up to: $BACKUP_DIR/files/app_backup_$TIMESTAMP.tar.gz"

# Backup logs
echo "\n[4/5] Backing up logs..."
tar -czf $BACKUP_DIR/logs/logs_backup_$TIMESTAMP.tar.gz \
    /var/log/supervisor/*.log \
    /var/log/nginx/*.log \
    2>/dev/null || echo "! Some logs may not exist"

echo "✓ Logs backed up to: $BACKUP_DIR/logs/logs_backup_$TIMESTAMP.tar.gz"

# Create consolidated backup
echo "\n[5/5] Creating consolidated backup..."
cd $BACKUP_DIR
tar -czf karma_nexus_full_backup_$TIMESTAMP.tar.gz \
    database/backup_$TIMESTAMP \
    database/redis_backup_$TIMESTAMP.rdb \
    files/app_backup_$TIMESTAMP.tar.gz \
    logs/logs_backup_$TIMESTAMP.tar.gz \
    2>/dev/null || true

echo "✓ Consolidated backup created: karma_nexus_full_backup_$TIMESTAMP.tar.gz"

# Calculate sizes
DB_SIZE=$(du -h $BACKUP_DIR/database/backup_$TIMESTAMP | cut -f1)
APP_SIZE=$(du -h $BACKUP_DIR/files/app_backup_$TIMESTAMP.tar.gz | cut -f1)
FULL_SIZE=$(du -h $BACKUP_DIR/karma_nexus_full_backup_$TIMESTAMP.tar.gz | cut -f1)

# Cleanup old backups (keep last 30 days)
echo "\nCleaning up old backups..."
find $BACKUP_DIR -name "karma_nexus_full_backup_*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR/database -name "backup_*" -mtime +30 -exec rm -rf {} \;
find $BACKUP_DIR/files -name "app_backup_*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR/logs -name "logs_backup_*.tar.gz" -mtime +30 -delete
echo "✓ Old backups cleaned (kept last 30 days)"

# Upload to S3 (optional, requires AWS CLI)
if command -v aws &> /dev/null; then
    echo "\nUploading to S3..."
    aws s3 cp $BACKUP_DIR/karma_nexus_full_backup_$TIMESTAMP.tar.gz \
        s3://karma-nexus-backups/$DATE/ || echo "! S3 upload failed or not configured"
fi

echo "\n========================================"
echo "✓ Backup completed successfully!"
echo "========================================"
echo "\nBackup details:"
echo "  - Timestamp: $TIMESTAMP"
echo "  - Database size: $DB_SIZE"
echo "  - Application size: $APP_SIZE"
echo "  - Total size: $FULL_SIZE"
echo "  - Location: $BACKUP_DIR/karma_nexus_full_backup_$TIMESTAMP.tar.gz"
echo "\nBackup structure:"
echo "  - Database: $BACKUP_DIR/database/backup_$TIMESTAMP"
echo "  - Redis: $BACKUP_DIR/database/redis_backup_$TIMESTAMP.rdb"
echo "  - Files: $BACKUP_DIR/files/app_backup_$TIMESTAMP.tar.gz"
echo "  - Logs: $BACKUP_DIR/logs/logs_backup_$TIMESTAMP.tar.gz"
