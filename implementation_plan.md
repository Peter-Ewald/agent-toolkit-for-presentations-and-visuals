# Implementation Plan

This file tracks work that is not completed yet. All repository documentation describes the
current implementation — this file describes only what's still pending.

This repository targets Claude Code as its primary agent. Earlier drafts explored a shared MCP
server with per-client adapters for GitHub Copilot, Cursor, and Claude Code; that direction was
dropped before any of it was built, in favor of a working Claude Code harness (`.claude/skills/`,
`.claude/hooks/`) backed by the same `docs/` and capability layers everything else already uses.

---

## Recommended Wave Progression

1. **Workflows layer refresh.** `workflows/*/README.md` currently routes to capability entry
   points that have already drifted once (`workflows/visualisations/README.md` lists
   `apply_theme.py`/`render.py` as the two command-level entry points but not `elements.py`,
   which is actually where every diagram build starts now, or `setup.sh`) — a symptom of
   `workflows/` staying prose-only with nothing checking it against the capability layer it
   describes. This wave:
   - Rewrites every `workflows/*/README.md` command-level entry point list against what each
     capability actually exposes today, including `elements.py` and
     `.claude/skills/diagram-excalidraw/scripts/setup.sh`.
   - Adds a `workflows/` recipe pointing at `setup.sh`, so "set this repo up" is itself a
     documented task, not something only the skill's own `README.md` mentions.
   - Decides, and documents the decision either way, whether each workflow family gets a real
     one-command helper script or stays a documentation-only routing layer on purpose — and
     updates `docs/workflow-layer.md` to state that decision explicitly instead of leaving it open.

---

## Later Considerations

These items are useful but not blocking the wave progression above:

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
