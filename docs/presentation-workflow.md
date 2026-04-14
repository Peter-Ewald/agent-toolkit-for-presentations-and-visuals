# Presentation Workflow

Use the `presentations/` subtree as the presentation capability layer.

Purpose:

- Document how presentations in this repository should consume reusable visual
  tooling.
- Hold presentation-specific guidance, briefs, examples, and future content.
- Explain how presentation workflows compose the shared presentation capability
  layer with visual capabilities when needed.

How presentation work uses the toolchains:

1. Create or update deck content with the Marp tooling in `presentations/marp/`.
2. Create or update diagrams and slide-ready graphics with
   `visualisations/excalidraw/`.
3. Reference rendered assets from the presentation deck.

How the workflow layer fits:

- `workflows/presentations/` owns recipes such as creating a new Ramboll deck
  or reapplying the shared theme to an existing deck.
- `workflows/combined/` owns flows that also touch visual assets.
- `presentations/marp/` remains the reusable capability layer rather than the
  place where every task description lives.

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
- `workflows/` owns action-oriented recipes built on top of those capabilities.