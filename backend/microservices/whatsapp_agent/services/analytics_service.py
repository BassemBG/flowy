"""
Analytics Service
In-memory tracking of WhatsApp agent metrics.
Resets when container restarts.
"""

from datetime import datetime, date
from typing import Dict, Any, List
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

# In-memory storage
_stats = {
    "start_time": datetime.now(),
    "messages_received": 0,
    "messages_sent": 0,
    "unique_users": set(),
    "users_first_seen": {},  # phone -> datetime
    "hourly_messages": defaultdict(int),  # hour (0-23) -> count
    "language_distribution": {"arabic": 0, "french": 0},
    "tool_usage": defaultdict(int),  # tool_name -> count
    "conversations": defaultdict(list),  # phone -> list of timestamps
}


def track_message_received(phone: str, language: str = "arabic"):
    """Track an incoming message from a user."""
    now = datetime.now()
    
    _stats["messages_received"] += 1
    _stats["hourly_messages"][now.hour] += 1
    _stats["language_distribution"][language] += 1
    
    # Track unique users
    if phone not in _stats["unique_users"]:
        _stats["users_first_seen"][phone] = now
    _stats["unique_users"].add(phone)
    
    # Track conversation
    _stats["conversations"][phone].append(now)
    
    logger.info(f"📊 Tracked incoming message from {phone[:6]}...")


def track_message_sent(phone: str):
    """Track an outgoing message to a user."""
    _stats["messages_sent"] += 1
    logger.info(f"📊 Tracked outgoing message to {phone[:6]}...")


def track_tool_usage(tool_name: str):
    """Track when a tool is used."""
    _stats["tool_usage"][tool_name] += 1
    logger.info(f"📊 Tracked tool usage: {tool_name}")


def get_analytics() -> Dict[str, Any]:
    """Get all analytics for the dashboard."""
    now = datetime.now()
    today = date.today()
    
    # Calculate messages today
    messages_today = sum(
        1 for phone, timestamps in _stats["conversations"].items()
        for ts in timestamps if ts.date() == today
    )
    
    # Calculate conversations today (unique users who messaged today)
    conversations_today = sum(
        1 for phone, timestamps in _stats["conversations"].items()
        if any(ts.date() == today for ts in timestamps)
    )
    
    # New vs returning clients this month
    month_start = today.replace(day=1)
    new_this_month = sum(
        1 for phone, first_seen in _stats["users_first_seen"].items()
        if first_seen.date() >= month_start
    )
    returning_this_month = len(_stats["unique_users"]) - new_this_month
    
    # Hourly distribution
    hourly_dist = []
    for hour in range(9, 18):  # 9 AM to 5 PM
        hour_label = f"{hour}AM" if hour < 12 else f"{hour-12 if hour > 12 else 12}PM"
        hourly_dist.append({
            "hour": hour_label,
            "count": _stats["hourly_messages"].get(hour, 0)
        })
    
    # Calculate average messages per conversation
    total_convs = len(_stats["conversations"])
    avg_per_conv = round(_stats["messages_received"] / max(total_convs, 1), 1)
    
    return {
        "messages_today": messages_today,
        "conversations_today": conversations_today,
        "total_clients": len(_stats["unique_users"]),
        "new_clients_this_month": new_this_month,
        "returning_clients": returning_this_month,
        "messages_sent": _stats["messages_sent"],
        "messages_received": _stats["messages_received"],
        "avg_messages_per_conversation": avg_per_conv,
        "tool_usage": dict(_stats["tool_usage"]),
        "hourly_distribution": hourly_dist,
        "language_distribution": _stats["language_distribution"].copy(),
        "uptime_seconds": (now - _stats["start_time"]).total_seconds()
    }


def reset_analytics():
    """Reset all analytics (for testing)."""
    global _stats
    _stats = {
        "start_time": datetime.now(),
        "messages_received": 0,
        "messages_sent": 0,
        "unique_users": set(),
        "users_first_seen": {},
        "hourly_messages": defaultdict(int),
        "language_distribution": {"arabic": 0, "french": 0},
        "tool_usage": defaultdict(int),
        "conversations": defaultdict(list),
    }
    logger.info("📊 Analytics reset")
