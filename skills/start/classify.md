# Task Classifier

Run this silently before responding. Classify the task, then show Jake one confirmation line.

## Classification Rules

### QUICK (minutes to an hour)
- Button, color, text, or layout tweak: 5–30 min
- Single UI component or page: 30–60 min

**Signals:** "just", "quick", "small", "simple", one thing mentioned, visual change, single file or node

### STANDARD (hours)
- New feature on an existing system: 2–4 hrs
- New n8n workflow or automation: 2–6 hrs

**Signals:** "add X to Y", "new page/tab/feature", "integrate", existing system, multiple components

### DEEP (days to weeks)
- New app with UI + backend: 3–7 days
- Full project (DB, auth, Slack, multiple integrations): weeks or months

**Signals:** "build a", "whole app", "from scratch", "with auth/database", "platform", months of work

---

## Output

After classifying silently, show Jake exactly one line:

> "This looks like a [QUICK/STANDARD/DEEP] task — about [time]. [one-line reason]. I'll treat it that way unless you want quick, standard, or deep instead."

Only wait for confirmation when the boundary is genuinely ambiguous.

---

## After Confirmation

| Classification | Next step |
|---|---|
| QUICK | Skip brainstorm.md — go directly to execute.md |
| STANDARD | Load brainstorm.md → plan.md → execute.md |
| DEEP | Load brainstorm.md → plan.md → tell Jake to use GSD for full execution |

**Token rule:** Only load the next file after Jake confirms. Never preload.
