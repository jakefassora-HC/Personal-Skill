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

### Step 0: Project Research (Before First Question)

Before asking anything, silently scan the current project directory:

- What files and folders already exist?
- Any existing Flask apps, databases, `.env` files, config files, or API credentials?
- Any existing code that should be built on top of — not duplicated?
- What port is already in use? What schema does an existing DB have?

Summarize what you found in one line before the first question:
> "I can see you have an existing Flask app on port 5000 and a `leads.db` SQLite database. I'll build on top of those."

If the directory is empty, say nothing and go straight to questions.

---

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
- Use what was found in Step 0 to skip questions already answered by existing code

---

### Step 2: Full Spec + Rich Summary

Translate all answers into a complete technical spec internally. Never ask the user to choose a framework, database, architecture, or stack.

**Default stack** (use unless user specified otherwise):
- Backend: Python / Flask
- Frontend: Vanilla JS + CSS (no npm, no build step)
- Database: SQLite
- Structure: Single-folder, runnable with `python app.py`

Then present the full plain-English summary. This is not a short list — cover everything so the user can catch anything wrong before a single line of code is written:

```
Here's what we're building:

WHAT IT DOES
[Full description of the app's purpose and how it works, 2-4 sentences]

WHO USES IT + HOW
[Walk through a complete typical session from open to close]

EVERY FEATURE
Must-haves:
  - [feature 1]
  - [feature 2]
  - [feature 3]
Nice-to-haves (built only if time allows):
  - [feature A]
  - [feature B]

WHAT GETS CREATED
  app.py              ← Flask server, all routes
  templates/
    index.html        ← main dashboard
    [other pages]     ← [purpose]
  static/
    main.js           ← frontend logic
    style.css         ← all styles
  db/
    [name].db         ← SQLite database, [what it stores]
  .env.example        ← API keys template (never hardcoded)

HOW TO RUN
  pip install flask [other deps]
  python app.py
  Open http://localhost:[port]

DATA + CONNECTIONS
  - Stores: [what gets saved, fields, structure]
  - Reads from: [any existing files or databases being reused]
  - Connects to: [any APIs, services, external sources]

WHAT "DONE" LOOKS LIKE
[Restate their success criteria in their words]
```

Wait for approval. User says `yes / ok / looks good / approved` → proceed.
If they correct anything, update the spec and re-show only the changed sections.

---

### Step 3: Scope Check

Estimate the number of independent implementation tasks from the spec.

**If 7 or fewer tasks:** proceed directly.

**If 8 or more tasks:** flag it before building:
> "This is a larger build — I'm estimating [N] tasks. One-shot will work but will take a while and use a lot of context.
> Two options:
> - **One-shot:** Build everything now, start to finish
> - **Core first:** Build the [2-3 most critical features] now, add the rest in the next session
> Which do you want?"

Wait for answer. Proceed accordingly.

---

### Step 4: Interface Contract

Before spawning any agents, generate a shared contract document that every agent will receive. This prevents agents building pieces that don't connect.

```
INTERFACE CONTRACT

API ENDPOINTS
  [METHOD] /[path]     → returns { [field]: [type], ... }
  [METHOD] /[path]     → returns { [field]: [type], ... }

DATABASE SCHEMA
  table [name] (
    [column]  [type],
    ...
  )

FILE STRUCTURE
  [file]    ← owned by: [agent/task]
  [file]    ← owned by: [agent/task]

SHARED CONSTANTS
  PORT = [number]
  DB_PATH = "[path]"
  [other shared values]
```

Show the user a brief version — just the API endpoints and file list:
> "Here's how the pieces connect: [endpoints] [files]"

This is informational, not a new approval gate. If they say something looks wrong, fix it. Otherwise proceed immediately.

---

### Step 5: Plan → Build

Invoke **`superpowers:writing-plans`** with the full spec AND the interface contract.

After the plan is written, invoke **`superpowers:subagent-driven-development`** to execute it.

Pass this into every agent via subagent-driven-development:
> "Apply these directives to all agents:
> - Lead with result, not explanation
> - Make all technical decisions — never ask the developer for technical choices
> - Default stack: Python/Flask + vanilla JS + SQLite, no npm, no build step
> - Functions under 50 lines, files under 400 lines
> - Always handle errors with try/catch or try/except
> - Never hardcode API keys — use .env
> - Backend tests: pytest. Frontend: no test framework — verify by checking it loads correctly
> - Follow the interface contract exactly — don't invent new endpoints or rename existing ones
> [paste full interface contract here]"

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
| During discovery questions | Answer to current question | Assess confidence, ask next |
| After full summary | Spec approved | Run scope check, show interface contract, invoke writing-plans |
| After scope options presented | Choice made | Proceed with selected scope |
| After interface contract shown | Acknowledged | Invoke subagent-driven-development |
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
User says "let's build X"
  → Step 0: scan project (existing files, DBs, APIs)
  → Step 1: questions until 90% confidence (5-15 questions)
  → Step 2: full plain-English summary (everything — features, files, how to run)
  → Step 3: scope check (flag if 8+ tasks, offer core-first option)
  → Step 4: interface contract (endpoints, schema, file ownership)
  → Step 5: writing-plans → subagent-driven-development (14+ agents)
  → "App is ready. Run python app.py"

User says "add Y"               → direct change → verification-before-completion
User pastes error               → systematic-debugging → fix
User says "yes/ok"              → advance current stage (see stage table)
User says "why/how/explain"     → plain English, 3–4 sentences
User says "commit/push"         → finishing-a-development-branch
```
