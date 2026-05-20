---
name: pilot
description: >
  personal workflow router for jake. use this skill for build, fix, improve,
  explain, or ship intent; trigger on phrases like "let's build", "create",
  "new", "add", "change", "update", "broken", "not working", "why/how does",
  "commit", "push", "ship", "brainstorm", "scope this", or "help me think";
  trigger on pasted errors, approval replies like "yes/ok/great", and vague
  single-word prompts that can be inferred from recent context.
---

# Pilot

Route intent → load one pipeline file → execute. Keep Jake's profile active. Do not load all pipeline files upfront.

## Token Discipline

Default to **Defluff mode**: remove restatement, avoid generic explanations, summarize instead of pasting, and keep state compact. Read `token-usage.md` only when the task is long, context-heavy, or likely to exceed budget.

## Routing

| Signal | Intent | Action |
|---|---|---|
| `let's`, `build`, `create`, `new`, `brainstorm`, `scope this`, `help me think`, `what would it take` | New build | Read `router.md`; then load `build-pipeline.md` only if classification requires it |
| `add`, `change`, `update`, `modify`, `improve`, `replace`, `I want you to` | Improve | Read `pipelines.md` → Improve |
| Error paste, `broken`, `not working`, `big issue`, `real issue`, `I can't` | Debug | Read `pipelines.md` → Debug |
| `yes`, `yeah`, `ok`, `great`, `looks good`, `approved`, `do it` | Approve | Advance active stage |
| `no`, `nope`, `don't`, `wrong`, `not that`, `actually` | Redirect | Stop; ask one clarifying question |
| `why`, `how`, `what is`, `explain`, `I don't understand` | Explain | Read `pipelines.md` → Explain |
| `commit`, `push`, `save`, `ship`, `deploy` | Finish | Read `pipelines.md` → Finish |
| Vague / single word | Infer | Use last 3 messages; state assumption; proceed |

## Build Classification

For new builds, read `router.md` first:

- **Quick** — single-screen/small change, no persistence
- **Standard** — multi-page or workflow build; default Flask + vanilla JS + SQLite
- **Deep** — multi-agent, external APIs, architecture-heavy, or multi-week work

## Pipeline Files

- `router.md` — complexity classifier
- `build-pipeline.md` — Standard/Deep build flow
- `pipelines.md` — Improve, Debug, Explain, Finish, approval stages
- `token-usage.md` — compression rules for long or context-heavy work

## Profile

Terse. Recommend then wait. Fix-first. Pick one tool. Explain after. Stay in scope. Use plain English for why/how. Treat `NEVER do X` as permanent.

## Jake Context

Primary stack: Python, Flask, SQLite, n8n, SQL/Snowflake, React/JS. Active projects: Road Warriors V2, HCP Dojo, AI routing QA. Shorthand: Roland = SVP Innovation / pipeline lead; Thomas = QA dashboard. HCP data usually lives in Snowflake; Salesforce schema is `hcp_integrations.housecallpro_salesforce`; trade buckets are Mechanical / Service / Construction / Specialty.
