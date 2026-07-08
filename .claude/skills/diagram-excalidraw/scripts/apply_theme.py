"""Apply a shared theme JSON to an Excalidraw scene file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _replace_color(value: str | None, color_map: dict[str, str]) -> str | None:
    """Replace a known color while preserving values that are not mapped."""

    if value is None:
        return None

    replacement = color_map.get(value.lower())
    if replacement is None:
        return value

    return replacement


def apply_theme(scene: dict, theme: dict) -> dict:
    """Return a themed copy of the scene using the shared theme metadata."""

    color_map = {
        key.lower(): value
        for key, value in theme.get("colorMap", {}).items()
    }
    text_defaults = theme.get("text", {})
    fonts = theme.get("fonts", {})

    scene.setdefault("appState", {})
    canvas = theme.get("canvas", {})
    view_background_color = canvas.get("viewBackgroundColor")
    if view_background_color:
        scene["appState"]["viewBackgroundColor"] = view_background_color

    for element in scene.get("elements", []):
        stroke_color = element.get("strokeColor")
        background_color = element.get("backgroundColor")

        themed_stroke_color = _replace_color(stroke_color, color_map)
        themed_background_color = _replace_color(background_color, color_map)
        if themed_stroke_color is not None:
            element["strokeColor"] = themed_stroke_color
        if themed_background_color is not None:
            element["backgroundColor"] = themed_background_color

        if element.get("type") == "text":
            container_id = element.get("containerId") or ""
            element["fontFamily"] = fonts.get("editorFontFamily", element.get("fontFamily", 2))
            element["strokeColor"] = text_defaults.get(
                "defaultStrokeColor",
                element.get("strokeColor", "#273943"),
            )
            if container_id.startswith("arrow-"):
                element["backgroundColor"] = text_defaults.get(
                    "labelBackgroundColor",
                    element.get("backgroundColor", "#ffffff"),
                )

    return scene


def main() -> None:
    """Load the scene and theme, apply the shared styling, and write the result."""

    parser = argparse.ArgumentParser(description="Apply a shared Excalidraw theme")
    parser.add_argument("input", type=Path, help="Path to a .excalidraw file")
    parser.add_argument("--theme", required=True, type=Path, help="Path to a theme JSON file")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path. Defaults to overwriting the input file.",
    )
    arguments = parser.parse_args()

    if not arguments.input.exists():
        print(f"ERROR: File not found: {arguments.input}", file=sys.stderr)
        sys.exit(1)
    if not arguments.theme.exists():
        print(f"ERROR: Theme file not found: {arguments.theme}", file=sys.stderr)
        sys.exit(1)

    scene = json.loads(arguments.input.read_text(encoding="utf-8"))
    theme = json.loads(arguments.theme.read_text(encoding="utf-8"))
    themed_scene = apply_theme(scene=scene, theme=theme)

    output_path = arguments.output or arguments.input
    output_path.write_text(json.dumps(themed_scene, indent=2) + "\n", encoding="utf-8")
    print(str(output_path))


if __name__ == "__main__":
    main()