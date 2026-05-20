import pathlib
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


class SkillDocRegressionTests(unittest.TestCase):
    def test_pilot_summary_no_long_prebuild_artifact_claims(self):
        text = (REPO_ROOT / "skills" / "pilot" / "build-pipeline.md").read_text()
        self.assertNotIn("**WHAT GETS CREATED**", text)
        self.assertNotIn("**HOW TO RUN IT**", text)
        self.assertIn("GOAL:", text)
        self.assertIn("MUST-HAVES:", text)

    def test_start_is_not_described_as_universal_autofire(self):
        text = (REPO_ROOT / "skills" / "start" / "SKILL.md").read_text()
        self.assertNotIn("Auto-fires on ANY intent", text)
        self.assertNotIn("When in doubt, trigger this skill.", text)

    def test_install_script_mentions_codex_home(self):
        text = (REPO_ROOT / "install.sh").read_text()
        self.assertIn('CODEX_HOME', text)
        self.assertIn('.codex', text)


if __name__ == "__main__":
    unittest.main()
