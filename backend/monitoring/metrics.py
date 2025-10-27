"""Metrics collection and monitoring."""

import time
import psutil
from typing import Dict, Any
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio


class MetricsCollector:
    """Collect and store application metrics."""

    def __init__(self):
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.start_time = time.time()

    def record_request(self, endpoint: str, method: str, status: int, duration: float):
        """Record API request metrics."""
        self.metrics['requests'].append({
            'endpoint': endpoint,
            'method': method,
            'status': status,
            'duration': duration,
            'timestamp': datetime.utcnow()
        })
        self.counters[f'requests_{status}'] += 1
        self.counters['requests_total'] += 1

    def record_ai_call(self, agent: str, tokens: int, cost: float, duration: float):
        """Record AI API call metrics."""
        self.metrics['ai_calls'].append({
            'agent': agent,
            'tokens': tokens,
            'cost': cost,
            'duration': duration,
            'timestamp': datetime.utcnow()
        })
        self.counters[f'ai_calls_{agent}'] += 1
        self.counters['ai_tokens_total'] += tokens
        self.gauges['ai_cost_total'] += cost

    def record_db_query(self, collection: str, operation: str, duration: float):
        """Record database query metrics."""
        self.metrics['db_queries'].append({
            'collection': collection,
            'operation': operation,
            'duration': duration,
            'timestamp': datetime.utcnow()
        })
        self.counters[f'db_queries_{collection}'] += 1

    def record_websocket_event(self, event_type: str, room: str = None):
        """Record WebSocket event metrics."""
        self.metrics['websocket_events'].append({
            'event_type': event_type,
            'room': room,
            'timestamp': datetime.utcnow()
        })
        self.counters[f'ws_events_{event_type}'] += 1

    def record_player_action(self, action_type: str, player_id: str):
        """Record player action metrics."""
        self.metrics['player_actions'].append({
            'action_type': action_type,
            'player_id': player_id,
            'timestamp': datetime.utcnow()
        })
        self.counters[f'actions_{action_type}'] += 1

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'uptime_seconds': time.time() - self.start_time,
        }

    def get_api_metrics(self, window_minutes: int = 60) -> Dict[str, Any]:
        """Get API request metrics for the last N minutes."""
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        recent_requests = [
            r for r in self.metrics['requests']
            if r['timestamp'] > cutoff
        ]

        if not recent_requests:
            return {
                'total_requests': 0,
                'avg_response_time': 0,
                'requests_per_minute': 0,
                'error_rate': 0
            }

        total = len(recent_requests)
        avg_duration = sum(r['duration'] for r in recent_requests) / total
        errors = sum(1 for r in recent_requests if r['status'] >= 400)

        return {
            'total_requests': total,
            'avg_response_time': round(avg_duration, 3),
            'requests_per_minute': round(total / window_minutes, 2),
            'error_rate': round(errors / total * 100, 2) if total > 0 else 0,
            'status_codes': defaultdict(int, {
                f"{r['status']}": sum(1 for r in recent_requests if r['status'] == r['status'])
                for r in recent_requests
            })
        }

    def get_ai_metrics(self, window_minutes: int = 60) -> Dict[str, Any]:
        """Get AI API metrics for the last N minutes."""
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        recent_calls = [
            c for c in self.metrics['ai_calls']
            if c['timestamp'] > cutoff
        ]

        if not recent_calls:
            return {
                'total_calls': 0,
                'total_tokens': 0,
                'total_cost': 0,
                'avg_duration': 0
            }

        return {
            'total_calls': len(recent_calls),
            'total_tokens': sum(c['tokens'] for c in recent_calls),
            'total_cost': round(sum(c['cost'] for c in recent_calls), 4),
            'avg_duration': round(sum(c['duration'] for c in recent_calls) / len(recent_calls), 3),
            'by_agent': defaultdict(int, {
                agent: sum(1 for c in recent_calls if c['agent'] == agent)
                for agent in set(c['agent'] for c in recent_calls)
            })
        }

    def get_db_metrics(self, window_minutes: int = 60) -> Dict[str, Any]:
        """Get database metrics for the last N minutes."""
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        recent_queries = [
            q for q in self.metrics['db_queries']
            if q['timestamp'] > cutoff
        ]

        if not recent_queries:
            return {
                'total_queries': 0,
                'avg_duration': 0,
                'queries_per_minute': 0
            }

        return {
            'total_queries': len(recent_queries),
            'avg_duration': round(sum(q['duration'] for q in recent_queries) / len(recent_queries), 3),
            'queries_per_minute': round(len(recent_queries) / window_minutes, 2),
            'by_collection': defaultdict(int, {
                coll: sum(1 for q in recent_queries if q['collection'] == coll)
                for coll in set(q['collection'] for q in recent_queries)
            })
        }

    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        return {
            'system': self.get_system_metrics(),
            'api': self.get_api_metrics(),
            'ai': self.get_ai_metrics(),
            'database': self.get_db_metrics(),
            'counters': dict(self.counters),
            'gauges': dict(self.gauges),
            'uptime_seconds': time.time() - self.start_time
        }

    def cleanup_old_metrics(self, hours: int = 24):
        """Clean up metrics older than N hours."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        for metric_type in self.metrics:
            self.metrics[metric_type] = [
                m for m in self.metrics[metric_type]
                if m['timestamp'] > cutoff
            ]


# Global metrics collector instance
metrics_collector = MetricsCollector()


async def metrics_cleanup_task():
    """Background task to cleanup old metrics."""
    while True:
        await asyncio.sleep(3600)  # Every hour
        metrics_collector.cleanup_old_metrics()
