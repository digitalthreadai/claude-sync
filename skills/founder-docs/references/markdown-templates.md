# Markdown Documentation Templates

Use these as structural guides when generating the 3 markdown files. Replace `[placeholders]` with actual project data from the discovery phase.

---

## strategy.md Template

```markdown
# Strategy & Feature Guide — [Project Name]

## Vision

**"[Positioning tagline]"** — [2-3 sentences about what makes this project unique and why it exists.]

---

## Competitive Landscape

| Competitor | Key Feature | Weakness |
|-----------|------------|----------|
| [Name] | [What they offer] | [Gap this project fills] |

> **Skip this section** if the project has no known competitors or is an internal tool.

---

## Revenue Streams (Built In From Day 1)

### Stream 1: [Revenue Method] ($X-Y/mo)
- **What:** [Description]
- **Where it shows:** [UI locations]
- **Database fields:** [relevant columns]
- **Target:** [revenue goal]

> **Skip this section** if the project has no monetization.

---

## Feature Map

### Core Public Features

#### 1. [Feature Name]
- **Route:** `/path`
- **Features:**
  - [bullet 1]
  - [bullet 2]

### Admin Features

#### N. [Feature Name]
- **Route:** `/admin/path`
- **Features:** [list]

### SEO & Infrastructure

#### N. [Feature Name]
- **Route/File:** [path]
- **Purpose:** [what it does]

---

## Database Schema ([N] Tables)

### [Group 1] Tables
| Table | Purpose |
|-------|---------|
| `table_name` | [one-line description] |

### Key Columns on `[main_table]`
| Column | Type | Purpose |
|--------|------|---------|
| `column` | `type` | [description] |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | [Name + version] |
| UI | [Library + version] |
| Database | [Name + features] |
| Auth | [Method] |
| Validation | [Library] |
| Icons | [Library] |
| Deployment | [Platform] |
| Fonts | [Names] |

---

## Roadmap

| Timeline | Milestones | Expected Outcome |
|----------|-----------|-----------------|
| [Phase 1] | [Goals] | [Metric] |
| [Phase 2] | [Goals] | [Metric] |

> **Skip** if no roadmap exists.

---

## File Structure (Key Files)

\```
src/
├── [dir]/
│   ├── [file]      # [description]
│   └── [file]      # [description]
├── [dir]/
│   └── [file]      # [description]
└── [file]           # [description]
\```
```

---

## setup.md Template

```markdown
# Site Configuration Guide — [Project Name]

## 1. [First Service] Setup

### 1a. [Sub-step]
1. [instruction]
2. [instruction]

### 1b. [Sub-step]
...

---

## 2. [Second Service] Setup
...

---

## 3. Environment Variables

Create a `.env.local` file:

\```bash
cp .env.local.example .env.local
\```

Fill in values:

\```env
# [Source description]
VARIABLE_NAME=value
ANOTHER_VAR=value
\```

| Variable | Description | Where to Find |
|----------|-------------|---------------|
| `VAR_NAME` | [purpose] | [location] |

---

## 4. [Additional Steps]
...

---

## 5. Seed Data (Optional)

\```sql
-- [Description]
INSERT INTO table (columns) VALUES (values);
\```

---

## 6. Deployment

### Deploy to [Platform]
1. [step]
2. [step]
3. [step]

---

## Schema Reference

### Tables Summary
| Table | Purpose | Access |
|-------|---------|--------|
| `name` | [purpose] | [Public Read / Admin Only] |

### Database Functions
| Function | Purpose |
|----------|---------|
| `name()` | [what it does] |

---

## Useful Admin Queries

### [Query Name]
\```sql
SELECT columns FROM table WHERE condition;
\```

---

## Checklist

### Initial Setup
- [ ] [Service] configured
- [ ] Database schema created
- [ ] Auth provider set up
- [ ] Environment variables set
- [ ] Dev server runs successfully

### Content Setup
- [ ] [First content item] created
- [ ] [Feature] verified working

### Deployment
- [ ] Deployed to [platform]
- [ ] Production URLs configured
- [ ] [Verification step]
```

---

## README.md Template

```markdown
# [Project Name]

[One-line project description.]

**Strategy:** [Positioning statement, if applicable.]

## Stack

- **Framework:** [Name + version]
- **Styling:** [CSS framework + theme note]
- **Database:** [Name + features]
- **Auth:** [Method + library]
- **[Category]:** [Library/tool]
- **Deployment:** [Platform]

## Features

### Public
- **[Feature]** — [short description]
- **[Feature]** — [short description]

### Admin (`/admin`)
- **[Feature]** — [short description]

### Infrastructure
- **[Feature]** — [short description]

## Quick Start

\```bash
# Install dependencies
[install command]

# Set up environment
[env command]

# Start dev server
[dev command]
\```

## Setup Guide

See **[SITECONFIGURATIONS.md](./SITECONFIGURATIONS.md)** for complete step-by-step setup.

## Strategy & Features

See **[COO.md](./COO.md)** for the full strategy document.

## Database

**[N] tables** with [security model]:

| Table | Purpose |
|-------|---------|
| `name` | [description] |

## Project Structure

\```
[directory tree with comments]
\```

## Scripts

\```bash
[script] # [description]
[script] # [description]
\```
```

---

## Adaptation Notes

1. **Skip sections** that don't apply — not every project has revenue streams, competitors, or a roadmap
2. **Add sections** for project-specific needs — e.g., Docker setup, CI/CD, testing
3. **Use actual data** from the codebase discovery — never fabricate dependencies, routes, or tables
4. **Match the project's naming conventions** — if they use `pages/` instead of `app/`, reflect that
5. **Include all dependencies** from package.json/requirements.txt — missing deps are the most common doc complaint
