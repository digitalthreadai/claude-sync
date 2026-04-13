---
name: Windows MCP server registration — use absolute node paths, not npx
description: Hard-won lesson about registering stdio MCP servers in Claude Code on Windows. The README-style `npx -y <package>` form is unreliable; absolute node + JS path is the only consistent fix.
type: feedback
---

## Rule

When registering a **stdio** MCP server in Claude Code on Windows (`~/.claude.json` `mcpServers`), do NOT use `command: "npx", args: ["-y", "<pkg>"]`. Install the package globally and register it as:

```json
{
  "type": "stdio",
  "command": "C:\\Program Files\\nodejs\\node.exe",
  "args": ["C:\\Users\\manba\\AppData\\Roaming\\npm\\node_modules\\<pkg>\\dist\\index.js"],
  "env": {}
}
```

For HTTP-transport MCP servers, just use `claude mcp add --transport http -s user <name> <url>` — no Windows quirks apply, the path issue is stdio-only.

## Why

- The npx form spawns through Windows shell-resolution and inherits PATH from Claude Code's parent process. PATH inheritance is flaky — `claude mcp list` will alternately show ✓ Connected and ✗ Failed to connect across runs of the same config, because the warm/cold state of npx + npm cache is non-deterministic.
- The `cmd /c <thing>.cmd` workaround also fails because Git Bash MSYS path-mangling can corrupt the `/c` flag into `C:/`, and even when written correctly via Node, cmd shim resolution adds another layer of fragility.
- Calling `node.exe` directly with the absolute path to the package's `dist/index.js` skips PATH, npx, and shell resolution entirely. It's the most direct spawn possible. Verified ✓ Connected on first try and stays connected.

## How to apply

1. `npm i -g <package>` to ensure it lives at `%APPDATA%\npm\node_modules\<package>\`.
2. Find the entry point (usually `dist/index.js`; check `bin` field in the package's `package.json` if unsure).
3. Edit `~/.claude.json` `mcpServers.<name>` directly (or use `claude mcp add` then patch the entry — `claude mcp add` doesn't accept absolute paths cleanly through bash).
4. **Editing JSON from bash:** don't pass JSON-with-backslashes through `node -e '...'` — bash eats backslashes and you get `C:Program Files` instead of `C:\Program Files`. Write a temp `.js` file with the Write tool and run it with `node temp.js`. Escape backslashes once in the JS literal (`'C:\\Program Files\\nodejs\\node.exe'`). Always re-read from disk and verify `JSON.parse` round-trips before declaring success.
5. Verify with `claude mcp list` (Claude binary on this laptop: `C:\Users\manba\AppData\Roaming\Claude\claude-code\<version>\claude.exe`).

## Confirmed working examples on this laptop

- **better-icons** — `C:\Program Files\nodejs\node.exe` + `C:\Users\manba\AppData\Roaming\npm\node_modules\better-icons\dist\index.js` → ✓ Connected
- **github (official)** — HTTP transport via `https://mcp.github.com/mcp` → registered, awaits OAuth on first session use (this is expected; HTTP MCPs show ✗ in `mcp list` until first auth)

## Related gotchas

- **Deprecated stdio github MCP:** `@modelcontextprotocol/server-github` is deprecated as of 2025.4.8. The official replacement is the HTTP transport at `https://mcp.github.com/mcp`. Don't register the old stdio package for new installs.
- **Settings.json schema:** `~/.claude/settings.json` does NOT have an `mcpServers` field — schema validator will reject it. MCP servers live in `~/.claude.json` (top-level `mcpServers` for user scope, or per-project under `projects.<path>.mcpServers` for project scope). Use `claude mcp add -s user|local|project` to choose.
- **Claude binary location on Windows:** not on PATH from Git Bash. Lives at `C:\Users\manba\AppData\Roaming\Claude\claude-code\<version>\claude.exe` — **do NOT hardcode the version**, it auto-updates silently (observed 2.1.78 → 2.1.87 during a single session restart). Resolve dynamically: `ls "/c/Users/manba/AppData/Roaming/Claude/claude-code/"` to get the current version directory, then invoke. Or use `tasklist` + `Get-Process claude | Select Path` if Claude is running.
- **HTTP MCP auth is interactive-only:** HTTP-transport MCPs that use OAuth (like the official github server) cannot be authenticated from a bash/tool call. The user must run `/mcp` inside an interactive Claude Code session to trigger the browser OAuth flow. `claude mcp list` will show ✗ Failed to connect until this is done — that's expected, not a registration bug. Setting `GITHUB_TOKEN` as an env var does NOT help HTTP MCPs; that only applied to the deprecated stdio server.
- **Slash command files MUST use CRLF line endings on Windows.** When writing a command file to `~/.claude/commands/*.md` on Windows, the Write tool emits LF (Unix) line endings by default, and the Claude Code `/` picker silently skips those files — the command appears in the backend skill registry (system reminders list it) but never shows up in the UI picker when the user types `/`. Existing working commands (quick-commit.md, grill.md, etc.) all use CRLF. **How to fix:** after Write, run a small Node one-liner to rewrite the file with `\r\n` endings: `node -e "const fs=require('fs');const p='<path>';const s=fs.readFileSync(p,'utf8');fs.writeFileSync(p,s.replace(/\r\n/g,'\n').replace(/\n/g,'\r\n'));"`. **How to verify:** `head -c 25 <file> | od -c` — first line should show `\r \n` after the closing `---` of frontmatter, not just `\n`. This also likely applies to SKILL.md files for custom skills, though unconfirmed.
