# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## General Instructions

- Execute promptly. Do not over-plan. If a task is clear, start implementing immediately rather than asking clarifying questions or producing lengthy plans.
- When resuming work from a previous session, immediately check current state (read key files, check `git log`, read `.claude/checkpoint.md`) before doing anything else. Do NOT start planning or exploring autonomously.
- After making code changes, always verify the app builds/runs. Do not wait for the user to remind you. Restart dev servers if needed.
- This is a Windows 11 machine. Do not suggest macOS-only tools (iOS Simulator, Xcode) or Unix-only paths.

## Tech Stack

- Prefer TypeScript for all new code.
- Primary stack: TypeScript, React, Supabase, Python for scripts/ML.
- Use Next.js or Expo depending on project context.
- Python 3.11+ for backend scripts and AI tools.

## UI/Design Conventions

- Default to dark themes unless explicitly told otherwise.
- When working on UI/styling tasks, confirm the color scheme and theme with the user BEFORE implementing if not specified.
- Standard dark palette: background `#0a0a0f` to `#12121a`, text `#e8e8ed`, muted `#8888a0`.
- Use Inter + JetBrains Mono fonts for web projects.

## Session Continuity Protocol

After every significant milestone (feature complete, major refactor, or before session might end), update `.claude/checkpoint.md` with current state, recent changes, architecture decisions, known issues, and next steps.

At the START of every new session, read `.claude/checkpoint.md` FIRST before doing anything else. Summarize what you understand, then ask if priorities have changed. Never start exploring code autonomously without reading this file.

## Dev Server Convention

All dev servers use **portless** for named URLs — no port numbers, no conflicts.

- Proxy daemon must be running: `portless proxy start --https`
- Access apps at `https://<project>.localhost:1355`
- Every project's `npm run dev` registers a portless alias + starts server on a fixed port
- Fallback without portless: `npm run dev:direct`
- On Windows, use the alias pattern (not command wrapping) because portless spawn uses `/bin/sh`

| Project | Port | URL |
|---------|------|-----|
| plmflow | 4001 | `https://plmflow.localhost:1355` |
| archflow2 | 4002 | `https://archflow2.localhost:1355` |
| resemble | 4003 | `https://resemble.localhost:1355` |
| landlawd | 4004 | `https://landlawd.localhost:1355` |
| threadplm | 4005 | `https://threadplm.localhost:1355` |
| skillsdir | 4006 | `https://skillsdir.localhost:1355` |
| mathfire | 4007 | `https://mathfire.localhost:1355` |
| grodeals | 4008 | `https://grodeals.localhost:1355` |
| alsurah | 4009 | `https://alsurah.localhost:1355` |
| archflow | 4010 | `https://archflow.localhost:1355` |
| familyface | 4011 | `https://familyface.localhost:1355` |
| appslauncher | 4100 | `https://appslauncher.localhost:1355` |

## Workspace Overview

`C:\Apps\claude` is a multi-project workspace containing independent apps. Each subdirectory is its own self-contained project.

---

## Projects

### PartClassifier (Python AI Agent)
**Path:** `C:\Apps\claude\PartClassifier`
**GitHub:** https://github.com/digitalthreadai/partclassifier

An AI agent that classifies mechanical parts from Excel input, scrapes distributor websites for specs, and writes per-class Excel output files.

**Run:**
```bash
cd PartClassifier
python main.py
```

**Key commands:**
```bash
pip install -r requirements.txt   # install dependencies
cp .env.example .env              # then set GROQ_API_KEY
```

**Stack:** Python 3.11+, Groq API (llama-3.3-70b via OpenAI SDK), curl_cffi, BeautifulSoup, openpyxl

**Architecture:**
- `main.py` — orchestrator: reads input Excel, loops parts, calls classifier → scraper → extractor → writer
- `src/part_classifier.py` — LLM call to classify part name into a category string
- `src/web_scraper.py` — DuckDuckGo search + curl_cffi scraping + URL cache (`url_cache.json`); preferred trusted domains scored higher; `_spec_score()` picks best page
- `src/attribute_extractor.py` — LLM call to extract structured attributes from scraped text; handles unit conversion (inches ↔ mm) per part
- `src/attr_schema.py` — canonical attribute names per class + alias normalization; this is what keeps columns consistent across parts
- `src/excel_handler.py` — reads input; writes one `.xlsx` per class into `output/`

**Input:** `input/PartClassifierInput.xlsx` — columns: Part Number, Part Name, Manufacturer Part Number, Manufacturer Name, Unit of Measure

**Adding a new part class:** Add its canonical attribute list to `CLASS_SCHEMAS` in `src/attr_schema.py`. Add any alias variants to `ALIASES`.

---

### archflow2 (React/TypeScript App)
**Path:** `C:\Apps\claude\archflow2`

**Run:**
```bash
cd archflow2
npm install
npm run dev       # dev server
npm run build     # production build
npm run preview   # preview production build
```

**Stack:** React 18, TypeScript, Vite, Tailwind CSS

**Structure:** `src/components/`, `src/hooks/`, `src/data/`, `src/types/`, `src/utils/`

---

### alsurah (Static HTML)
**Path:** `C:\Apps\claude\alsurah`
**GitHub:** https://github.com/digitalthreadai/alsurah (deployed via GitHub Pages)

Single `index.html` file. No build step.

---

### archflow (Static HTML)
**Path:** `C:\Apps\claude\archflow`

Single `index.html` file. No build step.

---

### familyface (Static HTML/JS — Original Resemble PWA)
**Path:** `C:\Apps\claude\familyface`

`index.html` + `app.js` + `style.css`. No build step. Original web-only version of Resemble.

---

### resemble (React Native / Expo — Mobile + Web)
**Path:** `C:\Apps\claude\resemble`

Native mobile app (iOS/Android) + web version of Resemble face comparison tool. Rewrite of `familyface` using React Native for proper native camera face scanning.

**Run:**
```bash
cd resemble
npm run web        # web dev server
npm run ios        # iOS simulator
npm run android    # Android emulator
```

**Stack:** Expo SDK 55, React Native, TypeScript, Expo Router, expo-camera, react-native-vision-camera, react-native-svg

**Structure:** `app/` (screens via Expo Router), `src/engine/` (face analysis), `src/components/`, `src/hooks/`, `src/theme/`

---

### appslauncher (Dev/Prod Dashboard)
**Path:** `C:\Apps\claude\appslauncher`

Browser-based dashboard to manage all dev/prod servers. Start/stop dev servers, view status, toggle Dev/Prod views.

**Run:**
```bash
cd appslauncher
npm run dev        # with portless
npm run dev:direct # without portless
```

**Stack:** Express 5, vanilla HTML/JS (no build step)

**Port:** 4100 → `https://appslauncher.localhost:1355`

**Config:** Edit `apps.config.json` to add/modify app entries, prod URLs, icons.

**API:** GET `/api/apps`, GET `/api/status`, POST `/api/apps/:id/start`, POST `/api/apps/:id/stop`, GET `/api/apps/:id/logs`

---

## GitHub

All projects push to the `digitalthreadai` GitHub organization:
- https://github.com/digitalthreadai/partclassifier
- https://github.com/digitalthreadai/alsurah
