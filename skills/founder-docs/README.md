# founder-docs

A Claude Code skill that generates a complete documentation suite for any web project — in one shot.

## What it produces

| File | Purpose |
|------|---------|
| `strategy.md` | Vision, features, tech stack, database schema, roadmap, file structure |
| `setup.md` | Step-by-step setup guide — env vars, services, SQL, deployment checklist |
| `README.md` | Project overview — stack, features, quick start, scripts |
| `docs/index.html` | Documentation hub — links to all HTML pages |
| `docs/README.html` | Project overview landing page with terminal mockup |
| `docs/strategy.html` | Strategy dashboard with sidebar nav, feature accordion, timeline |
| `docs/setup.html` | Interactive setup guide with copy buttons and localStorage checklist |

All HTML pages are self-contained (no build step), dark-themed, mobile-responsive, and use your project's brand colors if detectable.

## Install

Copy the `founder-docs/` folder into your `~/.claude/skills/` directory:

```bash
# From the claude-sync repo
cp -r skills/founder-docs ~/.claude/skills/
```

Or clone just this skill:

```bash
git clone https://github.com/digitalthreadai/claude-sync.git /tmp/claude-sync
cp -r /tmp/claude-sync/skills/founder-docs ~/.claude/skills/
```

## Usage

Invoke explicitly from any project directory:

```
use founder-docs
```

or

```
run founder-docs for this project
```

Claude will explore the codebase first, then generate all 7 files.

## Requirements

- Claude Code (claude.ai/code)
- Works with any web project: Next.js, React, Express, FastAPI, etc.

## License

MIT
