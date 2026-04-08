# hc — Personal Claude Code + Codex Setup

My personal pilot skill and workflow documentation. The `pilot` skill is a single entry point that routes natural language into the right superpowers workflow chains automatically, with my behavioral profile baked in.

Works in both **Claude Code** and **Codex** — one skill file, one source of truth.

---

## Install

### Claude Code

```bash
cp -r skills/pilot ~/.claude/skills/pilot
```

Restart Claude Code. `pilot` appears in the skills list automatically.

### Codex

Codex reads from `~/.agents/skills/`. Use a symlink so both tools share the same file — edit once, works everywhere:

```bash
mkdir -p ~/.agents/skills
ln -sf ~/.claude/skills/pilot ~/.agents/skills/pilot
```

If you don't have Claude Code installed, copy directly instead:

```bash
mkdir -p ~/.agents/skills
cp -r skills/pilot ~/.agents/skills/pilot
```

Restart Codex. `pilot` is discovered automatically.

### Keeping in sync

The symlink approach means `~/.claude/skills/pilot/SKILL.md` is the single source of truth. Any edit you make to the skill is instantly available in both Claude Code and Codex — no copy step needed.

### Prerequisites for Codex subagent features

The build pipeline spawns multiple agents in parallel. Enable multi-agent support in Codex:

```toml
# ~/.codex/config.toml
[features]
multi_agent = true
```

Without this, the improve/debug/finish pipelines still work — only the full build pipeline requires it.

---

## How Tool Names Map (Codex vs Claude Code)

The pilot skill calls superpowers skills by name — those work the same in both tools. Internally, superpowers uses Claude Code tool names. Codex translates them automatically:

| Claude Code | Codex |
|---|---|
| `Task` (dispatch subagent) | `spawn_agent` |
| `TodoWrite` | `update_plan` |
| `Skill` (invoke skill) | native — loads automatically |
| `Read`, `Write`, `Edit` | native file tools |
| `Bash` | native shell tools |

You don't need to do anything — Codex handles this translation via its built-in `codex-tools.md` reference from superpowers.

---

## What Pilot Does

One skill that detects what you want from how you naturally talk and chains the right superpowers skills — no manual skill invocations needed.

```
"let's build X"    → product questions → plan → parallel agent team → working app
"add X"            → direct change → verified
error paste        → diagnosed + fixed
"commit"           → staged, committed, pushed
```

---

## Full Routing Map

```
╔══════════════════════════════════════════════════════════════════╗
║                        YOUR MESSAGE                              ║
╚══════════════════════════╤═══════════════════════════════════════╝
                           │
                    ┌──────▼──────┐
                    │    PILOT    │  ← reads CLAUDE.md profile
                    │   detects   │    on every invoke
                    │   intent    │
                    └──────┬──────┘
                           │
     ┌──────────┬──────────┼──────────┬──────────┬──────────┐
     │          │          │          │          │          │
     ▼          ▼          ▼          ▼          ▼          ▼
 let's /    add /       error /    yes /      why /     commit /
 build /    change /    broken /   ok /       how /     push /
 create /   update /    big issue  yeah /     explain   ship
 new /      I want      [paste]    great
 want to    you to

     │          │          │          │          │          │
     ▼          ▼          ▼          ▼          ▼          ▼
 ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐
 │ BUILD │  │IMPROVE│  │ DEBUG │  │ADVANCE│  │EXPLAIN│  │FINISH │
 └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘
```

---

## Build Pipeline — Full Agent Map

```
  PILOT (you)
  ┌────────────────────────────────────────────────────────────────────┐
  │  DISCOVERY — questions until 90% confidence across 8 dimensions   │
  │                                                                    │
  │  Dimension        What it needs                                   │
  │  ─────────────    ────────────────────────────────────────────    │
  │  Core purpose     What it does in one sentence                    │
  │  Users            Who uses it and their goal                      │
  │  Key flows        What they open, click, see                      │
  │  Primary fn       Most important thing it does                    │
  │  Feature scope    Must-haves vs nice-to-haves                     │
  │  Success          What "done" looks like                          │
  │  Data / APIs      What data it needs, any connections             │
  │  Visual           Any UI requirements or examples                 │
  │                                                                    │
  │  Asks 1 question → gets answer → re-scores all dimensions         │
  │  Keeps going until all 8 are at 90%+  (usually 5–15 questions)   │
  └──────────────────────────────────┬─────────────────────────────────┘
                                     │  all 8 at 90%+
                                     ▼
  PILOT (internal)
  ┌────────────────────────────────────────────────────────────────────┐
  │  Silently generates complete technical spec                        │
  │  Chooses stack (Flask + vanilla JS + SQLite by default)           │
  │  Shows plain-English summary — 3–5 bullets                        │
  │  Waits for "yes/ok/looks good"                                    │
  └──────────────────────────────────┬─────────────────────────────────┘
                                     │  approved
                                     ▼
  superpowers:writing-plans
  ┌────────────────────────────────────────────────────────────────────┐
  │  spawns ──► PLAN AGENT                                            │
  │              Reads spec                                           │
  │              Breaks work into independent tasks                   │
  │              Writes PLAN.md                                       │
  │              Identifies file structure + dependencies             │
  └──────────────────────────────────┬─────────────────────────────────┘
                                     │  PLAN.md ready
                                     ▼
  superpowers:subagent-driven-development
  ┌────────────────────────────────────────────────────────────────────┐
  │  For EACH task in the plan:                                        │
  │                                                                    │
  │  ┌─────────────────────────────────────────────────────────────┐  │
  │  │  IMPLEMENTER AGENT  (fresh context, isolated)               │  │
  │  │  Follows TDD: test first → watch fail → write code          │  │
  │  │  Commits when done, self-reviews                            │  │
  │  └──────────────────────────┬──────────────────────────────────┘  │
  │                             │                                      │
  │  ┌──────────────────────────▼──────────────────────────────────┐  │
  │  │  SPEC REVIEWER AGENT                                        │  │
  │  │  Does code match the spec? Nothing missing, nothing extra?  │  │
  │  │  ❌ → implementer fixes → re-review                         │  │
  │  │  ✅ → next gate                                             │  │
  │  └──────────────────────────┬──────────────────────────────────┘  │
  │                             │  spec ✅                             │
  │  ┌──────────────────────────▼──────────────────────────────────┐  │
  │  │  CODE QUALITY REVIEWER AGENT                                │  │
  │  │  Is it clean, no regressions, no hacks?                     │  │
  │  │  ❌ → implementer fixes → re-review                         │  │
  │  │  ✅ → task complete                                         │  │
  │  └──────────────────────────┬──────────────────────────────────┘  │
  │                                                                    │
  │  Repeat per task ──────────────────────────────────────────────── │
  │                                                                    │
  │  All tasks done:                                                   │
  │  ┌─────────────────────────────────────────────────────────────┐  │
  │  │  FINAL REVIEWER AGENT                                       │  │
  │  │  Reviews entire implementation end-to-end                   │  │
  │  │  Checks all pieces wire together correctly                  │  │
  │  └─────────────────────────────────────────────────────────────┘  │
  └──────────────────────────────────┬─────────────────────────────────┘
                                     │  all approved
                                     ▼
                           ┌───────────────────┐
                           │   WORKING APP     │
                           │  python app.py    │
                           └───────────────────┘

  Agent count for a typical 4-task build:
    1  Plan agent
    4  Implementer agents    (one per task, each runs TDD)
    4  Spec reviewer agents
    4  Code quality agents
    1  Final reviewer agent
   ─────────────────────────
   14  agents minimum
```

---

## Improve Pipeline

```
  PILOT parses change from your message
       │
       ▼
  Makes the change directly (no agents for simple edits)
       │
       ▼
  superpowers:verification-before-completion
  Runs / checks / confirms nothing regressed
       │
       ▼
  "Done. [what changed and where]"
```

---

## Debug Pipeline

```
  superpowers:systematic-debugging
       │
       ▼
  DIAGNOSTIC AGENT
  Reads error + surrounding code
  Identifies root cause
  Applies fix
  Verifies fix didn't break anything
       │
       ▼
  fix + 1-line root cause
```

---

## Finish Pipeline

```
  superpowers:finishing-a-development-branch
       │
       ▼
  Checks uncommitted changes
  Stages files
  Commits with descriptive message
  Pushes to current branch
       │
       ▼
  "Committed to [branch]. [N] files changed."
```

---

## Stage Tracking (what "yes/ok" means at each point)

| When it appears | What it means | What happens |
|---|---|---|
| During discovery questions | Answer to current question | Ask next question |
| After plain-English spec summary | Spec approved | Invoke writing-plans |
| After plan presented | Plan approved | Invoke subagent-driven-development |
| After build complete | Looks good | Offer to commit/push |
| After a change/fix | Done looks right | Close out |
| After explanation | Got it | Continue |

---

## Profile Directives (baked into every pipeline)

| Directive | What it means in practice |
|---|---|
| Terse register | Lead with result. Match message length. No preambles. |
| Recommend then wait | State recommendation + 1-line reason, wait for "ok" |
| Fix-first | Diagnose + fix directly. No step-by-step walkthroughs. |
| Pick the tool | One library chosen and named. No comparison menus. |
| Explain after | Result first. Brief rationale only if non-obvious. |
| Stay in scope | Never touch outside what was asked. When in doubt, ask one question. |
| Guided learning | Plain English + analogies when asked "why/how". |
| Boundaries are hard | "NEVER do X" is permanent and absolute. No exceptions. |

---

## Skill File

→ [`skills/pilot/SKILL.md`](skills/pilot/SKILL.md)

To update: edit the SKILL.md, copy back to `~/.claude/skills/pilot/SKILL.md`, restart Claude Code.

---

## Superpowers Skills Reference

Skills pilot chains into:

| Skill | When used |
|---|---|
| `superpowers:writing-plans` | After spec approved — generates PLAN.md |
| `superpowers:subagent-driven-development` | Executes PLAN.md with parallel agents |
| `superpowers:verification-before-completion` | After every Improve change |
| `superpowers:systematic-debugging` | On any error / broken behavior |
| `superpowers:finishing-a-development-branch` | On commit/push/ship |
