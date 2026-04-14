# Workflows

This folder is the active recipe layer for the repository.

Use it when the user asks for a concrete task rather than a reusable capability
change.

Workflow families:

- `presentations/`: create, update, and theme decks
- `visualisations/`: create, theme, and render reusable visuals
- `combined/`: workflows that update both visual assets and decks

Rule:

- Keep the underlying implementation details in `presentations/` and
  `visualisations/`.
- Keep the task framing and step order here.
