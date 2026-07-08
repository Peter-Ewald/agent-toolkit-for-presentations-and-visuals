---
name: diagram-excalidraw
description: Create Ramboll-styled Excalidraw diagram JSON files that make visual arguments. Use when the user wants to visualize workflows, architectures, or concepts for a Ramboll deck or document.
---

# Ramboll Excalidraw Diagram Creator

Generate `.excalidraw` JSON files that **argue visually**, not just display information — styled with Ramboll's brand palette and typeface, with correct native bindings every time.

This skill's design methodology (depth assessment, visual pattern library, render-and-validate loop) is adapted from the open-source [excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill). The Ramboll-specific parts — brand palette, typography, and the binding-safe `elements.py` builder — are local to this repository.

## Before You Build Anything

1. **Colors and semantic mapping**: `references/ramboll-theme.json` (machine-readable palette) and `references/ramboll_guidance.md` (which color/shape means what, and the "restrained, editorial" look this repo's decks expect). Both are generated from `../../../docs/brand/` — see that folder if a color looks wrong; don't hand-edit `ramboll-theme.json`.
2. **Always build elements with `scripts/elements.py`, never by hand-writing JSON.** Hand-crafted Excalidraw JSON in this repo has never once produced correct bindings — this skill's own example diagrams had zero working `startBinding`/`endBinding`/`groupIds` before this module existed (every arrow was visually placed but structurally disconnected). `elements.py`'s `rect()`/`text()`/`arrow()`/`labeled_rect()`/`group()` functions set up bindings and grouping the way Excalidraw's own editor would, so a diagram built entirely from them is guaranteed structurally valid. See the module's docstrings for usage; run `uv run python elements.py` from `scripts/` to see it build and self-check a demo diagram.

   If the structure isn't settled yet, the official [Excalidraw MCP](https://github.com/excalidraw/excalidraw-mcp) can generate an interactive exploratory draft in chat first — it has no brand or binding guarantees, so port the settled structure into `elements.py` before it ships in a deck.

   Every Write/Edit to a `.excalidraw` file is also checked by `../../hooks/validate_excalidraw_bindings.py`, which blocks the edit if bindings are broken — a backstop against hand-patched JSON, not a reason to skip building through `elements.py` in the first place.

---

## Core Philosophy

**Diagrams should ARGUE, not DISPLAY.**

A diagram isn't formatted text. It's a visual argument that shows relationships, causality, and flow that words alone can't express. The shape should BE the meaning.

**The Isomorphism Test**: If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The Education Test**: Could someone learn something concrete from this diagram, or does it just label boxes? A good diagram teaches — it shows actual formats, real event names, concrete examples.

Ramboll's own visual language on top of this: keep the look clean, white, structured, and editorial — see `references/ramboll_guidance.md` before choosing colors or density. Ramboll cyan is a restrained accent, not the dominant fill on every shape.

---

## Depth Assessment (Do This First)

Before designing, determine what level of detail this diagram needs:

### Simple/Conceptual Diagrams
Use abstract shapes when:
- Explaining a mental model or philosophy
- The audience doesn't need technical specifics
- The concept IS the abstraction (e.g., "separation of concerns")

### Comprehensive/Technical Diagrams
Use concrete examples when:
- Diagramming a real system, protocol, or architecture
- The diagram will be used to teach or explain
- The audience needs to understand what things actually look like
- You're showing how multiple technologies integrate

**For technical diagrams, you MUST include evidence artifacts** (see below).

---

## Research Mandate (For Technical Diagrams)

**Before drawing anything technical, research the actual specifications.**

If you're diagramming a protocol, API, or framework:
1. Look up the actual JSON/data formats
2. Find the real event names, method names, or API endpoints
3. Understand how the pieces actually connect
4. Use real terminology, not generic placeholders

Bad: "Protocol" → "Frontend"
Good: "Job queue publishes `JobCompleted{job_id, result_url}`" → "Worker acks via `channel.basic_ack()`"

**Research makes diagrams accurate AND educational.**

---

## Evidence Artifacts

Evidence artifacts are concrete examples that prove your diagram is accurate and help viewers learn. Include them in technical diagrams.

| Artifact Type | When to Use | How to Render |
|---------------|-------------|---------------|
| **Code snippets** | APIs, integrations, implementation details | Dark rectangle + light monospace-styled text |
| **Data/JSON examples** | Data formats, schemas, payloads | Dark rectangle + colored text |
| **Event/step sequences** | Protocols, workflows, lifecycles | Timeline pattern (line + dots + labels) |
| **UI mockups** | Showing actual output/results | Nested rectangles mimicking real UI |
| **Real input content** | Showing what goes IN to a system | Rectangle with sample content visible |
| **API/method names** | Real function calls, endpoints | Use actual names from docs, not placeholders |

The key principle: **show what things actually look like**, not just what they're called.

---

## Multi-Zoom Architecture

Comprehensive diagrams operate at multiple zoom levels simultaneously — like a map that shows both country borders AND street names.

- **Level 1: Summary Flow** — a simplified overview of the full pipeline, often at the top or bottom.
- **Level 2: Section Boundaries** — labeled regions grouping related components.
- **Level 3: Detail Inside Sections** — evidence artifacts and concrete examples. This is where the educational value lives.

**For comprehensive diagrams, aim to include all three levels.**

### Bad vs Good

| Bad (Displaying) | Good (Arguing) |
|------------------|----------------|
| 5 equal boxes with labels | Each concept has a shape that mirrors its behavior |
| Card grid layout | Visual structure matches conceptual structure |
| Icons decorating text | Shapes that ARE the meaning |
| Same container for everything | Distinct visual vocabulary per concept |
| Everything in a box | Free-floating text with selective containers |

---

## Container vs. Free-Floating Text

**Not every piece of text needs a shape around it.** Default to free-floating text (`elements.py`'s `text()` with no `container`). Add containers (`labeled_rect()`, or `text(..., container=box)`) only when they serve a purpose:

| Use a Container When... | Use Free-Floating Text When... |
|------------------------|-------------------------------|
| It's the focal point of a section | It's a label or description |
| It needs visual grouping with other elements | It's supporting detail or metadata |
| Arrows need to connect to it | It describes something nearby |
| The shape itself carries meaning (decision diamond, etc.) | Typography alone creates sufficient hierarchy |

**The container test**: For each boxed element, ask "Would this work as free-floating text?" If yes, remove the container. Aim for <30% of text elements inside containers.

---

## Design Process (Do This BEFORE Writing Code)

### Step 0: Assess Depth Required
Simple/Conceptual or Comprehensive/Technical (see above). If comprehensive, research first.

### Step 1: Understand Deeply
For each concept: What does it **DO** (not what it IS)? What relationships exist? What's the core transformation or flow? What would someone need to **see** to understand this?

### Step 2: Map Concepts to Patterns

| If the concept... | Use this pattern |
|-------------------|------------------|
| Spawns multiple outputs | **Fan-out** (radial arrows from center) |
| Combines inputs into one | **Convergence** (funnel, arrows merging) |
| Has hierarchy/nesting | **Tree** (lines + free-floating text) |
| Is a sequence of steps | **Timeline** (line + dots + free-floating labels) |
| Loops or improves continuously | **Spiral/Cycle** (arrow returning to start) |
| Is an abstract state or context | **Cloud** (overlapping ellipses) |
| Transforms input to output | **Assembly line** (before → process → after) |
| Compares two things | **Side-by-side** (parallel with contrast) |
| Separates into phases | **Gap/Break** (visual separation between sections) |

### Step 3: Ensure Variety
For multi-concept diagrams: **each major concept must use a different visual pattern**. No uniform cards or grids.

### Step 4: Sketch the Flow
Before writing code, mentally trace how the eye moves through the diagram.

### Step 5: Build with `elements.py`
Only now write the Python that constructs the elements (see below).

### Step 6: Render & Validate (MANDATORY)
Run the render-view-fix loop until the diagram looks right — see **Render & Validate** below. Not optional.

---

## Building the Diagram

Write a short, throwaway Python script (or a series of edits to one) that imports `scripts/elements.py` and constructs the scene:

```python
import json
import sys
sys.path.insert(0, "path/to/.claude/skills/diagram-excalidraw/scripts")
from elements import rect, labeled_rect, text, arrow, group, scene

CYAN, OCEAN, FOREST, DIVIDER = "#0098eb", "#05326e", "#125a40", "#b1b2b3"  # from references/ramboll-theme.json

source, source_label = labeled_rect("source", 100, 100, 180, 90, "Job queue", stroke=OCEAN, fill="#cceafb")
worker, worker_label = labeled_rect("worker", 420, 100, 180, 90, "Worker", stroke=OCEAN)
flow = arrow("flow", source, worker, stroke=DIVIDER)

elements = [source, source_label, worker, worker_label, flow]
with open("my_diagram.excalidraw", "w") as f:
    json.dump(scene(elements), f, indent=2)
```

**For large/comprehensive diagrams, build in sections** — add one section's elements per edit rather than writing the whole diagram in one pass, so each section gets real attention to layout and spacing. Since every element is a plain Python object until you serialize it, cross-section arrows and groups work exactly like same-section ones — pass the actual shape dicts from earlier sections into `arrow()`/`group()`.

**Do not hand-write element JSON**, even for a single quick fix — always go through `elements.py`, including for edits to an existing diagram (rebuild the affected elements via the module rather than patching raw JSON).

### Shape Meaning

| Concept Type | Shape | Why |
|--------------|-------|-----|
| Labels, descriptions, details | free-floating `text()` | Typography creates hierarchy |
| Markers on a timeline | small `ellipse()` (10–20px) | Visual anchor, not container |
| Start, trigger, input | `ellipse()` | Soft, origin-like |
| End, output, result | `ellipse()` | Completion, destination |
| Decision, condition | `diamond()` | Classic decision symbol |
| Process, action, step | `rect()` / `labeled_rect()` | Contained action |
| Hierarchy node | lines + text, no boxes | Structure through lines |

### Color as Meaning

Pull every color from `references/ramboll-theme.json`'s `palette` — see `references/ramboll_guidance.md`'s "Suggested semantic mapping" for which palette color means what (pale cyan for inputs, forest for secondary derivations, ocean for emphasis, and so on). Don't invent new colors or use raw Excalidraw defaults.

### Modern Aesthetics

- `roughness: 0` (already the `elements.py` default) — clean, crisp edges.
- `strokeWidth: 1` for lines/dividers, `2` for shapes and primary arrows (both are `elements.py` defaults), `3` sparingly for emphasis.
- `opacity: 100` always (already the default) — use color/size/stroke width for hierarchy, not transparency.

### Layout Principles

- **Hierarchy through scale**: Hero 300×150, Primary 180×90, Secondary 120×60, Small 60×40.
- **Whitespace = importance**: the most important element gets the most empty space around it (200px+).
- **Flow direction**: left→right or top→bottom for sequences, radial for hub-and-spoke.
- **Connections required**: if A relates to B, there must be an `arrow()` — position alone doesn't show relationships.

---

## Render & Validate (MANDATORY)

You cannot judge a diagram from JSON alone. After building or editing the diagram, you MUST render it to PNG, view the image, and fix what you see — in a loop until it's right.

### First-Time Setup

```bash
cd .claude/skills/diagram-excalidraw/scripts
uv sync
uv run playwright install chromium
```

### How to Render

```bash
cd .claude/skills/diagram-excalidraw/scripts
uv run python render.py <path-to-file.excalidraw>
```

This outputs a PNG next to the `.excalidraw` file. Then use the **Read tool** on the PNG to actually view it — reading the JSON is not a substitute.

If the diagram mixes hand-authored colors with brand colors, or you're unsure everything is on-brand, run `uv run python apply_theme.py <file.excalidraw> --theme ../references/ramboll-theme.json` before rendering — diagrams built entirely with `elements.py` using palette hex values don't need this step.

### The Loop

1. **Render & View.**
2. **Audit against your original vision** — does the visual structure match what you planned? Does each section use its intended pattern? Does the eye flow in the intended order?
3. **Check for visual defects**: clipped/overflowing text, overlapping elements, arrows crossing through shapes or landing in empty space, ambiguous label placement, uneven spacing, unbalanced composition.
4. **Fix** — edit the Python that builds the elements (never the raw JSON) and rebuild.
5. **Re-render & re-view.**
6. **Repeat** until the diagram passes both the vision check and the defect check. Typically 2–4 iterations — don't stop after one pass just because there's no critical bug.

---

## Quality Checklist

1. Research done (technical diagrams): actual specs, formats, event names looked up?
2. Evidence artifacts present (technical diagrams): code snippets, JSON examples, real data?
3. Multi-zoom: summary flow + section boundaries + detail?
4. Isomorphism: does each visual structure mirror its concept's behavior?
5. Variety: does each major concept use a different visual pattern?
6. Container discipline: <30% of text elements inside containers?
7. Every relationship has an `arrow()` — none implied by position alone.
8. Built entirely via `elements.py` — no hand-written element JSON.
9. Colors come from `references/ramboll-theme.json` — none invented.
10. Rendered to PNG and visually inspected — not just JSON-reviewed.
11. No text overflow, no unintended overlaps, arrows land on the right elements.
12. Balanced composition — no large empty voids or overcrowded regions.
