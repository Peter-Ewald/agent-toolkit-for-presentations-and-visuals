"""Integration test for the real Playwright/Chromium render pipeline.

Not a pixel diff — just proves the pipeline produces a real image, which is the failure mode this
session actually hit (a broken environment silently produces nothing, or `render.py` crashes).
"""
from pathlib import Path

from render import render

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_PATH = (
    REPO_ROOT / ".claude" / "skills" / "diagram-excalidraw" / "examples" / "standard_deck_split.excalidraw"
)


def test_render_produces_a_nonzero_size_png(tmp_path):
    output_path = tmp_path / "out.png"

    result = render(EXAMPLE_PATH, output_path=output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0
