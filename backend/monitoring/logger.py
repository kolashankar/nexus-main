"""Centralized logging configuration."""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
import json


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for better parsing."""

    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, 'player_id'):
            log_data['player_id'] = record.player_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'endpoint'):
            log_data['endpoint'] = record.endpoint

        return json.dumps(log_data)


def setup_logging(
    log_dir: str = '/var/log/karma-nexus',
    log_level: str = 'INFO',
    json_format: bool = False
):
    """Configure application logging."""

    # Create log directory
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Create formatters
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handlers
    # 1. General application log
    app_handler = RotatingFileHandler(
        f'{log_dir}/app.log',
        maxBytes=50 * 1024 * 1024,  # 50MB
        backupCount=10
    )
    app_handler.setFormatter(formatter)
    app_handler.setLevel(logging.INFO)
    root_logger.addHandler(app_handler)

    # 2. Error log
    error_handler = RotatingFileHandler(
        f'{log_dir}/error.log',
        maxBytes=50 * 1024 * 1024,  # 50MB
        backupCount=10
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    root_logger.addHandler(error_handler)

    # 3. Access log (timed rotation)
    access_handler = TimedRotatingFileHandler(
        f'{log_dir}/access.log',
        when='midnight',
        interval=1,
        backupCount=30
    )
    access_handler.setFormatter(formatter)
    access_handler.setLevel(logging.INFO)

    # Create access logger
    access_logger = logging.getLogger('access')
    access_logger.addHandler(access_handler)
    access_logger.setLevel(logging.INFO)

    # 4. AI calls log
    ai_handler = RotatingFileHandler(
        f'{log_dir}/ai.log',
        maxBytes=50 * 1024 * 1024,  # 50MB
        backupCount=10
    )
    ai_handler.setFormatter(formatter)

    ai_logger = logging.getLogger('ai')
    ai_logger.addHandler(ai_handler)
    ai_logger.setLevel(logging.INFO)

    # 5. Database operations log
    db_handler = RotatingFileHandler(
        f'{log_dir}/database.log',
        maxBytes=50 * 1024 * 1024,  # 50MB
        backupCount=10
    )
    db_handler.setFormatter(formatter)

    db_logger = logging.getLogger('database')
    db_logger.addHandler(db_handler)
    db_logger.setLevel(logging.INFO)

    # 6. WebSocket log
    ws_handler = RotatingFileHandler(
        f'{log_dir}/websocket.log',
        maxBytes=50 * 1024 * 1024,  # 50MB
        backupCount=10
    )
    ws_handler.setFormatter(formatter)

    ws_logger = logging.getLogger('websocket')
    ws_logger.addHandler(ws_handler)
    ws_logger.setLevel(logging.INFO)

    logging.info(
        f'Logging configured - Level: {log_level}, Directory: {log_dir}')


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


class RequestLogger:
    """Log HTTP requests with context."""

    def __init__(self):
        self.logger = get_logger('access')

    def log_request(self, method: str, path: str, status: int, duration: float, **kwargs):
        """Log an HTTP request."""
        extra = {
            'method': method,
            'path': path,
            'status': status,
            'duration': duration,
            **kwargs
        }

        self.logger.info(
            f'{method} {path} - {status} - {duration:.3f}s',
            extra=extra
        )


class AILogger:
    """Log AI API calls with context."""

    def __init__(self):
        self.logger = get_logger('ai')

    def log_call(self, agent: str, prompt_tokens: int, completion_tokens: int,
                 cost: float, duration: float, **kwargs):
        """Log an AI API call."""
        extra = {
            'agent': agent,
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': prompt_tokens + completion_tokens,
            'cost': cost,
            'duration': duration,
            **kwargs
        }

        self.logger.info(
            f'{agent} - {prompt_tokens + completion_tokens} tokens - ${cost:.4f} - {duration:.2f}s',
            extra=extra
        )
