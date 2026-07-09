# Implementation Plan

This file tracks work that is not completed yet. All repository documentation describes the
current implementation — this file describes only what's still pending.

This repository targets Claude Code as its primary agent. Earlier drafts explored a shared MCP
server with per-client adapters for GitHub Copilot, Cursor, and Claude Code; that direction was
dropped before any of it was built, in favor of a working Claude Code harness (`.claude/skills/`,
`.claude/hooks/`) backed by the same `docs/` and capability layers everything else already uses.

---

No wave is currently queued. The items below are useful follow-ups, not blocking anything:

- **`presentation-marp` Claude Code skill.** `presentations/marp/` is still a plain capability
  folder (theme, template, two bootstrap scripts) with no injected design methodology, unlike
  `diagram-excalidraw`. A skill here would add: deck-narrative and slide-archetype guidance (when
  to reach for lead/bullets/image-right/full-image/statement/split, from `ramboll_default.md`),
  and a render-and-view loop using `npx @marp-team/marp-cli`'s existing PNG/PDF export (used ad
  hoc today, not wired into any script) — mirroring the discipline that keeps
  `diagram-excalidraw`'s output correct. Follow `docs/provider-contract.md`'s shape where it
  applies to a non-visual-diagram provider; deviate explicitly where slide decks don't fit it
  (e.g. no binding-style structural invariant to enforce).
- **Combined diagram-creation + deck-integration workflow.** Composing the two skills for one task
  ("build this diagram and drop it into that deck") is deliberately not a third skill — it's what
  `workflows/combined/README.md` exists for, per `docs/workflow-layer.md`'s own definition. That
  file currently only lists recipe types and implementation surfaces; it needs the actual step
  sequence (build/update diagram → render → embed the PNG path in deck markdown → re-apply deck
  theme) written out, plus a short cross-reference from each skill's own `SKILL.md` pointing at it
  for the composed case.
- Extend `docs/brand/sync_to_consumers.py`'s `write_excalidraw_theme`/`write_marp_theme_colors`/
  `write_excalidraw_font_face` to accept a parameterized output path, so `tests/unit/
  test_sync_to_consumers.py` can cover them without mutating real repo files as a side effect of
  running the suite (see that test file's module docstring for the current gap).
- Document a VS Code Test Explorer gotcha in `tests/README.md`: after switching the workspace's
  Python interpreter to `.venv` (e.g. via the interpreter picker), the Testing panel can keep
  showing no tests even though `.venv/bin/python -m pytest --collect-only` finds all of them from
  a terminal — the extension's test-discovery process caches the interpreter it started with and
  doesn't always re-run discovery on a plain interpreter switch. Before reaching for a full window
  reload, try, in order: (1) the refresh icon in the Testing panel (or Command Palette → "Test:
  Refresh Tests") — cheapest, sometimes enough on its own; (2) Command Palette → "Python: Configure
  Tests" → pytest → `tests` — re-runs the test configuration wizard against the currently-selected
  interpreter, forcing a real re-discovery instead of relying on cached state. If neither populates
  the panel, "Developer: Reload Window" is the reliable fix — the discovery subprocess only fully
  picks up a new interpreter on a fresh start.
