---
name: Claude Code custom slash commands - UNRESOLVED on this Windows install
description: After 15+ debugging attempts across 5 root-cause theories, custom slash commands cannot be made to appear in the `/` picker on manba's Windows Claude Code install. Official plugin CLI install reports success but commands never render. Workaround documented below.
type: feedback
---

## Status: UNRESOLVED

After exhaustive debugging on 2026-04-06, I could not get any custom slash command to appear in the `/` picker on manba's Windows Claude Code install (version 2.1.87+). DO NOT spend time on this again unless the user explicitly asks. Use the workaround.

## Workaround (use this every time)

Instead of `/ux design the ECO screen`, just say it in natural language:

> *"Use the ui-ux-pro-max skill to design the ECO approval screen for ThreadPLM"*

The skills auto-activate from natural language. Same end result, slightly more typing. The 8 design-family skills installed at `~/.claude/skills/` all work this way:

| Skill name | Trigger phrase example |
|---|---|
| `ui-ux-pro-max` | "use ui-ux-pro-max for..." or "design the [screen] for..." |
| `ui-styling` | "use ui-styling to build a [component]" |
| `design` | "use the design skill for a logo / CIP / icon" |
| `design-system` | "use design-system for tokens" |
| `brand` | "use brand for messaging / voice" |
| `banner-design` | "use banner-design for a [platform] banner" |
| `slides` | "use slides for an HTML deck on..." |
| `codebase-to-course` | "use codebase-to-course on [path or URL]" |

## What was tried and failed (do not retry)

| Attempt | Result |
|---|---|
| Drop `.md` into `~/.claude/commands/` (LF endings, frontmatter) | Appears in skill registry (system reminders), invisible in `/` picker |
| Same files with CRLF line endings | No effect |
| Same files with ASCII-only frontmatter (no em-dashes/arrows) | No effect |
| Renamed to avoid collision with existing skill names (`ux` instead of `ui-ux-pro-max`) | No effect |
| Backdated mtime to match `quick-commit.md` (Mar 18) | No effect |
| Backdated BIRTH time too (via PowerShell `(Get-Item).CreationTime`) | No effect |
| Byte-for-byte identical copy of working `quick-commit.md` under new filename | Invisible (proves filename is the discriminator OR there's a per-file allowlist) |
| Drop into `plugins/marketplaces/claude-code-plugins/.claude/commands/` | Invisible — that dir is not even registered in the skill backend |
| Drop into an existing plugin's commands dir (`commit-commands/commands/plugin-ux-test.md`) | Invisible — even though `commit-push-pr.md` in same dir works |
| Build proper local marketplace at `~/.claude/my-plugins/` with valid `.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json` + `commands/*.md` | Validates clean |
| `claude plugin marketplace add C:\Users\manba\.claude\my-plugins` | "Successfully added marketplace" |
| `claude plugin install threadplm-design@my-plugins -s user` | "Successfully installed", `claude plugin list` shows `Status: ✔ enabled` |
| Plugin commands cached correctly to `~/.claude/plugins/cache/my-plugins/threadplm-design/1.0.0/commands/*.md` | Verified all 8 files present and well-formed |
| Reinstalled at `-s local` (project) scope | No effect |
| `git init` the local marketplace dir to give it a real git SHA | No effect |
| Hacked `cachedGrowthBookFeatures.tengu_amber_lattice.plugins` array in `~/.claude.json` to add `threadplm-design` (the cached server-side feature flag listing "auto-enabled" plugins like `commit-commands`) | No effect |

## Why the working commands work (mystery)

The 7 commands that DO work in the picker — `grill`, `quick-commit`, `worktree`, `techdebt`, `test-and-fix`, `commit-push-pr`, `review-changes` — only exist as `.md` files in `~/.claude/commands/` on this machine. They are NOT sourced from any plugin (verified via grep across all plugin dirs and `plugin.json` manifests). They are NOT registered in any JSON config file (verified via grep across `~/.claude/`, `~/.claude.json`, `AppData/Local/claude-cli-nodejs/`, `AppData/Roaming/Claude/`).

The user's recollection: "they were originally installed in my other laptop". The Dropbox-synced backup at `C:\Users\manba\Dropbox\claude\.claude\` does NOT contain a `commands/` folder OR a `plugins/` folder. So the working commands were created locally on this Windows laptop, by some mechanism I couldn't identify, between when Claude Code was first installed and when manba copied other state from Dropbox. Some kind of one-time first-run import that I cannot replicate via any documented or hacky means.

## Possible next steps if user wants to escalate

1. **File a Claude Code bug report** at `github.com/anthropics/claude-code/issues`. Reproducer: "On Windows, after `claude plugin install <local-plugin>@<local-marketplace>`, commands from the plugin's `commands/` dir do not appear in the `/` picker. `claude plugin list` reports the plugin as enabled. Cached files are present. No errors logged."
2. **Try the same install on the Dropbox-source laptop** — if it works there, this is a corrupted-state issue specific to manba's primary Windows machine, fixable by deleting `~/.claude/plugins/` and reinstalling all plugins from scratch.
3. **Run Claude Code with `--debug` flag** at startup and capture what it logs about command/plugin discovery. Might reveal the actual filter being applied.
4. **Wait for a Claude Code update** and retest periodically.

## Current state on disk (after revert, 2026-04-06)

- `~/.claude/my-plugins/` — local marketplace dir KEPT INTACT as a ready-to-go source for when this is fixable. Contains `.claude-plugin/marketplace.json` + `plugins/threadplm-design/{plugin.json, commands/{ux,style,logo,tokens,voice,banner,deck,course}.md}`. Git-initialized with one commit. NOT registered with `claude plugin marketplace`. To re-attempt later: `claude plugin marketplace add C:\Users\manba\.claude\my-plugins && claude plugin install threadplm-design@my-plugins -s user`.
- `~/.claude.json` — restored from `.bak` (tengu_amber_lattice hack reverted)
- `~/.claude/commands/` — only the original 7 working commands remain. My 8 broken `.md` files have been deleted.
- The 8 underlying SKILLS at `~/.claude/skills/{ui-ux-pro-max, ui-styling, design, design-system, brand, banner-design, slides, codebase-to-course}/` are still installed and functional. They auto-activate from natural language requests.
