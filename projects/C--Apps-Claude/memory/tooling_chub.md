---
name: chub (Context Hub) installed
description: andrewyng/context-hub @aisuite/chub CLI is installed on this Windows laptop with the get-api-docs skill. Includes a local Windows bug patch and a confirmed catalog-coverage map for the user's actual stacks.
type: project
---

## chub install state (this Windows laptop)

- Package: `@aisuite/chub` v0.1.3, installed globally via npm (Node 24.14.1, installed via `winget OpenJS.NodeJS.LTS` on 2026-04-05).
- CLI: `chub` (use `chub -V`, not `--version`).
- Skill: `C:\Users\manba\.claude\skills\get-api-docs\SKILL.md` — verbatim copy of upstream `cli/skills/get-api-docs/SKILL.md`. Claude Code auto-discovers it as `get-api-docs`.
- Repo: https://github.com/andrewyng/context-hub

## CRITICAL: Local Windows patch applied

**Why:** Upstream bug in `src/lib/cache.js` line 190 — uses `cachedPath.lastIndexOf('/')` which returns -1 on Windows (path.join produces `\\`), causing `mkdirSync('')` ENOENT failure on every CDN-fetched (non-bundled) doc.

**Patch location:** `C:\Users\manba\AppData\Roaming\npm\node_modules\@aisuite\chub\src\lib\cache.js` — replaced the `substring(...lastIndexOf('/'))` line with `dirname(cachedPath)`. `dirname` is already imported.

**How to apply:** If `npm i -g @aisuite/chub` is ever re-run, the patch is overwritten. Re-apply the same one-line fix, or check whether upstream has shipped a fix (issue should be filed at andrewyng/context-hub).

**Symptom of unpatched state:** `Error: Failed to load "<id>": ENOENT: no such file or directory, mkdir ''` on `chub get` for any non-bundled doc.

## Validated catalog coverage for user's stacks (smoke-tested 2026-04-05)

**Covered (high value for user's projects):**
- `next/next` — Next.js 16.1.6 ← threadplm, plmflow, landlawd, skillsdir
- `react/react`, `tailwindcss/tailwindcss` ← all React projects
- `supabase/client` (js), `supabase/package` (py) ← every Supabase project
- `langgraph/package` (py) ← threadplm Python agent
- `openai/*`, `anthropic/claude-api` ← all LLM-using projects

**NOT covered (BYOD or accept the gap):**
- `drizzle` — landlawd loses Drizzle help
- `shadcn` — threadplm/plmflow lose shadcn help (minor — it's just React)
- `expo`, `react native` — **resemble, grodeals get almost no value from chub**
- `copilotkit`, `OpenGenerativeUI` — **biggest gap for threadplm; BYOD priority #1**
- `py-capellambse`, `capella`, `teamcenter` — confirmed missing; BYOD-only path for capella-agent / mcp-capella / tc-agent

## Adoption status by project

- **This laptop (`C:\Apps\Claude\`):** chub installed, skill registered. MathFire is the only active coding project that benefits.
- **Other laptop (`C:\Apps\claude\` per Dropbox checkpoint.md):** NOT YET installed. Same install steps will apply (Node + chub + skill + Windows patch).

## How to invoke

User doesn't need to do anything — the skill auto-fires when Claude Code is about to write code against an external SDK. If skill misfires, manually: `chub search <pkg>` then `chub get <id> --lang js|ts|py`.

## Cross-machine annotation sync

Annotations are local per-machine (not synced). If user wants to share notes across both laptops, candidate path is to commit/symlink chub's annotation directory through Dropbox. Not yet set up.

## Reference

- Plan that drove this install: `C:\Users\manba\.claude\plans\iridescent-cuddling-thunder.md`
- Other-laptop project inventory: `C:\Users\manba\Dropbox\claude\.claude\checkpoint.md`
