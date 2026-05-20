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

If confidence is high, say:

> "This looks like a **[QUICK / STANDARD / DEEP]** task — about [time estimate]. I'll treat it that way unless you want quick, standard, or deep instead."

Then continue immediately.

Only ask Jake to confirm or correct the classification when the boundary is genuinely ambiguous.

## Step 4 — Load the right pipeline

Load **one** of the following based on the confirmed or high-confidence classification:

- **QUICK** — Skip the planning phase. Execute directly using the Improve pipeline in `pipelines.md`. No spec needed.

- **STANDARD** — Load `build-pipeline.md`. Run the full discovery, spec, and parallel agent flow.

- **DEEP** — Load `build-pipeline.md`. After the spec is confirmed, note that the GSD plan-phase should be invoked to produce architecture documentation before any code is written.

Do not load a pipeline file before Jake confirms the classification.
