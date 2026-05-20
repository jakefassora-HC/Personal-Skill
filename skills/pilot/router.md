# Task Router

Loaded when Jake describes something he wants to build.

---

## Step 1 — Read the description

Take in whatever Jake said. It may be vague or one sentence. That's fine.

## Step 2 — Silently classify

Check the description against these signals:

**QUICK** (5 min – 1 hr)
- Words like "just", "quick", "small", "simple"
- Single file or component mentioned
- Visual change: button, color, text, layout
- Fixing one thing, no new integrations

**STANDARD** (2–6 hrs)
- "Add X to Y", "new page", "new tab", "new feature"
- Multiple components or steps involved
- Touches an existing system
- One integration, one new workflow

**DEEP** (days – weeks)
- "Build a", "from scratch", "whole", "platform", "full app"
- Needs a database, auth, or multiple new integrations
- New app with both a UI and a backend
- Multiple moving parts that don't exist yet

## Step 3 — State the classification

Say exactly this (fill in the brackets):

> "This looks like a **[QUICK / STANDARD / DEEP]** task — about [time estimate]."

Then ask:

> "Does that sound right? You can say quick, standard, or deep to adjust."

Wait for Jake to confirm or correct. Do not proceed until he does.

## Step 4 — Load the right pipeline

Once Jake confirms, load **one** of the following:

- **QUICK** — Skip the planning phase. Execute directly using the Improve pipeline in `pipelines.md`. No spec needed.

- **STANDARD** — Load `build-pipeline.md`. Run the full discovery, spec, and parallel agent flow.

- **DEEP** — Load `build-pipeline.md`. After the spec is confirmed, note that the GSD plan-phase should be invoked to produce architecture documentation before any code is written.

Do not load a pipeline file before Jake confirms the classification.
