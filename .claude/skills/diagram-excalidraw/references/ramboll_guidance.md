# Ramboll Excalidraw Guidance

Use this file as the human and agent-facing source of truth for presentation
diagram styling.

The default Ramboll PowerPoint template adds an important constraint:

- diagrams should align with the presentation template language, not just the
  broad brand palette.
- keep the look clean, white, structured, and editorial.
- use accent colors sparingly instead of turning every diagram node into a
  bright brand block.
- keep `NunitoCustom` for exported diagrams even though the current PPTX still
  declares Verdana.

Rules:

- Default canvas should be white or near-white, never gradient-heavy.
- Default text should use dark neutral text (`#333333`) rather than strong
  brand colors.
- Prefer Ramboll cyan as a restrained accent, not as the dominant fill across
  all shapes.
- Use ocean for selected outlines or emphasis blocks, not for all text.
- Use forest only for secondary semantic grouping when it materially improves
  comprehension.
- Use pebble, white, and pale cyan for fills and background surfaces.
- Prefer thin dividers and subtle separators over decorative framing.
- Avoid highly saturated warm colors unless a specific semantic warning or
  exception is needed.
- Keep shapes smooth: `roughness: 0`, `fillStyle: solid`, rounded corners where
  appropriate.
- Use the Excalidraw sans family in source diagrams.
- Use `NunitoCustom` in exported PNGs through the renderer template.
- Favor a restrained, editorial infographic look over playful sketch styling.
- Align diagrams to slide layouts: left-aligned content blocks, generous white
  space, and clear column structure.
- Use semantic color roles consistently within a diagram.
- Prefer a small number of color families per diagram.
- When a diagram contains headings inside the canvas, use a quiet hierarchy:
  large title, smaller uppercase section labels, compact body text.

Suggested semantic mapping:

- Source or input objects: pale cyan fill with ocean or dark-neutral stroke.
- Core processing objects: white fill with dark-neutral or ocean stroke.
- Secondary derivations: pale green fill with forest stroke.
- Final indexed or published outputs: white fill with cyan stroke.
- Section containers or callouts: pebble-pale or white surfaces.
- Free text and metadata: dark neutral text (`#333333`).
- Arrow labels: dark neutral text on white labels.
- Dividers: thin gray line (`#B1B2B3`) when needed.

Presentation-template cues to preserve:

- White slide feeling, not branded wallpaper.
- Dark gray title text rather than large colored titles.
- Modest contrast and limited decoration.
- Accent color appears as a cue, not as the whole visual system.
- Image or diagram regions can be separated by thin vertical or horizontal
  divider lines.

Maintenance note:

- `ramboll-theme.json`'s `palette` and `colorMap` values, and the embedded
  font in `../scripts/render_template.html`, are generated from
  `../../../../docs/brand/colours/colors.scss` by
  `../../../../docs/brand/sync_to_consumers.py` — don't hand-edit them. Change
  the brand source and re-run that script instead.
- Add new semantic roles here before using them broadly in multiple diagrams.
- If the official PPTX template changes, prefer its layout behavior over older
  generalized brand assumptions.