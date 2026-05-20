Called after brainstorm.md when Jake has approved the summary.

## What you do

Write a complete internal spec based on the approved summary. Pick the tech stack silently — Python/Flask + vanilla JS + SQLite by default for apps, or whatever fits the project type. Do not ask Jake about the stack.

## Steps

1. Write the full spec internally. Decide: tech stack, file structure, API shape, data model, task list.

2. Label every task as either:
   - PARALLEL — independent, can run at the same time
   - SEQUENTIAL — depends on something else finishing first

3. Generate an HTML plan file at `.planning/plan.html`. Use this layout:
   - System font, max-width 860px, white cards with light shadow, 16px base text
   - Sections in order: Goal, Features, Task Breakdown, Agent Assignments, Time Estimate
   - Each task gets a colored badge: green = PARALLEL, yellow = SEQUENTIAL, purple = agent role
   - Keep it clean and readable — Jake will open this in a browser

4. Tell Jake: "Plan saved. Open it: `open .planning/plan.html`"

5. Wait. Do not proceed until Jake comes back.

6. If Jake requests changes → update the spec and regenerate the HTML, then wait again.

7. If Jake approves → load execute.md and follow it.

## Deep tasks

If the plan spans multiple weeks or has 10+ tasks, tell Jake:

"This is a multi-week project. The right tool for tracking this is GSD. Run `/gsd-plan-phase` to start — it will document and track the full project. Your plan is saved at `.planning/plan.html` as a reference."

Then stop. Do not execute. GSD takes over.
