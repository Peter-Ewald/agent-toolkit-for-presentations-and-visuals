"""Build Excalidraw elements with correct native bindings and grouping.

Hand-crafted Excalidraw JSON in this repo has reliably ended up with empty
`groupIds`, null `boundElements`, and null `startBinding`/`endBinding` — every
element in this skill's own example diagrams had none of these set correctly
before this module existed (see `../references/ramboll_guidance.md` for the
history). Use these functions instead of writing element dicts by hand; each
one either fills in bindings itself or mutates its arguments the way
Excalidraw's own editor would, so a diagram built entirely from this module
is guaranteed structurally valid.

Typical usage:

    from elements import rect, labeled_rect, arrow, group, scene
    import json

    box_a, label_a = labeled_rect("input", 100, 100, 180, 90, "Input", stroke=OCEAN)
    box_b, label_b = labeled_rect("output", 420, 100, 180, 90, "Output", stroke=OCEAN)
    connector = arrow("flow", box_a, box_b, stroke=DIVIDER)

    Path("diagram.excalidraw").write_text(
        json.dumps(scene([box_a, label_a, box_b, label_b, connector]), indent=2)
    )

Colors: pull hex values from `../references/ramboll-theme.json`'s `palette`
(don't hand-type hex codes here — see that file's own maintenance note).
"""

from __future__ import annotations

import zlib
from typing import Literal

FONT_FAMILY = 2  # "Normal" — matches ramboll-theme.json's editorFontFamily.
                  # The renderer overrides the exported font to NunitoCustom
                  # regardless of this id (see scripts/render_template.html).


def _seed(id_: str, salt: str = "") -> int:
    """Deterministic pseudo-random int, so rebuilding a diagram from the same
    IDs produces a byte-identical file (clean diffs when a script regenerates
    a diagram after a content change)."""

    return zlib.crc32(f"{id_}{salt}".encode()) % 100_000


def _base(id_: str, type_: str, x: float, y: float, width: float, height: float,
          stroke: str, fill: str = "transparent") -> dict:
    return {
        "id": id_,
        "type": type_,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "strokeColor": stroke,
        "backgroundColor": fill,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": _seed(id_),
        "version": 1,
        "versionNonce": _seed(id_, salt="version"),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": None,
        "link": None,
        "locked": False,
    }


def rect(id_: str, x: float, y: float, width: float, height: float,
         stroke: str, fill: str = "transparent", rounded: bool = True) -> dict:
    """A rectangle. Pass the result to `text(..., container=...)` to add a
    centered label, or to `arrow(...)` as a start/end endpoint — or use
    `labeled_rect()` to get a rectangle and its bound label in one call."""

    element = _base(id_, "rectangle", x, y, width, height, stroke, fill)
    if rounded:
        element["roundness"] = {"type": 3}
    return element


def diamond(id_: str, x: float, y: float, width: float, height: float,
            stroke: str, fill: str = "transparent") -> dict:
    """A diamond — conventionally used for decisions/conditions."""

    return _base(id_, "diamond", x, y, width, height, stroke, fill)


def ellipse(id_: str, x: float, y: float, width: float, height: float,
            stroke: str, fill: str = "transparent") -> dict:
    """An ellipse — conventionally used for entry/exit points or markers."""

    return _base(id_, "ellipse", x, y, width, height, stroke, fill)


def text(id_: str, value: str, x: float, y: float, width: float, height: float,
         stroke: str, font_size: int = 16,
         text_align: Literal["left", "center", "right"] = "center",
         vertical_align: Literal["top", "middle", "bottom"] = "middle",
         container: dict | None = None) -> dict:
    """Free-floating text, or a label bound inside `container` (a shape dict
    from `rect()`/`diamond()`/`ellipse()`).

    Passing `container` sets this element's `containerId` AND appends the
    reciprocal `{"id": ..., "type": "text"}` entry to the container's
    `boundElements` — the pairing Excalidraw's own editor creates when you
    double-click a shape to add a label.
    """

    element = {
        "id": id_,
        "type": "text",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "text": value,
        "originalText": value,
        "fontSize": font_size,
        "fontFamily": FONT_FAMILY,
        "textAlign": text_align,
        "verticalAlign": vertical_align,
        "strokeColor": stroke,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": _seed(id_),
        "version": 1,
        "versionNonce": _seed(id_, salt="version"),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": None,
        "link": None,
        "locked": False,
        "containerId": container["id"] if container is not None else None,
        "lineHeight": 1.25,
    }

    if container is not None:
        if container["boundElements"] is None:
            container["boundElements"] = []
        container["boundElements"].append({"id": id_, "type": "text"})

    return element


def labeled_rect(id_: str, x: float, y: float, width: float, height: float,
                  label: str, stroke: str, fill: str = "transparent",
                  font_size: int = 16, rounded: bool = True) -> tuple[dict, dict]:
    """A rectangle with a centered, bound text label. Returns `(rect, text)` —
    include both in the scene's element list."""

    box = rect(id_, x, y, width, height, stroke, fill, rounded=rounded)
    label_element = text(
        f"{id_}_label", label,
        x=x + 8, y=y + height / 2 - font_size * 0.75,
        width=width - 16, height=font_size * 1.5,
        stroke=stroke, font_size=font_size, container=box,
    )
    return box, label_element


def _edge_point(shape: dict, towards: tuple[float, float]) -> tuple[float, float]:
    """Where the line from `shape`'s center toward `towards` crosses its
    boundary. Exact for rectangles; a reasonable approximation for ellipses
    and diamonds."""

    center_x = shape["x"] + shape["width"] / 2
    center_y = shape["y"] + shape["height"] / 2
    delta_x = towards[0] - center_x
    delta_y = towards[1] - center_y

    if delta_x == 0 and delta_y == 0:
        return (center_x, center_y)

    scale_candidates = []
    if delta_x != 0:
        scale_candidates.append((shape["width"] / 2) / abs(delta_x))
    if delta_y != 0:
        scale_candidates.append((shape["height"] / 2) / abs(delta_y))
    scale = min(scale_candidates)

    return (center_x + delta_x * scale, center_y + delta_y * scale)


def arrow(id_: str, start: dict, end: dict, stroke: str,
          start_arrowhead: str | None = None,
          end_arrowhead: str | None = "arrow",
          waypoints: list[tuple[float, float]] | None = None) -> dict:
    """An arrow bound at both ends to `start` and `end` (shape dicts from
    `rect()`/`diamond()`/`ellipse()`).

    By default, draws a straight line between the two shapes' facing edges
    (matching what dragging an arrow between two shapes produces in the
    Excalidraw editor). Pass `waypoints` (a list of absolute `(x, y)` points,
    first and last still touching each shape) to route around other elements
    instead.

    Sets this arrow's `startBinding`/`endBinding` AND appends the reciprocal
    `{"id": ..., "type": "arrow"}` entry to both endpoints' `boundElements` —
    the link Excalidraw needs to treat the connection as live, so moving
    either shape drags the arrow with it.
    """

    start_center = (start["x"] + start["width"] / 2, start["y"] + start["height"] / 2)
    end_center = (end["x"] + end["width"] / 2, end["y"] + end["height"] / 2)

    if waypoints is None:
        waypoints = [_edge_point(start, end_center), _edge_point(end, start_center)]

    origin = waypoints[0]
    relative_points = [(px - origin[0], py - origin[1]) for px, py in waypoints]
    xs = [p[0] for p in relative_points]
    ys = [p[1] for p in relative_points]

    element = {
        "id": id_,
        "type": "arrow",
        "x": origin[0],
        "y": origin[1],
        "width": max(xs) - min(xs),
        "height": max(ys) - min(ys),
        "strokeColor": stroke,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "angle": 0,
        "seed": _seed(id_),
        "version": 1,
        "versionNonce": _seed(id_, salt="version"),
        "isDeleted": False,
        "groupIds": [],
        "boundElements": None,
        "link": None,
        "locked": False,
        "points": [list(p) for p in relative_points],
        "startBinding": {"elementId": start["id"], "focus": 0, "gap": 4},
        "endBinding": {"elementId": end["id"], "focus": 0, "gap": 4},
        "startArrowhead": start_arrowhead,
        "endArrowhead": end_arrowhead,
    }

    for endpoint in (start, end):
        if endpoint["boundElements"] is None:
            endpoint["boundElements"] = []
        endpoint["boundElements"].append({"id": id_, "type": "arrow"})

    return element


def group(*elements: dict, group_id: str) -> None:
    """Make `elements` move together by appending a shared group id.

    Use this for elements that should travel as one unit but are *not* a
    shape+bound-label pair (which already moves together via `containerId`/
    `boundElements`) — e.g. a shape plus a free-floating caption beside it,
    or several shapes that form one logical section.
    """

    for element in elements:
        element["groupIds"] = [*element["groupIds"], group_id]


def scene(elements: list[dict], background: str = "#ffffff") -> dict:
    """Wrap a flat element list in the top-level Excalidraw file structure."""

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"viewBackgroundColor": background, "gridSize": 20},
        "files": {},
    }


def _check_bindings(elements: list[dict]) -> list[str]:
    """Self-test helper: every arrow binding is mutual, every bound text has
    a real container. Not a replacement for the standalone validation hook
    planned for `.claude/hooks/` — just enough to prove this module's own
    output is correct."""

    by_id = {element["id"]: element for element in elements}
    problems = []

    for element in elements:
        if element["type"] == "arrow":
            for side in ("startBinding", "endBinding"):
                binding = element.get(side)
                if binding is None:
                    problems.append(f"{element['id']}.{side} is null")
                    continue
                target = by_id.get(binding["elementId"])
                if target is None:
                    problems.append(f"{element['id']}.{side} points at a missing element")
                    continue
                back_refs = target.get("boundElements") or []
                if not any(ref["id"] == element["id"] for ref in back_refs):
                    problems.append(
                        f"{binding['elementId']} is missing a reciprocal boundElements "
                        f"entry for arrow {element['id']}"
                    )

        if element["type"] == "text" and element.get("containerId"):
            container = by_id.get(element["containerId"])
            if container is None:
                problems.append(f"{element['id']}.containerId points at a missing element")
                continue
            back_refs = container.get("boundElements") or []
            if not any(ref["id"] == element["id"] for ref in back_refs):
                problems.append(
                    f"{element['containerId']} is missing a reciprocal boundElements "
                    f"entry for text {element['id']}"
                )

    return problems


if __name__ == "__main__":
    import json
    import sys
    from pathlib import Path

    box_a, label_a = labeled_rect("box_a", 100, 100, 180, 90, "Input", stroke="#05326e", fill="#cceafb")
    box_b, label_b = labeled_rect("box_b", 420, 100, 180, 90, "Output", stroke="#05326e")
    connector = arrow("flow", box_a, box_b, stroke="#b1b2b3")
    caption = text("caption", "elements.py self-test", x=100, y=220, width=400, height=25,
                    stroke="#333333", text_align="left")
    group(box_b, caption, group_id="group_1")

    built_elements = [box_a, label_a, box_b, label_b, connector, caption]
    problems = _check_bindings(built_elements)
    if problems:
        print("FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("elements_self_test.excalidraw")
    output_path.write_text(json.dumps(scene(built_elements), indent=2) + "\n", encoding="utf-8")
    print(f"OK: wrote {output_path}")
