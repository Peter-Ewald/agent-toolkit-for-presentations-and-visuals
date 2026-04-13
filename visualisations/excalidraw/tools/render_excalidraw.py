"""Render Excalidraw JSON to PNG using Playwright and headless Chromium."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate_excalidraw(data: dict) -> list[str]:
    """Validate the top-level structure before attempting a render."""

    errors: list[str] = []

    if data.get("type") != "excalidraw":
        errors.append(f"Expected type 'excalidraw', got '{data.get('type')}'")

    elements = data.get("elements")
    if elements is None:
        errors.append("Missing 'elements' array")
    elif not isinstance(elements, list):
        errors.append("'elements' must be an array")
    elif not elements:
        errors.append("'elements' array is empty")

    return errors


def compute_bounding_box(elements: list[dict]) -> tuple[float, float, float, float]:
    """Compute the rendered bounds across all visible elements."""

    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    for element in elements:
        if element.get("isDeleted"):
            continue

        x = element.get("x", 0)
        y = element.get("y", 0)
        width = element.get("width", 0)
        height = element.get("height", 0)

        if element.get("type") in {"arrow", "line"} and "points" in element:
            for point_x, point_y in element["points"]:
                min_x = min(min_x, x + point_x)
                min_y = min(min_y, y + point_y)
                max_x = max(max_x, x + point_x)
                max_y = max(max_y, y + point_y)
        else:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + abs(width))
            max_y = max(max_y, y + abs(height))

    if min_x == float("inf"):
        return (0, 0, 800, 600)

    return (min_x, min_y, max_x, max_y)


def render(
    excalidraw_path: Path,
    output_path: Path | None = None,
    scale: int = 2,
    max_width: int = 1920,
) -> Path:
    """Render a single Excalidraw scene into a PNG file."""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright is not installed.", file=sys.stderr)
        print(
            "Run: uv sync && uv run playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        data = json.loads(excalidraw_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"ERROR: Invalid JSON in {excalidraw_path}: {error}", file=sys.stderr)
        sys.exit(1)

    errors = validate_excalidraw(data)
    if errors:
        print("ERROR: Invalid Excalidraw file:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    elements = [element for element in data["elements"] if not element.get("isDeleted")]
    min_x, min_y, max_x, max_y = compute_bounding_box(elements)
    padding = 80
    diagram_width = max_x - min_x + padding * 2
    diagram_height = max_y - min_y + padding * 2
    viewport_width = min(int(diagram_width), max_width)
    viewport_height = max(int(diagram_height), 600)

    final_output_path = output_path or excalidraw_path.with_suffix(".png")
    template_path = Path(__file__).with_name("render_template.html")
    template_url = template_path.as_uri()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": viewport_width, "height": viewport_height},
            device_scale_factor=scale,
        )
        page.goto(template_url)
        page.wait_for_function("window.__moduleReady === true", timeout=30000)

        result = page.evaluate(f"window.renderDiagram({json.dumps(data)})")
        if not result or not result.get("success"):
            error_message = result.get("error", "Unknown render error") if result else "renderDiagram returned null"
            print(f"ERROR: Render failed: {error_message}", file=sys.stderr)
            browser.close()
            sys.exit(1)

        page.wait_for_function("window.__renderComplete === true", timeout=15000)
        svg_element = page.query_selector("#root svg")
        if svg_element is None:
            print("ERROR: No SVG element found after render.", file=sys.stderr)
            browser.close()
            sys.exit(1)

        svg_element.screenshot(path=str(final_output_path))
        browser.close()

    return final_output_path


def main() -> None:
    """Parse CLI arguments and render the requested diagram."""

    parser = argparse.ArgumentParser(description="Render Excalidraw JSON to PNG")
    parser.add_argument("input", type=Path, help="Path to a .excalidraw file")
    parser.add_argument("--output", "-o", type=Path, default=None)
    parser.add_argument("--scale", "-s", type=int, default=2)
    parser.add_argument("--width", "-w", type=int, default=1920)
    arguments = parser.parse_args()

    if not arguments.input.exists():
        print(f"ERROR: File not found: {arguments.input}", file=sys.stderr)
        sys.exit(1)

    png_path = render(
        excalidraw_path=arguments.input,
        output_path=arguments.output,
        scale=arguments.scale,
        max_width=arguments.width,
    )
    print(str(png_path))


if __name__ == "__main__":
    main()