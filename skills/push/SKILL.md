---
name: push
description: Stage all changes, generate a commit message from the diff, commit, and push to the current branch. Use when you want to quickly save and push your work without creating a PR.
disable-model-invocation: true
---

# Push to GitHub

Quick git workflow: stage, commit with a descriptive message, and push.

## Steps

1. Run `git status` to see what changed
2. Run `git diff --staged` and `git diff` to understand the changes
3. Stage all changes: `git add -A`
4. Generate a concise conventional commit message from the diff:
   - Format: `type: description` (feat, fix, refactor, docs, test, chore, style)
   - Active voice: "Add feature" not "Added feature"
   - Keep under 72 characters
   - If multiple unrelated changes, use the most significant one for the message
5. Commit: `git commit -m "<message>"`
6. Push: `git push origin $(git branch --show-current)`
7. If push fails because remote is ahead, run `git pull --rebase` first, then push again
8. Report: show the commit hash, message, and branch pushed to

## Rules

- Never force push
- Never push to main/master without explicit user confirmation
- If there are no changes to commit, say so and stop
- If on a detached HEAD, warn the user and stop
