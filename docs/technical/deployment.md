# Deployment Guide - Karma Nexus

Complete guide for deploying Karma Nexus to production.

## Prerequisites

### System Requirements
- **OS**: Ubuntu 22.04 LTS or newer
- **CPU**: 4+ cores
- **RAM**: 16GB minimum, 32GB recommended
- **Disk**: 100GB SSD minimum
- **Network**: Static IP, open ports 80, 443

### Software Requirements
- Docker 24.0+
- Docker Compose 2.20+
- Git
- nginx (reverse proxy)
- SSL certificates (Let's Encrypt)

## Quick Deployment

### 1. Clone Repository
```bash
git clone https://github.com/karmanexus/karmanexus.git
cd karmanexus
```

### 2. Configure Environment
```bash
cp .env.example .env
nano .env
```

**Required environment variables:**
```bash
# Database
MONGO_URL=mongodb://admin:password@mongodb:27017/karma_nexus?authSource=admin
MONGO_USERNAME=admin
MONGO_PASSWORD=your_secure_password_here

# Redis
REDIS_URL=redis://:redispassword@redis:6379/0
REDIS_PASSWORD=your_redis_password_here

# JWT
JWT_SECRET=your_super_secret_jwt_key_change_this

# AI
GEMINI_API_KEY=your_GEMINI_API_KEY_here

# App
REACT_APP_BACKEND_URL=https://api.yourdomain.com
ENVIRONMENT=production
```

### 3. Deploy with Docker Compose
```bash
# Build and start all services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Initialize Database
```bash
# Run database migrations
docker-compose exec backend python -m alembic upgrade head

# Seed initial data (optional)
docker-compose exec backend python scripts/seed_data.py
```

### 5. Configure SSL
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Production Setup

### Docker Compose Configuration

See `/app/docker-compose.yml` for the complete configuration.

**Services:**
- `mongodb` - Database (port 27017)
- `redis` - Cache (port 6379)
- `backend` - FastAPI API (port 8001)
- `frontend` - React app (port 3000)
- `nginx` - Reverse proxy (ports 80, 443)

### Nginx Configuration

See `/app/nginx/nginx.conf` for the complete configuration.

**Features:**
- Reverse proxy for backend API
- WebSocket support
- Static file serving
- SSL termination
- Rate limiting
- Gzip compression

### Supervisor Configuration

See `/app/backend/supervisord.conf` for process management.

**Managed processes:**
- `backend` - FastAPI server (4 workers)
- `celery-worker` - Background tasks
- `celery-beat` - Scheduled tasks

## Monitoring Setup

### Prometheus

```bash
# Add Prometheus to docker-compose
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

**Access**: http://localhost:9090

### Grafana

```bash
# Import dashboard
curl -X POST http://admin:admin@localhost:3001/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @config/grafana-dashboard.json
```

**Access**: http://localhost:3001  
**Default credentials**: admin / admin

### Alertmanager

Configure alerts in `/app/config/alerts.yml`.

**Alerts:**
- High error rate
- Slow API responses
- Database down
- High resource usage
- Service down

## Backup & Recovery

### Automated Backups

```bash
# Run backup script
./scripts/backup.sh

# Schedule with cron
crontab -e
```

Add:
```cron
# Daily backup at 2 AM
0 2 * * * /app/karma-nexus/scripts/backup.sh
```

### Manual Backup

```bash
# Database backup
docker-compose exec mongodb mongodump \
  --uri="mongodb://admin:password@localhost:27017/karma_nexus?authSource=admin" \
  --out=/tmp/backup

# Copy backup
docker cp karma-nexus-mongodb:/tmp/backup ./backup

# Application backup
tar -czf app-backup.tar.gz /app/karma-nexus
```

### Restore

```bash
# Stop services
docker-compose down

# Restore database
docker-compose up -d mongodb
docker cp ./backup karma-nexus-mongodb:/tmp/backup
docker-compose exec mongodb mongorestore \
  --uri="mongodb://admin:password@localhost:27017" \
  /tmp/backup

# Restore application
tar -xzf app-backup.tar.gz -C /

# Restart services
docker-compose up -d
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend workers
docker-compose up -d --scale backend=4

# Scale Celery workers
docker-compose up -d --scale celery-worker=8
```

### Load Balancing

Use nginx upstream:

```nginx
upstream backend {
    least_conn;
    server backend-1:8001;
    server backend-2:8001;
    server backend-3:8001;
    server backend-4:8001;
}
```

### Database Scaling

**MongoDB Replica Set:**

```yaml
# docker-compose.yml
mongodb-primary:
  image: mongo:7.0
  command: --replSet rs0

mongodb-secondary:
  image: mongo:7.0
  command: --replSet rs0
```

## Security

### Firewall

```bash
# Configure UFW
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### Secrets Management

**Use Docker secrets:**

```yaml
secrets:
  mongo_password:
    external: true
  jwt_secret:
    external: true

services:
  backend:
    secrets:
      - mongo_password
      - jwt_secret
```

### Security Headers

Configured in nginx:
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Referrer-Policy

## CI/CD Pipeline

See `.github/workflows/ci-cd.yml` for automated deployment.

**Pipeline stages:**
1. Lint and test
2. Build Docker images
3. Push to registry
4. Deploy to production
5. Run health checks
6. Notify team

## Maintenance

### Update Application

```bash
# Run deployment script
sudo ./scripts/deploy.sh production
```

### Update Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
yarn upgrade
```

### Database Migrations

```bash
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec backend alembic upgrade head

# Rollback
docker-compose exec backend alembic downgrade -1
```

### Cleanup

```bash
# Remove old Docker images
docker system prune -af

# Clean old backups
find /backups -mtime +30 -delete

# Rotate logs
docker-compose exec backend logrotate /etc/logrotate.conf
```

## Troubleshooting

### Common Issues

**Services won't start:**
```bash
# Check logs
docker-compose logs -f

# Check resource usage
docker stats

# Restart services
docker-compose restart
```

**Database connection issues:**
```bash
# Check MongoDB
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"

# Check Redis
docker-compose exec redis redis-cli ping
```

**High memory usage:**
```bash
# Check processes
docker stats

# Restart heavy services
docker-compose restart backend
```

### Health Checks

```bash
# Overall health
curl http://localhost/health

# Detailed health
curl http://localhost/api/health/detailed

# Metrics
curl http://localhost/api/health/metrics
```

## Support

- **Documentation**: [https://docs.karmanexus.com](https://docs.karmanexus.com)
- **Issues**: [GitHub Issues](https://github.com/karmanexus/karmanexus/issues)
- **Email**: [devops@karmanexus.com](mailto:devops@karmanexus.com)
- **Discord**: [Join our community](https://discord.gg/karmanexus)
