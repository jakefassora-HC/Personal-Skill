---
name: prompt-improver
description: Research-first clarification engine. Fires when a vague prompt is detected by the UserPromptSubmit hook. Researches codebase context before asking any questions, then generates targeted AskUserQuestion calls grounded in actual findings. Use when a prompt lacks enough specificity to execute well and the hook has flagged it for clarification.
---

# prompt-improver

Transforms vague prompts into executable requests — by researching first, then asking only what matters.

---

## Phase 1 — RESEARCH (never skip)

Before forming any question, gather context:

1. **Check conversation history** — scan for prior decisions, stated constraints, mentioned files, or established patterns.
2. **Explore the codebase** — use Task/Explore agents to run Glob and Grep. Look for:
   - Files related to the domain mentioned in the prompt
   - Existing patterns (naming, structure, conventions)
   - Entry points, config files, relevant modules
3. **Document findings** — internally note what you found before proceeding. Questions must be grounded in these findings.

Route all file exploration through Task or Explore agents. Never call Glob, Grep, WebSearch, or WebFetch directly.

---

## Phase 2 — QUESTION GENERATION

Generate 1–6 targeted questions based on research findings.

**Rules:**
- Each question addresses exactly ONE decision point
- Options must reference actual files, patterns, or values found in research — not generic assumptions
- Never ask about things already answered by conversation history or codebase context
- If research resolves a decision point, skip that question entirely

**Question count by complexity:**

| Prompt type | Questions |
|---|---|
| Simple / narrow scope | 1–2 |
| Moderate / multiple unknowns | 3–4 |
| Complex / cross-cutting | 5–6 (max) |

**AskUserQuestion format:**

```
tool: AskUserQuestion
question: [specific question ending with ?]
header: [max 12 chars]
multiSelect: false
options:
  - label: [1–5 words]
    description: [trade-off or implication, one sentence]
  - label: [1–5 words]
    description: [trade-off or implication, one sentence]
```

Each option label is 1–5 words. Each description states a concrete trade-off, not a restatement of the label. Provide 2–4 options per question.

---

## Phase 3 — CLARIFICATION

Present questions one at a time using AskUserQuestion. Wait for each answer before presenting the next (unless the tool supports batching).

Do not explain why you are asking. Do not summarize what you are doing. Just ask.

---

## Phase 4 — EXECUTE

Once answers are collected:

1. Merge answers with original prompt to form an enriched request
2. Hand off to the `start` skill for routing
3. Do not re-ask anything already answered

---

## Bypass conditions

Skip this skill entirely and execute immediately if:
- The prompt is specific and actionable
- You have sufficient context from conversation history
- Intent can be clearly inferred without ambiguity

When in doubt, lean toward executing — only invoke this skill when clarification would materially change what gets built.

---

## Rules

- Research before every question. No exceptions.
- Questions must cite findings, not assumptions.
- Never ask more than 6 questions total.
- Never ask generic questions like "what framework?" — find the framework first.
- If the prompt is clear, skip this skill entirely.
