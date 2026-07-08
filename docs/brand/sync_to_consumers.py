"""Project docs/brand/ color values into the Excalidraw and Marp theme consumers.

docs/brand/colours/colors.scss is the only easily machine-readable brand color
source, so it is the input here. The Excalidraw theme JSON and the Marp theme
CSS each keep their own copy of a handful of these values (JSON has no way to
reference an external file, and the Marp CSS is inlined into deck frontmatter
by presentations/marp/tools/apply_default_ramboll_theme_to_slide_deck.py) —
this script keeps those copies correct instead of hand-typing them.

Run manually whenever docs/brand/colours/colors.scss changes:

    uv run python docs/brand/sync_to_consumers.py

It is not run on a schedule or by a hook.
"""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BRAND_DIR = Path(__file__).resolve().parent
COLORS_SCSS_PATH = BRAND_DIR / "colours" / "colors.scss"
FONTS_DIR = BRAND_DIR / "fonts"
EXCALIDRAW_SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "diagram-excalidraw"
EXCALIDRAW_THEME_PATH = EXCALIDRAW_SKILL_DIR / "references" / "ramboll-theme.json"
EXCALIDRAW_RENDER_TEMPLATE_PATH = EXCALIDRAW_SKILL_DIR / "scripts" / "render_template.html"
MARP_THEME_PATH = REPO_ROOT / "presentations" / "marp" / "themes" / "ramboll.css"

# Excalidraw theme palette keys, resolved from docs/brand/colours/colors.scss tokens.
PALETTE_SOURCE = {
    "cyan": "cyan",
    "cyanSoft": "cyan-20",
    "cyanPale": "cyan-10",
    "oceanPale": "ocean-10",
    "ocean": "ocean",
    "forest": "forest",
    "heath": "heath",
    "mountain": "mountain",
    "grass": "grass",
    "grassPale": "grass-20",
    "pebble": "pebble",
    "pebblePale": "pebble-20",
    "field": "field",
    "sand": "sand",
    "white": "white",
}

# Fixed neutrals documented in visualisations/excalidraw/themes/RAMBOLL_GUIDANCE.md
# ("dark neutral text", "thin gray divider") — not brand-palette tints, so they
# are not derived from colors.scss.
FIXED_EXCALIDRAW_COLORS = {
    "text": "#333333",
    "divider": "#b1b2b3",
}

EXCALIDRAW_PALETTE_KEYS = (
    "cyan", "cyanSoft", "cyanPale", "ocean", "forest", "heath", "mountain",
    "text", "divider", "grass", "pebble", "pebblePale", "field", "sand", "white",
)

# Excalidraw's own default swatch hex -> the palette key (or fixed literal) it
# should be remapped to. This curated key set is a design decision and is not
# regenerated; only the resolved hex *values* are kept in sync with the palette.
EXCALIDRAW_COLOR_MAP_SOURCE = {
    "#0098eb": "cyan",
    "#2551b3": "ocean",
    "#dceaff": "cyanSoft",
    "#6d3ccf": "ocean",
    "#efe4ff": "white",
    "#247a3d": "forest",
    "#e7f8e9": "grassPale",
    "#d06a00": "ocean",
    "#fff0cd": "oceanPale",
    "#0c7d8f": "cyan",
    "#dff7f9": "white",
    "#b63b4b": "forest",
    "#ffe0e7": "pebblePale",
    "#3b4d73": "ocean",
    "#56657c": "text",
    "#122033": "text",
    "#273943": "text",
    "#fffdf8": "white",
    "#fcfcfb": "white",
    "#6984a8": "#6984a8",
    "#b1b2b3": "divider",
}

# Marp CSS custom properties that map directly onto the same palette. Only
# these are touched — every other `--ramboll-*` variable in the theme (e.g.
# --ramboll-ocean-80, --ramboll-muted) is an intentional, already-correct
# derived tone that isn't part of this shared palette and is left alone.
MARP_CSS_VAR_TO_PALETTE_KEY = {
    "--ramboll-cyan": "cyan",
    "--ramboll-title-blue": "cyan",
    "--ramboll-cyan-20": "cyanSoft",
    "--ramboll-cyan-10": "cyanPale",
    "--ramboll-ocean": "ocean",
    "--ramboll-forest": "forest",
    "--ramboll-heath": "heath",
    "--ramboll-mountain": "mountain",
    "--ramboll-grass": "grass",
    "--ramboll-pebble": "pebble",
    "--ramboll-pebble-20": "pebblePale",
    "--ramboll-field": "field",
    "--ramboll-sand": "sand",
}

RAMBOLL_FONT_FACE_START = "<!-- RAMBOLL_FONT_FACE_START -->"
RAMBOLL_FONT_FACE_END = "<!-- RAMBOLL_FONT_FACE_END -->"

# Marp decks copy font files locally (see _copy_font_assets in
# apply_default_ramboll_theme_to_slide_deck.py) instead of embedding them, so
# that per-deck Markdown files stay small and diffable. The Excalidraw render
# template is a single tool asset rendered transiently by Playwright, so it
# embeds the one weight Excalidraw actually uses (elements carry a font
# *family* id, not a weight/style axis) directly as a data URI — no relative
# path to keep correct if the template ever moves.
EXCALIDRAW_FONT_WEIGHT_FILE = "NunitoCustom-Regular.ttf"


def parse_scss_colors(path: Path) -> dict[str, str]:
    """Parse `$name: rgb(r, g, b);` lines into a lowercase hex dict."""

    colors: dict[str, str] = {}
    pattern = re.compile(r"^\$([\w-]+):\s*rgb\((\d+),\s*(\d+),\s*(\d+)\)")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        name, r, g, b = match.groups()
        colors[name] = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
    return colors


def build_palette(scss_colors: dict[str, str]) -> dict[str, str]:
    palette = {key: scss_colors[token] for key, token in PALETTE_SOURCE.items()}
    palette.update(FIXED_EXCALIDRAW_COLORS)
    return palette


def resolve(key_or_hex: str, palette: dict[str, str]) -> str:
    return palette.get(key_or_hex, key_or_hex)


def write_excalidraw_theme(palette: dict[str, str]) -> None:
    theme = json.loads(EXCALIDRAW_THEME_PATH.read_text(encoding="utf-8"))
    theme["palette"] = {key: palette[key] for key in EXCALIDRAW_PALETTE_KEYS}
    theme["colorMap"] = {
        swatch: resolve(target, palette)
        for swatch, target in EXCALIDRAW_COLOR_MAP_SOURCE.items()
    }
    EXCALIDRAW_THEME_PATH.write_text(json.dumps(theme, indent=2) + "\n", encoding="utf-8")


def write_marp_theme_colors(palette: dict[str, str]) -> None:
    css = MARP_THEME_PATH.read_text(encoding="utf-8")
    line_pattern = re.compile(r"^(\s*)(--ramboll-[\w-]+):\s*#[0-9a-fA-F]{6};\s*$")
    updated_lines = []
    for line in css.splitlines():
        match = line_pattern.match(line)
        if match:
            indent, prop = match.groups()
            palette_key = MARP_CSS_VAR_TO_PALETTE_KEY.get(prop)
            if palette_key is not None:
                line = f"{indent}{prop}: {palette[palette_key]};"
        updated_lines.append(line)
    MARP_THEME_PATH.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")


def write_excalidraw_font_face() -> None:
    font_path = FONTS_DIR / EXCALIDRAW_FONT_WEIGHT_FILE
    encoded = base64.b64encode(font_path.read_bytes()).decode("ascii")
    block = (
        f"{RAMBOLL_FONT_FACE_START}\n"
        "    <style>\n"
        "      @font-face {\n"
        "        font-family: \"NunitoCustom\";\n"
        f"        src: url(data:font/ttf;base64,{encoded}) format(\"truetype\");\n"
        "        font-weight: 400;\n"
        "        font-style: normal;\n"
        "      }\n"
        "    </style>\n"
        f"    {RAMBOLL_FONT_FACE_END}"
    )

    html = EXCALIDRAW_RENDER_TEMPLATE_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(RAMBOLL_FONT_FACE_START) + r".*?" + re.escape(RAMBOLL_FONT_FACE_END),
        re.DOTALL,
    )
    if not pattern.search(html):
        raise RuntimeError(
            f"{EXCALIDRAW_RENDER_TEMPLATE_PATH} is missing the "
            f"{RAMBOLL_FONT_FACE_START} ... {RAMBOLL_FONT_FACE_END} markers."
        )
    updated_html = pattern.sub(block, html, count=1)
    EXCALIDRAW_RENDER_TEMPLATE_PATH.write_text(updated_html, encoding="utf-8")


def main() -> None:
    scss_colors = parse_scss_colors(COLORS_SCSS_PATH)
    palette = build_palette(scss_colors)
    write_excalidraw_theme(palette)
    write_marp_theme_colors(palette)
    write_excalidraw_font_face()
    print(f"Synced {EXCALIDRAW_THEME_PATH.relative_to(REPO_ROOT)}")
    print(f"Synced {MARP_THEME_PATH.relative_to(REPO_ROOT)} (colors only)")
    print(f"Synced {EXCALIDRAW_RENDER_TEMPLATE_PATH.relative_to(REPO_ROOT)} (@font-face)")


if __name__ == "__main__":
    main()
