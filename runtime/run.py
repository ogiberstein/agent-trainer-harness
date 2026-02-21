#!/usr/bin/env python3
"""Harness Concurrent Mode — autonomous multi-agent project delivery.

Usage:
    python runtime/run.py --project /path/to/project
    python runtime/run.py --project /path/to/project --resume
    python runtime/run.py --project /path/to/project --config custom-config.yaml
"""

import argparse
import os
import sys

from orchestrator import run
from config import load_config


def main():
    parser = argparse.ArgumentParser(
        description="Run harness in Concurrent mode (autonomous multi-agent delivery)"
    )
    parser.add_argument("--project", required=True, help="Path to harness-enabled project directory")
    parser.add_argument("--config", default=None, help="Config file path (default: <project>/runtime/config.yaml)")
    parser.add_argument("--resume", action="store_true", help="Clear checkpoint and resume paused run")
    parser.add_argument("--dry-run", action="store_true", help="Print dispatch plan without executing workers")
    args = parser.parse_args()

    project = os.path.abspath(args.project)
    if not os.path.isdir(project):
        print(f"Project directory not found: {project}")
        sys.exit(1)

    agents_md = os.path.join(project, "AGENTS.md")
    if not os.path.isfile(agents_md):
        print(f"Not a harness project (AGENTS.md missing): {project}")
        sys.exit(1)

    config_path = args.config or os.path.join(project, "runtime", "config.yaml")
    config = load_config(config_path)
    config.project_name = config.project_name or os.path.basename(project)

    if args.resume:
        checkpoint = os.path.join(project, "runtime", ".checkpoint")
        if os.path.exists(checkpoint):
            os.remove(checkpoint)
            print("Checkpoint cleared. Resuming...")
        else:
            print("No checkpoint found. Starting normally.")

    run(project, config, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
