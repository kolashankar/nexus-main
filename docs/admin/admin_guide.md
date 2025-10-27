# Administrator Guide - Karma Nexus

Complete guide for system administrators managing Karma Nexus.

## Overview

As an administrator, you're responsible for:
- System health and uptime
- User management
- Data integrity
- Performance monitoring
- Security
- Backups

## Admin Access

### Login

Admin panel: `https://yourdomain.com/admin`

**Credentials:**
- Set during deployment
- Stored in environment variables
- Never commit to Git

### Admin API Endpoints

All admin endpoints require admin authentication:

```http
GET /api/admin/stats
Authorization: Bearer <admin_token>
```

## Dashboard

### System Stats

```bash
# Get overall system statistics
curl -H "Authorization: Bearer <token>" \
  http://localhost/api/admin/stats
```

**Response:**
```json
{
  "users": {
    "total": 15000,
    "online": 850,
    "new_today": 45
  },
  "system": {
    "cpu_percent": 65,
    "memory_percent": 72,
    "disk_percent": 45
  },
  "api": {
    "requests_per_minute": 1250,
    "avg_response_time": 0.045,
    "error_rate": 0.02
  },
  "database": {
    "collections": 12,
    "total_documents": 5000000,
    "data_size_gb": 15.5
  }
}
```

## User Management

### View Users

```bash
# List users
curl -H "Authorization: Bearer <token>" \
  "http://localhost/api/admin/users?page=1&limit=50"
```

### Ban User

```bash
# Ban a user
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"reason": "Violating terms of service"}' \
  http://localhost/api/admin/ban-user/USER_ID
```

### Unban User

```bash
# Unban a user
curl -X POST \
  -H "Authorization: Bearer <token>" \
  http://localhost/api/admin/unban-user/USER_ID
```

### Reset Password

```bash
# Reset user password
curl -X POST \
  -H "Authorization: Bearer <token>" \
  http://localhost/api/admin/reset-password/USER_ID
```

## Content Moderation

### Reports

```bash
# View user reports
curl -H "Authorization: Bearer <token>" \
  "http://localhost/api/admin/reports?status=pending"
```

### Handle Report

```bash
# Resolve a report
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"action": "ban", "duration": "7d", "note": "Harassment"}' \
  http://localhost/api/admin/reports/REPORT_ID/resolve
```

## Game Management

### Trigger Events

```bash
# Trigger a world event
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "golden_age",
    "duration": 3600
  }' \
  http://localhost/api/admin/trigger-event
```

**Available events:**
- `golden_age` - Double XP and credits
- `the_purge` - No karma penalties
- `meteor_shower` - Rare resources
- `economic_collapse` - Market volatility

### Adjust Economy

```bash
# Adjust global prices
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"multiplier": 0.9}' \
  http://localhost/api/admin/adjust-prices
```

### Season Management

```bash
# End current season
curl -X POST \
  -H "Authorization: Bearer <token>" \
  http://localhost/api/admin/season/end

# Start new season
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "season_number": 2,
    "duration_days": 90,
    "theme": "Shadow Wars"
  }' \
  http://localhost/api/admin/season/start
```

## Monitoring

### Real-time Monitoring

**Access Grafana:**
http://localhost:3001

**Dashboards:**
- System Overview
- API Performance
- Database Metrics
- User Activity
- AI API Usage

### Logs

```bash
# View live logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend

# View errors only
docker-compose logs -f backend | grep ERROR

# Export logs
docker-compose logs --since 24h > logs_24h.txt
```

**Log locations:**
- Application: `/var/log/karma-nexus/app.log`
- Errors: `/var/log/karma-nexus/error.log`
- Access: `/var/log/karma-nexus/access.log`
- AI calls: `/var/log/karma-nexus/ai.log`
- Database: `/var/log/karma-nexus/database.log`

### Alerts

**Configure in Prometheus:**
`/app/config/alerts.yml`

**Alert channels:**
- Email
- Slack
- PagerDuty
- Discord

**Key alerts:**
- Service down
- High error rate
- Database issues
- High resource usage
- Security issues

## Performance

### Database Optimization

```bash
# Check slow queries
docker-compose exec mongodb mongosh --eval "
  db.setProfilingLevel(2);
  db.system.profile.find().sort({millis: -1}).limit(10);
"

# Add indexes
docker-compose exec mongodb mongosh --eval "
  use karma_nexus;
  db.players.createIndex({username: 1}, {unique: true});
  db.players.createIndex({karma_points: -1});
  db.actions.createIndex({timestamp: -1});
"

# Compact database
docker-compose exec mongodb mongosh --eval "
  use karma_nexus;
  db.runCommand({compact: 'players'});
"
```

### Cache Management

```bash
# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL

# Check cache hit rate
docker-compose exec redis redis-cli INFO stats | grep hits

# Monitor cache
docker-compose exec redis redis-cli MONITOR
```

### API Performance

```bash
# Check slow endpoints
curl -H "Authorization: Bearer <token>" \
  http://localhost/api/admin/performance/slow-endpoints

# Check AI API costs
curl -H "Authorization: Bearer <token>" \
  http://localhost/api/health/metrics/ai
```

## Backups

### Manual Backup

```bash
# Full system backup
sudo ./scripts/backup.sh
```

### Automated Backups

**Configured in cron:**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /app/karma-nexus/scripts/backup.sh >> /var/log/backup.log 2>&1
```

### Verify Backups

```bash
# List backups
ls -lh /backups/karma-nexus/

# Test restore (staging environment)
sudo ./scripts/rollback.sh backup_20240101_020000.tar.gz
```

### Offsite Backup

**S3 sync:**
```bash
# Configure AWS CLI
aws configure

# Sync backups to S3
aws s3 sync /backups/karma-nexus/ s3://karma-nexus-backups/
```

## Security

### Security Audit

```bash
# Check for vulnerabilities
docker-compose exec backend pip-audit

# Check dependencies
docker-compose exec frontend yarn audit

# Scan with Trivy
trivy image karma-nexus-backend:latest
```

### Update Security Patches

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker images
docker-compose pull
docker-compose up -d
```

### Review Access Logs

```bash
# Check failed login attempts
grep "401" /var/log/karma-nexus/access.log | tail -50

# Check suspicious activity
grep -E "(sql|script|eval)" /var/log/karma-nexus/access.log
```

## Maintenance

### Scheduled Maintenance

```bash
# 1. Notify users (24h in advance)
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -d '{"message": "Maintenance scheduled..."}' \
  http://localhost/api/admin/broadcast

# 2. Enable maintenance mode
docker-compose exec backend python -c "
  from backend.core.config import settings
  settings.MAINTENANCE_MODE = True
"

# 3. Perform maintenance
./scripts/backup.sh
./scripts/deploy.sh production

# 4. Disable maintenance mode
docker-compose exec backend python -c "
  from backend.core.config import settings
  settings.MAINTENANCE_MODE = False
"

# 5. Verify
curl http://localhost/health
```

### Emergency Maintenance

```bash
# Quick rollback
sudo ./scripts/rollback.sh <backup_file>

# If rollback fails, restore from backup
sudo ./scripts/restore.sh <backup_file>
```

## Troubleshooting

See [Troubleshooting Guide](./troubleshooting.md) for common issues and solutions.

## Best Practices

### Daily Tasks
- [ ] Check system health dashboard
- [ ] Review error logs
- [ ] Monitor AI API costs
- [ ] Check backup status

### Weekly Tasks
- [ ] Review user reports
- [ ] Analyze performance metrics
- [ ] Update documentation
- [ ] Security audit

### Monthly Tasks
- [ ] Review and optimize database
- [ ] Update dependencies
- [ ] Capacity planning
- [ ] Disaster recovery test

## Support

### Documentation
- [Deployment Guide](../technical/deployment.md)
- [Monitoring Guide](./monitoring.md)
- [Backup & Recovery](./backup_recovery.md)
- [Troubleshooting](./troubleshooting.md)

### Contact
- **Email**: [admin-support@karmanexus.com](mailto:admin-support@karmanexus.com)
- **Discord**: [Admin channel](https://discord.gg/karmanexus-admin)
- **On-call**: Check PagerDuty
