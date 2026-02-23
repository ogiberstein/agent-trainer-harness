#!/usr/bin/env python3
"""Preflight check for Concurrent mode prerequisites.

Verifies that the environment and project are ready for the concurrent
orchestrator. Agents can run this programmatically before self-launching.

Usage:
    python3 cli/preflight_concurrent.py --project .
    python3 cli/preflight_concurrent.py --project . --json
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import List


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def check_python_version() -> Check:
    major, minor = sys.version_info[:2]
    if major >= 3 and minor >= 10:
        return Check("python_3.10+", True, f"Python {major}.{minor}")
    return Check("python_3.10+", False, f"Python {major}.{minor} — need 3.10+")


def check_claude_cli() -> Check:
    path = shutil.which("claude")
    if path is None:
        return Check("claude_cli", False, "claude not found on PATH")
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True, text=True, timeout=10,
        )
        version = result.stdout.strip() or result.stderr.strip()
        return Check("claude_cli", True, f"claude found: {version[:80]}")
    except Exception as e:
        return Check("claude_cli", False, f"claude found but --version failed: {e}")


def check_git(project_path: str) -> Check:
    if not os.path.isdir(os.path.join(project_path, ".git")):
        return Check("git_repo", False, "Not a git repository (.git/ missing)")
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_path, capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            return Check("git_repo", False, "Git repo exists but has no commits")
        return Check("git_repo", True, f"HEAD: {result.stdout.strip()[:12]}")
    except Exception as e:
        return Check("git_repo", False, f"Git check failed: {e}")


def check_runtime_dir(project_path: str) -> Check:
    runtime_dir = os.path.join(project_path, "runtime")
    if not os.path.isdir(runtime_dir):
        return Check("runtime_dir", False, "runtime/ directory missing")
    run_py = os.path.join(runtime_dir, "run.py")
    if not os.path.isfile(run_py):
        return Check("runtime_dir", False, "runtime/ exists but run.py missing")
    return Check("runtime_dir", True, "runtime/ directory with run.py present")


def check_config(project_path: str) -> Check:
    config_path = os.path.join(project_path, "runtime", "config.yaml")
    if not os.path.isfile(config_path):
        return Check("config_yaml", False, "runtime/config.yaml missing")
    try:
        import yaml
        with open(config_path) as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return Check("config_yaml", False, "config.yaml is not a valid YAML mapping")
        return Check("config_yaml", True, "runtime/config.yaml valid")
    except ImportError:
        return Check("config_yaml", False, "Cannot validate — pyyaml not installed")
    except Exception as e:
        return Check("config_yaml", False, f"config.yaml parse error: {e}")


def check_deps() -> Check:
    missing = []
    try:
        import yaml  # noqa: F401
    except ImportError:
        missing.append("pyyaml")
    try:
        import requests  # noqa: F401
    except ImportError:
        missing.append("requests")
    if missing:
        return Check("python_deps", False, f"Missing: {', '.join(missing)} — run: pip install -r runtime/requirements.txt")
    return Check("python_deps", True, "pyyaml and requests importable")


def check_brief(project_path: str) -> Check:
    brief_path = os.path.join(project_path, "BRIEF.md")
    if not os.path.isfile(brief_path):
        return Check("brief_md", False, "BRIEF.md missing")
    with open(brief_path) as f:
        content = f.read().strip()
    if len(content) < 100:
        return Check("brief_md", False, f"BRIEF.md too short ({len(content)} chars) — fill in project scope before launching")
    placeholder_markers = ["[describe", "[your", "TODO", "TBD", "PLACEHOLDER"]
    for marker in placeholder_markers:
        if marker.lower() in content.lower():
            return Check("brief_md", False, f"BRIEF.md contains placeholder text ('{marker}')")
    return Check("brief_md", True, f"BRIEF.md present ({len(content)} chars)")


def run_preflight(project_path: str) -> List[Check]:
    return [
        check_python_version(),
        check_claude_cli(),
        check_git(project_path),
        check_runtime_dir(project_path),
        check_config(project_path),
        check_deps(),
        check_brief(project_path),
    ]


def main():
    parser = argparse.ArgumentParser(description="Preflight check for Concurrent mode")
    parser.add_argument("--project", default=".", help="Path to harness-enabled project")
    parser.add_argument("--json", action="store_true", dest="json_output", help="JSON output")
    args = parser.parse_args()

    project = os.path.abspath(args.project)
    checks = run_preflight(project)

    passed = sum(1 for c in checks if c.passed)
    failed = sum(1 for c in checks if not c.passed)
    all_pass = failed == 0

    if args.json_output:
        print(json.dumps({
            "all_pass": all_pass,
            "passed": passed,
            "failed": failed,
            "checks": [{"name": c.name, "passed": c.passed, "detail": c.detail} for c in checks],
        }, indent=2))
    else:
        print(f"Concurrent Mode Preflight: {project}")
        print("=" * 60)
        for c in checks:
            icon = "PASS" if c.passed else "FAIL"
            print(f"  [{icon}] {c.name}: {c.detail}")
        print("=" * 60)
        print(f"Result: {passed}/{len(checks)} passed, {failed} failed")
        if all_pass:
            print("\nReady to launch: python3 cli/harness_cli.py --project . launch-concurrent")
        else:
            print("\nFix the failures above before launching concurrent mode.")
            print("Fallback: use solo-autonomous Full mode (day-0-start.md).")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
