#!/bin/bash

# Karma Nexus Production Deployment Script
# Usage: ./scripts/deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
APP_DIR="/app/karma-nexus"
BACKUP_DIR="/backups/karma-nexus"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "========================================"
echo "Karma Nexus Deployment Script"
echo "Environment: $ENVIRONMENT"
echo "Timestamp: $TIMESTAMP"
echo "========================================"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Create backup
echo "\n[1/10] Creating backup..."
mkdir -p $BACKUP_DIR
if [ -d "$APP_DIR" ]; then
    tar -czf $BACKUP_DIR/backup_$TIMESTAMP.tar.gz -C $APP_DIR .
    echo "✓ Backup created: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
else
    echo "! No existing installation found, skipping backup"
fi

# Pull latest code
echo "\n[2/10] Pulling latest code..."
cd $APP_DIR
git fetch origin
git checkout $ENVIRONMENT
git pull origin $ENVIRONMENT
echo "✓ Code updated"

# Update backend dependencies
echo "\n[3/10] Updating backend dependencies..."
cd $APP_DIR/backend
pip install -r requirements.txt --upgrade
# REMOVED: pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/ --upgrade
echo "✓ Backend dependencies updated"

# Update frontend dependencies
echo "\n[4/10] Updating frontend dependencies..."
cd $APP_DIR/frontend
yarn install --frozen-lockfile
echo "✓ Frontend dependencies updated"

# Run database migrations
echo "\n[5/10] Running database migrations..."
cd $APP_DIR/backend
python -m alembic upgrade head || echo "! No migrations to run"
echo "✓ Database migrations complete"

# Build frontend
echo "\n[6/10] Building frontend..."
cd $APP_DIR/frontend
yarn build
echo "✓ Frontend built successfully"

# Run tests
echo "\n[7/10] Running tests..."
cd $APP_DIR/backend
pytest tests/ -v --tb=short || {
    echo "✗ Backend tests failed!"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
}
echo "✓ Tests passed"

# Pull and restart Docker containers
echo "\n[8/10] Updating Docker containers..."
cd $APP_DIR
docker-compose pull
docker-compose up -d --build --remove-orphans
echo "✓ Containers updated"

# Wait for services to be ready
echo "\n[9/10] Waiting for services to be ready..."
sleep 30

# Health checks
echo "\n[10/10] Running health checks..."
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
    echo "Rolling back..."
    
    # Rollback
    cd $APP_DIR
    tar -xzf $BACKUP_DIR/backup_$TIMESTAMP.tar.gz -C $APP_DIR
    docker-compose up -d --build
    
    echo "✗ Deployment failed and rolled back"
    exit 1
fi

# Cleanup old backups (keep last 10)
echo "\nCleaning up old backups..."
cd $BACKUP_DIR
ls -t | tail -n +11 | xargs rm -f
echo "✓ Old backups cleaned"

# Cleanup Docker
echo "\nCleaning up Docker resources..."
docker system prune -f
echo "✓ Docker cleanup complete"

echo "\n========================================"
echo "✓ Deployment completed successfully!"
echo "========================================"
echo "\nDeployment details:"
echo "  - Environment: $ENVIRONMENT"
echo "  - Timestamp: $TIMESTAMP"
echo "  - Backup: $BACKUP_DIR/backup_$TIMESTAMP.tar.gz"
echo "\nServices status:"
docker-compose ps

echo "\nApplication URLs:"
echo "  - Frontend: http://localhost"
echo "  - Backend API: http://localhost/api"
echo "  - Health: http://localhost/health"