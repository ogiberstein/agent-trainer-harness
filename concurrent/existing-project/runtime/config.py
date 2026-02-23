"""Load and validate runtime configuration."""

import os
from dataclasses import dataclass, field
from typing import Optional

import yaml


@dataclass
class Config:
    model: str = "claude-sonnet-4-20250514"
    gate_model: Optional[str] = None
    max_workers: int = 3
    max_retries: int = 2
    checkpoint_after_requirements: bool = True
    notification_webhook: str = ""
    worker_timeout: int = 3600
    gate_timeout: int = 120
    skip_phases: list[str] = field(default_factory=list)
    project_name: str = ""


def load_config(path: str) -> Config:
    if not os.path.isfile(path):
        print(f"Config not found at {path}, using defaults.")
        return Config()

    with open(path) as f:
        raw = yaml.safe_load(f) or {}

    config = Config()
    for key, value in raw.items():
        if hasattr(config, key) and value is not None:
            setattr(config, key, value)

    return config
