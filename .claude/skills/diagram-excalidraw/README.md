# Ramboll Excalidraw Diagram Skill

A Claude Code skill that generates Ramboll-styled Excalidraw diagrams — brand colors, `NunitoCustom` typography, and correct native bindings (arrows connected at both ends, labels grouped with their shapes) every time.

Ask Claude to create a diagram (e.g. "create an Excalidraw diagram showing how the offline evaluation pipeline scores a dataset run") and this skill handles concept mapping, layout, building the JSON, rendering, and visual validation. See `SKILL.md` for the full methodology Claude follows.

## Why a Python module instead of hand-written JSON

Excalidraw's native bindings — `startBinding`/`endBinding` on arrows, reciprocal `boundElements` entries, shared `groupIds` for label+shape pairs — are easy to get wrong by hand and impossible to tell apart from a broken diagram just by reading the JSON. Before `scripts/elements.py` existed, every element in this skill's own example diagrams had empty `groupIds` and null bindings — the diagrams looked right when rendered but had zero live structure. `scripts/elements.py` is a small, tested builder module (`rect()`, `text()`, `arrow()`, `labeled_rect()`, `group()`) that always produces the correct shape, so diagrams built through it are guaranteed structurally valid without anyone having to remember the binding rules.

As a repo-wide backstop, `../../hooks/validate_excalidraw_bindings.py` runs on every Write/Edit to any `.excalidraw` file (wired via `../../settings.json`) and blocks the edit if bindings are broken — catching a diagram hand-patched outside `elements.py`, not just proving `elements.py`'s own output is correct.

## Setup

```bash
.claude/skills/diagram-excalidraw/scripts/setup.sh
```

### If setup breaks after moving this folder

`uv run`/`playwright` commands failing with a path or interpreter error usually means `scripts/`
was moved or renamed without also refreshing its `.venv` — a `uv`-managed virtual environment
caches the absolute path of the project directory it was created in, and moving that directory
invalidates it. This happened once already when this skill moved from
`visualisations/excalidraw/tools/` into its current location. Fix: `rm -rf .venv && ./setup.sh`.

## File Structure

```
diagram-excalidraw/
  SKILL.md                          # Design methodology + workflow (what Claude reads)
  scripts/
    setup.sh                        # One-shot environment setup — run this first
    elements.py                     # Binding-safe element builder — see its docstrings
    apply_theme.py                  # Optional color/font normalization pass
    render.py                       # Render .excalidraw to PNG (Playwright + headless Chromium)
    render_template.html            # Browser template used by render.py; embeds NunitoCustom
    pyproject.toml, uv.lock         # Python dependencies (playwright)
  references/
    ramboll-theme.json              # Brand palette + font defaults — generated, don't hand-edit
    ramboll_guidance.md             # Semantic color mapping and Ramboll's diagram style rules
  examples/
    standard_deck_full.excalidraw, standard_deck_split.excalidraw
    rendered/*.png                  # Their rendered output, reused by presentations/examples/
```

`references/ramboll-theme.json` and the embedded font in `render_template.html` are generated from `../../../docs/brand/` by `../../../docs/brand/sync_to_consumers.py` — change the brand source and re-run that script rather than editing either file directly.

## Related tools

If you're sketching a new diagram concept and haven't settled on a structure yet, the official
[Excalidraw MCP](https://github.com/excalidraw/excalidraw-mcp) can generate an interactive draft
directly in chat. It's a different tool for a different job — exploratory, chat-driven sketching
with no brand or binding guarantees — so once the structure is settled, port it into
`scripts/elements.py` to lock it into Ramboll branding and guarantee correct bindings before it
ships in a deck.

## Design methodology credit

The diagram-design methodology in `SKILL.md` (depth assessment, visual pattern library, research mandate, render-and-validate loop) is adapted from the open-source [excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill). This repository no longer keeps that project as an in-tree clone — the parts worth keeping have been folded into `SKILL.md` directly, and the parts that didn't fit this repo's needs (notably its "don't write a generator script" advice) were deliberately not carried over, since hand-written JSON is exactly what produced this skill's original binding bugs.
