# Agent Guide

This file is the canonical guidance for portable agent behavior inside this
repository.

Documentation model:

- Keep long-form instructions here in `docs/`.
- Keep root and nested `AGENTS.md` and `CLAUDE.md` files short.
- Use those agent files to route agents to the correct docs and subtree.

Layer model:

- Use `docs/` when the task is about repository standards, architecture,
  ownership boundaries, or future direction.
- Use `presentations/` and `visualisations/` when the task is about shared
  capabilities, templates, themes, tooling, or reusable source assets.
- Use `workflows/` when the task is phrased as a concrete deliverable or action
  sequence.

Source-of-truth rules:

- Edit `.excalidraw` files instead of rendered PNGs.
- Edit shared Marp theme and deck templates instead of manually editing large
  inline CSS blocks in copied decks.
- Treat generated deck frontmatter and rendered images as outputs.
- Treat the cloned upstream Excalidraw skill as an upstream reference unless a
  local Ramboll-specific wrapper requirement clearly belongs in this repository.

Scoping model:

- Root files explain the repo-wide intent and route agents.
- Nested files explain domain-specific behavior for `presentations/`,
  `visualisations/`, and `workflows/`.
- More specific instruction files should refine, not contradict, the canonical
  docs.

Cross-tool portability:

- `AGENTS.md` supports Cursor and Copilot discovery.
- `CLAUDE.md` supports Claude Code directly.
- Keep these files aligned and brief to reduce drift.
- Do not depend on user-specific global instructions or editor-specific local
  setup outside this repository.

Decision rules:

- If a user asks "what should this repository support", update `docs/` first.
- If a user asks "how do I do task X", update or add a workflow under
  `workflows/`.
- If a user asks to improve a toolchain, update the capability subtree that
  owns it.
- If an upstream Excalidraw skill file already solves a generic problem,
  prefer reusing or documenting it over copying its logic into multiple local
  files.