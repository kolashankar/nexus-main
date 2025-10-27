"""Configuration for The Architect AI"""

import os
from typing import Dict, Any


class ArchitectConfig:
    """Configuration settings for The Architect"""

    # AI Model settings
    MODEL = os.getenv("ARCHITECT_MODEL", "gpt-4o")
    TEMPERATURE = float(os.getenv("ARCHITECT_TEMPERATURE", "0.8"))
    MAX_TOKENS = int(os.getenv("ARCHITECT_MAX_TOKENS", "2000"))

    # Event timing
    MIN_EVENT_INTERVAL_HOURS = int(os.getenv("MIN_EVENT_INTERVAL", "6"))
    MAX_EVENT_DURATION_HOURS = int(os.getenv("MAX_EVENT_DURATION", "72"))

    # Trigger thresholds
    # Multiplier for karma thresholds
    KARMA_SENSITIVITY = float(os.getenv("KARMA_SENSITIVITY", "1.0"))
    AUTO_TRIGGER_ENABLED = os.getenv(
        "AUTO_TRIGGER_EVENTS", "true").lower() == "true"

    # Event generation
    USE_AI_GENERATION = os.getenv(
        "USE_AI_GENERATION", "true").lower() == "true"
    FALLBACK_TO_TEMPLATES = os.getenv(
        "FALLBACK_TO_TEMPLATES", "true").lower() == "true"

    # Caching
    CACHE_EVENTS = os.getenv("CACHE_EVENTS", "true").lower() == "true"
    CACHE_TTL_SECONDS = int(os.getenv("EVENT_CACHE_TTL", "3600"))  # 1 hour

    # Regional events
    REGIONAL_EVENTS_ENABLED = os.getenv(
        "REGIONAL_EVENTS_ENABLED", "true").lower() == "true"
    REGIONAL_EVENT_FREQUENCY_HOURS = int(
        os.getenv("REGIONAL_EVENT_FREQUENCY", "12"))

    # Notification settings
    BROADCAST_EVENTS = os.getenv("BROADCAST_EVENTS", "true").lower() == "true"
    EVENT_NOTIFICATION_CHANNELS = os.getenv(
        "EVENT_NOTIFICATION_CHANNELS", "websocket,email").split(",")

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "model": cls.MODEL,
            "temperature": cls.TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS,
            "min_event_interval_hours": cls.MIN_EVENT_INTERVAL_HOURS,
            "max_event_duration_hours": cls.MAX_EVENT_DURATION_HOURS,
            "karma_sensitivity": cls.KARMA_SENSITIVITY,
            "auto_trigger_enabled": cls.AUTO_TRIGGER_ENABLED,
            "use_ai_generation": cls.USE_AI_GENERATION,
            "cache_events": cls.CACHE_EVENTS,
            "regional_events_enabled": cls.REGIONAL_EVENTS_ENABLED
        }
