"""LLM-based gate evaluation for phase transitions."""

import json
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


def gate_check(task: Task, output_path: str, config: Config) -> GateResult:
    """Evaluate gate criteria by sending artifacts + criteria to an LLM judge."""
    criteria = GATE_CRITERIA.get(task.phase, "All acceptance criteria for this task are met.")

    worker_output = _read_truncated(output_path, max_chars=4000)

    prompt = f"""You are a quality gate reviewer for an automated software delivery pipeline.

Phase: {task.phase}
Task: {task.title} ({task.id})

Gate criteria:
{criteria}

Task acceptance criteria:
{task.acceptance}

Worker output (last 4000 chars):
{worker_output}

Evaluate whether the gate criteria are met based on the worker's output.
Return ONLY valid JSON (no markdown fences):
{{"passed": true/false, "summary": "one-line summary", "evidence": "key evidence", "missing": ["list of unmet criteria if any"]}}
"""

    model = config.gate_model or config.model
    result = _call_llm_judge(prompt, model, config.gate_timeout)
    return _parse_result(result)


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
