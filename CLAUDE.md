# Claude Summary

This repository is for agent-assisted visual asset generation and optional slide
deck creation.

Read first:

- `docs/repo-overview.md`
- `docs/agent-guide.md`

Working model:

- `docs/` contains canonical human docs.
- `AGENTS.md` and `CLAUDE.md` files are short adapters that point to those
  docs.
- Repository behavior should be understandable from repo-local files only.
- More specific nested instruction files override broader ones when they apply.

Subtree routing:

- `presentations/` for presentation-facing guidance and usage.
- `visualisations/` for reusable generation tools and render workflows.