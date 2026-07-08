# Implementation Plan

This file tracks work that is not completed yet. All repository documentation describes the
current implementation — this file describes only what's still pending.

This repository targets Claude Code as its primary agent. Earlier drafts explored a shared MCP
server with per-client adapters for GitHub Copilot, Cursor, and Claude Code; that direction was
dropped before any of it was built, in favor of a working Claude Code harness (`.claude/skills/`,
`.claude/hooks/`) backed by the same `docs/` and capability layers everything else already uses.

---

## Recommended Wave Progression

1. **`diagram-excalidraw` Claude skill.** Build `.claude/skills/diagram-excalidraw/`: a palette
   reference pointed at `docs/brand`, a small tested Python helper module (`rect()`/`text()`/
   `arrow()`/`group()`) that always emits correct `startBinding`/`endBinding` with reciprocal
   `boundElements` and shared `groupIds`, one consolidated render script, and a mandatory
   "render, then view the PNG" final step. This replaces `visualisations/excalidraw/tools/`'s
   render logic and the nested `excalidraw-diagram-skill/` upstream clone, both of which are
   retired once their useful parts (renderer, design methodology) are folded in.
2. **Binding validation hook.** A script that checks every Excalidraw arrow's bindings are
   mutual and every label/shape pair shares a `groupIds` entry, wired as a project `PostToolUse`
   hook (`.claude/settings.json`) on `Write`/`Edit` matching `*.excalidraw`, so a broken diagram
   is caught immediately instead of discovered by opening the app.
3. **Environment setup script.** A one-shot `uv sync && uv run playwright install chromium`
   script plus a short troubleshooting note for the "stale `.venv` after a directory move"
   failure mode, so the next agent doesn't have to rediscover the fix by hand.
4. **Harness finalization.** Remove the temporary `@~/Projects/agents/CLAUDE.md` import from
   this repo's root `CLAUDE.md` once its own instructions and skills are complete and
   self-sufficient — that import exists only to carry shared wave/plan-mode conventions during
   the harness build-out, not as a permanent dependency for other agents opening this repo.

---

## Later Considerations

These items are useful but not blocking the wave progression above:

- Add smoke tests for the two Marp CLIs (`presentations/marp/tools/*.py`) and for the render
  pipeline once it moves into the skill.
- Drop the committed `presentations/marp/tools/__pycache__/` folder and add `__pycache__/` to
  `.gitignore`.
- Revisit whether future visual providers (draw.io, matplotlib) fit the same
  `visualisations/<provider>/` model once a second provider is actually needed — no second
  provider is planned yet.
