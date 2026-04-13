# claude-dotfiles

Claude Code configuration — settings, skills, agents, commands, and custom plugins. Clone this as `~/.claude` on any new machine to restore the full setup.

## What's in here

| Path | Contents |
|------|----------|
| `settings.json` | Model (opus[1m]), permissions allow/deny list, hooks, marketplace config |
| `keybindings.json` | Custom key bindings (16 contexts) |
| `commands/` | 7 slash commands: grill, ship, techdebt, commit-push-pr, quick-commit, review-changes, test-and-fix, worktree |
| `agents/` | 139 agent definitions (code, design, engineering, domain specialists) |
| `skills/` | 28 installed skills — see `skills-sources.json` for origins |
| `my-plugins/` | ThreadPLM custom design plugin (8 commands: ux, logo, style, tokens, voice, banner, course, deck) |
| `plugins/installed_plugins.json` | Active plugins snapshot |
| `plugins/known_marketplaces.json` | Registered marketplaces (claude-plugins-official, claude-code-plugins, openai-codex) |
| `skills-sources.json` | Where each skill came from (for updates / selective reinstall) |
| `projects/**/memory/` | Per-project memory files (context that persists across sessions) |

## New machine setup

### Prerequisites
1. Install [Claude Code](https://claude.ai/download)
2. Install [Git](https://git-scm.com/download/win)
3. Install Python 3.x (for `last30days` skill)

### One-command setup (from PowerShell)

Close Claude Code first, then run:

```powershell
irm https://raw.githubusercontent.com/digitalthreadai/claude-sync/main/setup.ps1 | iex
```

This script backs up any existing `~/.claude`, clones the repo, and installs skill dependencies automatically.

### From inside Claude Code terminal (if already open)

Tell Claude in a new session:
> "Run the setup script from my dotfiles repo: `irm https://raw.githubusercontent.com/digitalthreadai/claude-sync/main/setup.ps1 | iex` — but warn me to close Claude Code first"

### Post-install (manual steps)
1. Set `GITHUB_PERSONAL_ACCESS_TOKEN` as a **system-level** environment variable (for GitHub MCP)
2. Restart Claude Code
3. Run `/plugin install codex@openai-codex` in Claude Code, then `/reload-plugins`

## Updating from this machine

```powershell
cd "$env:USERPROFILE\.claude"
git add -A
git commit -m "Update dotfiles"
git push
```

## Pulling updates on another machine

```powershell
cd "$env:USERPROFILE\.claude"
git pull
```

## Skill notes

- **gstack** is a bundle that includes `browse`, `qa`, `ship`, `retro`, `review`, `plan-ceo-review`, `plan-eng-review`, `gstack-upgrade`, and `setup-browser-cookies` — no need to install those separately
- **last30days** requires Python + `pip install -r requirements.txt` after cloning
- **founder-guide** was created by the owner of this repo (not from a public source)
- See `skills-sources.json` for full source details and post-install steps
