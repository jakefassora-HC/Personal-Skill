# Personal Skill - pilot

`pilot` is Jake's personal workflow router for build, debug, improve, explain, and ship requests.

It works as a single skill folder under `skills/pilot` and loads only the file needed for the current task:

- `SKILL.md` - compact trigger rules, profile directives, and routing table
- `router.md` - Quick / Standard / Deep build classification
- `build-pipeline.md` - Standard and Deep build workflow
- `pipelines.md` - Improve, Debug, Explain, Finish, and stage tracking
- `token-usage.md` - Defluff-style compression rules for long or context-heavy work

## Token usage model

`SKILL.md` stays small on purpose. It points to deeper files instead of carrying every rule inline.

The skill uses Defluff mode by default:

- avoid restating the full request
- load only one route file at a time
- summarize large context instead of copying it
- keep progress updates short
- preserve exact commands, file names, errors, and constraints

Caveman-style shorthand is reserved for private state only. User-facing responses should stay clear enough to resume later.

## One-command install

From the repo root:

```bash
./install.sh
```

That installs `skills/pilot` into:

- `~/.claude/skills/pilot`
- `~/.agents/skills/pilot` as a symlink to the Claude Code copy, when possible

Restart Claude Code or Codex after installing.

## Install options

Claude Code only:

```bash
./install.sh --claude
```

Codex only:

```bash
./install.sh --codex
```

Both:

```bash
./install.sh --both
```

Custom source folder:

```bash
./install.sh --source ./skills/pilot --both
```

## Make commands

```bash
make install
make install-claude
make install-codex
```

## Codex multi-agent support

For the full build pipeline, enable multi-agent support in `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

Improve, Debug, Explain, and Finish flows do not require multi-agent support.
