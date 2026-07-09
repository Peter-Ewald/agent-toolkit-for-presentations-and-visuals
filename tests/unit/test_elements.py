"""Unit tests for the binding-safe Excalidraw element builder.

This is the module the whole diagram-excalidraw skill exists to make correct — these tests prove
`_check_bindings` actually catches breakage, not just that a hand-picked valid scene passes it
(the module's own `__main__` self-test only proves the latter).
"""
from elements import arrow, group, labeled_rect, rect, text, _check_bindings


def test_rect_has_no_bindings_by_default():
    box = rect("box", 0, 0, 100, 50, stroke="#000000")
    assert box["groupIds"] == []
    assert box["boundElements"] is None


def test_text_with_container_sets_reciprocal_binding():
    box = rect("box", 0, 0, 100, 50, stroke="#000000")
    label = text("label", "Hello", x=10, y=10, width=80, height=20, stroke="#000000", container=box)

    assert label["containerId"] == "box"
    assert box["boundElements"] == [{"id": "label", "type": "text"}]


def test_text_without_container_has_no_container_id():
    label = text("label", "Hello", x=10, y=10, width=80, height=20, stroke="#000000")
    assert label["containerId"] is None


def test_labeled_rect_returns_bound_pair():
    box, label = labeled_rect("box", 0, 0, 100, 50, "Hello", stroke="#000000")
    assert label["containerId"] == box["id"]
    assert box["boundElements"] == [{"id": label["id"], "type": "text"}]


def test_arrow_sets_mutual_bindings_on_both_endpoints():
    start = rect("start", 0, 0, 100, 50, stroke="#000000")
    end = rect("end", 200, 0, 100, 50, stroke="#000000")
    connector = arrow("flow", start, end, stroke="#000000")

    assert connector["startBinding"]["elementId"] == "start"
    assert connector["endBinding"]["elementId"] == "end"
    assert {"id": "flow", "type": "arrow"} in start["boundElements"]
    assert {"id": "flow", "type": "arrow"} in end["boundElements"]


def test_group_assigns_shared_group_id_to_all_members():
    box = rect("box", 0, 0, 100, 50, stroke="#000000")
    caption = text("caption", "note", x=0, y=60, width=100, height=20, stroke="#000000")
    group(box, caption, group_id="section-1")

    assert box["groupIds"] == ["section-1"]
    assert caption["groupIds"] == ["section-1"]


def test_check_bindings_passes_on_a_valid_scene():
    box_a, label_a = labeled_rect("box_a", 0, 0, 100, 50, "A", stroke="#000000")
    box_b, label_b = labeled_rect("box_b", 200, 0, 100, 50, "B", stroke="#000000")
    connector = arrow("flow", box_a, box_b, stroke="#000000")

    problems = _check_bindings([box_a, label_a, box_b, label_b, connector])
    assert problems == []


def test_check_bindings_catches_a_null_arrow_binding():
    start = rect("start", 0, 0, 100, 50, stroke="#000000")
    end = rect("end", 200, 0, 100, 50, stroke="#000000")
    connector = arrow("flow", start, end, stroke="#000000")
    connector["startBinding"] = None  # simulate hand-edited JSON breaking the binding

    problems = _check_bindings([start, end, connector])
    assert any("startBinding is null" in p for p in problems)


def test_check_bindings_catches_a_missing_reciprocal_bound_element():
    start = rect("start", 0, 0, 100, 50, stroke="#000000")
    end = rect("end", 200, 0, 100, 50, stroke="#000000")
    connector = arrow("flow", start, end, stroke="#000000")
    end["boundElements"] = None  # simulate hand-edited JSON dropping the back-reference

    problems = _check_bindings([start, end, connector])
    assert any("missing a reciprocal boundElements entry" in p for p in problems)


def test_check_bindings_catches_a_dangling_container_id():
    label = text("label", "orphan", x=0, y=0, width=50, height=20, stroke="#000000")
    label["containerId"] = "does-not-exist"

    problems = _check_bindings([label])
    assert any("points at a missing element" in p for p in problems)
