#!/usr/bin/env python3
"""
UserPromptSubmit hook — prompt clarity evaluator.

Reads the hook event JSON from stdin, applies bypass rules, and wraps
vague prompts with evaluation instructions that tell Claude to invoke
the prompt-improver skill if clarification is needed.

Exit codes:
  0  — allow the prompt through (with or without wrapper)
  2  — block the prompt (unused here, reserved)
"""

import json
import re
import sys


EVALUATION_WRAPPER = """\
[PROMPT EVAL] Evaluate if this prompt has enough context to execute well.

Proceed immediately if:
- The prompt is specific and actionable
- You have sufficient context from conversation history
- Intent can be clearly inferred without ambiguity

If genuinely vague or missing key details that would materially change the output, \
invoke the prompt-improver skill to research the codebase and ask targeted questions first.

When in doubt, proceed — only invoke prompt-improver if clarification is truly needed.

User prompt:
{prompt}"""

ACTION_VERBS = {
    "add",
    "build",
    "change",
    "commit",
    "create",
    "debug",
    "deploy",
    "document",
    "explain",
    "fix",
    "improve",
    "investigate",
    "merge",
    "plan",
    "push",
    "refactor",
    "remove",
    "rename",
    "replace",
    "ship",
    "update",
    "write",
}

DEBUG_HINTS = {
    "broken",
    "crash",
    "error",
    "failing",
    "mismatch",
    "not working",
    "traceback",
}

VAGUE_PROMPTS = {
    "app",
    "broken",
    "dashboard",
    "feature",
    "help",
    "idea",
    "pipeline",
    "this",
}

FILE_HINT_RE = re.compile(
    r"[/\\]|`[^`]+`|\b[\w.-]+\.(?:py|md|js|ts|tsx|jsx|json|toml|yaml|yml|sh)\b"
)

WORD_RE = re.compile(r"[a-z0-9_.-]+")


def build_output(additional_context: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context,
        }
    }


def _word_tokens(prompt: str) -> list[str]:
    return WORD_RE.findall(prompt.lower())


def prompt_is_specific(prompt: str) -> bool:
    stripped = prompt.strip()
    if not stripped:
        return True

    words = _word_tokens(stripped)
    if not words:
        return False

    if len(words) <= 2 and all(word in VAGUE_PROMPTS for word in words):
        return False

    lower = stripped.lower()

    if "\n" in stripped and len(stripped) >= 40:
        return True

    if FILE_HINT_RE.search(stripped):
        return True

    if any(hint in lower for hint in DEBUG_HINTS) and len(words) >= 4:
        return True

    if any(word in ACTION_VERBS for word in words) and len(words) >= 5:
        return True

    if stripped.endswith("?") and len(words) >= 5:
        return True

    return False


def main() -> None:
    try:
        raw = sys.stdin.read()
        event = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as e:
        # Malformed input — pass through without modification
        print(json.dumps(build_output("")))
        sys.exit(0)

    prompt: str = event.get("prompt", "")

    # Bypass: slash commands (skill invocations, built-in commands)
    if prompt.startswith("/"):
        print(json.dumps(build_output("")))
        sys.exit(0)

    # Bypass: comment / annotation lines
    if prompt.startswith("#"):
        print(json.dumps(build_output("")))
        sys.exit(0)

    # Bypass: explicit pass-through prefix (*) — strip the marker and allow
    if prompt.startswith("*"):
        stripped = prompt[1:].lstrip()
        output = build_output("")
        # Rewrite the prompt without the bypass marker
        output["hookSpecificOutput"]["suppressedPrompt"] = prompt
        output["hookSpecificOutput"]["prompt"] = stripped
        print(json.dumps(output))
        sys.exit(0)

    if prompt_is_specific(prompt):
        print(json.dumps(build_output("")))
        sys.exit(0)

    # All other prompts: wrap with evaluation instructions
    wrapped = EVALUATION_WRAPPER.format(prompt=prompt)
    print(json.dumps(build_output(wrapped)))
    sys.exit(0)


if __name__ == "__main__":
    main()
