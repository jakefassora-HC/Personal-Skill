Called directly from SKILL.md when Jake says something is broken.

## What you do

Investigate, find the root cause, fix it, verify it. Jake does not need to explain the bug technically.

## Steps

1. If you have zero context on what broke, ask one question max: "Where does it break — what do you see vs what you expect?" Do not ask anything else.

2. Read the relevant files. Check error output, logs, and stack traces directly — do not ask Jake to paste them unless there is no other way to access them.

3. Identify the root cause. Do not list hypotheses. Find the actual cause.

4. Apply the fix.

5. Check that the fix does not break anything adjacent. Read any files that call the code you changed.

6. Report: "Fixed. [one-line root cause]. [file:line]"

## Rules

- Never ask Jake to explain an error technically.
- Never ask Jake to run commands to get logs if Claude can read those files directly.
- Never present multiple possible causes — diagnose and commit to one.
- If the fix requires a choice between two approaches, make the simpler one and note why in the report.
