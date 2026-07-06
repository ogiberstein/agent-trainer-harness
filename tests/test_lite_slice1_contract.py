import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LITE_KINDS = ("new-project", "existing-project")
ROLE_FILES = ("orchestrator.md", "fullstack-engineer.md", "qa-engineer.md")


class TestLiteSlice1Contract(unittest.TestCase):
    def _lite_agents(self, kind: str) -> str:
        return (REPO_ROOT / "lite" / kind / "AGENTS.md").read_text(encoding="utf-8")

    def test_lite_agents_require_decide_before_build(self):
        for kind in LITE_KINDS:
            content = self._lite_agents(kind)
            self.assertIn("Decide Before Build", content)
            self.assertIn("Before non-trivial implementation", content)
            self.assertIn("approach", content)
            self.assertIn("open unknowns", content)

    def test_lite_agents_require_verified_done_checklist(self):
        for kind in LITE_KINDS:
            content = self._lite_agents(kind)
            self.assertIn("Done Means Verified", content)
            self.assertIn("Tests/build/validation were run", content)
            self.assertIn("Unable to verify", content)
            self.assertIn("do not claim done", content)

    def test_lite_agents_define_fresh_context_delegation_without_ceremony(self):
        for kind in LITE_KINDS:
            content = self._lite_agents(kind)
            self.assertIn("Fresh-Context Delegation", content)
            self.assertIn("heavy work", content)
            self.assertIn("fresh-context subagent", content)
            self.assertIn("Small local edits do not need delegation", content)

    def test_lite_agents_define_complex_task_guardrail_without_mandatory_ceremony(self):
        for kind in LITE_KINDS:
            agents = self._lite_agents(kind)
            self.assertIn("complex-task guardrail", agents)
            self.assertIn("fact-only note", agents)
            self.assertIn("feasible, atomic, clear, testable, and scoped", agents)
            self.assertIn("Skip this ceremony for tiny local edits", agents)

            orchestrator = (REPO_ROOT / "lite" / kind / "harness" / "agents" / "orchestrator.md").read_text(encoding="utf-8")
            self.assertIn("fact-only research", orchestrator)
            self.assertIn("feasible, atomic, clear, testable, and scoped", orchestrator)

            guidelines = (REPO_ROOT / "lite" / kind / "operations" / "context-efficiency-guidelines.md").read_text(encoding="utf-8")
            self.assertIn("memory/plans/", guidelines)
            self.assertIn("do not create plan files for tiny edits", guidelines)

    def test_lite_role_files_are_plain_checklists_without_personas(self):
        for kind in LITE_KINDS:
            for role_file in ROLE_FILES:
                content = (REPO_ROOT / "lite" / kind / "harness" / "agents" / role_file).read_text(encoding="utf-8")
                self.assertNotIn("## Identity", content)
                self.assertNotIn("**Name:**", content)
                self.assertNotIn("**Profile:**", content)
                self.assertNotIn("**Voice:**", content)
                self.assertIn("## Role", content)
                self.assertIn("## Acceptance Checklist", content)


if __name__ == "__main__":
    unittest.main()
