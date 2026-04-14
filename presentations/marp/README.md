# Marp Toolkit

This folder contains reusable Marp-based deck tooling.

It is a capability layer, not the task-recipe layer.

Contents:

- `themes/ramboll.css`: shared visual source of truth for Marp styling.
- `templates/ramboll_default.md`: reusable default deck structure.
- `tools/apply_default_ramboll_theme_to_slide_deck.py`: applies the shared
  Ramboll theme to a deck by inlining the CSS and copying the logo asset.
- `tools/create_default_ramboll_slide_deck.py`: creates a new deck from the
  Ramboll default template and copies example assets.

Source of truth:

- Edit `themes/ramboll.css` for shared styling.
- Edit `templates/ramboll_default.md` for default slide structure.
- Use `create_default_ramboll_slide_deck.py` to bootstrap a new deck.
- Keep higher-level workflow docs in `../../docs/`, especially
  `presentation-workflow.md`.
- Keep task-oriented recipes in `../../workflows/presentations/`.

Generated behavior:

- `apply_default_ramboll_theme_to_slide_deck.py` rewrites deck frontmatter to
  inline the shared theme.
- This avoids depending on Marp workspace theme registration.
- The generated deck keeps the same Markdown body but gets deterministic inline
  CSS and a deck-local logo asset.

Typical workflow:

1. Create a new deck from `create_default_ramboll_slide_deck.py`.
2. Edit the Markdown content in the new deck.
3. If the shared look changes, update `themes/ramboll.css`.
4. Re-run `apply_default_ramboll_theme_to_slide_deck.py` for the affected decks.

Do not do this:

- Do not manually paste large CSS blocks into random decks by hand.
- Do not edit generated inline CSS inside copied decks unless you intend that
  deck to diverge from the shared theme.