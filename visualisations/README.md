# Visualisations

This folder is the reusable visual capability layer of the repository.

Use this folder for:

- provider-specific visual tooling
- reusable visual source assets
- shared theming and rendering logic
- provider-level guidance that should remain presentation-agnostic

Current providers:

- `./excalidraw/` for Ramboll-wrapped Excalidraw diagram work

Related layers:

- `../workflows/visualisations/` for visual-only task recipes
- `../workflows/combined/` for workflows that feed visuals into decks
- `../docs/visualisation-workflow.md` for the canonical provider model

Rule:

- Add new providers as peer subfolders under `visualisations/` instead of
  expanding one provider to represent all visual work.