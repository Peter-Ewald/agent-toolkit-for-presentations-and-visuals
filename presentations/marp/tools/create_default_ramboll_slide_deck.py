"""Create a new slide deck from the shared Ramboll default template.

The generated deck gets the template Markdown, example assets, and an inlined
copy of the shared Ramboll theme so it previews consistently in multi-root
workspaces.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from apply_default_ramboll_theme_to_slide_deck import (
    _resolve_deck_path_for_workspace,
    apply_default_ramboll_theme_to_slide_deck,
)

EXAMPLE_ASSET_FILE_NAMES = ("example_split.png", "example_full.png")


def _template_directory() -> Path:
    """Return the directory containing the shared Marp template files.

    The script lives alongside the theme sync helper, so the template and asset
    paths are resolved relative to this tools directory to keep the workflow
    portable across repositories.
    """

    return Path(__file__).resolve().parent.parent / "templates"


def _copy_example_assets(target_assets_directory_path: Path) -> None:
    """Copy the shared placeholder graphics into the new deck's assets folder.

    The standard template references these files directly, so the bootstrap step
    copies them beside the new deck to keep the result immediately previewable.
    """

    template_assets_directory_path = _template_directory() / "assets"
    target_assets_directory_path.mkdir(parents=True, exist_ok=True)

    for asset_file_name in EXAMPLE_ASSET_FILE_NAMES:
        source_path = template_assets_directory_path / asset_file_name
        target_path = target_assets_directory_path / asset_file_name
        if not source_path.exists():
            raise FileNotFoundError(f"Example asset not found: {source_path}")
        shutil.copy2(source_path, target_path)


def create_default_ramboll_slide_deck(
    target_deck_path: Path,
    overwrite: bool = False,
) -> Path:  # noqa: FBT001
    """Create a new deck file from the shared Ramboll default template.

    The function copies the template Markdown, copies the example assets used by
    the split and full-image slides, and then regenerates the inline CSS so the
    new deck points at its own local assets folder.
    """

    template_directory_path = _template_directory()
    template_deck_path = template_directory_path / "ramboll_default.md"
    theme_path = (
        Path(__file__).resolve().parent
        / "apply_default_ramboll_theme_to_slide_deck.py"
    )
    shared_theme_path = Path(__file__).resolve().parent.parent / "themes" / "ramboll.css"

    resolved_target_deck_path = _resolve_deck_path_for_workspace(
        target_path=target_deck_path,
    )

    if not template_deck_path.exists():
        raise FileNotFoundError(f"Template deck not found: {template_deck_path}")
    if not shared_theme_path.exists():
        raise FileNotFoundError(f"Shared theme not found: {shared_theme_path}")
    if not theme_path.exists():
        raise FileNotFoundError(f"Theme sync helper not found: {theme_path}")
    if resolved_target_deck_path.exists() and not overwrite:
        raise FileExistsError(f"Target deck already exists: {resolved_target_deck_path}")

    resolved_target_deck_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(template_deck_path, resolved_target_deck_path)
    _copy_example_assets(
        target_assets_directory_path=resolved_target_deck_path.parent / "assets"
    )
    apply_default_ramboll_theme_to_slide_deck(
        deck_path=resolved_target_deck_path,
        theme_path=shared_theme_path,
    )
    return resolved_target_deck_path


def main() -> None:
    """Parse command-line arguments and create the requested deck.

    The CLI exposes a minimal interface so it can be used directly from VS Code
    tasks and launch configurations with an optional overwrite flag.
    """

    parser = argparse.ArgumentParser(
        description="Create a slide deck from the shared Ramboll default template"
    )
    parser.add_argument("target", type=Path, help="Path to the new deck Markdown file")
    parser.add_argument("--force", action="store_true", help="Overwrite the target file if it already exists")
    arguments = parser.parse_args()

    try:
        created_deck_path = create_default_ramboll_slide_deck(
            target_deck_path=arguments.target,
            overwrite=arguments.force,
        )
    except (FileExistsError, FileNotFoundError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print(str(created_deck_path))


if __name__ == "__main__":
    main()