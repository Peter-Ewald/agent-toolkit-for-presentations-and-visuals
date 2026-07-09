# Visualisation Workflows

Use this folder for visual-only tasks.

Current recipe types:

- Set up the local environment (first time only, before any other recipe below)
- Create or update an Excalidraw source diagram
- Apply the Ramboll Excalidraw theme to a diagram
- Render a diagram to PNG for reuse elsewhere

Implementation surface:

- `../../.claude/skills/diagram-excalidraw/`

Current command-level entry points:

- `../../.claude/skills/diagram-excalidraw/scripts/setup.sh`: one-shot environment setup —
  run this before any of the entry points below, the first time.
- `../../.claude/skills/diagram-excalidraw/scripts/elements.py`: not a standalone command —
  a binding-safe builder module imported from a throwaway per-diagram Python script. This is
  where every diagram build actually starts; see `../../.claude/skills/diagram-excalidraw/
  SKILL.md` for the full design methodology (depth assessment, pattern mapping, the mandatory
  render-and-validate loop).
- `../../.claude/skills/diagram-excalidraw/scripts/apply_theme.py`: optional — normalizes
  colors/fonts on a diagram that mixes hand-authored values with brand colors. Diagrams built
  entirely through `elements.py` don't need this step.
- `../../.claude/skills/diagram-excalidraw/scripts/render.py`: renders a `.excalidraw` file to
  PNG.
