# Personal Skill Bundle

`pilot` is Jake's personal workflow router for build, debug, improve, explain, and ship requests.

The repo ships a small skill bundle:

- `skills/pilot` - the main user-facing router
- `skills/start` - a narrower support router for enriched handoffs
- `skills/prompt-improver` - the optional clarification helper used by the prompt hook

`pilot` still does the main routing work and loads only the file it needs for the current task:

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

This copies the bundled skill folders into:

- `~/.claude/skills/`
- `${CODEX_HOME:-~/.codex}/skills/`

`skills/*/agents/openai.yaml` files ship as Codex metadata inside each installed skill folder; they do not change the install destination.

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

Single-skill install:

```bash
./install.sh --source ./skills/pilot --both
```

Use the default bundle install if you want the `start` and `prompt-improver` support skills available alongside `pilot`.

## Make commands

```bash
make install
make install-claude
make install-codex
make test
```

## Codex multi-agent support

For the full build pipeline, enable multi-agent support in `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

Improve, Debug, Explain, and Finish flows do not require multi-agent support.

## Optional prompt hook

`scripts/improve-prompt.py` is a `UserPromptSubmit` hook for genuinely vague prompts. It should stay quiet for specific asks and only route into `prompt-improver` when clarification would materially change the build.
