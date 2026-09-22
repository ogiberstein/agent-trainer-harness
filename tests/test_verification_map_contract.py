import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FULL_AND_CONCURRENT = (
    REPO_ROOT / "full" / "new-project",
    REPO_ROOT / "full" / "existing-project",
    REPO_ROOT / "concurrent" / "new-project",
    REPO_ROOT / "concurrent" / "existing-project",
)
LITE = (
    REPO_ROOT / "lite" / "new-project",
    REPO_ROOT / "lite" / "existing-project",
)
CONCURRENT = (
    REPO_ROOT / "concurrent" / "new-project",
    REPO_ROOT / "concurrent" / "existing-project",
)
MAP_COLUMNS = (
    "Material code area",
    "Invariant",
    "Fastest feedback loop",
    "Expected runtime range",
    "Oracle",
    "Smallest real-boundary check",
)


def load_preflight(template_root: Path):
    path = template_root / "cli" / "preflight_concurrent.py"
    spec = importlib.util.spec_from_file_location(
        f"preflight_{template_root.name}_{id(template_root)}", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load preflight module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def brief_with_map(row: str, budget: str = "10 minutes") -> str:
    return f"""# Project Brief

## Goal
Ship a bounded autonomous change with evidence.

## Verification Map
Required only for unattended Full and Concurrent runs.

- Run verification budget: {budget}

| {' | '.join(MAP_COLUMNS)} |
| {' | '.join(['---'] * len(MAP_COLUMNS))} |
{row}

## Success Criteria
- The requested behavior is verified.
"""


class TestVerificationMapContract(unittest.TestCase):
    def test_full_and_concurrent_briefs_define_one_authoritative_map(self):
        for template_root in FULL_AND_CONCURRENT:
            brief = (template_root / "BRIEF.md").read_text(encoding="utf-8")
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertEqual(brief.count("## Verification Map"), 1)
                for column in MAP_COLUMNS:
                    self.assertIn(column, brief)
                self.assertIn(
                    "Required only for unattended Full and Concurrent runs", brief
                )
                self.assertIn("Lite or supervised small-task workflows", brief)

    def test_map_keeps_design_guidance_conditional(self):
        for template_root in FULL_AND_CONCURRENT:
            brief = (template_root / "BRIEF.md").read_text(encoding="utf-8")
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertIn(
                    "make impossible states unrepresentable where this simplifies correctness",
                    brief,
                )
                self.assertIn("not a mandate for extra type scaffolding", brief)

    def test_existing_codex_review_challenges_map_without_new_lane(self):
        for template_root in FULL_AND_CONCURRENT:
            brief = (template_root / "BRIEF.md").read_text(encoding="utf-8")
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertIn("existing pre-build review", brief)
                self.assertIn("Codex", brief)
                self.assertIn("missing coverage", brief)
                self.assertIn("weak oracles", brief)
                self.assertIn("exceed the run budget", brief)
                self.assertIn("existing post-build code audit", brief)
                self.assertIn("not a new review lane", brief)

    def test_lite_briefs_do_not_add_verification_map_policy(self):
        for template_root in LITE:
            brief = (template_root / "BRIEF.md").read_text(encoding="utf-8")
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertNotIn("## Verification Map", brief)
                self.assertNotIn("existing pre-build review", brief)

    def test_concurrent_runbook_names_map_as_a_preflight_check(self):
        for template_root in CONCURRENT:
            commands = (template_root / "COMMANDS.md").read_text(encoding="utf-8")
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertIn("including its completed Verification Map", commands)

    def test_concurrent_has_no_unattended_full_fallback(self):
        stale_fallbacks = (
            "solo-autonomous Full mode",
            "fall back to sequential Full mode",
            "agent should fall back to Full mode",
        )
        for template_root in CONCURRENT:
            for relative in (
                "AGENTS.md",
                "COMMANDS.md",
                "start.md",
                "runtime/DESIGN.md",
                "cli/preflight_concurrent.py",
                "cli/harness_cli.py",
            ):
                path = template_root / relative
                content = path.read_text(encoding="utf-8")
                with self.subTest(
                    template=str(template_root.relative_to(REPO_ROOT)), file=relative
                ):
                    for stale in stale_fallbacks:
                        self.assertNotIn(stale, content)

    def test_concurrent_preflight_rejects_missing_verification_map(self):
        for template_root in CONCURRENT:
            module = load_preflight(template_root)
            with tempfile.TemporaryDirectory() as temp_dir:
                Path(temp_dir, "BRIEF.md").write_text(
                    "# Project Brief\n\n## Goal\n" + "Autonomous build. " * 12,
                    encoding="utf-8",
                )
                result = module.check_brief(temp_dir)
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertFalse(result.passed)
                self.assertIn("Verification Map", result.detail)

    def test_direct_concurrent_runtime_rejects_missing_verification_map(self):
        for template_root in CONCURRENT:
            with tempfile.TemporaryDirectory() as temp_dir:
                project = Path(temp_dir)
                (project / "AGENTS.md").write_text("Harness project.\n", encoding="utf-8")
                (project / "BRIEF.md").write_text(
                    "# Project Brief\n\n## Goal\n" + "Autonomous build. " * 12,
                    encoding="utf-8",
                )
                result = subprocess.run(
                    [
                        sys.executable,
                        str(template_root / "runtime" / "run.py"),
                        "--project",
                        str(project),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertEqual(result.returncode, 1)
                self.assertIn("Verification Map", result.stdout + result.stderr)

    def test_concurrent_preflight_rejects_placeholder_run_budget(self):
        row = "| API | Requests are authenticated | unit test | 1-3s | explicit allow/deny assertions | loopback request |"
        for template_root in CONCURRENT:
            module = load_preflight(template_root)
            with tempfile.TemporaryDirectory() as temp_dir:
                Path(temp_dir, "BRIEF.md").write_text(
                    brief_with_map(row, budget="[...]"), encoding="utf-8"
                )
                result = module.check_brief(temp_dir)
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertFalse(result.passed)
                self.assertIn("run verification budget", result.detail.lower())

    def test_concurrent_preflight_rejects_duplicate_map_sections(self):
        row = "| API | Requests are authenticated | unit test | 1-3s | explicit allow/deny assertions | loopback request |"
        duplicate = brief_with_map(row) + "\n## Verification Map\n"
        for template_root in CONCURRENT:
            module = load_preflight(template_root)
            with tempfile.TemporaryDirectory() as temp_dir:
                Path(temp_dir, "BRIEF.md").write_text(duplicate, encoding="utf-8")
                result = module.check_brief(temp_dir)
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertFalse(result.passed)
                self.assertIn("exactly one", result.detail.lower())

    def test_concurrent_preflight_rejects_commented_duplicate_map(self):
        row = "| API | Requests are authenticated | unit test | 1-3s | explicit allow/deny assertions | loopback request |"
        duplicate = brief_with_map(row) + "\n<!-- ## Verification Map -->\n"
        for template_root in CONCURRENT:
            module = load_preflight(template_root)
            with tempfile.TemporaryDirectory() as temp_dir:
                Path(temp_dir, "BRIEF.md").write_text(duplicate, encoding="utf-8")
                result = module.check_brief(temp_dir)
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertFalse(result.passed)
                self.assertIn("exactly one", result.detail.lower())

    def test_concurrent_preflight_rejects_commented_out_map(self):
        row = "| API | Requests are authenticated | unit test | 1-3s | explicit allow/deny assertions | loopback request |"
        commented = brief_with_map(row).replace(
            "## Verification Map", "<!--\n## Verification Map"
        ).replace("\n## Success Criteria", "\n-->\n\n## Success Criteria")
        for template_root in CONCURRENT:
            module = load_preflight(template_root)
            with tempfile.TemporaryDirectory() as temp_dir:
                Path(temp_dir, "BRIEF.md").write_text(commented, encoding="utf-8")
                result = module.check_brief(temp_dir)
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertFalse(result.passed)
                self.assertIn("Verification Map", result.detail)

    def test_concurrent_preflight_accepts_escaped_pipe_in_map_cell(self):
        row = r"| CLI | Output is bounded | command \| focused assertion | 1-3s | exact exit and output | real CLI process |"
        for template_root in CONCURRENT:
            module = load_preflight(template_root)
            with tempfile.TemporaryDirectory() as temp_dir:
                Path(temp_dir, "BRIEF.md").write_text(
                    brief_with_map(row), encoding="utf-8"
                )
                result = module.check_brief(temp_dir)
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertTrue(result.passed, result.detail)

    def test_concurrent_preflight_rejects_incomplete_map_row(self):
        row = "| API | Requests are authenticated | unit test | 1-3s | | loopback request |"
        for template_root in CONCURRENT:
            module = load_preflight(template_root)
            with tempfile.TemporaryDirectory() as temp_dir:
                Path(temp_dir, "BRIEF.md").write_text(
                    brief_with_map(row), encoding="utf-8"
                )
                result = module.check_brief(temp_dir)
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertFalse(result.passed)
                self.assertIn("incomplete", result.detail.lower())

    def test_concurrent_preflight_accepts_complete_map(self):
        row = "| API | Requests are authenticated | unit test | 1-3s | explicit allow/deny assertions | loopback request |"
        for template_root in CONCURRENT:
            module = load_preflight(template_root)
            with tempfile.TemporaryDirectory() as temp_dir:
                Path(temp_dir, "BRIEF.md").write_text(
                    brief_with_map(row), encoding="utf-8"
                )
                result = module.check_brief(temp_dir)
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertTrue(result.passed, result.detail)


if __name__ == "__main__":
    unittest.main()
