"""Notification layer for Concurrent mode — alerts human on block or completion."""

from datetime import datetime, timezone

import requests

from config import Config


def notify(config: Config, message: str, level: str = "info"):
    """Send a notification via webhook and print locally.

    Args:
        config: Runtime config with webhook URL and project name.
        message: Human-readable notification message.
        level: One of "info", "warning", "error", "complete".
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    prefix = {
        "info": "[INFO]",
        "warning": "[WARN]",
        "error": "[ERROR]",
        "complete": "[DONE]",
    }.get(level, "[INFO]")

    local_msg = f"{prefix} {timestamp} | {config.project_name} | {message}"
    print(local_msg)

    if config.notification_webhook:
        _send_webhook(config, message, level, timestamp)


def _send_webhook(config: Config, message: str, level: str, timestamp: str):
    """Send to Slack/Telegram/generic webhook."""
    payload = {
        "text": f"[Harness Concurrent] {message}",
        "project": config.project_name,
        "level": level,
        "timestamp": timestamp,
    }
    try:
        resp = requests.post(config.notification_webhook, json=payload, timeout=10)
        if resp.status_code >= 400:
            print(f"[NOTIFY] Webhook returned {resp.status_code}")
    except requests.RequestException as e:
        print(f"[NOTIFY] Webhook failed: {e}")
