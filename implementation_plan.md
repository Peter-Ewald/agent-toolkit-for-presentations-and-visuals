# Implementation Plan

This file tracks work that is not completed yet. All repository documentation describes the
current implementation — this file describes only what's still pending.

This repository targets Claude Code as its primary agent. Earlier drafts explored a shared MCP
server with per-client adapters for GitHub Copilot, Cursor, and Claude Code; that direction was
dropped before any of it was built, in favor of a working Claude Code harness (`.claude/skills/`,
`.claude/hooks/`) backed by the same `docs/` and capability layers everything else already uses.

---

No wave is currently queued. The items below are useful follow-ups, not blocking anything:

- Add smoke tests for the two Marp CLIs (`presentations/marp/tools/*.py`) and for
  `.claude/skills/diagram-excalidraw/scripts/{elements,render}.py`.
- Add CI or a local verification script that catches broken references between workflow docs
  and capability files — a manual cross-reference sweep has already found stale paths drifting
  silently more than once.
- Define the minimum contract a new visual provider skill should follow (source format, theme
  assets, render/export tool, provider-level workflow doc) using `diagram-excalidraw` as the
  reference implementation, before adding a second provider (draw.io, matplotlib, ...). No second
  provider is planned yet.
- Drop the committed `presentations/marp/tools/__pycache__/` folder and add `__pycache__/` to
  `.gitignore`.
