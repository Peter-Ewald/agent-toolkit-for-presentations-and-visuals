"""Shared pytest fixtures and import setup.

None of `.claude/skills/diagram-excalidraw/scripts/`, `presentations/marp/tools/`, or
`docs/brand/` is an installed package — all are loose scripts imported via `sys.path`, the same
throwaway-import pattern `SKILL.md` documents for `elements.py`. Adding all three directories
here once means every test file can `import elements`, `import apply_theme`, `import render`,
`import create_default_ramboll_slide_deck`, `import apply_default_ramboll_theme_to_slide_deck`,
and `import sync_to_consumers` directly.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCALIDRAW_SCRIPTS = REPO_ROOT / ".claude" / "skills" / "diagram-excalidraw" / "scripts"
MARP_TOOLS = REPO_ROOT / "presentations" / "marp" / "tools"
BRAND_DIR = REPO_ROOT / "docs" / "brand"

sys.path.insert(0, str(EXCALIDRAW_SCRIPTS))
sys.path.insert(0, str(MARP_TOOLS))
sys.path.insert(0, str(BRAND_DIR))
