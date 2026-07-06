import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FULL_KINDS = ("new-project", "existing-project")


class TestFullComplexGuardrailContract(unittest.TestCase):
    def test_full_agents_define_complex_implementation_guardrail(self):
        for kind in FULL_KINDS:
            content = (REPO_ROOT / "full" / kind / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Complex implementation guardrail", content)
            self.assertIn("fact-only code/context note", content)
            self.assertIn("bounded task checklist", content)
            self.assertIn("clear verification per task or phase", content)

    def test_full_implementation_gate_checks_complex_tasks(self):
        for kind in FULL_KINDS:
            content = (REPO_ROOT / "full" / kind / "evaluation" / "release-gates.md").read_text(encoding="utf-8")
            self.assertIn("Phase 3 — Implementation Gate", content)
            self.assertIn("Complex implementation tasks have a fact-only code/context note", content)
            self.assertIn("bounded, testable task checklist", content)


if __name__ == "__main__":
    unittest.main()
