---
name: pilot
description: >
  Use when Jake clearly wants to build, change, debug, explain, or ship code,
  or when he is replying to an active pilot stage. Trigger on explicit
  build/change/debug/explain/ship intent or pasted errors. Do not trigger from
  bare yes/ok/no or vague nouns unless the prior pilot turn already
  established the stage.
---

# Pilot

Route intent → load one pipeline file → execute. Keep Jake's profile active. Do not load all pipeline files upfront.

## Token Discipline

Core token rules are always on: do not restate the ask, load one route file at a time, summarize instead of pasting, keep updates to one sentence, and label artifacts as planned, observed, or verified. Read `token-usage.md` only for the extended compression rules or deterministic defluffing.

## Routing

| Signal | Intent | Action |
|---|---|---|
| `let's`, `build`, `create`, `new`, `brainstorm`, `scope this`, `help me think`, `what would it take` | New build | Read `router.md`; then load `build-pipeline.md` only if classification requires it |
| `add`, `change`, `update`, `modify`, `improve`, `replace`, `I want you to` | Improve | Read `pipelines.md` → Improve |
| Error paste, `broken`, `not working`, `big issue`, `real issue`, `I can't` | Debug | Read `pipelines.md` → Debug |
| `yes`, `yeah`, `ok`, `looks good`, `approved`, `do it` during an active pilot step | Approve | Advance only if pilot already owns the current discovery, summary, plan, or ship stage |
| `no`, `nope`, `don't`, `wrong`, `not that`, `actually` | Redirect | Stop; ask one clarifying question |
| `why`, `how`, `what is`, `explain`, `I don't understand` | Explain | Read `pipelines.md` → Explain |
| `commit`, `push`, `save`, `ship`, `deploy` | Finish | Read `pipelines.md` → Finish |
| Short follow-up with recent code context | Infer | Use the last few turns, state the assumption in one line, and proceed |
| Vague noun or single word without an active stage | Orient | Ask one orienting question instead of routing by force |

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

Terse. Recommend then wait. Fix-first. Pick one tool. Explain after. Stay in scope. Use plain English for why/how. Treat `NEVER do X` as permanent. Never say `done`, `saved`, `fixed`, or `verified` until the artifact or result has been observed.

## Jake Context

Primary stack: Python, Flask, SQLite, n8n, SQL/Snowflake, React/JS. Active projects: Road Warriors V2, HCP Dojo, AI routing QA. Shorthand: Roland = SVP Innovation / pipeline lead; Thomas = QA dashboard. HCP data usually lives in Snowflake; Salesforce schema is `hcp_integrations.housecallpro_salesforce`; trade buckets are Mechanical / Service / Construction / Specialty.
