import os
import pathlib
import subprocess
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = REPO_ROOT / "install.sh"


class InstallScriptTests(unittest.TestCase):
    def run_install(self, *args):
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)

        home = pathlib.Path(tmpdir.name) / "home"
        codex_home = pathlib.Path(tmpdir.name) / "codex-home"
        home.mkdir()
        codex_home.mkdir()

        env = os.environ.copy()
        env["HOME"] = str(home)
        env["CODEX_HOME"] = str(codex_home)

        result = subprocess.run(
            ["bash", str(INSTALL_SCRIPT), *args],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        return result, home, codex_home

    def test_codex_install_uses_codex_home_skills_directory(self):
        result, _, codex_home = self.run_install("--codex", "--source", "skills/pilot")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((codex_home / "skills" / "pilot" / "SKILL.md").is_file())

    def test_default_install_copies_full_skill_bundle(self):
        result, home, codex_home = self.run_install("--both")
        self.assertEqual(result.returncode, 0, result.stderr)
        for root in (home / ".claude" / "skills", codex_home / "skills"):
            self.assertTrue((root / "pilot" / "SKILL.md").is_file())
            self.assertTrue((root / "start" / "SKILL.md").is_file())
            self.assertTrue((root / "prompt-improver" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
