"""Unit tests for render.py's pure helper functions (no browser needed)."""
from render import compute_bounding_box, validate_excalidraw


def test_validate_excalidraw_accepts_a_valid_scene():
    data = {"type": "excalidraw", "elements": [{"type": "rectangle"}]}
    assert validate_excalidraw(data) == []


def test_validate_excalidraw_rejects_wrong_type():
    data = {"type": "not-excalidraw", "elements": [{"type": "rectangle"}]}
    errors = validate_excalidraw(data)
    assert any("Expected type 'excalidraw'" in e for e in errors)


def test_validate_excalidraw_rejects_missing_elements():
    data = {"type": "excalidraw"}
    errors = validate_excalidraw(data)
    assert any("Missing 'elements'" in e for e in errors)


def test_validate_excalidraw_rejects_empty_elements():
    data = {"type": "excalidraw", "elements": []}
    errors = validate_excalidraw(data)
    assert any("empty" in e for e in errors)


def test_bounding_box_covers_a_single_rect():
    elements = [{"type": "rectangle", "x": 10, "y": 20, "width": 100, "height": 50}]
    assert compute_bounding_box(elements) == (10, 20, 110, 70)


def test_bounding_box_ignores_deleted_elements():
    elements = [
        {"type": "rectangle", "x": 10, "y": 20, "width": 100, "height": 50},
        {"type": "rectangle", "x": 500, "y": 500, "width": 10, "height": 10, "isDeleted": True},
    ]
    assert compute_bounding_box(elements) == (10, 20, 110, 70)


def test_bounding_box_includes_arrow_points():
    elements = [{
        "type": "arrow", "x": 0, "y": 0, "width": 0, "height": 0,
        "points": [[0, 0], [50, 30]],
    }]
    assert compute_bounding_box(elements) == (0, 0, 50, 30)


def test_bounding_box_defaults_when_no_elements():
    assert compute_bounding_box([]) == (0, 0, 800, 600)
