"""Integration tests for the Marp deck bootstrap/theme-apply scripts.

Real file I/O against `tmp_path`, using the real shared theme and `docs/brand/fonts/` as sources
(both scripts resolve font/logo paths relative to the real `theme_path` argument, so passing the
real theme file is what makes asset copying resolve correctly — no repo files are written to,
only read).
"""
import shutil
from pathlib import Path

import pytest
from apply_default_ramboll_theme_to_slide_deck import apply_default_ramboll_theme_to_slide_deck
from create_default_ramboll_slide_deck import create_default_ramboll_slide_deck

REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_THEME_PATH = REPO_ROOT / "presentations" / "marp" / "themes" / "ramboll.css"
REAL_TEMPLATE_PATH = REPO_ROOT / "presentations" / "marp" / "templates" / "ramboll_default.md"


def test_creates_a_deck_with_theme_and_assets_inlined(tmp_path):
    target = tmp_path / "deck.md"

    result = create_default_ramboll_slide_deck(target_deck_path=target)

    assert result == target
    text = target.read_text()
    assert "marp: true" in text
    assert "style: |" in text
    assert (tmp_path / "assets" / "example_split.png").exists()
    assert (tmp_path / "assets" / "example_full.png").exists()
    assert (tmp_path / "assets" / "ramboll-logo.png").exists()
    assert (tmp_path / "assets" / "fonts" / "NunitoCustom-Regular.ttf").exists()


def test_refuses_to_overwrite_an_existing_deck_without_force(tmp_path):
    target = tmp_path / "deck.md"
    target.write_text("existing content")

    with pytest.raises(FileExistsError):
        create_default_ramboll_slide_deck(target_deck_path=target)


def test_overwrites_an_existing_deck_when_forced(tmp_path):
    target = tmp_path / "deck.md"
    target.write_text("existing content")

    result = create_default_ramboll_slide_deck(target_deck_path=target, overwrite=True)

    assert "marp: true" in result.read_text()


def test_apply_theme_inlines_css_and_replaces_asset_placeholders(tmp_path):
    deck_path = tmp_path / "deck.md"
    shutil.copy2(REAL_TEMPLATE_PATH, deck_path)

    apply_default_ramboll_theme_to_slide_deck(deck_path=deck_path, theme_path=REAL_THEME_PATH)

    text = deck_path.read_text()
    assert "__RAMBOLL_LOGO_URL__" not in text
    assert "__RAMBOLL_FONT_REGULAR_URL__" not in text
    assert "style: |" in text
    assert (tmp_path / "assets" / "ramboll-logo.png").exists()


def test_apply_theme_raises_on_missing_deck(tmp_path):
    with pytest.raises(FileNotFoundError):
        apply_default_ramboll_theme_to_slide_deck(
            deck_path=tmp_path / "does-not-exist.md", theme_path=REAL_THEME_PATH,
        )
