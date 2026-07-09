# Visual Provider Contract

A visual provider is a tool this repository wraps to produce Ramboll-branded visual output —
`diagram-excalidraw` today, and a candidate shape for future providers such as draw.io or
matplotlib. This doc is the minimum shape a new provider must have before it's considered part of
the repository's capability layer, so a second provider doesn't have to guess the pattern or
quietly diverge from it. `diagram-excalidraw` is the reference implementation throughout.

## Where it lives

`.claude/skills/<provider-name>/`, per `docs/repo-overview.md`'s rule: a provider becomes a Claude
Code skill (not just a `presentations/`-style capability folder) specifically because it needs
injected design methodology, not just scripts and assets. If a future provider genuinely has no
methodology worth injecting — no visual pattern library, no structural pitfalls, no design
process — it doesn't need to be a skill; it can live as a plain capability folder instead, the way
`presentations/marp/` does today.

## Required pieces

- **`SKILL.md`** — the design methodology: when to use this provider, its visual vocabulary and
  pattern library, how it derives brand values from `docs/brand/` (never hand-typed), and a
  **mandatory render-and-validate loop** — render to a viewable artifact, look at it, fix it,
  repeat. `diagram-excalidraw/SKILL.md`'s depth assessment, pattern-mapping table, and "Render &
  Validate (MANDATORY)" section are the template.
- **`README.md`** — the human-facing overview: why this provider exists, setup instructions, file
  structure, and credit for any third-party methodology it adapts.
- **`scripts/setup.sh`** — one-shot environment setup, if the provider needs a runtime environment
  at all (a provider with no dependencies beyond stdlib doesn't need one).
- **A structural-correctness builder**, if the provider's native format has pitfalls worth
  encoding in code rather than trusted to hand-authored source — `elements.py`'s role for
  Excalidraw's bindings/groupIds. Not every format has an equivalent; skip this if the provider's
  source format has no comparable structural trap.
- **`scripts/render.py`** (or equivalent) — produces the viewable artifact `SKILL.md`'s
  render-and-validate loop looks at. A provider with no visual rendering step doesn't fit this
  contract at all.
- **A theme reference generated from `docs/brand/`** — extend `docs/brand/sync_to_consumers.py`
  with a new target for the provider rather than writing a second, parallel sync mechanism or
  hand-copying palette values. One script, one source of truth, projected into every consumer.
- **`examples/`** — at least one worked example plus its rendered output, kept in sync with
  whatever builder/validation tooling exists. `diagram-excalidraw`'s own shipped examples went
  stale for a while after a folder move — don't let a new provider's examples rot the same way.
- **A validation hook under `.claude/hooks/`**, only if the provider's native format has a
  structural invariant worth enforcing automatically on every edit — `validate_excalidraw_
  bindings.py`'s role. Skip this if the format has no such invariant.
- **A `workflows/<family>/README.md` entry** listing the provider's real command-level entry
  points, cross-checked against what actually exists on disk — this has drifted twice already for
  `diagram-excalidraw` (see `docs/workflow-layer.md`'s "Automation level" section for the
  documentation-only-by-design decision that still applies to any new provider's workflow entry).

## What a new provider does not need to duplicate

- The brand palette, fonts, and logos — those live once in `docs/brand/`. Extend the sync script;
  don't fork it.
- A design methodology from scratch, if an existing open-source project already has one worth
  adapting — credit the origin in the new skill's own docs rather than re-deriving it, the way
  `diagram-excalidraw/SKILL.md` credits its upstream methodology source.
- Its own workflow-automation layer — `workflows/` stays documentation-only across every
  provider, per `docs/workflow-layer.md`; a provider that genuinely needs one-command automation
  adds that script to its own `scripts/`, not to `workflows/`.
