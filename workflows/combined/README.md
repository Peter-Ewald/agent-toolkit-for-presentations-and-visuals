# Combined Workflows

Use this folder for tasks that compose presentation and visual capabilities.

Current recipe types:

- Create or update a diagram, render it, and embed it in a deck
- Refresh a shared visual and then re-export the deck that uses it
- Create a new deck that is expected to consume shared rendered assets

Implementation surfaces:

- `../../presentations/marp/`
- `../../visualisations/excalidraw/`

Rule:

- Keep visual generation logic in the visual provider.
- Keep deck generation logic in the presentation provider.
- Use this folder to explain orchestration order and handoff points.
