# Instructions.ai

This directory is the global instruction source for AI agents and IDE assistants.

It is intentionally tool-agnostic. Codex, Claude, Cursor, Antigravity, Windsurf,
VS Code agents, OpenCode, Gemini-style agents, and project-local assistants should
all be pointed here or given a project copy of these rules.

## Entry Points

- `AGENTS.md` - universal agent contract; use this first in any project.
- `universal-ai-flow.md` - lifecycle for understanding, planning, building, reviewing, and shipping.
- `handoff.md` - persistent memory rules and session update format.
- `project_context.md` - template for project-specific context. Keep this generic here; copy it into projects and customize there.
- `quality-gates.md` - required verification gates before saying work is done.
- `AUTO_CONTEXT.md` - how automatic project context generation works.
- `templates/` - files to copy into new projects.
- `scripts/bootstrap-project.sh` - prepares a project folder with agent-readable instruction files.

## How Agents Must Use This

1. Read `AGENTS.md`.
2. Read `universal-ai-flow.md`.
3. Read `handoff.md`.
4. Read project-local context if present:
   - `PROJECT_CONTEXT.md`
   - `project_context.md`
   - `ai-system/project_context.md`
5. If implementing anything, update the project handoff file before final response.

## Important

Global rules must stay generic. Do not put one project's business details here.
Project-specific details belong in that project's `PROJECT_CONTEXT.md` and
`HANDOFF.md`.
