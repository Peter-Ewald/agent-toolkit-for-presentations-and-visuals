# Implementation Plan

This file tracks work that is not completed yet. All repository documentation describes the
current implementation — this file describes only what's still pending.

This repository targets Claude Code as its primary agent. Earlier drafts explored a shared MCP
server with per-client adapters for GitHub Copilot, Cursor, and Claude Code; that direction was
dropped before any of it was built, in favor of a working Claude Code harness (`.claude/skills/`,
`.claude/hooks/`) backed by the same `docs/` and capability layers everything else already uses.

---

## Recommended Wave Progression

1. **Environment setup script.** A one-shot `uv sync && uv run playwright install chromium`
   script plus a short troubleshooting note for the "stale `.venv` after a directory move"
   failure mode, so the next agent doesn't have to rediscover the fix by hand.
2. **Harness finalization.** Remove the temporary `@~/Projects/agents/CLAUDE.md` import from
   this repo's root `CLAUDE.md` once its own instructions and skills are complete and
   self-sufficient — that import exists only to carry shared wave/plan-mode conventions during
   the harness build-out, not as a permanent dependency for other agents opening this repo.

---

## Later Considerations

These items are useful but not blocking the wave progression above:

- Add smoke tests for the two Marp CLIs (`presentations/marp/tools/*.py`) and for
  `.claude/skills/diagram-excalidraw/scripts/{elements,render}.py`.
- Add CI or a local verification script that catches broken references between workflow docs
  and capability files — a manual cross-reference sweep has already found stale paths drifting
  silently more than once.
- Add workflow-oriented helper scripts so the recipes documented under `workflows/` can be run
  with consistent commands instead of only being described in prose.
- Define the minimum contract a new visual provider skill should follow (source format, theme
  assets, render/export tool, provider-level workflow doc) using `diagram-excalidraw` as the
  reference implementation, before adding a second provider (draw.io, matplotlib, ...). No second
  provider is planned yet.
- Drop the committed `presentations/marp/tools/__pycache__/` folder and add `__pycache__/` to
  `.gitignore`.
