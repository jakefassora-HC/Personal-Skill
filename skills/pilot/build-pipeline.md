# Build Pipeline

Full flow for STANDARD and DEEP builds after the router has classified intent. Execute steps in order.

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

After showing the summary, ask:
> "Anything you want to push back on or change before I write the full plan?"

If Jake has feedback → revise the summary and ask again.
If "looks good" / "no" / approval → proceed to Step 4.

---

## Step 4 — Interface Contract (for builds with 2+ agents)

Before invoking writing-plans, define the interface contract. This prevents agents building non-integrating pieces.

Write a short contract block covering:
- **API endpoints**: every route, method, and what it returns
- **Shared schema**: any data objects passed between frontend and backend
- **File ownership**: which file each agent owns (no overlaps)

Include this contract in the plan as a shared reference for all agents.

Then write a clean HTML plan file:

1. Create `.planning/` in the project root if it doesn't exist
2. Write `.planning/plan.html` with:
   - Goal and feature list
   - Task breakdown with PARALLEL / SEQUENTIAL labels
   - Agent assignments
   - Time estimate
   - Style: system font, max-width 860px, clean and readable
3. Tell Jake:
   > "Plan saved. Run: `open .planning/plan.html`"
4. Wait for Jake to review and approve before executing anything.

---

## Step 5 — Execute

### DEEP tasks (multi-week projects)

After plan is approved, say:
> "This is a multi-week project. I'll use GSD to document and track progress. Run `/gsd-plan-phase` to begin."

Then stop. Do not execute. Let GSD take over.

---

### STANDARD tasks

After plan is approved, dispatch agents based on what the plan requires:

- **UI work only** → UI agent handles all frontend
- **Backend work only** → backend agent handles all API/logic
- **Both** → run UI and backend agents in parallel; use the interface contract to prevent conflicts

**Always include:**
- A reviewer agent that checks output against the spec after each task completes
- Atomic commits per task

**Agent team per task:**
1. Implementer (TDD: test → fail → code → pass)
2. Spec reviewer (does code match spec? nothing missing, nothing extra?)
3. Code quality reviewer (clean, no regressions, no hacks?)

Final reviewer checks the entire implementation end-to-end after all tasks complete.

When done: tell Jake the exact command to run the app.
