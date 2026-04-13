# Visualisations Repository

Agent-first repository for creating reusable visual assets and optional
presentation decks.

Agents should infer how to use this repository from the files inside this
repository only. Do not assume any user-global or editor-global instruction
files.

This repository is organized so visual tooling can evolve independently from the
presentation-facing layer while still being easy to combine in slide decks.

Repository layout:

- `docs/`: canonical human-readable documentation.
- `presentations/`: presentation-facing guidance, conventions, and future deck
  content.
- `visualisations/`: reusable tooling for diagram, image, and deck generation.

Current toolchains:

- `visualisations/excalidraw/`: diagram source, theming, and PNG rendering.
- `presentations/marp/`: Marp themes, deck templates, and deck bootstrap/sync
  scripts.

Start here:

1. Read `docs/repo-overview.md`.
2. Read `docs/agent-guide.md`.
3. Then move into `presentations/` or `visualisations/` depending on the task.