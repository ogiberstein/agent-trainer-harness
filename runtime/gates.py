"""LLM-based gate evaluation for phase transitions."""

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Optional

from config import Config
from state import Task

GATE_CRITERIA = {
    "requirements": (
        "Every functional requirement has a user story and at least 2 acceptance criteria. "
        "Edge cases and out-of-scope are explicit. Open questions are listed."
    ),
    "design": (
        "Component states defined (default/loading/empty/error). "
        "Responsive behavior and accessibility specified. "
        "Architecture includes data model and API design."
    ),
    "implementation": (
        "Core functional requirements are implemented. "
        "Integration path is clear. "
        "Tests are present and runnable."
    ),
    "qa": (
        "No critical or major issues are open (unless human-approved exception). "
        "Recommendation is Ship or Ship-with-known-issues."
    ),
    "documentation": (
        "No placeholders remain. "
        "Setup steps are explicit and coherent. "
        "Known issues and workarounds from QA are reflected."
    ),
    "growth": (
        "SEO/GEO strategy is explicit and measurable. "
        "Landing and social strategy tied to actual product capabilities. "
        "Experiment backlog includes hypothesis, metric, and owner."
    ),
    "review": (
        "All previous phase gates passed. "
        "Delivery summary covers what was built, deferred, risks, and follow-ups."
    ),
}


@dataclass
class GateResult:
    passed: bool
    summary: str
    evidence: str = ""
    missing: list[str] = None

    def __post_init__(self):
        if self.missing is None:
            self.missing = []


PHASE_ARTIFACTS = {
    "requirements": ["specs/requirements.md"],
    "design": ["specs/architecture.md", "specs/ui-spec.md"],
    "implementation": ["src/", "tests/"],
    "qa": ["qa/test-plan.md", "qa/issues.md"],
    "documentation": ["docs/README.md", "docs/SETUP.md", "docs/API.md"],
    "growth": ["specs/growth-plan.md"],
    "review": ["STATUS.md", "DECISIONS.md"],
}


def gate_check(task: Task, output_path: str, config: Config, project_path: str = "") -> GateResult:
    """Evaluate gate criteria by sending artifacts + criteria to an LLM judge."""
    criteria = GATE_CRITERIA.get(task.phase, "All acceptance criteria for this task are met.")

    worker_output = _read_truncated(output_path, max_chars=3000)
    artifacts_summary = _collect_artifacts(task, project_path) if project_path else ""

    prompt = f"""You are a quality gate reviewer for an automated software delivery pipeline.

Phase: {task.phase}
Task: {task.title} ({task.id})

Gate criteria:
{criteria}

Task acceptance criteria:
{task.acceptance}

Artifact files produced (first 500 chars each):
{artifacts_summary or "(no artifacts found)"}

Worker output (last 3000 chars):
{worker_output}

Evaluate whether the gate criteria are met based on the artifacts and worker output.
Return ONLY valid JSON (no markdown fences):
{{"passed": true/false, "summary": "one-line summary", "evidence": "key evidence", "missing": ["list of unmet criteria if any"]}}
"""

    model = config.gate_model or config.model
    result = _call_llm_judge(prompt, model, config.gate_timeout)
    return _parse_result(result)


def _collect_artifacts(task: Task, project_path: str) -> str:
    """Read phase-relevant artifact files and return a truncated summary."""
    artifact_paths = PHASE_ARTIFACTS.get(task.phase, [])
    parts = []

    for rel_path in artifact_paths:
        full = os.path.join(project_path, rel_path)
        if os.path.isfile(full):
            content = _read_truncated(full, max_chars=500)
            parts.append(f"--- {rel_path} ---\n{content}\n")
        elif os.path.isdir(full):
            files = _list_dir_files(full, max_files=10)
            if files:
                parts.append(f"--- {rel_path} (directory, {len(files)} files) ---\n")
                parts.append(", ".join(files[:10]) + "\n")

    return "\n".join(parts) if parts else ""


def _list_dir_files(dir_path: str, max_files: int = 10) -> list[str]:
    """List files in a directory (non-recursive, up to max_files)."""
    try:
        entries = os.listdir(dir_path)
        return [e for e in entries if os.path.isfile(os.path.join(dir_path, e))][:max_files]
    except OSError:
        return []


def _call_llm_judge(prompt: str, model: str, timeout: int) -> str:
    """Call Claude CLI as a stateless judge.

    TODO: Replace with direct API call if preferred (avoids CLI overhead).
    """
    try:
        result = subprocess.run(
            ["claude", "--print", "--model", model, "-p", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return '{"passed": false, "summary": "Gate evaluation timed out", "evidence": "", "missing": ["timeout"]}'
    except FileNotFoundError:
        return '{"passed": false, "summary": "Claude CLI not found", "evidence": "", "missing": ["cli_missing"]}'


def _parse_result(raw: str) -> GateResult:
    """Parse LLM JSON response into a GateResult."""
    try:
        data = json.loads(raw)
        return GateResult(
            passed=bool(data.get("passed", False)),
            summary=data.get("summary", ""),
            evidence=data.get("evidence", ""),
            missing=data.get("missing", []),
        )
    except (json.JSONDecodeError, KeyError):
        return GateResult(
            passed=False,
            summary=f"Failed to parse gate result: {raw[:200]}",
            missing=["parse_error"],
        )


def _read_truncated(path: str, max_chars: int = 4000) -> str:
    try:
        with open(path) as f:
            content = f.read()
        if len(content) > max_chars:
            return f"...truncated...\n{content[-max_chars:]}"
        return content
    except FileNotFoundError:
        return "(no output file found)"
