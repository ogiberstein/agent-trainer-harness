import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "harness_drift_report.py"


def parse_stamp(path: Path) -> dict[str, str]:
    data = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" in line and not line.strip().startswith("#"):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


CANONICAL_VERSION = parse_stamp(REPO_ROOT / ".harness-version")["HARNESS_VERSION"]


class TestHarnessVersionStamps(unittest.TestCase):
    def test_canonical_templates_have_machine_readable_version_stamps(self):
        expected = [
            REPO_ROOT / ".harness-version",
            REPO_ROOT / "lite" / "new-project" / ".harness-version",
            REPO_ROOT / "lite" / "existing-project" / ".harness-version",
            REPO_ROOT / "full" / "new-project" / ".harness-version",
            REPO_ROOT / "full" / "existing-project" / ".harness-version",
            REPO_ROOT / "concurrent" / "new-project" / ".harness-version",
            REPO_ROOT / "concurrent" / "existing-project" / ".harness-version",
        ]
        for path in expected:
            with self.subTest(path=path):
                stamp = parse_stamp(path)
                self.assertEqual(stamp["HARNESS_VERSION"], CANONICAL_VERSION)
                self.assertEqual(stamp["source_repo"], "ogiberstein/agent-trainer-harness")
                self.assertIn("source_commit", stamp)
                self.assertIn("relationship", stamp)
                if path.name == ".harness-version" and path.parent != REPO_ROOT:
                    self.assertIn(stamp["project_kind"], {"new-project", "existing-project"})


class TestHarnessDriftReport(unittest.TestCase):
    def _make_project(self, root: Path, *, stamp_extra: str = "", kind: str = "existing-project") -> Path:
        project = root / "project"
        (project / "harness" / "agents").mkdir(parents=True)
        (project / "operations").mkdir()
        (project / "AGENTS.md").write_text(
            "# Agent Operating Instructions — Lite Mode\n\n"
            "## Visual Pipeline Ownership (amended 2026-05-18 per DEC-021)\ncustom\n\n"
            "## First Actions\n",
            encoding="utf-8",
        )
        (project / "start.md").write_text("local drift\n", encoding="utf-8")
        (project / "harness" / "agents" / "orchestrator.md").write_text("local\n", encoding="utf-8")
        (project / "harness" / "agents" / "fullstack-engineer.md").write_text("local\n", encoding="utf-8")
        (project / "harness" / "agents" / "qa-engineer.md").write_text("local\n", encoding="utf-8")
        (project / "operations" / "context-efficiency-guidelines.md").write_text("local\n", encoding="utf-8")
        (project / ".harness-version").write_text(
            f"HARNESS_VERSION: {CANONICAL_VERSION}\nmode: lite\nproject_kind: {kind}\nrelationship: vendored-lite\nsource_repo: ogiberstein/agent-trainer-harness\nsource_commit: old\n{stamp_extra}",
            encoding="utf-8",
        )
        return project

    def _run_json(self, args):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args, "--json"],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        return json.loads(result.stdout)

    def test_report_json_includes_version_divergence_and_section_flags_without_stamp_file_divergence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = self._make_project(Path(tmpdir), stamp_extra="local_note: legitimate\n")
            payload = self._run_json([
                "--canonical-root", str(REPO_ROOT),
                "--project", f"sample={project}:lite:vendored-lite:Visual Pipeline Ownership",
            ])
            sample = payload["projects"][0]
            self.assertEqual(sample["version"]["project"], CANONICAL_VERSION)
            self.assertEqual(sample["version"]["canonical"], CANONICAL_VERSION)
            self.assertTrue(sample["project_specific_sections"]["Visual Pipeline Ownership"])
            self.assertFalse(any(item["path"] == ".harness-version" for item in sample["divergence"]))
            self.assertIn("source_commit_current", sample["version"])

    def test_missing_default_project_config_reports_canonical_only(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            canonical_copy = Path(tmpdir) / "public_harness_copy"
            subprocess.run(["cp", "-R", str(REPO_ROOT), str(canonical_copy)], check=True)
            config = canonical_copy / "harness-projects.json"
            if config.exists():
                config.unlink()
            result = subprocess.run(
                [sys.executable, str(canonical_copy / "scripts" / "harness_drift_report.py"), "--canonical-root", str(canonical_copy), "--json"],
                cwd=canonical_copy,
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["canonical"]["source_repo"], "ogiberstein/agent-trainer-harness")
            self.assertEqual(payload["projects"], [])

    def test_project_config_file_is_external_and_supports_relative_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canonical_copy = tmp / "agent_trainer_copy"
            project = self._make_project(tmp)
            subprocess.run(["cp", "-R", str(REPO_ROOT), str(canonical_copy)], check=True)
            config = canonical_copy / "harness-projects.json"
            config.write_text(json.dumps({
                "projects": [{
                    "name": "sample",
                    "path": "../project",
                    "mode": "lite",
                    "relationship": "vendored-lite",
                    "sections": ["Visual Pipeline Ownership"],
                }]
            }), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(canonical_copy / "scripts" / "harness_drift_report.py"), "--canonical-root", str(canonical_copy), "--json"],
                cwd=canonical_copy,
                check=True,
                text=True,
                capture_output=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["projects"][0]["name"], "sample")
            self.assertEqual(payload["projects"][0]["path"], str(project.resolve()))

    def test_template_selection_honors_project_kind(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = self._make_project(Path(tmpdir), kind="new-project")
            payload = self._run_json([
                "--canonical-root", str(REPO_ROOT),
                "--project", f"sample={project}:lite:vendored-lite",
            ])
            sample = payload["projects"][0]
            self.assertEqual(sample["project_kind"], "new-project")
            self.assertIn("lite/new-project", sample["canonical_template"])

    def test_markdown_render_includes_staleness_without_decorative_source_commit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = self._make_project(Path(tmpdir))
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--canonical-root", str(REPO_ROOT), "--project", f"sample={project}:lite:vendored-lite"],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertIn("Source commit current:", result.stdout)
            self.assertNotIn("project_source_commit", result.stdout)

    def test_missing_and_extra_statuses_are_reported(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = self._make_project(Path(tmpdir))
            (project / "start.md").unlink()
            (project / "operations" / "local-only.md").write_text("extra\n", encoding="utf-8")
            payload = self._run_json([
                "--canonical-root", str(REPO_ROOT),
                "--project", f"sample={project}:lite:vendored-lite",
            ])
            statuses = {(item["path"], item["status"]) for item in payload["projects"][0]["divergence"]}
            self.assertIn(("start.md", "missing"), statuses)
            self.assertIn(("operations/local-only.md", "extra"), statuses)

    def test_source_commit_current_tracks_template_commit_not_repo_head(self):
        def git(*args: str) -> str:
            return subprocess.run(
                ["git", *args], cwd=REPO_ROOT, check=True, text=True, capture_output=True
            ).stdout.strip()

        template_commit = git("log", "-1", "--format=%H", "--", "lite/existing-project")
        older_commit = git("rev-parse", f"{template_commit}^")
        for source_commit, expected in ((template_commit, True), (older_commit, False)):
            with self.subTest(source_commit=source_commit):
                with tempfile.TemporaryDirectory() as tmpdir:
                    project = self._make_project(Path(tmpdir))
                    (project / ".harness-version").write_text(
                        f"HARNESS_VERSION: {CANONICAL_VERSION}\nmode: lite\n"
                        f"project_kind: existing-project\nrelationship: vendored-lite\n"
                        f"source_repo: ogiberstein/agent-trainer-harness\n"
                        f"source_commit: {source_commit}\n",
                        encoding="utf-8",
                    )
                    payload = self._run_json([
                        "--canonical-root", str(REPO_ROOT),
                        "--project", f"sample={project}:lite:vendored-lite",
                    ])
                    version = payload["projects"][0]["version"]
                    self.assertEqual(version["template_commit"], template_commit)
                    self.assertEqual(version["source_commit_current"], expected)


    def test_control_doc_status_reports_roadmap_migration_state_without_hash_divergence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = self._make_project(Path(tmpdir))
            (project / "BRIEF.md").write_text("brief\n", encoding="utf-8")
            (project / "STATUS.md").write_text("status\n", encoding="utf-8")
            (project / "DECISIONS.md").write_text("decisions\n", encoding="utf-8")
            (project / "PROGRESS.md").write_text("legacy progress\n", encoding="utf-8")
            payload = self._run_json([
                "--canonical-root", str(REPO_ROOT),
                "--project", f"sample={project}:lite:vendored-lite",
            ])
            sample = payload["projects"][0]
            self.assertEqual(sample["summary"]["changed_files"], len(sample["divergence"]))
            self.assertFalse(any(item["path"] in {"ROADMAP.md", "PROGRESS.md"} for item in sample["divergence"]))
            self.assertEqual(sample["control_docs"]["migration_state"], "missing_roadmap_with_legacy_progress")
            self.assertTrue(sample["control_docs"]["roadmap_missing"])
            self.assertTrue(sample["control_docs"]["legacy_progress_present"])
            self.assertIn("ROADMAP.md", sample["control_docs"]["missing"])

    def test_markdown_render_surfaces_control_doc_migration_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = self._make_project(Path(tmpdir))
            (project / "PROGRESS.md").write_text("legacy progress\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--canonical-root", str(REPO_ROOT), "--project", f"sample={project}:lite:vendored-lite"],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assertIn("Control docs: `missing_roadmap_with_legacy_progress`", result.stdout)
            self.assertIn("Missing control docs:", result.stdout)
            self.assertIn("Legacy control doc present: `PROGRESS.md`", result.stdout)

    def test_report_is_read_only_for_project_tree(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project = self._make_project(Path(tmpdir))
            before = {p.relative_to(project): p.read_bytes() for p in project.rglob("*") if p.is_file()}
            self._run_json([
                "--canonical-root", str(REPO_ROOT),
                "--project", f"sample={project}:lite:vendored-lite",
            ])
            after = {p.relative_to(project): p.read_bytes() for p in project.rglob("*") if p.is_file()}
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
