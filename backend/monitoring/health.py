"""Health check system for monitoring service status."""

import asyncio
from typing import Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as aioredis


class HealthChecker:
    """Check health of various system components."""

    def __init__(self, mongo_url: str, redis_url: str):
        self.mongo_url = mongo_url
        self.redis_url = redis_url
        self.last_check = {}

    async def check_mongodb(self) -> Dict[str, Any]:
        """Check MongoDB connectivity and status."""
        try:
            client = AsyncIOMotorClient(
                self.mongo_url, serverSelectionTimeoutMS=5000)
            await client.admin.command('ping')

            # Get database stats
            db = client.get_default_database()
            stats = await db.command('dbStats')

            result = {
                'status': 'healthy',
                'latency_ms': 0,
                'collections': stats.get('collections', 0),
                'data_size': stats.get('dataSize', 0),
                'storage_size': stats.get('storageSize', 0),
            }
        except Exception as e:
            result = {
                'status': 'unhealthy',
                'error': str(e)
            }
        finally:
            if 'client' in locals():
                client.close()

        self.last_check['mongodb'] = result
        return result

    async def check_redis(self) -> Dict[str, Any]:
        """Check Redis connectivity and status."""
        try:
            redis_client = aioredis.from_url(self.redis_url)
            await redis_client.ping()

            # Get Redis info
            info = await redis_client.info()

            result = {
                'status': 'healthy',
                'version': info.get('redis_version', 'unknown'),
                'used_memory': info.get('used_memory_human', 'unknown'),
                'connected_clients': info.get('connected_clients', 0),
            }
        except Exception as e:
            result = {
                'status': 'unhealthy',
                'error': str(e)
            }
        finally:
            if 'redis_client' in locals():
                await redis_client.close()

        self.last_check['redis'] = result
        return result

    async def check_disk_space(self) -> Dict[str, Any]:
        """Check disk space availability."""
        import shutil

        try:
            total, used, free = shutil.disk_usage('/')
            percent_used = (used / total) * 100

            status = 'healthy'
            if percent_used > 90:
                status = 'critical'
            elif percent_used > 80:
                status = 'warning'

            result = {
                'status': status,
                'total_gb': round(total / (1024**3), 2),
                'used_gb': round(used / (1024**3), 2),
                'free_gb': round(free / (1024**3), 2),
                'percent_used': round(percent_used, 2)
            }
        except Exception as e:
            result = {
                'status': 'unhealthy',
                'error': str(e)
            }

        self.last_check['disk'] = result
        return result

    async def check_memory(self) -> Dict[str, Any]:
        """Check memory usage."""
        import psutil

        try:
            memory = psutil.virtual_memory()

            status = 'healthy'
            if memory.percent > 90:
                status = 'critical'
            elif memory.percent > 80:
                status = 'warning'

            result = {
                'status': status,
                'total_gb': round(memory.total / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'percent_used': round(memory.percent, 2)
            }
        except Exception as e:
            result = {
                'status': 'unhealthy',
                'error': str(e)
            }

        self.last_check['memory'] = result
        return result

    async def check_cpu(self) -> Dict[str, Any]:
        """Check CPU usage."""
        import psutil

        try:
            cpu_percent = psutil.cpu_percent(interval=1)

            status = 'healthy'
            if cpu_percent > 90:
                status = 'critical'
            elif cpu_percent > 80:
                status = 'warning'

            result = {
                'status': status,
                'percent_used': round(cpu_percent, 2),
                'count': psutil.cpu_count()
            }
        except Exception as e:
            result = {
                'status': 'unhealthy',
                'error': str(e)
            }

        self.last_check['cpu'] = result
        return result

    async def check_all(self) -> Dict[str, Any]:
        """Run all health checks."""
        checks = await asyncio.gather(
            self.check_mongodb(),
            self.check_redis(),
            self.check_disk_space(),
            self.check_memory(),
            self.check_cpu(),
            return_exceptions=True
        )

        mongodb_health, redis_health, disk_health, memory_health, cpu_health = checks

        # Determine overall status
        all_healthy = all(
            check.get('status') == 'healthy'
            for check in [mongodb_health, redis_health, disk_health, memory_health, cpu_health]
            if isinstance(check, dict)
        )

        overall_status = 'healthy' if all_healthy else 'degraded'

        # Check for critical issues
        if any(
            check.get('status') == 'critical'
            for check in [disk_health, memory_health, cpu_health]
            if isinstance(check, dict)
        ):
            overall_status = 'critical'

        return {
            'status': overall_status,
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {
                'mongodb': mongodb_health if isinstance(mongodb_health, dict) else {'status': 'error', 'error': str(mongodb_health)},
                'redis': redis_health if isinstance(redis_health, dict) else {'status': 'error', 'error': str(redis_health)},
                'disk': disk_health if isinstance(disk_health, dict) else {'status': 'error', 'error': str(disk_health)},
                'memory': memory_health if isinstance(memory_health, dict) else {'status': 'error', 'error': str(memory_health)},
                'cpu': cpu_health if isinstance(cpu_health, dict) else {'status': 'error', 'error': str(cpu_health)},
            }
        }

    def get_last_check(self) -> Dict[str, Any]:
        """Get results of last health check."""
        return self.last_check
