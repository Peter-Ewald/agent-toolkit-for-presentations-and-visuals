# Visualisation Workflow

Use the `visualisations/` subtree for reusable generation tooling.

Current workflow families:

- `visualisations/excalidraw/`: source diagrams, theme application, PNG render.

Provider model:

- Each visual provider should own its source formats, theme assets, tooling,
  and provider-specific guidance in its own subtree.
- The current provider is `visualisations/excalidraw/`.
- Future providers such as `visualisations/drawio/` should fit the same model
  rather than changing the repository architecture.

Excalidraw flow:

1. Edit or create a `.excalidraw` source file.
2. Apply the shared theme.
3. Render to PNG.
4. Reuse the PNG in decks or elsewhere.

Wrapper model:

- `visualisations/excalidraw/` is the Ramboll-specific wrapper and operating
  surface.
- `visualisations/excalidraw/excalidraw-diagram-skill/` is an upstream skill
  clone that can supply generic methodology and renderer assets.
- Local changes should stay focused on Ramboll-specific theming, workflow
  integration, and repository conventions rather than rewriting the upstream
  methodology.

How this subtree interacts with presentations:

- Assets generated here can be embedded in decks under `presentations/`.
- Deck assembly itself lives in `presentations/marp/`.
- Task-oriented recipes for visual-only or combined work live under
  `workflows/`.