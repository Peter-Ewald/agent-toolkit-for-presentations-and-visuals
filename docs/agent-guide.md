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
- Use `presentations/` and `.claude/skills/` when the task is about shared
  capabilities, templates, themes, tooling, or reusable source assets.
- Use `workflows/` when the task is phrased as a concrete deliverable or action
  sequence.

Source-of-truth rules:

- Edit `.excalidraw` files instead of rendered PNGs.
- Edit shared Marp theme and deck templates instead of manually editing large
  inline CSS blocks in copied decks.
- Treat generated deck frontmatter and rendered images as outputs.

Scoping model:

- Root files explain the repo-wide intent and route agents.
- Nested files explain domain-specific behavior for `presentations/`,
  `.claude/skills/`, and `workflows/`.
- More specific instruction files should refine, not contradict, the canonical
  docs.

Claude Code is the primary target:

- `CLAUDE.md` files, `.claude/skills/`, and `.claude/hooks/` are the primary,
  authoritative way this repository is used, and route into the `docs/` layer
  below.
- `AGENTS.md` files are kept as a short, generic fallback for other agents
  that discover this repository passively. They should stay aligned with what
  `CLAUDE.md` says and must not describe behavior specific to any other tool.
- Do not depend on user-specific global instructions or editor-specific local
  setup outside this repository.

Decision rules:

- If a user asks "what should this repository support", update `docs/` first.
- If a user asks "how do I do task X", update or add a workflow under
  `workflows/`.
- If a user asks to improve a toolchain, update the capability subtree that
  owns it.
- If a design methodology is adapted from a third-party skill or project,
  credit the origin in that skill's own docs instead of re-deriving the same
  methodology from scratch elsewhere in the repository.