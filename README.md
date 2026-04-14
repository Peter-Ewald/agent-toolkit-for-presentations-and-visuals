# Visualisations Repository

Agent-first repository for reusable visuals, presentation tooling, and explicit
task workflows.

Agents should infer how to use this repository from repo-local files only. Do
not assume any user-global or editor-global instruction files.

This repository is organized as three layers:

- `docs/`: canonical standards, architecture, and decision records.
- `presentations/` and `visualisations/`: reusable capability layers.
- `workflows/`: active task recipes that tell an agent how to perform a
  concrete job.

Current capabilities:

- `visualisations/excalidraw/`: Ramboll-specific wrapper for Excalidraw diagram
  creation, theming, and PNG rendering.
- `visualisations/excalidraw/excalidraw-diagram-skill/`: cloned upstream skill
  kept as a reusable reference and future sync point.
- `presentations/marp/`: Ramboll Marp themes, templates, and deck bootstrap
  and theme-application scripts.

Use the layers like this:

1. Read `docs/repo-overview.md` and `docs/agent-guide.md` to understand the
   model.
2. Go to `workflows/` when the task is phrased as a deliverable, such as
   "create a new Ramboll deck" or "render this Excalidraw file to PNG".
3. Go to `presentations/` or `visualisations/` when the task is about improving
   shared tooling, themes, templates, or reusable assets.

The repository is intentionally split so that:

- standards live in one place,
- capabilities can evolve independently,
- workflows can combine capabilities without collapsing them into one subtree.