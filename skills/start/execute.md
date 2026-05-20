Called after plan.md is approved for STANDARD tasks.

## What you do

Build everything in the plan. Determine how to execute based on what the plan contains.

## Execution modes

**Single file or component** — execute inline. No agents needed. Just build it.

**2+ independent pieces** — dispatch parallel agents simultaneously.

## Parallel execution rules

Read the interface contract from the plan before dispatching. Agents must agree on shared types, endpoints, and data shapes before they start writing code.

Dispatch these specialist agents:
- **UI agent** — owns all frontend files
- **Backend agent** — owns all API and logic files
- If only one type exists (pure frontend or pure backend), use a single specialist agent

Always include a **reviewer agent** that reads all output and checks it matches the spec. The reviewer does not write code — it only verifies.

Each agent commits atomically after its piece is complete.

## Final check

After all agents finish, verify end-to-end:
- Does the app start without errors?
- Do the pieces connect correctly?
- Does it match what Jake approved in the plan?

## Report when done

"Done. [one sentence describing what was built]. Run: [exact command to start or test it]"

No extra explanation unless something went wrong.
