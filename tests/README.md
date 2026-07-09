# Tests

Covers the most important correctness paths across the repo's Python tooling — not every edge
case. This is a separate Python environment from `.claude/skills/diagram-excalidraw/scripts/`'s
own: that one is the skill's runtime, this one is the repo-wide test harness.

## Setup

```bash
uv sync
uv run playwright install chromium
```

Run once from the repo root. VS Code's Python extension picks up `.venv` automatically
(`.vscode/settings.json` points at it) — use the Testing panel, or run from a terminal:

```bash
uv run pytest
```

## Structure

- `tests/unit/` — pure functions, no filesystem/browser/subprocess: Excalidraw element bindings
  (`elements.py`), theme color remapping (`apply_theme.py`), render bounding-box/validation
  helpers (`render.py`), and brand color parsing (`docs/brand/sync_to_consumers.py`).
- `tests/integration/` — real filesystem, browser, or subprocess: the actual Playwright render
  pipeline, the `.claude/hooks/validate_excalidraw_bindings.py` PostToolUse hook (invoked exactly
  as Claude Code invokes it, via stdin JSON), and the Marp deck bootstrap/theme-apply scripts.

`tests/conftest.py` adds `.claude/skills/diagram-excalidraw/scripts/`, `presentations/marp/tools/`,
and `docs/brand/` to `sys.path` so their modules import directly — none of the three is an
installed package, all are loose scripts, same as how `SKILL.md` documents importing
`elements.py` from a throwaway build script.

## Known gap

`docs/brand/sync_to_consumers.py`'s three `write_*` functions (which actually write the
Excalidraw theme JSON, Marp CSS, and font `@font-face` block) are not tested — they write to
hardcoded real repo paths with no parameterization, so testing them would mutate real theme files
as a side effect of running the suite. Only the pure, parameterized parsing/palette-building
functions they depend on (`parse_scss_colors`, `build_palette`, `resolve`) are covered. If those
three functions ever gain a parameterized output path, extending coverage to them is a natural
follow-up.
