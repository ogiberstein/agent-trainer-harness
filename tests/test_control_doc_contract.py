import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOTS = (
    REPO_ROOT / "lite" / "new-project",
    REPO_ROOT / "lite" / "existing-project",
    REPO_ROOT / "full" / "new-project",
    REPO_ROOT / "full" / "existing-project",
    REPO_ROOT / "concurrent" / "new-project",
    REPO_ROOT / "concurrent" / "existing-project",
)


class TestControlDocContract(unittest.TestCase):
    def test_templates_use_roadmap_not_progress(self):
        for template_root in TEMPLATE_ROOTS:
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                self.assertTrue((template_root / "ROADMAP.md").is_file())
                self.assertFalse((template_root / "PROGRESS.md").exists())

    def test_agents_reference_roadmap_contract(self):
        for template_root in TEMPLATE_ROOTS:
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                agents = (template_root / "AGENTS.md").read_text(encoding="utf-8")
                self.assertIn("ROADMAP.md", agents)
                self.assertIn("Product sequencing", agents)
                self.assertNotIn("PROGRESS.md", agents)

    def test_roadmap_template_has_required_sections(self):
        required_sections = (
            "## North Star",
            "## Now / Next / Later",
            "### Now",
            "### Next",
            "### Later / Deferred",
            "## Milestones",
            "## Non-Goals / Parking Lot",
            "## Roadmap Change Log",
        )
        for template_root in TEMPLATE_ROOTS:
            roadmap = (template_root / "ROADMAP.md").read_text(encoding="utf-8")
            with self.subTest(template=str(template_root.relative_to(REPO_ROOT))):
                for section in required_sections:
                    self.assertIn(section, roadmap)

    def test_operational_docs_do_not_omit_roadmap_from_core_contract(self):
        stale_snippets = (
            "always keep `STATUS.md`, `DECISIONS.md`, and `BRIEF.md`",
            "always keep `STATUS.md`, `DECISIONS.md`, and memory summaries",
            "always maintain `STATUS.md`, `DECISIONS.md`, and memory summaries",
            "Core files exist (`AGENTS.md`, `BRIEF.md`, `STATUS.md`, `DECISIONS.md`)",
            "Add at minimum: `STATUS.md`, `DECISIONS.md`, `memory/summaries/`",
            "Light-touch: Add `STATUS.md`, `DECISIONS.md`, `memory/`, `runtime/`, and `cli/`",
            "Memory layer: Phase summaries with carried constraints, decision log. Survives session boundaries. (`memory/`, `STATUS.md`, `DECISIONS.md`)",
        )
        docs = []
        for template_root in TEMPLATE_ROOTS:
            docs.extend(template_root.glob("*.md"))
            docs.extend((template_root / "operations").glob("*.md"))
            docs.extend((template_root / "memory").glob("*.md"))
        for doc in docs:
            content = doc.read_text(encoding="utf-8")
            with self.subTest(path=str(doc.relative_to(REPO_ROOT))):
                for snippet in stale_snippets:
                    self.assertNotIn(snippet, content)

    def test_readme_uses_dotfile_safe_copy_commands_and_no_manual_counts(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("cp -a full/new-project/.", readme)
        self.assertIn("cp -a full/existing-project/.", readme)
        self.assertNotIn("cp -R full/new-project/*", readme)
        self.assertNotIn("files —", readme)

    def test_root_roadmap_is_general_harness_roadmap_not_concurrent_only(self):
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("# Agent Trainer Harness Roadmap", roadmap)
        self.assertIn("## North Star", roadmap)
        self.assertIn("## Concurrent Harness Parking Lot", roadmap)
        self.assertNotIn("# Roadmap — Concurrent Harness", roadmap)


if __name__ == "__main__":
    unittest.main()
