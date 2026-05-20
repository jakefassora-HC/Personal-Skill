# Personal Skill — pilot

`pilot` is Jake's personal workflow router for build, debug, improve, explain, and ship requests.

It works as a single skill folder under `skills/pilot` and loads only the pipeline file needed for the current task:

- `SKILL.md` — trigger rules, profile directives, and routing table
- `router.md` — Quick / Standard / Deep build classification
- `build-pipeline.md` — Standard and Deep build workflow
- `pipelines.md` — Improve, Debug, Explain, Finish, and stage tracking

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

Install for Claude Code only:

```bash
./install.sh --claude
```

Install for Codex only:

```bash
./install.sh --codex
```

Install both:

```bash
./install.sh --both
```

Use a custom skill source folder:

```bash
./install.sh --source ./skills/pilot --both
```

## Make commands

```bash
make install          # same as ./install.sh --both
make install-claude   # Claude Code only
make install-codex    # Codex only
```

## Manual install

Claude Code:

```bash
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/pilot
cp -R skills/pilot ~/.claude/skills/pilot
```

Codex:

```bash
mkdir -p ~/.agents/skills
ln -sfn ~/.claude/skills/pilot ~/.agents/skills/pilot
```

If symlinks are not available, copy instead:

```bash
rm -rf ~/.agents/skills/pilot
cp -R skills/pilot ~/.agents/skills/pilot
```

## Codex multi-agent support

For the full build pipeline, enable multi-agent support in `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

Improve, Debug, Explain, and Finish flows do not require multi-agent support.
