"""
Reading Time Calculator Utility
Calculates estimated reading time based on content
"""

import re
from typing import List, Dict, Any


def calculate_reading_time(content: str, words_per_minute: int = 200) -> int:
    """
    Calculate reading time in minutes based on word count
    
    Args:
        content: Text content to analyze
        words_per_minute: Average reading speed (default: 200 wpm)
    
    Returns:
        Reading time in minutes
    """
    if not content:
        return 0
    
    # Remove markdown formatting
    clean_content = re.sub(r'[#*_`~\[\](){}]', '', content)
    clean_content = re.sub(r'https?://\S+', '', clean_content)
    
    # Count words
    words = clean_content.split()
    word_count = len([w for w in words if w.strip()])
    
    # Calculate time (minimum 1 minute)
    reading_time = max(1, round(word_count / words_per_minute))
    
    return reading_time


def calculate_roadmap_reading_time(nodes: List[Dict[str, Any]]) -> str:
    """
    Calculate total reading time for all nodes in a roadmap
    
    Args:
        nodes: List of roadmap nodes with content
    
    Returns:
        Formatted reading time string (e.g., "45 mins", "2 hours 15 mins")
    """
    if not nodes:
        return "0 mins"
    
    total_minutes = 0
    
    for node in nodes:
        # Calculate from node content
        content = node.get('content', '')
        description = node.get('description', '')
        combined_content = f"{content} {description}"
        
        total_minutes += calculate_reading_time(combined_content)
        
        # Add estimated time if specified
        estimated_time = node.get('estimated_time', '')
        if estimated_time:
            # Parse estimated_time (e.g., "2 hours", "30 mins", "1 week")
            time_value = parse_time_to_minutes(estimated_time)
            total_minutes += time_value
    
    # Format the result
    if total_minutes < 60:
        return f"{total_minutes} mins"
    elif total_minutes < 1440:  # Less than 24 hours
        hours = total_minutes // 60
        mins = total_minutes % 60
        if mins == 0:
            return f"{hours} {'hour' if hours == 1 else 'hours'}"
        return f"{hours} {'hour' if hours == 1 else 'hours'} {mins} mins"
    else:  # Days
        days = total_minutes // 1440
        remaining_hours = (total_minutes % 1440) // 60
        if remaining_hours == 0:
            return f"{days} {'day' if days == 1 else 'days'}"
        return f"{days} {'day' if days == 1 else 'days'} {remaining_hours} {'hour' if remaining_hours == 1 else 'hours'}"


def parse_time_to_minutes(time_str: str) -> int:
    """
    Parse time string to minutes
    
    Args:
        time_str: Time string (e.g., "2 hours", "30 mins", "1 week")
    
    Returns:
        Time in minutes
    """
    if not time_str:
        return 0
    
    time_str = time_str.lower().strip()
    
    # Extract number and unit
    match = re.search(r'(\d+)\s*(min|mins|minute|minutes|hour|hours|day|days|week|weeks|month|months)', time_str)
    
    if not match:
        return 0
    
    value = int(match.group(1))
    unit = match.group(2)
    
    # Convert to minutes
    if 'min' in unit:
        return value
    elif 'hour' in unit:
        return value * 60
    elif 'day' in unit:
        return value * 1440
    elif 'week' in unit:
        return value * 10080
    elif 'month' in unit:
        return value * 43200
    
    return 0
