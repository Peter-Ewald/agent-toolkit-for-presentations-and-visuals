# Presentations

This folder is the presentation-facing layer of the repository.

It exists to document how slide decks and presentation work should use the
reusable tooling under `../visualisations/`.

Use this folder for:

- presentation-specific guidance
- reusable Marp-based deck tooling
- future example decks and briefs
- presentation conventions and usage notes

Use the reusable tooling here:

- `./marp/` for Marp themes, templates, and deck bootstrap tooling
- `../visualisations/excalidraw/` for diagram theming and rendering

Concrete example:

- `examples/consume_visual_asset.md` is a small Marp deck under
	`presentations/`.
- It imports a rendered graphic from
	`../visualisations/excalidraw/examples/rendered/standard_deck_split.png`.
- That example shows the intended separation clearly: presentation decks live
	here, while reusable visual assets are produced in `visualisations/`.
- `examples/use_split_and_full_visuals.md` demonstrates both the split-layout
	and full-image slide patterns with visuals rendered from
	`../visualisations/excalidraw/examples/rendered/`.

Canonical docs:

- `../docs/repo-overview.md`
- `../docs/presentation-workflow.md`
- `../docs/visualisation-workflow.md`