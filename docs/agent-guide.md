# Agent Guide

This file is the canonical guidance for portable agent behavior inside this
repository.

Documentation model:

- Keep long-form instructions here in `docs/`.
- Keep root and nested `AGENTS.md` and `CLAUDE.md` files short.
- Use those agent files to route agents to the correct docs and subtree.

Source-of-truth rules:

- Edit `.excalidraw` files instead of rendered PNGs.
- Edit shared Marp theme and deck templates instead of manually editing large
  inline CSS blocks in copied decks.
- Treat generated deck frontmatter and rendered images as outputs.

Scoping model:

- Root files explain the repo-wide intent and route agents.
- Nested files explain domain-specific behavior for `presentations/` and
  `visualisations/`.
- More specific instruction files should refine, not contradict, the canonical
  docs.

Cross-tool portability:

- `AGENTS.md` supports Cursor and Copilot discovery.
- `CLAUDE.md` supports Claude Code directly.
- Keep these files aligned and brief to reduce drift.
- Do not depend on user-specific global instructions or editor-specific local
  setup outside this repository.