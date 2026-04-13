"""Apply the shared Ramboll Marp theme to one or more slide decks.

This keeps a single theme source of truth while avoiding reliance on Marp's
workspace theme registration behavior in complex multi-root workspaces.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

LOGO_FILE_NAME = "ramboll-logo.png"
LOGO_PLACEHOLDER = "__RAMBOLL_LOGO_URL__"


def _resolve_deck_path_for_workspace(target_path: Path) -> Path:
    """Resolve a deck path against the repo or a sibling workspace folder.

    When the user passes a relative path from a multi-root workspace launch
    configuration, they may intend a sibling repository such as
    `origami_ai_wiki/...` rather than a path inside the current repository.
    This helper keeps normal repo-relative behavior, but if the first path
    segment does not exist in the current repository and does exist beside it,
    the path is resolved against the parent directory instead.
    """

    if target_path.is_absolute():
        return target_path

    current_working_directory_path = Path.cwd()
    repo_relative_candidate_path = current_working_directory_path / target_path

    if not target_path.parts:
        return repo_relative_candidate_path

    sibling_root_name = target_path.parts[0]
    sibling_workspace_candidate_path = (
        current_working_directory_path.parent / sibling_root_name
    )
    repo_relative_root_path = current_working_directory_path / sibling_root_name

    if not repo_relative_root_path.exists() and sibling_workspace_candidate_path.exists():
        return current_working_directory_path.parent / target_path

    return repo_relative_candidate_path


def _copy_logo_asset(theme_path: Path, deck_path: Path) -> Path:
    """Copy the shared Ramboll logo into the deck-local assets folder.

    Each deck gets its own relative logo asset so the generated inline CSS is
    portable and does not depend on an absolute machine-specific path.
    """

    logo_source_path = theme_path.parent.parent / "templates" / "Ramboll Logo.png"
    if not logo_source_path.exists():
        raise FileNotFoundError(f"Logo not found: {logo_source_path}")

    assets_directory_path = deck_path.parent / "assets"
    assets_directory_path.mkdir(parents=True, exist_ok=True)
    logo_target_path = assets_directory_path / LOGO_FILE_NAME
    shutil.copy2(logo_source_path, logo_target_path)
    return logo_target_path


def _load_inline_css(theme_path: Path) -> str:
    """Load theme CSS and strip theme-registration directives for inline use.

    The inline frontmatter style block should contain plain CSS rules only.
    Marp theme registration directives such as `@theme` and `@import 'default'`
    belong in standalone theme files and are removed here.
    """

    theme_text = theme_path.read_text(encoding="utf-8")
    filtered_lines: list[str] = []

    for line in theme_text.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith("/* @theme"):
            continue
        if stripped_line == "@import 'default';":
            continue
        filtered_lines.append(line)

    return "\n".join(filtered_lines).strip() + "\n"


def _prepare_inline_css(theme_path: Path, deck_path: Path) -> str:
    """Load the shared CSS and replace deck-specific asset placeholders.

    This keeps the theme file generic while making the generated deck fully
    self-contained relative to its own folder structure.
    """

    inline_css = _load_inline_css(theme_path=theme_path)
    logo_target_path = _copy_logo_asset(theme_path=theme_path, deck_path=deck_path)
    relative_logo_path = logo_target_path.relative_to(deck_path.parent).as_posix()
    return inline_css.replace(LOGO_PLACEHOLDER, relative_logo_path)


def _replace_frontmatter(deck_text: str, inline_css: str) -> str:
    """Replace Marp frontmatter with a version that inlines the shared CSS.

    The function preserves the rest of the Markdown document and standardizes the
    frontmatter to use the built-in default theme plus a `style` block.
    """

    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", deck_text, re.DOTALL)
    if frontmatter_match is None:
        raise ValueError("Deck does not start with YAML frontmatter.")

    frontmatter_text = frontmatter_match.group(1)
    frontmatter_lines = frontmatter_text.splitlines()
    kept_lines: list[str] = []

    skipping_style_block = False
    for line in frontmatter_lines:
        stripped_line = line.strip()

        if skipping_style_block:
            if line.startswith(" ") or line.startswith("\t") or stripped_line == "":
                continue
            skipping_style_block = False

        if stripped_line.startswith("style:"):
            skipping_style_block = True
            continue

        if stripped_line.startswith("theme:"):
            kept_lines.append("theme: default")
            continue

        kept_lines.append(line)

    inline_block_lines = ["style: |"]
    inline_block_lines.extend(f"  {line}" if line else "" for line in inline_css.splitlines())

    new_frontmatter = "---\n" + "\n".join(kept_lines + inline_block_lines) + "\n---\n"
    return new_frontmatter + deck_text[frontmatter_match.end():]


def apply_default_ramboll_theme_to_slide_deck(
    deck_path: Path,
    theme_path: Path,
) -> None:
    """Rewrite a deck file so it inlines the shared theme CSS.

    This creates deterministic Marp preview behavior in environments where
    external custom theme registration is unreliable.
    """

    resolved_deck_path = _resolve_deck_path_for_workspace(target_path=deck_path)

    if not resolved_deck_path.exists():
        raise FileNotFoundError(f"Deck not found: {deck_path}")
    if not theme_path.exists():
        raise FileNotFoundError(f"Theme not found: {theme_path}")

    inline_css = _prepare_inline_css(theme_path=theme_path, deck_path=resolved_deck_path)
    original_text = resolved_deck_path.read_text(encoding="utf-8")
    updated_text = _replace_frontmatter(deck_text=original_text, inline_css=inline_css)
    resolved_deck_path.write_text(updated_text, encoding="utf-8")


def main() -> None:
    """Parse CLI arguments and sync the requested decks.

    The same shared theme file can be applied to multiple deck files in one run,
    which keeps generated deck frontmatter consistent across the workspace.
    """

    parser = argparse.ArgumentParser(description="Inline a shared Marp theme into decks")
    parser.add_argument("theme", type=Path, help="Path to the shared Marp theme CSS file")
    parser.add_argument("decks", nargs="+", type=Path, help="One or more Marp deck files")
    arguments = parser.parse_args()

    try:
        for deck_path in arguments.decks:
            apply_default_ramboll_theme_to_slide_deck(
                deck_path=deck_path,
                theme_path=arguments.theme,
            )
            print(str(_resolve_deck_path_for_workspace(target_path=deck_path)))
    except (FileNotFoundError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()