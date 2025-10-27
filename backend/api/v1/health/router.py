"""Health check routes."""

from fastapi import APIRouter
from typing import Dict, Any
import os

from backend.monitoring.health import HealthChecker
from backend.monitoring.metrics import metrics_collector

router = APIRouter(prefix="/health", tags=["health"])

# Initialize health checker
health_checker = HealthChecker(
    mongo_url=os.environ.get('MONGO_URL', 'mongodb://localhost:27017'),
    redis_url=os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
)


@router.get("", response_model=Dict[str, Any])
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "Karma Nexus API",
        "version": "2.0.0"
    }


@router.get("/detailed", response_model=Dict[str, Any])
async def detailed_health_check():
    """Detailed health check with all components."""
    health_status = await health_checker.check_all()
    return health_status


@router.get("/db", response_model=Dict[str, Any])
async def database_health():
    """Check database connectivity."""
    mongo_status = await health_checker.check_mongodb()
    redis_status = await health_checker.check_redis()

    return {
        "mongodb": mongo_status,
        "redis": redis_status
    }


@router.get("/system", response_model=Dict[str, Any])
async def system_health():
    """Check system resources."""
    disk_status = await health_checker.check_disk_space()
    memory_status = await health_checker.check_memory()
    cpu_status = await health_checker.check_cpu()

    return {
        "disk": disk_status,
        "memory": memory_status,
        "cpu": cpu_status
    }


@router.get("/metrics", response_model=Dict[str, Any])
async def metrics():
    """Get application metrics."""
    return metrics_collector.get_summary()


@router.get("/metrics/api", response_model=Dict[str, Any])
async def api_metrics(window_minutes: int = 60):
    """Get API metrics for specified time window."""
    return metrics_collector.get_api_metrics(window_minutes)


@router.get("/metrics/ai", response_model=Dict[str, Any])
async def ai_metrics(window_minutes: int = 60):
    """Get AI API metrics for specified time window."""
    return metrics_collector.get_ai_metrics(window_minutes)


@router.get("/metrics/db", response_model=Dict[str, Any])
async def db_metrics(window_minutes: int = 60):
    """Get database metrics for specified time window."""
    return metrics_collector.get_db_metrics(window_minutes)
