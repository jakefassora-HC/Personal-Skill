# Pipelines

Improve, Debug, Explain, Finish, and stage tracking.

---

## Improve

For "add", "change", "update", "modify", "replace" intent.

1. Read the relevant file(s) before touching anything
2. Make the change directly — no agents for simple edits
3. Invoke `superpowers:verification-before-completion` before declaring done
4. Report: "Done. [what changed, file:line]"

Never touch files outside what was asked. If scope is unclear, ask one question.

---

## Debug

For error pastes, "broken", "not working", "big issue", "I can't" intent.

Invoke `superpowers:systematic-debugging`.

1. Read the error and surrounding code
2. Identify root cause
3. Apply fix
4. Verify fix didn't break anything else

Report: fix applied + one-line root cause (only if it helps avoid the same mistake).

---

## Explain

For "why", "how", "what is", "explain", "I don't understand" intent.

Answer directly in plain English. Use analogies for unfamiliar concepts.
Lead with the answer, not the background. Keep it short unless they ask for more.

No code unless it makes the explanation clearer.

---

## Finish

For "commit", "push", "save", "ship", "deploy" intent.

Invoke `superpowers:finishing-a-development-branch`.

1. Check for uncommitted changes
2. Stage relevant files (specific names, not `git add .`)
3. Commit with a descriptive message (what changed and why)
4. Push to current branch

Report: "Committed to [branch]. [N] files changed."

---

## Stage Tracking

What "yes / ok / looks good" means at each point in a build:

| When it appears | What it means | What happens next |
|---|---|---|
| During discovery questions | Answer to current question | Ask next question |
| After scope check offer | Full build or core-first decision | Proceed accordingly |
| After plain-English summary | Spec approved | Invoke writing-plans |
| After plan presented | Plan approved | Invoke subagent-driven-development |
| After build complete | Looks good | Offer to commit/push |
| After a change/fix | Done looks right | Close out |
| After explanation | Got it | Continue |

If "yes" is ambiguous, check which stage you're in and advance accordingly.
