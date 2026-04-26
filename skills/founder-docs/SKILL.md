---
name: founder-docs
description: |
  Generate a complete founder documentation suite for a web project: strategy doc, setup guide, README, and dark-themed HTML landing pages. Only trigger when the user explicitly invokes this skill by name ("use founder-docs", "run founder-docs", "founder-docs") or clearly asks for the full documentation suite (e.g. "generate the full doc suite", "create all project docs with HTML pages"). Do NOT trigger for partial requests like "document this function", "add a README", or general documentation questions.
---

# App Founder Guide

Generate a complete documentation suite for any web project: strategy docs, setup guide, README, and beautiful dark-themed HTML landing pages.

## What This Skill Produces

| File | Purpose |
|------|---------|
| `strategy.md` | Strategy & feature guide — vision, features, schema, tech stack, roadmap, file structure |
| `setup.md` | Step-by-step setup guide — every service, env var, SQL, deployment, checklist |
| `README.md` | Project overview — stack, features, quick start, structure, scripts |
| `docs/index.html` | Documentation hub — links to all HTML pages |
| `docs/README.html` | Project overview landing page — hero, terminal, stack grid, features |
| `docs/strategy.html` | Strategy dashboard — sidebar nav, revenue cards, feature accordion, timeline |
| `docs/setup.html` | Interactive setup guide — numbered steps, copy buttons, checklist |

---

## Phase 1: Codebase Discovery

Before writing any documentation, thoroughly explore the project. This is the most important phase — the quality of the docs depends entirely on understanding the codebase.

### What to discover

Run these explorations in parallel where possible:

**1. Project metadata**
- Read `package.json` / `requirements.txt` / `Cargo.toml` / `pyproject.toml` — extract ALL dependencies, scripts, project name, version
- Read any existing `README.md`, `.env.example`, `docker-compose.yml`

**2. Application structure**
- Glob for all page/route files: `src/app/**/page.tsx`, `pages/**/*.tsx`, `app/**/*.py`, `routes/**/*`
- Glob for all component files: `src/components/**/*`, `components/**/*`
- Glob for hooks, utilities, middleware: `src/hooks/*`, `src/lib/*`, `src/middleware.*`
- Count files per directory to understand the project's shape

**3. Database & data layer**
- Find migrations: `migrations/**/*.sql`, `prisma/schema.prisma`, `drizzle/**/*`, `supabase/migrations/*`
- Find models/schemas: `models/**/*`, `schema/**/*`, `types/**/*`
- Read schema files to extract table names, columns, relationships

**4. Configuration & deployment**
- Read config files: `next.config.*`, `vite.config.*`, `tailwind.config.*`, `vercel.json`, `Dockerfile`
- Find auth setup: search for OAuth, JWT, session, auth provider references
- Read `.env.example` or `.env.local.example` for required environment variables
- Find CSS/theme files for brand colors (to use in HTML pages)

**5. Features & API**
- Glob for API routes: `api/**/*`, `routes/**/*`
- Read key pages to understand features
- Identify admin vs public routes
- Find any revenue/monetization features (subscriptions, payments, featured listings)

### Output of discovery

Organize findings into these categories (used as input for all docs):
- **Project name & description**
- **Complete dependency list** (with versions)
- **All routes/pages** (grouped: public, admin, API, auth)
- **All components** (grouped by directory)
- **Database tables** (with columns if available)
- **Environment variables** (with descriptions)
- **Auth method** (OAuth, JWT, etc.)
- **Deployment target** (Vercel, AWS, Docker, etc.)
- **Brand colors** (from CSS/theme config, or use defaults)
- **Available scripts** (from package.json)

---

## Phase 2: Generate Markdown Documentation

### A. strategy.md — Strategy & Feature Guide

Use this structure. Adapt sections based on what's relevant to the project. Skip sections that don't apply (e.g., skip "Revenue Streams" for open-source tools with no monetization).

```markdown
# Strategy & Feature Guide — [Project Name]

## Vision
[1-2 paragraph description of what this project is and why it exists]

## Competitive Landscape (if applicable)
| Competitor | Key Feature | Weakness |
|-----------|------------|----------|
| [name] | [what they do] | [gap we fill] |

## Revenue Streams (if applicable)
### Stream 1: [Name] ($X/mo)
- What, where, how
### Stream 2: ...

## Feature Map
### Core Public Features
#### 1. [Feature Name]
- **Route:** `/path`
- **Features:** [bullet list]

### Admin Features
#### N. [Feature Name]
...

### Infrastructure Features
#### N. [Feature Name]
...

## Database Schema ([N] Tables)
### Tables
| Table | Purpose |
|-------|---------|
| `name` | description |

### Key Columns (if schema is known)
| Column | Type | Purpose |
|--------|------|---------|

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Framework | [name + version] |
| ... | ... |

## Roadmap (if applicable)
| Timeline | Milestones | Target |
|----------|-----------|--------|

## File Structure
[Full tree with comments for key files]
```

### B. setup.md — Setup Guide

```markdown
# Site Configuration Guide — [Project Name]

## 1. [First Service Setup] (e.g., Database)
[Step-by-step instructions]

## 2. [Second Service] (e.g., Auth Provider)
[Step-by-step with sub-steps]

## 3. Environment Variables
| Variable | Description | Where to Find |
|----------|-------------|---------------|
| `VAR_NAME` | what it does | where to get it |

## 4. [Additional Setup Steps]
...

## 5. Seed Data (if applicable)
```sql
-- Insert statements
```

## 6. Deployment
[Platform-specific instructions]

## Schema Reference
### Tables Summary
| Table | Purpose | RLS |
|-------|---------|-----|

### Functions
| Function | Purpose |
|----------|---------|

## Useful Queries
### [Query Name]
```sql
SELECT ...
```

## Checklist
### Initial Setup
- [ ] Step 1 done
- [ ] Step 2 done
### Content Setup
- [ ] First content created
### Deployment
- [ ] Deployed and verified
```

### C. README.md — Project Overview

```markdown
# [Project Name]
[One-line description]

**Strategy:** [positioning statement if applicable]

## Stack
- **Framework:** [name + version]
- **Styling:** [CSS framework]
- **Database:** [database + features]
- **Auth:** [method]
- [additional deps]

## Features
### Public
- **[Feature]** — description
### Admin
- **[Feature]** — description
### Infrastructure
- **[Feature]** — description

## Quick Start
```bash
[install command]
[env setup command]
[dev server command]
```

## Setup Guide
See **[setup.md](./setup.md)** for complete setup.

## Strategy & Features
See **[strategy.md](./strategy.md)** for full strategy document.

## Database
| Table | Purpose |
|-------|---------|

## Project Structure
```
[tree]
```

## Scripts
```bash
[available npm/make/etc scripts]
```
```

---

## Phase 3: Generate HTML Landing Pages

Read `references/design.md` for the complete design system — HTML component library (Parts 1–2) and markdown document templates (Part 3).

### Color Customization

Extract the project's brand colors from CSS/theme config. If not found, use these defaults:

```
--bg: #0A0A0F          (dark background)
--surface: #12121A     (card surface)
--surface-hover: #1E1E2E
--terminal-bg: #1A1A2E
--terminal-border: #2A2A3E
--text: #E8E8ED
--muted: #8888A0
--primary: #FFD600     (main accent — adapt to project brand)
--secondary: #E87040   (secondary accent — adapt to project brand)
--green: #4ADE80
--blue: #60A5FA
--purple: #A78BFA
--red: #F87171
```

Replace `--primary` and `--secondary` with the project's actual brand colors if known.

### A. `docs/index.html` — Documentation Hub

A simple landing page with cards linking to all 3 doc pages:
- Project name as hero title with gradient text
- 3 cards in a grid: README (overview), strategy (strategy), setup (setup)
- Each card: icon, title, description, "Open →" link
- Same dark theme as other pages

### B. `docs/README.html` — Project Overview Landing Page

Sections (refer to `references/html-patterns.md` for components):
1. **Hero** — Full-viewport, gradient text title, CTA buttons, terminal mockup with quick start commands
2. **Stack** — Card grid (one card per dependency with version badge)
3. **Features** — Grouped cards (public, admin, infra) with accent-colored groups
4. **Quick Start** — Terminal block with copy button
5. **Database** — Styled table with table names and purposes
6. **Structure** — Collapsible file tree
7. **Footer** — Links to other docs

### C. `docs/strategy.html` — Strategy Dashboard

Layout: Fixed 260px sidebar + main content area
1. **Sidebar** — Logo, nav sections with scroll spy, footer links
2. **Hero banner** — Title with gradient, description
3. **Vision** — Quote card with gradient border, differentiator cards
4. **Competitors** — Styled comparison table (if applicable)
5. **Revenue** — 2x2 card grid with pricing badges (if applicable)
6. **Features** — Accordion sections (Public / Admin / Infra)
7. **Database** — Schema tables with type badges
8. **Tech Stack** — Compact card grid
9. **Roadmap** — Horizontal timeline (if applicable)
10. **File Structure** — Collapsible tree

### D. `docs/setup.html` — Interactive Setup Guide

Layout: Fixed 260px sidebar + main content area
1. **Sidebar** — Logo, time estimate, progress bar, numbered step links, footer
2. **Hero banner** — Title, description
3. **Step sections** — Each with numbered badge, title, sub-time, content
4. **Code blocks** — Terminal-styled with syntax highlighting, copy buttons, collapsible
5. **Env vars** — Styled table
6. **Schema reference** — Tables with color-coded badges
7. **Query cards** — Collapsible with copy buttons
8. **Checklist** — localStorage-persisted checkboxes with progress bar

---

## Key Principles

1. **Discover first, write second.** Never assume project structure — always explore.
2. **Skip irrelevant sections.** Not every project has revenue streams or competitors. Adapt.
3. **Self-contained HTML.** Only external dependency is Google Fonts (Inter + JetBrains Mono).
4. **Responsive.** All HTML pages work on mobile (sidebar collapses under 900px).
5. **Interactive.** Copy buttons, collapsible sections, localStorage checklist, scroll spy.
6. **Accurate.** Every dependency, route, component, and table mentioned must exist in the codebase.
