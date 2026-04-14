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

Routing rule:

- If the user asks for a concrete action or deliverable, start in `workflows/`.
- If the user asks to improve a reusable tool, theme, or template, start in the
  owning capability folder.
