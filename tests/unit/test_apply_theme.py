"""Unit tests for the Excalidraw theme color/font remapping pass."""
from apply_theme import apply_theme


def _theme(**overrides):
    theme = {
        "colorMap": {"#old-cyan": "#0098eb"},
        "text": {"defaultStrokeColor": "#333333", "labelBackgroundColor": "#ffffff"},
        "fonts": {"editorFontFamily": 2},
        "canvas": {"viewBackgroundColor": "#f9f9f7"},
    }
    theme.update(overrides)
    return theme


def _scene(elements):
    return {"type": "excalidraw", "elements": elements, "appState": {}}


def test_mapped_stroke_color_is_replaced():
    scene = _scene([{"type": "rectangle", "strokeColor": "#old-cyan", "backgroundColor": "transparent"}])
    result = apply_theme(scene, _theme())
    assert result["elements"][0]["strokeColor"] == "#0098eb"


def test_unmapped_color_passes_through_unchanged():
    scene = _scene([{"type": "rectangle", "strokeColor": "#05326e", "backgroundColor": "transparent"}])
    result = apply_theme(scene, _theme())
    assert result["elements"][0]["strokeColor"] == "#05326e"


def test_color_lookup_is_case_insensitive():
    scene = _scene([{"type": "rectangle", "strokeColor": "#OLD-CYAN", "backgroundColor": "transparent"}])
    result = apply_theme(scene, _theme())
    assert result["elements"][0]["strokeColor"] == "#0098eb"


def test_text_element_gets_default_stroke_and_font():
    scene = _scene([{
        "type": "text", "strokeColor": "#ff0000", "backgroundColor": "transparent",
        "fontFamily": 1, "containerId": None,
    }])
    result = apply_theme(scene, _theme())
    text_element = result["elements"][0]
    assert text_element["strokeColor"] == "#333333"
    assert text_element["fontFamily"] == 2


def test_arrow_label_gets_label_background_color():
    scene = _scene([{
        "type": "text", "strokeColor": "#333333", "backgroundColor": "transparent",
        "fontFamily": 2, "containerId": "arrow-flow",
    }])
    result = apply_theme(scene, _theme())
    assert result["elements"][0]["backgroundColor"] == "#ffffff"


def test_non_arrow_label_background_is_left_alone():
    scene = _scene([{
        "type": "text", "strokeColor": "#333333", "backgroundColor": "transparent",
        "fontFamily": 2, "containerId": "box-1",
    }])
    result = apply_theme(scene, _theme())
    assert result["elements"][0]["backgroundColor"] == "transparent"


def test_canvas_background_sets_view_background_color():
    scene = _scene([])
    result = apply_theme(scene, _theme())
    assert result["appState"]["viewBackgroundColor"] == "#f9f9f7"
