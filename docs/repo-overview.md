# Repo Overview

This repository is designed for agents and humans to share one portable toolkit
for visual work.

Goals:

- Generate diagrams, images, and visual assets with low setup cost.
- Generate presentation decks when needed.
- Keep reusable toolchains separate from presentation-facing guidance.

Structure:

- `presentations/`: presentation-facing layer. Use this for guidance,
  conventions, future examples, and presentation-specific context.
- `visualisations/`: reusable tools and assets. This is where generation
  toolchains live.
- `docs/`: canonical documentation that agent-facing files should reference.

Current reusable tools:

- `visualisations/excalidraw/` for diagram source, theming, and rendering.
- `presentations/marp/` for Marp themes, templates, and deck bootstrap/sync.

Design principle:

- Visual tooling should be reusable outside slide decks.
- Presentation work can depend on those reusable visual tools.
- Deck tooling belongs to the presentation-facing subtree because it is the
  presentation assembly layer.