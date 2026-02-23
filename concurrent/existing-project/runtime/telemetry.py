"""JSONL telemetry for concurrent orchestrator runs.

Appends structured events to logs/runs.jsonl so operators can review
performance, cost patterns, and failure modes after a run completes.
"""

import json
import os
import time
import uuid
from typing import Optional


_run_id: Optional[str] = None


def init_run(project_path: str) -> str:
    """Initialise a new run and return its ID."""
    global _run_id
    _run_id = uuid.uuid4().hex[:12]
    log_event("run_start", {}, project_path)
    return _run_id


def log_event(
    event_type: str,
    data: dict,
    project_path: str,
    *,
    task_id: str = "",
    role: str = "",
    phase: str = "",
    duration_s: float = 0,
    model: str = "",
    retry_count: int = 0,
):
    """Append one event line to logs/runs.jsonl."""
    log_dir = os.path.join(project_path, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "runs.jsonl")

    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run_id": _run_id or "unknown",
        "event": event_type,
        "task_id": task_id,
        "role": role,
        "phase": phase,
        "duration_s": round(duration_s, 2),
        "model": model,
        "retry_count": retry_count,
    }
    record.update(data)

    with open(log_path, "a") as f:
        f.write(json.dumps(record) + "\n")


def log_run_complete(project_path: str, total_duration_s: float):
    log_event(
        "run_complete",
        {"total_duration_s": round(total_duration_s, 2)},
        project_path,
    )
