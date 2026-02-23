#!/usr/bin/env python3
"""Validate internal consistency of a harness-enabled project.

Checks file references, role/prompt alignment, skills registry,
handoff templates, and core file existence. Outputs human-readable
report or JSON for CI integration.

Usage:
    python cli/validate_harness.py --project /path/to/project
    python cli/validate_harness.py --project . --json
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field

import yaml


@dataclass
class Check:
    name: str
    passed: bool
    details: str = ""


@dataclass
class ValidationReport:
    project: str
    checks: list[Check] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def summary(self) -> str:
        total = len(self.checks)
        passed = sum(1 for c in self.checks if c.passed)
        failed = total - passed
        return f"{passed}/{total} checks passed, {failed} failed"

    def to_dict(self) -> dict:
        return {
            "project": self.project,
            "passed": self.passed,
            "summary": self.summary,
            "checks": [
                {"name": c.name, "passed": c.passed, "details": c.details}
                for c in self.checks
            ],
        }


def validate(project_path: str) -> ValidationReport:
    report = ValidationReport(project=project_path)

    report.checks.append(_check_core_files(project_path))
    report.checks.append(_check_roles_vs_prompts(project_path))
    report.checks.append(_check_skills_registry(project_path))
    report.checks.append(_check_handoff_templates(project_path))
    report.checks.append(_check_agents_md_references(project_path))
    report.checks.append(_check_commands_md_references(project_path))
    report.checks.append(_check_runtime_config(project_path))

    return report


def _check_core_files(project_path: str) -> Check:
    required = ["AGENTS.md", "BRIEF.md", "STATUS.md", "DECISIONS.md"]
    missing = [f for f in required if not os.path.isfile(os.path.join(project_path, f))]
    if missing:
        return Check("core_files", False, f"Missing: {', '.join(missing)}")
    return Check("core_files", True, "All core files present")


def _check_roles_vs_prompts(project_path: str) -> Check:
    """Verify every role in permissions-matrix.md has a matching agent prompt file."""
    matrix_path = os.path.join(project_path, "harness", "permissions-matrix.md")
    agents_dir = os.path.join(project_path, "harness", "agents")

    if not os.path.isfile(matrix_path):
        return Check("roles_vs_prompts", False, "harness/permissions-matrix.md not found")
    if not os.path.isdir(agents_dir):
        return Check("roles_vs_prompts", False, "harness/agents/ directory not found")

    content = _read(matrix_path)
    role_name_map = {
        "orchestrator": "orchestrator.md",
        "product manager": "product-manager.md",
        "designer": "designer.md",
        "fullstack engineer": "fullstack-engineer.md",
        "frontend engineer": "frontend-engineer.md",
        "qa engineer": "qa-engineer.md",
        "documentation writer": "documentation-writer.md",
        "growth strategist": "growth-strategist.md",
        "domain sme": "domain-sme.md",
        "setup engineer": "setup-engineer.md",
    }

    rows = re.findall(r"^\|\s*([^|]+?)\s*\|", content, re.MULTILINE)
    roles_in_matrix = set()
    for row in rows:
        normalized = row.strip().lower()
        if normalized in role_name_map:
            roles_in_matrix.add(normalized)

    missing = []
    for role in roles_in_matrix:
        filename = role_name_map[role]
        if not os.path.isfile(os.path.join(agents_dir, filename)):
            missing.append(f"{role} -> harness/agents/{filename}")

    if missing:
        return Check("roles_vs_prompts", False, f"Missing prompt files: {'; '.join(missing)}")
    return Check("roles_vs_prompts", True, f"{len(roles_in_matrix)} roles matched to prompt files")


def _check_skills_registry(project_path: str) -> Check:
    """Verify every active skill in active-skills.yaml has a directory in skills/."""
    skills_file = os.path.join(project_path, "profiles", "active-skills.yaml")
    skills_dir = os.path.join(project_path, "skills")

    if not os.path.isfile(skills_file):
        return Check("skills_registry", True, "No active-skills.yaml found (skipped)")

    try:
        with open(skills_file) as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        return Check("skills_registry", False, f"Invalid YAML in active-skills.yaml: {e}")

    active_names = []
    for section in ["required", "optional", "domain", "security"]:
        entries = data.get(section, []) or []
        for entry in entries:
            if isinstance(entry, dict) and "name" in entry:
                active_names.append(entry["name"])

    missing = []
    for name in active_names:
        skill_path = os.path.join(skills_dir, name)
        if not os.path.isdir(skill_path):
            missing.append(name)

    if missing:
        return Check("skills_registry", False, f"Active skills missing directories: {', '.join(missing)}")
    return Check("skills_registry", True, f"{len(active_names)} active skills verified")


def _check_handoff_templates(project_path: str) -> Check:
    """Verify handoff templates exist and have required sections."""
    handoffs_dir = os.path.join(project_path, "handoffs")
    if not os.path.isdir(handoffs_dir):
        return Check("handoff_templates", True, "No handoffs/ directory (skipped)")

    issues = []
    required_sections = ["status", "context", "deliverables", "acceptance criteria"]

    for filename in os.listdir(handoffs_dir):
        if not filename.endswith(".md") or filename == "TEMPLATE.md":
            continue
        filepath = os.path.join(handoffs_dir, filename)
        content = _read(filepath).lower()
        for section in required_sections:
            if section not in content:
                issues.append(f"{filename}: missing '{section}' section")

    if issues:
        return Check("handoff_templates", False, "; ".join(issues[:5]))
    count = len([f for f in os.listdir(handoffs_dir) if f.endswith(".md") and f != "TEMPLATE.md"])
    return Check("handoff_templates", True, f"{count} handoff templates validated")


def _check_agents_md_references(project_path: str) -> Check:
    """Check that file paths mentioned in AGENTS.md exist."""
    agents_md = os.path.join(project_path, "AGENTS.md")
    if not os.path.isfile(agents_md):
        return Check("agents_md_refs", False, "AGENTS.md not found")

    content = _read(agents_md)
    return _check_backtick_paths(content, project_path, "AGENTS.md")


def _check_commands_md_references(project_path: str) -> Check:
    """Check that file paths mentioned in COMMANDS.md exist."""
    commands_md = os.path.join(project_path, "COMMANDS.md")
    if not os.path.isfile(commands_md):
        return Check("commands_md_refs", True, "No COMMANDS.md (skipped)")

    content = _read(commands_md)
    return _check_backtick_paths(content, project_path, "COMMANDS.md")


EXTERNAL_REFS = {"CLAUDE.md", ".claude/CLAUDE.md"}

def _check_backtick_paths(content: str, project_path: str, source_file: str) -> Check:
    """Find backtick-quoted paths and verify they exist on disk."""
    path_pattern = re.compile(r"`([a-zA-Z][a-zA-Z0-9_\-./]*(?:\.(?:md|yaml|py|sh|txt)|\/))`")
    matches = path_pattern.findall(content)

    missing = []
    checked = set()
    for ref in matches:
        ref_clean = ref.rstrip("/")
        if ref_clean in checked or ref_clean in EXTERNAL_REFS:
            continue
        checked.add(ref_clean)

        full = os.path.join(project_path, ref_clean)
        if not os.path.exists(full):
            if "*" not in ref_clean and not ref_clean.startswith("http"):
                missing.append(ref_clean)

    name = f"{source_file.lower().replace('.', '_')}_refs"
    if missing:
        return Check(name, False, f"Missing referenced paths: {', '.join(missing[:8])}")
    return Check(name, True, f"{len(checked)} path references verified in {source_file}")


def _check_runtime_config(project_path: str) -> Check:
    """If runtime/config.yaml exists, validate it parses as YAML."""
    config_path = os.path.join(project_path, "runtime", "config.yaml")
    if not os.path.isfile(config_path):
        return Check("runtime_config", True, "No runtime/config.yaml (skipped)")

    try:
        with open(config_path) as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return Check("runtime_config", False, "config.yaml is not a YAML mapping")
        return Check("runtime_config", True, "runtime/config.yaml is valid YAML")
    except yaml.YAMLError as e:
        return Check("runtime_config", False, f"Invalid YAML: {e}")


def _read(path: str) -> str:
    with open(path) as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Validate harness internal consistency")
    parser.add_argument("--project", default=".", help="Path to harness-enabled project")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output JSON for CI")
    args = parser.parse_args()

    project = os.path.abspath(args.project)
    if not os.path.isdir(project):
        print(f"Error: directory not found: {project}")
        sys.exit(2)

    report = validate(project)

    if args.json_output:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(f"Harness Validation: {project}")
        print(f"{'=' * 60}")
        for check in report.checks:
            status = "PASS" if check.passed else "FAIL"
            print(f"  [{status}] {check.name}: {check.details}")
        print(f"{'=' * 60}")
        print(f"Result: {report.summary}")

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
