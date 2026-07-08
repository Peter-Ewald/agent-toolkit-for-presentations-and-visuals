# Ramboll Excalidraw Diagram Skill

A Claude Code skill that generates Ramboll-styled Excalidraw diagrams — brand colors, `NunitoCustom` typography, and correct native bindings (arrows connected at both ends, labels grouped with their shapes) every time.

Ask Claude to create a diagram (e.g. "create an Excalidraw diagram showing how the offline evaluation pipeline scores a dataset run") and this skill handles concept mapping, layout, building the JSON, rendering, and visual validation. See `SKILL.md` for the full methodology Claude follows.

## Why a Python module instead of hand-written JSON

Excalidraw's native bindings — `startBinding`/`endBinding` on arrows, reciprocal `boundElements` entries, shared `groupIds` for label+shape pairs — are easy to get wrong by hand and impossible to tell apart from a broken diagram just by reading the JSON. Before `scripts/elements.py` existed, every element in this skill's own example diagrams had empty `groupIds` and null bindings — the diagrams looked right when rendered but had zero live structure. `scripts/elements.py` is a small, tested builder module (`rect()`, `text()`, `arrow()`, `labeled_rect()`, `group()`) that always produces the correct shape, so diagrams built through it are guaranteed structurally valid without anyone having to remember the binding rules.

## Setup

```bash
cd .claude/skills/diagram-excalidraw/scripts
uv sync
uv run playwright install chromium
```

## File Structure

```
diagram-excalidraw/
  SKILL.md                          # Design methodology + workflow (what Claude reads)
  scripts/
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

## Design methodology credit

The diagram-design methodology in `SKILL.md` (depth assessment, visual pattern library, research mandate, render-and-validate loop) is adapted from the open-source [excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill). This repository no longer keeps that project as an in-tree clone — the parts worth keeping have been folded into `SKILL.md` directly, and the parts that didn't fit this repo's needs (notably its "don't write a generator script" advice) were deliberately not carried over, since hand-written JSON is exactly what produced this skill's original binding bugs.
