# Visualisation Workflow

Use the `visualisations/` subtree for reusable generation tooling.

Current workflow families:

- `visualisations/excalidraw/`: source diagrams, theme application, PNG render.

Excalidraw flow:

1. Edit or create a `.excalidraw` source file.
2. Apply the shared theme.
3. Render to PNG.
4. Reuse the PNG in decks or elsewhere.

How this subtree interacts with presentations:

- Assets generated here can be embedded in decks under `presentations/`.
- Deck assembly itself lives in `presentations/marp/`.