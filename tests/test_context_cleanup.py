import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_runtime_module(module_path: Path, unique_name: str):
    runtime_dir = str(module_path.parent)
    inserted = False
    if runtime_dir not in sys.path:
        sys.path.insert(0, runtime_dir)
        inserted = True
    try:
        spec = importlib.util.spec_from_file_location(unique_name, module_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module
    finally:
        if inserted and sys.path and sys.path[0] == runtime_dir:
            sys.path.pop(0)


class TestConcurrentWorkerContextCleanup(unittest.TestCase):
    def _build_prompt(self, template_root: Path):
        worker = load_runtime_module(template_root / "runtime" / "worker.py", f"worker_{template_root.parts[-2]}_{template_root.parts[-1]}")
        state = load_runtime_module(template_root / "runtime" / "state.py", f"state_{template_root.parts[-2]}_{template_root.parts[-1]}")

        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            (project / "BRIEF.md").write_text("Short project brief.", encoding="utf-8")
            summaries = project / "memory" / "summaries"
            summaries.mkdir(parents=True)
            (summaries / "phase-1-requirements.md").write_text("Old summary that should stay out of default prompt context.", encoding="utf-8")
            (summaries / "phase-2-design.md").write_text("Latest summary that should be loaded automatically.", encoding="utf-8")

            task_kwargs = dict(
                id="TASK-IMP-001",
                title="Implement feature",
                role="fullstack-engineer",
                phase="implementation",
                acceptance="Ship the implementation.",
            )
            if "required_reads" in getattr(state.Task, "__dataclass_fields__", {}):
                task_kwargs["required_reads"] = ["specs/requirements.md"]
            task = state.Task(**task_kwargs)
            return worker._build_task_prompt(task, str(project))

    def test_latest_phase_summary_is_included_for_new_project_worker(self):
        prompt = self._build_prompt(REPO_ROOT / "concurrent" / "new-project")
        self.assertIn("Latest summary that should be loaded automatically.", prompt)
        self.assertNotIn("Old summary that should stay out of default prompt context.", prompt)

    def test_latest_phase_summary_is_included_for_existing_project_worker(self):
        prompt = self._build_prompt(REPO_ROOT / "concurrent" / "existing-project")
        self.assertIn("Latest summary that should be loaded automatically.", prompt)
        self.assertNotIn("Old summary that should stay out of default prompt context.", prompt)

    def test_prompt_contains_context_cleanup_instruction(self):
        prompt = self._build_prompt(REPO_ROOT / "concurrent" / "new-project")
        self.assertIn("Treat the latest phase summary as the canonical prior context.", prompt)
        self.assertIn("Do not reopen older summaries or archived snapshots", prompt)


class TestHarnessTemplatesMentionContextCleanup(unittest.TestCase):
    def test_all_mode_agents_define_active_context_cleanup(self):
        for mode in ("lite", "full", "concurrent"):
            for project_kind in ("new-project", "existing-project"):
                content = (REPO_ROOT / mode / project_kind / "AGENTS.md").read_text(encoding="utf-8")
                self.assertIn("drop old optional context from your active set", content)
                self.assertIn("latest relevant summary", content)

    def test_all_mode_guidelines_define_cleanup_step(self):
        for mode in ("lite", "full", "concurrent"):
            for project_kind in ("new-project", "existing-project"):
                content = (REPO_ROOT / mode / project_kind / "operations" / "context-efficiency-guidelines.md").read_text(encoding="utf-8")
                self.assertIn("Context Cleanup on Phase/Task Change", content)
                self.assertIn("Treat that latest summary or handoff as canonical.", content)


if __name__ == "__main__":
    unittest.main()
