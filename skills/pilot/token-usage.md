# Token Usage

Load this file only when the task is long, context-heavy, repetitive, or likely to exceed budget.

## Defluff Mode

Use the uploaded Defluffer pattern: preserve meaning, remove prompt ceremony, and keep exact technical details intact. The source script protects code spans/blocks before compression, then applies phrase/logic replacements, synonym aliases, blacklist removal, cleanup, and restoration of protected items.

Apply by default:

- Do not restate the full user request unless ambiguity requires it.
- Do not paste large file contents into chat; summarize and cite file paths, symbols, or line ranges.
- Do not load every pipeline file. Load exactly one route file unless the active stage explicitly needs another.
- Prefer pointers over copies: file path, function name, section heading, command.
- Prefer compact state over transcript recap.
- Collapse repeated constraints into one named rule, then reference that rule.
- Keep progress updates to one sentence.
- Explain only the non-obvious decision.

## Compression Order

For long prompts or internal state, compress in this order:

1. Protect code blocks, inline code, commands, file paths, error messages, table names, schema names, URLs, and quoted strings.
2. Collapse common phrases:
   - `could you please`, `i would like you to`, `i need you to` -> remove
   - `the goal is to` -> `goal:`
   - `the task is to` -> `task:`
   - `the output should be` -> `output:`
   - `what is the difference between` -> `diff:`
   - `take into consideration` -> `consider`
   - `due to the fact that` -> `because`
   - `in order to` -> `to`
   - `without using` -> `no`
3. Collapse technical terms only when unambiguous:
   - repository -> repo
   - database -> db
   - configuration -> config
   - environment -> env
   - request -> req
   - response -> resp
   - authentication -> auth
   - authorization -> authz
   - dependency -> dep
   - migration -> mig
   - implementation -> impl
   - asynchronous -> async
   - synchronous -> sync
   - pull request -> pr
4. Remove filler and politeness when it does not change meaning.
5. Restore protected items exactly.
6. Do a final ambiguity check before using the compressed form.

## Output Upgrade

Use compression to improve output quality, not just shorten text:

- Convert vague asks into labeled fields: `goal`, `inputs`, `constraints`, `output`, `done`.
- Preserve acceptance criteria verbatim.
- Replace long recaps with a state block.
- Use clear abbreviations only after the first obvious mention or when standard in engineering contexts.
- Never compress user-facing explanations so far that they become cryptic.

## Compact State Template

When context gets long, keep this internally:

```text
state:
  intent: build|improve|debug|explain|finish
  stage: discovery|spec|plan|execute|verify|ship
  loaded: router.md|build-pipeline.md|pipelines.md|token-usage.md
  decisions: [short list]
  constraints: [must keep]
  next: one action
```

Update the state instead of repeating prior reasoning.

## Caveman Comparison

Caveman-style compression is useful for ultra-short private notes, but it becomes too cryptic for reusable skill instructions.

Prefer:

```text
intent: debug
file: app.py
symptom: 500 on /upload
root: missing tmp dir
next: create dir + add test
```

Avoid:

```text
dbg app.py 500 upload tmpdir fix test
```

The first version costs a few more tokens but is safer for future agents to resume.

## File Loading Rules

1. `SKILL.md` is the trigger and routing layer.
2. `router.md` is loaded only for new-build classification.
3. `build-pipeline.md` is loaded only after a Standard or Deep build path is confirmed.
4. `pipelines.md` is loaded only for Improve, Debug, Explain, Finish, or stage tracking.
5. `token-usage.md` is loaded only for long or context-heavy tasks.
6. `scripts/defluff.js` is optional. Use it only when a prompt or block of instructions needs deterministic compression.

## Compression Guardrails

Never compress away:

- User constraints
- File names
- Commands
- Error messages
- Security boundaries
- Acceptance criteria
- External API, table, or schema names
- The current active stage
- Values inside code or quotes

If compression risks ambiguity, keep the longer form.
