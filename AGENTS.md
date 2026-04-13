# Agent Summary

Use this repository to generate diagrams, images, and presentation decks.

Canonical docs live in:

- `docs/repo-overview.md`
- `docs/agent-guide.md`
- `docs/visualisation-workflow.md`
- `docs/presentation-workflow.md`

Rules:

- Treat Markdown in `docs/` as the human-maintained source of truth.
- Treat AGENTS and CLAUDE files as thin adapters that summarize and point to
  those docs.
- Do not rely on user-global or editor-global instruction files for repository
  behavior.
- Treat rendered PNGs and synced deck frontmatter as generated outputs.
- Prefer editing source templates, source diagrams, and shared themes over
  editing generated artifacts.

Routing:

- For diagram or image work, go to `visualisations/AGENTS.md`.
- For presentation-facing workflow or deck-usage guidance, go to
  `presentations/AGENTS.md`.