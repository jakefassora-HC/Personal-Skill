Called when Jake says commit, push, save, or ship.

## What you do

Get the work committed and pushed to the current branch.

## Steps

1. Run `git status` to see what is uncommitted.

2. Stage specific files by name. Never use `git add -A` or `git add .`.

3. Write a descriptive commit message: what changed and why, not just what. Keep it under 72 characters for the subject line. Add a body if the change needs more context.

4. Push to the current branch.

5. Report: "Committed to [branch]. [N] files changed."

## Rules

- Never push to main or master directly.
- Never use --no-verify.
- If there is nothing to commit, tell Jake: "Nothing to commit — working tree is clean."
- If the push is rejected (branch behind remote), tell Jake what happened and ask before force-pushing or rebasing.
