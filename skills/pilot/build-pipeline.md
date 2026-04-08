# Build Pipeline

Full flow for "let's build X" intent. Execute steps in order.

---

## Step 0 — Research (Silent)

Before asking anything, read the project directory to understand what already exists:
- Check for existing files, config, dependencies
- Note the stack, any partial work, constraints in CLAUDE.md
- Silently inform all later steps — do NOT report findings to user unless directly relevant

---

## Step 1 — Discovery (Product Questions Only)

Ask questions one at a time. No tech jargon. Score 8 dimensions after each answer.
Stop when all 8 are at 90%+. Typical: 5–15 questions.

| Dimension | What You Need |
|---|---|
| Core purpose | What it does in one sentence |
| Users | Who uses it and their goal |
| Key flows | What they open, click, see |
| Primary function | Most important thing it does |
| Feature scope | Must-haves vs nice-to-haves |
| Success | What "done" looks like |
| Data / APIs | What data it needs, any connections |
| Visual | Any UI requirements or examples |

**Rules:**
- One question per message
- Plain English — no framework names, no architecture choices
- Multiple choice preferred when options are clear
- Never ask about stack, database, hosting — you decide those silently

---

## Step 2 — Scope Check

Before writing the spec, count estimated tasks.

**If 8+ tasks:** Stop. Say:
> "This is a big build — roughly [N] pieces of work. I can build the full thing, or we can start with the core and add from there. Which do you want?"

Wait for answer. If "core first": ask what the one most important piece is, scope down, continue.
If "full build": continue as-is.

**If under 8 tasks:** Proceed directly to Step 3.

---

## Step 3 — Rich Plain-English Summary

Generate a full spec internally (you pick the stack: Python/Flask + vanilla JS/CSS + SQLite, no npm, no build step). Then show a plain-English summary — no tech jargon, no code. Structured exactly like this:

---

**WHAT IT DOES**
One paragraph. What the app does as if explaining to a non-technical person.

**WHO USES IT + HOW**
Who opens the app and what their typical session looks like from start to finish.

**EVERY FEATURE**
Bulleted list. Every feature, no summaries. If it does something, it's on this list.

**WHAT GETS CREATED**
List every file that will be created and what it does in one line each.

**HOW TO RUN IT**
Exact command to start the app. What URL to open.

**DATA + CONNECTIONS**
What data gets stored. Any APIs or external services connected.

**WHAT "DONE" LOOKS LIKE**
Specific outcomes. "User can do X", "App shows Y", "Data persists across Z".

---

Wait for "yes", "ok", "looks good", or approval. If no, re-ask one question and revise.

---

## Step 4 — Interface Contract (for builds with 2+ agents)

Before invoking writing-plans, define the interface contract. This prevents agents building non-integrating pieces.

Write a short contract block covering:
- **API endpoints**: every route, method, and what it returns
- **Shared schema**: any data objects passed between frontend and backend
- **File ownership**: which file each agent owns (no overlaps)

Include this contract in the plan as a shared reference for all agents.

---

## Step 5 — Plan + Build

Invoke `superpowers:writing-plans` — pass the spec and interface contract.

After plan is written, invoke `superpowers:subagent-driven-development` to execute.

Agent team per task:
1. Implementer (TDD: test → fail → code → pass)
2. Spec reviewer (does code match spec? nothing missing, nothing extra?)
3. Code quality reviewer (clean, no regressions, no hacks?)

Final reviewer checks entire implementation end-to-end after all tasks complete.

When done: tell user the exact command to run the app.
