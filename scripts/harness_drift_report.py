#!/usr/bin/env python3
"""Read-only Agent Trainer Harness drift/version report.

The report compares canonical-managed harness files from the canonical
Agent Trainer templates to vendored project copies. It never writes to any
inspected project.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_PROJECT_CONFIG = "harness-projects.json"

MODE_TEMPLATE = {
    "lite": {
        "new-project": Path("lite/new-project"),
        "existing-project": Path("lite/existing-project"),
    },
    "full": {
        "new-project": Path("full/new-project"),
        "existing-project": Path("full/existing-project"),
    },
    "concurrent": {
        "new-project": Path("concurrent/new-project"),
        "existing-project": Path("concurrent/existing-project"),
    },
}

# .harness-version is intentionally excluded from byte-hash divergence.
# It is compared semantically in the version block because project copies
# legitimately differ from templates by relationship/source_commit/project_kind.
MANAGED_ROOTS = {
    "lite": ["AGENTS.md", "start.md", "harness", "operations"],
    "full": [
        "AGENTS.md",
        "COMMANDS.md",
        "start.md",
        "harness",
        "operations",
        "profiles",
        "evaluation",
        "handoffs",
        "skills",
    ],
    "concurrent": [
        "AGENTS.md",
        "COMMANDS.md",
        "start.md",
        "harness",
        "operations",
        "profiles",
        "evaluation",
        "handoffs",
        "skills",
        "cli",
        "runtime",
    ],
}


@dataclass(frozen=True)
class ProjectSpec:
    name: str
    path: Path
    mode: str
    relationship: str
    sections: tuple[str, ...] = ()
    project_kind: str | None = None


def parse_simple_yaml(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def file_hash(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_files(root: Path, managed_roots: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for rel in managed_roots:
        path = root / rel
        if path.is_file():
            files.append(Path(rel))
        elif path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file():
                    files.append(child.relative_to(root))
    return sorted(set(files), key=lambda p: str(p))


def parse_project_spec(raw: str) -> ProjectSpec:
    if "=" not in raw:
        raise ValueError(f"project spec must be name=path:mode:relationship[:section...], got {raw!r}")
    name, rest = raw.split("=", 1)
    parts = rest.split(":")
    if len(parts) < 3:
        raise ValueError(f"project spec must be name=path:mode:relationship[:section...], got {raw!r}")
    path, mode, relationship, *sections = parts
    if mode not in MODE_TEMPLATE:
        raise ValueError(f"unsupported mode {mode!r} for {name}")
    return ProjectSpec(name=name, path=Path(path).expanduser().resolve(), mode=mode, relationship=relationship, sections=tuple(sections))


def project_spec_from_config(item: dict[str, object], config_dir: Path) -> ProjectSpec:
    name = str(item["name"])
    mode = str(item["mode"])
    relationship = str(item["relationship"])
    raw_path = Path(str(item["path"])).expanduser()
    path = raw_path if raw_path.is_absolute() else (config_dir / raw_path)
    sections = tuple(str(section) for section in item.get("sections", []))
    project_kind = item.get("project_kind")
    if mode not in MODE_TEMPLATE:
        raise ValueError(f"unsupported mode {mode!r} for {name}")
    return ProjectSpec(
        name=name,
        path=path.resolve(),
        mode=mode,
        relationship=relationship,
        sections=sections,
        project_kind=str(project_kind) if project_kind else None,
    )


def load_project_config(path: Path) -> list[ProjectSpec]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    projects = payload.get("projects", [])
    if not isinstance(projects, list):
        raise ValueError(f"project config {path} must contain a projects list")
    return [project_spec_from_config(item, path.parent) for item in projects]


def git_status(root: Path) -> dict[str, object]:
    if not (root / ".git").exists():
        return {"is_git_repo": False, "status_short": None}
    try:
        status = subprocess.run(
            ["git", "status", "--short", "--branch"],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        return {"is_git_repo": True, "status_short": status}
    except Exception as exc:  # pragma: no cover - defensive report path
        return {"is_git_repo": True, "status_short": f"Unable to read git status: {exc}"}


def git_head(root: Path) -> str | None:
    if not (root / ".git").exists():
        return None
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
    except Exception:  # pragma: no cover - defensive report path
        return None


def last_commit_for_path(root: Path, rel: Path) -> str | None:
    """Hash of the last commit that modified `rel` within `root`'s history."""
    if not (root / ".git").exists():
        return None
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", str(rel)],
            cwd=root,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        return out or None
    except Exception:  # pragma: no cover - defensive report path
        return None


def commit_contains(root: Path, ancestor: str, descendant: str) -> bool | None:
    """True when `ancestor` is an ancestor of (or equal to) `descendant`.

    Returns None when ancestry cannot be determined — e.g. either commit is
    not present in `root`'s history.
    """
    if not (root / ".git").exists():
        return None
    try:
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=root,
            text=True,
            capture_output=True,
        )
    except Exception:  # pragma: no cover - defensive report path
        return None
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    return None


def resolve_project_kind(spec: ProjectSpec, project_version: dict[str, str]) -> str:
    kind = spec.project_kind or project_version.get("project_kind") or "existing-project"
    if kind not in MODE_TEMPLATE[spec.mode]:
        return "existing-project"
    return kind


def control_doc_status(project_root: Path) -> dict[str, object]:
    """Report root control-doc migration state without byte-hashing project state.

    Root control docs are project-owned once a harness is copied, so the drift
    reporter should not compare their contents to canonical templates. It still
    must surface whether required control docs exist and whether legacy state
    docs such as PROGRESS.md are present after a migration.
    """
    required = ["BRIEF.md", "ROADMAP.md", "STATUS.md", "DECISIONS.md"]
    present = {name: (project_root / name).is_file() for name in required}
    missing = [name for name, exists in present.items() if not exists]
    legacy_progress_present = (project_root / "PROGRESS.md").is_file()
    return {
        **present,
        "PROGRESS.md": legacy_progress_present,
        "missing": missing,
        "roadmap_missing": not present["ROADMAP.md"],
        "legacy_progress_present": legacy_progress_present,
        "both_roadmap_and_progress_present": present["ROADMAP.md"] and legacy_progress_present,
        "migration_state": (
            "missing_roadmap_with_legacy_progress" if not present["ROADMAP.md"] and legacy_progress_present
            else "missing_roadmap" if not present["ROADMAP.md"]
            else "roadmap_with_legacy_progress" if legacy_progress_present
            else "roadmap_present"
        ),
    }


def compare_project(canonical_root: Path, spec: ProjectSpec) -> dict[str, object]:
    project_version = parse_simple_yaml(spec.path / ".harness-version")
    project_kind = resolve_project_kind(spec, project_version)
    template_root = canonical_root / MODE_TEMPLATE[spec.mode][project_kind]
    managed = MANAGED_ROOTS[spec.mode]
    canonical_files = iter_files(template_root, managed)
    project_files = iter_files(spec.path, managed)
    all_files = sorted(set(canonical_files) | set(project_files), key=lambda p: str(p))

    divergence = []
    for rel in all_files:
        canonical_path = template_root / rel
        project_path = spec.path / rel
        canonical_exists = canonical_path.exists()
        project_exists = project_path.exists()
        if canonical_exists and not project_exists:
            status = "missing"
        elif project_exists and not canonical_exists:
            status = "extra"
        elif file_hash(canonical_path) == file_hash(project_path):
            status = "same"
        else:
            status = "modified"
        if status != "same":
            divergence.append({"path": str(rel), "status": status})

    canonical_version = parse_simple_yaml(template_root / ".harness-version")
    agents_text = (spec.path / "AGENTS.md").read_text(encoding="utf-8", errors="replace") if (spec.path / "AGENTS.md").exists() else ""
    project_source_commit = project_version.get("source_commit")
    template_commit = last_commit_for_path(canonical_root, MODE_TEMPLATE[spec.mode][project_kind])
    source_commit_current = None
    if template_commit and project_source_commit:
        source_commit_current = commit_contains(canonical_root, template_commit, project_source_commit)

    return {
        "name": spec.name,
        "path": str(spec.path),
        "mode": spec.mode,
        "relationship": spec.relationship,
        "project_kind": project_kind,
        "canonical_template": str(template_root),
        "git": git_status(spec.path),
        "version": {
            "canonical": canonical_version.get("HARNESS_VERSION"),
            "project": project_version.get("HARNESS_VERSION"),
            "matches": canonical_version.get("HARNESS_VERSION") == project_version.get("HARNESS_VERSION"),
            "source_commit": project_source_commit,
            "template_commit": template_commit,
            "source_commit_current": source_commit_current,
            "missing_version_stamp": not bool(project_version),
        },
        "project_specific_sections": {section: section in agents_text for section in spec.sections},
        "control_docs": control_doc_status(spec.path),
        "divergence": divergence,
        "summary": {
            "changed_files": len(divergence),
            "missing_version_stamp": not bool(project_version),
        },
    }


def build_report(canonical_root: Path, specs: list[ProjectSpec]) -> dict[str, object]:
    canonical_root = canonical_root.resolve()
    root_version = parse_simple_yaml(canonical_root / ".harness-version")
    canonical_head = git_head(canonical_root)
    return {
        "canonical": {
            "path": str(canonical_root),
            "source_repo": root_version.get("source_repo", "ogiberstein/agent-trainer-harness"),
            "HARNESS_VERSION": root_version.get("HARNESS_VERSION"),
            "head": canonical_head,
            "git": git_status(canonical_root),
        },
        "projects": [compare_project(canonical_root, spec) for spec in specs],
    }


def render_markdown(report: dict[str, object]) -> str:
    lines = ["# Harness Drift Report", ""]
    canonical = report["canonical"]
    lines += [
        f"Canonical: `{canonical['source_repo']}`",
        f"Version: `{canonical['HARNESS_VERSION']}`",
        f"Path: `{canonical['path']}`",
        f"HEAD: `{canonical['head']}`",
        "",
        "If no project registry is configured, pass `--project name=path:mode:relationship[:section...]` "
        "or `--project-config path/to/harness-projects.json` to compare vendored projects.",
        "",
        "## Projects",
        "",
    ]
    for project in report["projects"]:
        version = project["version"]
        lines += [
            f"### {project['name']}",
            "",
            f"- Path: `{project['path']}`",
            f"- Mode / relationship / kind: `{project['mode']}` / `{project['relationship']}` / `{project['project_kind']}`",
            f"- Version: project `{version['project']}` vs canonical `{version['canonical']}`; matches: `{version['matches']}`",
            f"- Source commit current: `{version['source_commit_current']}`",
            f"- Git: `{project['git']['status_short']}`",
            f"- Divergent managed files: `{project['summary']['changed_files']}`",
            f"- Control docs: `{project['control_docs']['migration_state']}`",
        ]
        control_docs = project["control_docs"]
        if control_docs["missing"]:
            lines.append(f"- Missing control docs: {', '.join(control_docs['missing'])}")
        if control_docs["legacy_progress_present"]:
            lines.append("- Legacy control doc present: `PROGRESS.md`")
        sections = project["project_specific_sections"]
        if sections:
            flags = ", ".join(f"{name}={present}" for name, present in sections.items())
            lines.append(f"- Project-specific sections: {flags}")
        if project["divergence"]:
            lines.append("- Divergence:")
            for item in project["divergence"]:
                lines.append(f"  - `{item['status']}` `{item['path']}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def resolve_project_specs(args: argparse.Namespace, canonical_root: Path) -> list[ProjectSpec]:
    if args.project:
        return [parse_project_spec(raw) for raw in args.project]
    config_path = Path(args.project_config) if args.project_config else canonical_root / DEFAULT_PROJECT_CONFIG
    if not config_path.is_absolute():
        config_path = canonical_root / config_path
    if not config_path.exists():
        if args.project_config:
            raise FileNotFoundError(
                f"No project config found at {config_path}. Pass an existing --project-config or use --project name=path:mode:relationship[:section...]"
            )
        return []
    return load_project_config(config_path.resolve())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", default=".", help="canonical Agent Trainer Harness repo root")
    parser.add_argument("--project-config", help="JSON project registry path; defaults to <canonical-root>/harness-projects.json")
    parser.add_argument("--project", action="append", help="name=path:mode:relationship[:section...]", default=[])
    parser.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    args = parser.parse_args()

    canonical_root = Path(args.canonical_root).expanduser().resolve()
    specs = resolve_project_specs(args, canonical_root)
    report = build_report(canonical_root, specs)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
