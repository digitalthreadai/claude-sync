---
name: ThreadPLM Project
description: AI-native PLM SaaS with CopilotKit generative UI — active development project at C:\Apps\claude\threadplm
type: project
---

## ThreadPLM — Active Project

**Path:** `C:\Apps\claude\threadplm`
**GitHub:** `digitalthreadai/threadplm`
**Status:** Week 1 build started 2026-03-14

### What It Is
Next-generation PLM (Product Lifecycle Management) SaaS for mechanical engineers. AI-powered generative UI using CopilotKit v2 + OpenGenerativeUI.

### V1 Scope
- Parts + BOMs + ECO/ECN management
- Traditional UI (tables, forms, trees) + AI copilot sidebar
- 2 OpenGenerativeUI visualizations (BOM Cost Treemap, Change Impact Graph)
- No CAD integration, no admin UI (Week 5+)

### Tech Stack
- Turborepo monorepo (pnpm)
- Frontend: Next.js 15 + React 19 + TypeScript + TailwindCSS 4 + shadcn/ui
- Agent: Python + LangGraph + GPT-4o/GPT-4o-mini
- DB: Supabase PostgreSQL + RLS
- Auth: Supabase Google OAuth
- Deploy: Vercel (web) + Railway (agent)

### Key Architectural Decisions
- Single Zustand store (UI only) + React Query (server state)
- Agent calls Next.js API, not Supabase directly
- Zod schemas in shared package for JSONB validation
- ECO state machine enforced by DB trigger
- Concurrency-safe numbering via counter table with FOR UPDATE
- Two-tier LLM: GPT-4o-mini for reads, GPT-4o for writes
- OpenGenerativeUI with template-seeded generation + fallback to data tables

### Plan File
`C:\Users\manba\.claude\plans\cosmic-dreaming-elephant.md`
