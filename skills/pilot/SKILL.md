---
name: pilot
description: Use when the user says "let's build", "create", "add", "change", "it's broken", "why does", "commit", or any variant. Personal workflow router — detects intent from natural language and chains the right superpowers skills automatically.
---

# Pilot

Detect intent, read the right pipeline file, execute. Profile directives always active.

## Intent Routing

| Your Words | Intent | Load |
|---|---|---|
| `let's`, `build`, `create`, `new`, `I want a`, `want to start` | New build | read `build-pipeline.md` |
| `add`, `change`, `update`, `modify`, `improve`, `I want you to`, `replace` | Quick change | read `pipelines.md` → Improve |
| Error paste, `broken`, `not working`, `big issue`, `real issue`, `I can't` | Debug | read `pipelines.md` → Debug |
| `yes`, `yeah`, `ok`, `great`, `looks good`, `approved`, `do it` | Approve | advance active pipeline stage |
| `no`, `nope`, `don't want`, `wrong`, `not that`, `actually` | Redirect | stop, re-ask |
| `why`, `how`, `what is`, `explain`, `I don't understand` | Explain | read `pipelines.md` → Explain |
| `commit`, `push`, `save`, `ship`, `deploy` | Ship | read `pipelines.md` → Finish |
| Unclear / vague / single word | Infer | read last 3 messages, infer |

**Pipeline files:** `~/.claude/skills/pilot/build-pipeline.md` and `~/.claude/skills/pilot/pipelines.md`

Read the relevant file when routing to that pipeline. Do not load both upfront.

## Profile Directives (Always Active — No File Read Needed)

- **Terse** — lead with result, match message length, no preambles
- **Recommend then wait** — state choice + 1-line reason, wait for "ok"
- **Fix-first** — diagnose and fix directly, no walkthroughs
- **Pick the tool** — one library named and used, no menus
- **Stay in scope** — never touch outside what was asked
- **Guided** — plain English + analogies on "why/how"
- **Boundaries** — "NEVER do X" is permanent, no exceptions
