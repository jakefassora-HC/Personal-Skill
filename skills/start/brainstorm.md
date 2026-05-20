# Brainstorm

## Prompt Quality Check (runs first)

Before asking any questions, check if the prompt-improver skill already ran and collected answers. If it did, use those answers to skip or reduce questions here — don't ask the same thing twice.

If the prompt arrived already enriched (user answered clarifying questions from the hook), jump directly to generating the plain-English summary.

Turn Jake's vague description into a clear, agreed-upon spec through back-and-forth conversation.

## Rules

- One question at a time — never ask multiple questions at once
- Prefer multiple choice answers over open-ended questions
- Never ask about tech stack, database, hosting, or architecture
- Never ask anything that requires technical knowledge to answer
- Keep it conversational — adjust based on Jake's pushback

---

## Six Dimensions to Uncover

Ask questions until all six are clear. Stop asking once you have them.

1. **Core goal** — what it does in one sentence
2. **Who uses it** — and what they're trying to accomplish
3. **Key actions** — what they open, click, see
4. **Must-haves** — what's essential vs. nice-to-have
5. **Success** — what "done" looks like in plain terms
6. **Constraints** — anything that can't change (deadline, existing system, required tools)

---

## After You Have Enough Context

Generate a plain-English summary with no jargon:

```
WHAT IT DOES: [one sentence]
WHO USES IT: [who and why]
EVERY FEATURE: [bulleted list of everything it does]
WHAT DONE LOOKS LIKE: [plain description of the finished thing]
```

Then ask:

> "Anything you want to change or push back on before I write the plan?"

Loop on feedback until Jake says yes, ok, or looks good.

Once confirmed, load plan.md.
