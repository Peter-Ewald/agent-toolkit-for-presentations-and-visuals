# Repo Overview

This repository is designed for agents and humans to share one portable toolkit
for visual work without mixing standards, reusable capabilities, and task
execution instructions into the same place.

Goals:

- Generate diagrams, images, and visual assets with low setup cost.
- Generate presentation decks when needed.
- Keep reusable toolchains separate from deliverable-specific workflows.
- Stay open to future providers such as draw.io without rewriting the whole
  repository model.

Repository model:

- `docs/`: canonical standards, architecture, and repository decisions.
- `presentations/`: presentation capability layer.
- `visualisations/`: reusable visual capability layer.
- `workflows/`: active workflow layer for concrete tasks.

Ownership boundaries:

- `docs/` explains what the layers are, what belongs where, and why, and owns
  `docs/brand/` — the canonical Ramboll color, font, and logo kit that every
  other layer derives its brand values from, instead of hand-copying them.
  `docs/brand/sync_to_consumers.py` projects color changes into the Excalidraw
  and Marp theme files; run it after editing `docs/brand/colours/colors.scss`.
- `presentations/` owns shared presentation assets such as Marp themes,
  templates, and presentation-oriented examples.
- `visualisations/` owns reusable visual providers, their themes, and their
  render pipelines.
- `workflows/` owns task recipes that compose one or more capabilities into a
  user-facing action.

Current capabilities:

- `docs/brand/` for the canonical Ramboll color, font, and logo kit (colour
  guidelines, `NunitoCustom` font files, logo SVGs).
- `presentations/marp/` for Ramboll Marp themes, templates, deck bootstrap,
  and theme application.
- `visualisations/excalidraw/` for Ramboll Excalidraw theming and rendering.
- `visualisations/excalidraw/excalidraw-diagram-skill/` as an upstream skill
  snapshot that the Ramboll wrapper can reuse and later track more formally.

Examples of the workflow layer:

- Create a new Ramboll deck at a target path.
- Apply the default Ramboll Marp theme to an existing deck.
- Create or update an Excalidraw diagram and render it to PNG.
- Update a visual and then embed it in a deck.

Design principles:

- Standards should stay stable even when tooling changes.
- Capabilities should be reusable outside any single workflow.
- Workflows should reference capabilities rather than hide or duplicate them.
- Upstream third-party skills should remain recognizable as upstream so local
  wrappers can stay small and maintainable.