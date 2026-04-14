# Implementation Plan

This file tracks follow-up code and implementation work that is still worth
doing after the documentation and folder-structure alignment.

## Near-Term

- Consolidate local Excalidraw renderer assets with the upstream skill so the
  wrapper reuses one generic render implementation instead of carrying two near-
  duplicate copies.
- Decide whether the Ramboll color system should move closer to the upstream
  `color-palette.md` model or remain as the current JSON plus guidance split.
- Add workflow-oriented helper scripts or tasks so the documented recipes in
  `workflows/` can be executed with consistent commands.

## Provider Architecture

- Define the minimum contract for a visual provider such as Excalidraw or
  draw.io: source format, theme assets, render/export tool, and provider-level
  workflow doc.
- Add a second provider only after that contract is documented and tested on the
  first provider.

## Upstream Sync

- Document how to refresh the cloned `excalidraw-diagram-skill/` folder from its
  upstream source.
- Add a lightweight validation checklist for upstream refreshes.
- Revisit whether to convert the upstream clone into a git submodule after the
  sync process is routine.

## Validation

- Add smoke tests for the Marp and Excalidraw helper scripts.
- Add at least one validation path that checks a documented workflow end to end.
- Add CI or a local verification script that catches broken references between
  workflow docs and capability files.
