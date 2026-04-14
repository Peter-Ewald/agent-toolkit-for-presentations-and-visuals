# Excalidraw Toolkit

This folder contains the Ramboll-specific Excalidraw capability used across the
repository.

Contents:

- `examples/`: reusable source diagrams and placeholders.
- `themes/ramboll-theme.json`: machine-readable color and text defaults.
- `themes/RAMBOLL_GUIDANCE.md`: human guidance for diagram style.
- `tools/apply_excalidraw_theme.py`: maps a source diagram onto the shared
  theme.
- `tools/render_excalidraw.py`: renders `.excalidraw` source to PNG.
- `excalidraw-diagram-skill/`: cloned upstream skill kept as a reusable
  reference and future sync candidate.

Source of truth:

- Edit `.excalidraw` files in `examples/` or your deck-specific source folder.
- Keep the theme in `themes/ramboll-theme.json` aligned with the human guidance
  file.
- Keep higher-level workflow docs in `../../docs/`.

Wrapper model:

- This folder is the Ramboll wrapper and repository integration layer.
- The upstream `excalidraw-diagram-skill/` folder contains generic methodology,
  palette structure, templates, and renderer assets that we should reuse where
  practical.
- Ramboll-specific changes should prefer wrapper docs, theme assets, and
  workflow integration over forking generic upstream methodology.

Typical workflow:

1. Create or edit a `.excalidraw` source file.
2. Apply the shared theme.
3. Render to PNG.
4. Reference the PNG from a deck.

Repository example:

- `examples/rendered/standard_deck_split.png` is a rendered asset consumed by
  `../../presentations/examples/consume_visual_asset.md`.
- `examples/rendered/standard_deck_full.png` is a rendered asset consumed by
  `../../presentations/examples/use_split_and_full_visuals.md`.

Do not do this:

- Do not treat rendered PNGs as the editable master.
- Do not bypass theming if you want diagrams to remain visually consistent.
- Do not mix Ramboll wrapper behavior into the cloned upstream folder unless you
  intentionally want to carry a fork.