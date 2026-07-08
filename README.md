# Visualisations Repository

Agent-first repository for reusable visuals, presentation tooling, and explicit
task workflows, built primarily around Claude Code (`CLAUDE.md`,
`.claude/skills/`, `.claude/hooks/`). `AGENTS.md` files are kept as a short,
generic fallback for other agents that discover this repository passively.

Agents should infer how to use this repository from repo-local files only. Do
not assume any user-global or editor-global instruction files.

This repository is organized as three layers:

- `docs/`: canonical standards, architecture, and decision records, including
  the Ramboll brand kit (colors, fonts, logos) under `docs/brand/`.
- `presentations/` and `.claude/skills/`: reusable capability layers —
  `presentations/` for plain shared assets and scripts, `.claude/skills/` for
  capabilities that need Claude Code's own skill methodology.
- `workflows/`: active task recipes that tell an agent how to perform a
  concrete job.

Current capabilities:

- `docs/brand/`: the canonical Ramboll color, font, and logo kit that the
  capability layers below derive their brand values from.
- `.claude/skills/diagram-excalidraw/`: Ramboll-specific Excalidraw diagram
  creation, theming, and PNG rendering, with correct native bindings.
- `.claude/hooks/validate_excalidraw_bindings.py`: blocks any edit to a
  `.excalidraw` file that breaks its native bindings, however the edit was made.
- `presentations/marp/`: Ramboll Marp themes, templates, and deck bootstrap
  and theme-application scripts.

Use the layers like this:

1. Read `docs/repo-overview.md` and `docs/agent-guide.md` to understand the
   model.
2. Go to `workflows/` when the task is phrased as a deliverable, such as
   "create a new Ramboll deck" or "render this Excalidraw file to PNG".
3. Go to `presentations/` or `.claude/skills/` when the task is about
   improving shared tooling, themes, templates, or reusable assets.

The repository is intentionally split so that:

- standards live in one place,
- capabilities can evolve independently,
- workflows can combine capabilities without collapsing them into one subtree.