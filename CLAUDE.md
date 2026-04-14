# Claude Summary

This repository is for agent-assisted visual asset generation and optional slide
deck creation.

Read first:

- `docs/repo-overview.md`
- `docs/agent-guide.md`
- `docs/workflow-layer.md`

Working model:

- `docs/` contains canonical human docs.
- `presentations/` and `visualisations/` contain reusable capabilities.
- `workflows/` contains task-oriented recipes.
- `AGENTS.md` and `CLAUDE.md` files are short adapters that point to those docs
  and layers.
- Repository behavior should be understandable from repo-local files only.
- More specific nested instruction files override broader ones when they apply.

Subtree routing:

- `workflows/` for explicit deliverable-oriented flows.
- `presentations/` for presentation-facing guidance and usage.
- `visualisations/` for reusable generation tools and render workflows.