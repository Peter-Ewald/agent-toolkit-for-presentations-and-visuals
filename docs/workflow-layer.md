# Workflow Layer

This repository distinguishes between reusable capabilities and active
workflows.

Purpose:

- Keep shared tooling stable and reusable.
- Give agents a direct place to look when a user asks for a concrete outcome.
- Make it easy to add more providers and more composed flows without rewriting
  the repository model.

What belongs in `workflows/`:

- Task recipes such as "create a new Ramboll deck at path X"
- Task recipes such as "apply the default Ramboll theme to deck Y"
- Task recipes such as "render Excalidraw source Z to PNG"
- Combined flows such as "update a diagram and then refresh the deck that uses
  it"

What does not belong in `workflows/`:

- Shared theme files
- Reusable provider implementation details
- Long-lived source assets
- Canonical architectural rules

Current workflow families:

- `workflows/presentations/`: active presentation-only recipes
- `workflows/visualisations/`: active visual-only recipes
- `workflows/combined/`: recipes that compose presentation and visual
  capabilities

How workflows should be written:

- Start from the user-facing task name.
- Point to the capability layer that owns the implementation.
- Keep the task steps concrete and executable.
- Avoid duplicating the underlying tool documentation unless the workflow needs
  task-specific framing.

Automation level:

- `workflows/` is a documentation-only routing layer, deliberately, not a layer of its own
  scripts. Each recipe names the task and points at the exact capability entry point that does
  it — it doesn't wrap that entry point in a second script.
- This holds even where a task-specific wrapper script would be technically easy to add: the Marp
  side is already one command per task (`presentations/marp/tools/*.py`), so a wrapper would only
  duplicate that command and need to be kept in sync with it. The Excalidraw side is deliberately
  *not* one command — diagram creation is a supervised, iterative design process (see the
  `diagram-excalidraw` skill's own `SKILL.md`), and flattening it into a single script would
  misrepresent it as mechanical and invite skipping the render-and-validate loop that keeps
  diagrams correct.
- If a future capability genuinely is a multi-step process better run as one command than
  described in prose, add that automation to the capability layer itself (as a script alongside
  the tools it composes), not to `workflows/`.

Routing rule:

- If the user asks for a concrete action or deliverable, start in `workflows/`.
- If the user asks to improve a reusable tool, theme, or template, start in the
  owning capability folder.
