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


def build_output(additional_context: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context,
        }
    }


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

    # All other prompts: wrap with evaluation instructions
    wrapped = EVALUATION_WRAPPER.format(prompt=prompt)
    print(json.dumps(build_output(wrapped)))
    sys.exit(0)


if __name__ == "__main__":
    main()
