# Marp Agent Notes

Use this folder when the task involves slide decks or Marp theming.

If the task is phrased as a concrete job, read `../../workflows/presentations/`
first and then use this folder as the implementation surface.

Key files:

- `themes/ramboll.css`: shared styling source.
- `templates/ramboll_default.md`: default deck body.
- `tools/create_default_ramboll_slide_deck.py`: bootstrap new decks.
- `tools/apply_default_ramboll_theme_to_slide_deck.py`: regenerate inline deck
  styling; also copies the logo and `NunitoCustom` font files into the deck's
  local `assets/` folder.
- `../../docs/presentation-workflow.md`: canonical higher-level workflow doc.

How to work safely:

- Change the shared theme in `themes/ramboll.css` first.
- Change shared slide archetypes in `templates/ramboll_default.md`.
- If creating a new deck, use `create_default_ramboll_slide_deck.py` instead of
  copying files manually.
- After changing shared styling, run the sync helper on affected decks.
- Don't hand-type the `:root` color values or the `@font-face` `src`
  placeholders in `themes/ramboll.css` — they're generated from
  `../../docs/brand/` by `../../docs/brand/sync_to_consumers.py`. Change
  `docs/brand/colours/colors.scss` and re-run that script instead.

Mental model:

- Standalone theme CSS is the design source.
- Deck-local inline CSS is generated for reliable preview.

When not to use this folder:

- If the task is about diagram source content or PNG rendering, move to
  `../../visualisations/excalidraw/AGENTS.md`.