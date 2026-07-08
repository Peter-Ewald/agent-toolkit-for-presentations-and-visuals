# Implementation Plan

This file tracks work that is not completed yet. All repository documentation describes the
current implementation — this file describes only what's still pending.

This repository targets Claude Code as its primary agent. Earlier drafts explored a shared MCP
server with per-client adapters for GitHub Copilot, Cursor, and Claude Code; that direction was
dropped before any of it was built, in favor of a working Claude Code harness (`.claude/skills/`,
`.claude/hooks/`) backed by the same `docs/` and capability layers everything else already uses.

---

## Recommended Wave Progression

1. **Canonical brand pipeline + font/color fixes.** `visualisations/excalidraw/themes/ramboll-theme.json`
   and `presentations/marp/themes/ramboll.css` each hand-type their own copy of the Ramboll palette,
   and each copy has a different wrong cyan (`#009df0` and `#0094e3`; the correct value, per
   `docs/brand/colours/color_guidelines.md`, is `#0098EB`). Neither the Excalidraw render template
   nor the Marp theme has a working `@font-face` rule, so both silently fall back away from
   `NunitoCustom`. Replace the hand-typed values in both consumers with values derived
   programmatically from `docs/brand/colours/colors.scss` (or `colors.oco`), and add real
   `@font-face` blocks in both places pointing at `docs/brand/fonts/*.ttf`.
2. **`diagram-excalidraw` Claude skill.** Build `.claude/skills/diagram-excalidraw/`: a palette
   reference pointed at `docs/brand`, a small tested Python helper module (`rect()`/`text()`/
   `arrow()`/`group()`) that always emits correct `startBinding`/`endBinding` with reciprocal
   `boundElements` and shared `groupIds`, one consolidated render script, and a mandatory
   "render, then view the PNG" final step. This replaces `visualisations/excalidraw/tools/`'s
   render logic and the nested `excalidraw-diagram-skill/` upstream clone, both of which are
   retired once their useful parts (renderer, design methodology) are folded in.
3. **Binding validation hook.** A script that checks every Excalidraw arrow's bindings are
   mutual and every label/shape pair shares a `groupIds` entry, wired as a project `PostToolUse`
   hook (`.claude/settings.json`) on `Write`/`Edit` matching `*.excalidraw`, so a broken diagram
   is caught immediately instead of discovered by opening the app.
4. **Environment setup script.** A one-shot `uv sync && uv run playwright install chromium`
   script plus a short troubleshooting note for the "stale `.venv` after a directory move"
   failure mode, so the next agent doesn't have to rediscover the fix by hand.
5. **Harness finalization.** Remove the temporary `@~/Projects/agents/CLAUDE.md` import from
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
