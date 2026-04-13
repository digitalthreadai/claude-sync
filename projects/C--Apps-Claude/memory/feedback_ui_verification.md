---
name: UI verification gate before declaring done
description: After any UI/CSS/theme change in a project with a dev server, run a dev-browser or Claude_Preview verification script before claiming the task is complete. Must also check sidebar/header/navigation still render.
type: feedback
---

# Rule

After any UI/CSS/theme change in a project with a running dev server, run a verification script (dev-browser preferred, Claude_Preview as fallback) that:

1. Navigates to the changed page
2. Inspects the specific element(s) that were modified
3. **Additionally verifies sidebar, header, and primary navigation still render correctly**
4. Reports pass/fail with a screenshot or computed-style readout

Do not say "done" until the verification script passes. If no dev server is available, explicitly state that verification was skipped and why.

## Why

Five sessions in the month leading up to 2026-04-06 shipped broken UI:
- Streamlit dark-mode session: CSS hid the header element, breaking the sidebar toggle
- Streamlit light mode was "so broken" the user asked to remove it entirely
- LandLawd landing page first draft was "too basic" and needed full redo
- Face-similarity app: unescaped apostrophe caused a JS syntax error, app wouldn't run
- UI styling was the #1 project-area friction (5 sessions)

The `/insights` report flagged "verify before declaring done" as a top-three recommendation. User approved this rule on 2026-04-06 after installing dev-browser as the primary scripted-verification tool.

## How to apply

**When triggered:** Any Edit/Write to .css, .scss, .tsx/.jsx styling props, Tailwind classes, theme config, Streamlit st.markdown/st.components styling, or HTML template changes in a repo that has a dev server.

**Tool priority:**
1. `dev-browser` CLI (cheapest, fastest, sandboxed) — use for scripted navigate+inspect+screenshot flows. Permission pre-allowed via `Bash(dev-browser *)`.
2. `Claude_Preview` MCP — use when already working with a local dev server defined in `.claude/launch.json`. Better for exact computed-style inspection via `preview_inspect`.
3. `Claude_in_Chrome` MCP — only when we need the user's real logged-in browser session.

**Minimum verification for theme/CSS changes:**
- Screenshot or inspect the modified element
- Confirm sidebar renders (if the app has one)
- Confirm header renders
- Confirm primary nav/toggle buttons are visible and clickable
- For theme work: verify BOTH light and dark mode (unless user has explicitly removed one)

**Skip only when:**
- User explicitly says "don't verify" or "just commit it"
- No dev server exists for the project
- Change is pure code/logic with zero visual surface
