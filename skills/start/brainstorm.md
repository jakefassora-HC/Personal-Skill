# Brainstorm

## Prompt Quality Check (runs first)

Before asking any questions, check if the prompt-improver skill already ran and collected answers. If it did, use those answers to skip or reduce questions here — don't ask the same thing twice.

If the prompt arrived already enriched (user answered clarifying questions from the hook), jump directly to generating the compact summary unless one key gap remains.

Turn Jake's vague description into a clear, agreed-upon spec through back-and-forth conversation.

## Rules

- One question at a time — never ask multiple questions at once
- Prefer multiple choice answers over open-ended questions
- Never ask about tech stack, database, hosting, or architecture
- Never ask anything that requires technical knowledge to answer
- Keep it conversational — adjust based on Jake's pushback
- Ask at most 3 questions total, and stop earlier if the brief is already clear

---

## Five Dimensions to Uncover

Ask questions until the brief is clear. Stop once you can summarize the request confidently.

1. **Core goal** — what it does in one sentence
2. **Who uses it** — and what they're trying to accomplish
3. **Key actions** — what they open, click, see
4. **Must-haves** — what's essential vs. nice-to-have
5. **Constraints / success** — fixed requirements plus what "done" looks like

---

## After You Have Enough Context

Generate a compact plain-English brief with no jargon:

```
GOAL: [one sentence]
WHO + FLOW: [who uses it and their typical flow]
MUST-HAVES:
- ...
OUT OF SCOPE:
- ...
DONE:
- ...
```

Then ask:

> "Anything off before I write the plan?"

Loop on feedback until Jake says yes, ok, or looks good.

Once confirmed, load plan.md.
