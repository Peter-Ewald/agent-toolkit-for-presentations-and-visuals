"""Integration test for the .claude/hooks/validate_excalidraw_bindings.py PostToolUse hook.

Invoked exactly as Claude Code would invoke it: JSON event on stdin, exit code is the signal.
Codifies the pass/block/no-op matrix that was originally verified by hand for the hook's own wave.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = REPO_ROOT / ".claude" / "hooks" / "validate_excalidraw_bindings.py"
EXAMPLES_DIR = REPO_ROOT / ".claude" / "skills" / "diagram-excalidraw" / "examples"


def run_hook(tool_name: str, file_path: str) -> subprocess.CompletedProcess:
    event = json.dumps({"tool_name": tool_name, "tool_input": {"file_path": file_path}})
    return subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=event, capture_output=True, text=True, timeout=10,
    )


def test_passes_on_the_shipped_full_example():
    result = run_hook("Write", str(EXAMPLES_DIR / "standard_deck_full.excalidraw"))
    assert result.returncode == 0


def test_passes_on_the_shipped_split_example():
    result = run_hook("Edit", str(EXAMPLES_DIR / "standard_deck_split.excalidraw"))
    assert result.returncode == 0


def test_noops_on_a_non_edit_write_tool():
    result = run_hook("Read", str(EXAMPLES_DIR / "standard_deck_full.excalidraw"))
    assert result.returncode == 0


def test_noops_on_a_non_excalidraw_file(tmp_path):
    scratch = tmp_path / "notes.txt"
    scratch.write_text("hello")
    result = run_hook("Write", str(scratch))
    assert result.returncode == 0


def test_blocks_a_null_arrow_binding(tmp_path):
    scene = {
        "type": "excalidraw",
        "elements": [
            {"id": "a", "type": "rectangle", "boundElements": None, "groupIds": []},
            {"id": "b", "type": "rectangle", "boundElements": None, "groupIds": []},
            {
                "id": "arr", "type": "arrow", "boundElements": None, "groupIds": [],
                "startBinding": None,
                "endBinding": {"elementId": "b", "focus": 0, "gap": 4},
            },
        ],
        "appState": {}, "files": {},
    }
    scratch = tmp_path / "broken.excalidraw"
    scratch.write_text(json.dumps(scene))

    result = run_hook("Write", str(scratch))

    assert result.returncode == 2
    assert "startBinding is null" in result.stderr


def test_blocks_an_orphaned_group_id(tmp_path):
    scene = {
        "type": "excalidraw",
        "elements": [{"id": "a", "type": "rectangle", "boundElements": None, "groupIds": ["lonely"]}],
        "appState": {}, "files": {},
    }
    scratch = tmp_path / "orphan_group.excalidraw"
    scratch.write_text(json.dumps(scene))

    result = run_hook("Write", str(scratch))

    assert result.returncode == 2
    assert "lonely" in result.stderr


def test_blocks_invalid_json(tmp_path):
    scratch = tmp_path / "invalid.excalidraw"
    scratch.write_text("{ this is not json")

    result = run_hook("Write", str(scratch))

    assert result.returncode == 2
    assert "not valid JSON" in result.stderr
