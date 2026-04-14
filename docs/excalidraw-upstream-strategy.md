# Excalidraw Upstream Strategy

This repository now contains two distinct Excalidraw concerns:

- `visualisations/excalidraw/`: Ramboll-specific wrapper and repository
  integration layer
- `visualisations/excalidraw/excalidraw-diagram-skill/`: cloned upstream skill
  snapshot

Why the upstream clone is useful:

- It already contains strong generic methodology for designing diagrams that
  argue visually.
- It separates brand palette concerns from layout and methodology concerns.
- It includes renderer assets that are very close to the local render pipeline.
- It gives this repository a visible upstream reference point instead of hiding
  third-party logic inside Ramboll-specific files.

What we should reuse from upstream:

- The design methodology in `SKILL.md`
- The brand-palette pattern in `references/color-palette.md`
- Generic element-template and schema references
- Renderer improvements when they are generic rather than Ramboll-specific

What should stay local to this repository:

- Ramboll-specific theme assets and guidance
- Repository-specific workflow documentation
- Presentation integration decisions
- Any wrapper behavior needed to fit this repository's standards and folder
  model

Current decision:

- Keep the cloned upstream skill in-tree for now.
- Treat it as a tracked reference and wrapper dependency, not as the main place
  to customize Ramboll behavior.
- Do not convert it to a git submodule yet.

Why not a submodule yet:

- A plain in-tree clone is easier for agents to read without extra git
  initialization steps.
- The repository does not yet have an explicit upstream update workflow,
  compatibility checks, or ownership rules for submodule bumps.
- Submodules are best introduced once update cadence and validation are clear.

When a submodule becomes reasonable:

- We decide that staying closely synced with upstream matters more than keeping
  repo setup friction low.
- We add a documented update process.
- We add enough validation to verify that local wrapper behavior still works
  after an upstream update.
