# Build Pipeline

Full flow for STANDARD and DEEP builds after the router has classified intent. Execute steps in order.

---

## Step 0 — Research (Silent)

Before asking anything, read the project directory to understand what already exists:
- Check for existing files, config, dependencies
- Note the stack, any partial work, constraints in CLAUDE.md
- Silently inform all later steps — do NOT report findings to user unless directly relevant
- Never mention files, previews, URLs, or run commands until they have actually been created or verified

---

## Step 1 — Discovery (Product Questions Only)

Ask at most 3 product questions, one at a time. No tech jargon.
Skip any dimension already answered in the prompt or prior turns. If the prompt already makes the key dimensions clear, skip discovery entirely.

| Dimension | What You Need |
|---|---|
| Core purpose | What it does in one sentence |
| Users | Who uses it and their goal |
| Key flows | What they open, click, see |
| Must-haves | What is essential vs. optional |
| Constraints / done | Anything fixed plus what success looks like |

**Rules:**
- One question per message
- Plain English — no framework names, no architecture choices
- Multiple choice preferred when options are clear
- Never ask about stack, database, hosting — you decide those silently
- Stop as soon as you can write a compact brief with reasonable assumptions

---

## Step 2 — Scope Check

Before writing the spec, count estimated tasks.

**If 8+ tasks:** Stop. Say:
> "This is larger than one clean pass. I recommend starting with the core slice first; if you want the full map now, I can do that."

If Jake wants the core first, ask for the one most important slice and scope down.
If Jake wants the full map, continue as-is.

**If under 8 tasks:** Proceed directly to Step 3.

---

## Step 3 — Compact Build Brief

Generate a full spec internally (you pick the stack: Python/Flask + vanilla JS/CSS + SQLite, no npm, no build step). Then show a compact plain-English brief — no tech jargon, no code. Structured exactly like this:

---

GOAL: one sentence
WHO + FLOW: one short paragraph
MUST-HAVES:
- ...
OUT OF SCOPE:
- ...
DONE:
- ...

---

After showing the summary, ask:
> "Anything off before I write the plan?"

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
