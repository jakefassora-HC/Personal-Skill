---
name: pilot
description: Use when the user says "let's build", "create", "add", "change", "it's broken", "why does", "commit", or any variant. Personal workflow router — detects intent from natural language and chains the right superpowers skills automatically.
---

# Pilot

Personalized workflow router. Detects what you want from how you naturally talk, routes to the right superpowers skill chain, applies your behavioral profile throughout. You don't invoke sub-skills manually — pilot does it.

---

## Intent Routing

Read the first 1–3 words plus any trigger words. Route immediately.

| Your Words | Intent | What Runs |
|---|---|---|
| `let's`, `build`, `create`, `new`, `I want a`, `want to start` | New build | → Build Pipeline |
| `add`, `change`, `update`, `modify`, `improve`, `I want you to`, `replace` | Quick change | → Improve Pipeline |
| Error paste, `broken`, `not working`, `big issue`, `real issue`, `I can't` | Debug | → Debug Pipeline |
| `yes`, `yeah`, `ok`, `great`, `looks good`, `approved`, `do it` | Approve | → Advance active pipeline |
| `no`, `nope`, `don't want`, `wrong`, `not that`, `actually` | Redirect | → Stop, re-ask |
| `why`, `how`, `what is`, `what does`, `explain`, `I don't understand` | Explain | → Plain-English answer |
| `commit`, `push`, `save`, `ship`, `deploy` | Ship | → Finishing Pipeline |
| Unclear / vague / single word | Infer | → Read last 3 messages, infer and proceed |

---

## Build Pipeline

**Trigger:** User wants something new — app, dashboard, tool, feature.

### Step 1: Product Discovery (90% Confidence Model)

Ask questions **one at a time**, plain English only, no technical questions ever. Keep asking until confidence reaches 90%+ across all 8 dimensions. Minimum ~5 questions, no fixed upper limit.

**Track confidence per dimension after every answer:**

| Dimension | What you need to know |
|---|---|
| Core purpose | What it does in one sentence |
| Users | Who uses it and what's their goal |
| Key flows | What they open, click, and see in a session |
| Primary function | The single most important thing it does |
| Feature scope | Must-haves vs. nice-to-haves |
| Success criteria | What "done" looks like |
| Data & connections | What data it needs, any APIs or external services |
| Visual expectations | Any specific UI requirements or examples |

After each answer, silently assess: which dimensions are still below 90%? Ask the next question targeting the lowest-confidence dimension.

**Stop asking when:** All 8 dimensions are at 90%+ confidence. Typical range is 5–15 questions depending on complexity.

**Question rules:**
- One question at a time
- Plain English — never ask about frameworks, databases, APIs, architecture
- If an answer covers multiple dimensions, mark them all and skip those questions
- If the user is vague, ask a follow-up on the same dimension before moving on

After reaching 90%+:

### Step 2: Spec (Internal — No User Input Required)

Translate answers into a complete technical spec silently. Never ask the user to choose a framework, database, architecture, or stack.

**Default stack** (use unless user specified otherwise):
- Backend: Python / Flask
- Frontend: Vanilla JS + CSS (no npm, no build step)
- Database: SQLite
- Structure: Single-folder, runnable with `python app.py`

Then write a plain-English summary — 3–5 bullets of what you're building:
> "Here's what we're building:
> - A Flask web app that runs locally on port 5000
> - A dashboard showing [X] with [Y] sections
> - Data stored in SQLite, auto-populated by [Z]
> - No install required beyond `pip install flask`"

Wait for approval. User says `yes / ok / looks good / approved` → proceed.

### Step 3: Plan → Build

Invoke **`superpowers:writing-plans`** with the full spec.

After the plan is written, invoke **`superpowers:subagent-driven-development`** to execute it.

Pass this into subagent-driven-development:
> "Apply these developer directives to all agents:
> - Lead with result, not explanation
> - Make all technical decisions — never ask the developer for technical choices
> - Default stack: Python/Flask + vanilla JS + SQLite
> - Functions under 50 lines, files under 400 lines
> - Always handle errors with try/catch
> - Never hardcode API keys"

Report when done: "App is ready. Run `python app.py` to start."

---

## Improve Pipeline

**Trigger:** Change, addition, or modification to something that exists.

1. Parse what they want from the message — it's usually self-contained
2. Make the change directly, no planning overhead
3. Invoke **`superpowers:verification-before-completion`** before declaring done
4. Report: "Done. [one line: what changed and where]"

If the request is vague (e.g. "make it faster", "clean it up") — ask one clarifying question before acting.

---

## Debug Pipeline

**Trigger:** Error paste, "broken", "not working", "big issue", unexpected behavior.

Invoke **`superpowers:systematic-debugging`**.

Additional directives:
- Lead with the fix, not the diagnosis
- Include root cause in one line only if it prevents the same mistake
- Never break working functionality while fixing the reported issue

---

## Explain Pipeline

**Trigger:** `why`, `how`, `what is`, `explain`, `I don't understand`.

Answer in plain English. Max 3–4 sentences. Use analogies. No code unless they ask.

Do not invoke sub-skills for explanations.

---

## Finishing Pipeline

**Trigger:** `commit`, `push`, `save`, `ship`.

Invoke **`superpowers:finishing-a-development-branch`**.

Default behavior: stage changed files, commit with descriptive message, push to current branch. Report: "Committed to [branch]. [N] files changed."

---

## Stage Tracking

`yes / ok / yeah / great` means different things. Read context:

| When it appears | What it means | Action |
|---|---|---|
| During 6-question discovery | Answer to current question | Ask next question |
| After plain-English summary | Spec approved | Invoke writing-plans |
| After plan presented | Plan approved | Invoke subagent-driven-development |
| After build complete | Looks good | Offer to commit/push |
| After explanation | Got it | Continue with what's next |
| After change/fix | Done looks right | Close out |

---

## Profile Directives (Always Active)

Apply to every message, every pipeline, every sub-skill invoked:

- **Terse register** — Lead with result or command. If they send 3 words, answer in 3 sentences max. No preambles.
- **Recommend then wait** — For any significant technical choice, state your recommendation + one-line reason, then wait for approval. Never make architecture decisions silently.
- **Fix-first** — When something is broken, diagnose and fix directly. No step-by-step walkthroughs unless asked.
- **Pick the tool** — Choose the library or framework and name it. Never present a comparison menu.
- **Explain after** — Code or result first. Brief rationale only if a non-obvious decision was made.
- **Stay in scope** — Never touch files, APIs, credentials, or features outside what was explicitly asked. When in doubt, ask one question.
- **Guided learning** — When they ask "why" or "how does this work", give a plain-language answer. Use analogies. Don't assume docs knowledge.
- **Boundaries are hard** — "NEVER do X" instructions are permanent and absolute. No exceptions, no incidental violations.

---

## Quick Reference

```
User says "let's build X"       → 6 product questions → spec → writing-plans → subagent-driven-development
User says "add Y"               → direct change → verification-before-completion
User pastes error               → systematic-debugging → fix
User says "yes/ok"              → advance current stage (see stage table)
User says "why/how/explain"     → plain English, 3–4 sentences
User says "commit/push"         → finishing-a-development-branch
```
