# Excalidraw Agent Notes

Use this folder when the task involves diagram generation, theming, or image
export.

Key files:

- `examples/`: source diagrams that agents should edit.
- `themes/ramboll-theme.json`: shared theme mapping used by the helper script.
- `themes/RAMBOLL_GUIDANCE.md`: design intent and semantic color rules.
- `tools/apply_excalidraw_theme.py`: preprocess source diagrams.
- `tools/render_excalidraw.py`: render PNG output.
- `../../docs/visualisation-workflow.md`: canonical higher-level workflow doc.

How to work safely:

- Edit the `.excalidraw` source, not the PNG.
- Re-run theme application before rendering if the source uses older colors.
- Keep diagrams editorial and restrained rather than decorative.
- Prefer simple layouts that read well when embedded in slides.

Expected output chain:

- `.excalidraw` source -> themed `.excalidraw` -> rendered `.png` -> Marp deck

When not to use this folder:

- If the task is primarily about deck structure or slide styling, move to
  `../marp/AGENTS.md`.