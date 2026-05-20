import importlib.util
import io
import json
import pathlib
import unittest
from contextlib import redirect_stdout
from unittest import mock


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "improve-prompt.py"


def load_module():
    spec = importlib.util.spec_from_file_location("improve_prompt", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ImprovePromptHookTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def run_main(self, prompt):
        stdin = io.StringIO(json.dumps({"prompt": prompt}))
        stdout = io.StringIO()

        with mock.patch("sys.stdin", stdin), redirect_stdout(stdout):
            with self.assertRaises(SystemExit) as ctx:
                self.module.main()

        self.assertEqual(ctx.exception.code, 0)
        return json.loads(stdout.getvalue())

    def test_slash_commands_bypass_wrapper(self):
        result = self.run_main("/pilot")
        self.assertEqual(result["hookSpecificOutput"]["additionalContext"], "")

    def test_star_prefix_passes_through_and_strips_marker(self):
        result = self.run_main("* build a dashboard")
        hook = result["hookSpecificOutput"]
        self.assertEqual(hook["additionalContext"], "")
        self.assertEqual(hook["prompt"], "build a dashboard")
        self.assertEqual(hook["suppressedPrompt"], "* build a dashboard")

    def test_specific_actionable_prompt_skips_wrapper(self):
        result = self.run_main("Add a loading spinner to repo/skills/pilot/SKILL.md")
        self.assertEqual(result["hookSpecificOutput"]["additionalContext"], "")

    def test_specific_debug_prompt_skips_wrapper(self):
        result = self.run_main("Fix the install path mismatch in install.sh for Codex")
        self.assertEqual(result["hookSpecificOutput"]["additionalContext"], "")

    def test_vague_prompt_gets_wrapper(self):
        result = self.run_main("dashboard")
        context = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("[PROMPT EVAL]", context)
        self.assertIn("dashboard", context)


if __name__ == "__main__":
    unittest.main()
