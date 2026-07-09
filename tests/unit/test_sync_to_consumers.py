"""Unit tests for the brand color sync script's parsing/palette-building logic.

Only the pure, parameterized functions (`parse_scss_colors`, `build_palette`, `resolve`) are
tested here. The three `write_*` functions write to hardcoded real repo paths with no
parameterization — testing them would mutate real theme files as a side effect of running the
suite, so that's deliberately out of scope (see `tests/README.md`).
"""
from pathlib import Path

from sync_to_consumers import build_palette, parse_scss_colors, resolve

REPO_ROOT = Path(__file__).resolve().parents[2]
COLORS_SCSS_PATH = REPO_ROOT / "docs" / "brand" / "colours" / "colors.scss"


def test_parse_scss_colors_reads_the_real_brand_source():
    colors = parse_scss_colors(COLORS_SCSS_PATH)
    assert colors["cyan"] == "#0098eb"


def test_build_palette_resolves_every_required_key_without_error():
    colors = parse_scss_colors(COLORS_SCSS_PATH)
    palette = build_palette(colors)

    assert palette["cyan"] == "#0098eb"
    assert palette["text"] == "#333333"  # fixed neutral, not derived from colors.scss
    assert palette["divider"] == "#b1b2b3"


def test_resolve_looks_up_a_known_palette_key():
    palette = {"cyan": "#0098eb"}
    assert resolve("cyan", palette) == "#0098eb"


def test_resolve_passes_through_an_unknown_value_unchanged():
    palette = {"cyan": "#0098eb"}
    assert resolve("#123456", palette) == "#123456"
