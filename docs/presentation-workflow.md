# Presentation Workflow

Use the `presentations/` subtree as the presentation-facing layer.

Purpose:

- Document how presentations in this repository should consume reusable visual
  tooling.
- Hold presentation-specific guidance, briefs, examples, and future content.

How presentation work uses the toolchains:

1. Create or update deck content with the Marp tooling in `presentations/marp/`.
2. Create or update diagrams and slide-ready graphics with
   `visualisations/excalidraw/`.
3. Reference rendered assets from the presentation deck.

Why the Marp sync step exists:

- `presentations/marp/tools/apply_default_ramboll_theme_to_slide_deck.py`
  copies the shared Marp CSS into a deck's frontmatter.
- We use it because Marp custom theme registration in multi-root workspaces is
  not reliable enough for shared daily use.
- So in this repository it is a normal part of the workflow.

Separation of concerns:

- `visualisations/` owns reusable generation tools.
- `presentations/` owns deck tooling, presentation-facing usage guidance, and
  context.