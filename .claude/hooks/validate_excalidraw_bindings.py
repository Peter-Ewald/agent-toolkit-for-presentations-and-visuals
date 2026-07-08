#!/usr/bin/python3
"""PostToolUse hook (matcher: Edit|Write) — blocks a Write/Edit to an `.excalidraw` file if its
native bindings are broken: an arrow's startBinding/endBinding missing or not reciprocated by the
target element's boundElements, a bound text's containerId not reciprocated, or a groupIds entry
used by only one element (an orphaned/incomplete grouping).

Mirrors the checks in `.claude/skills/diagram-excalidraw/scripts/elements.py`'s `_check_bindings`
(kept as a separate, self-contained copy here — same convention as this repo's other hooks, which
don't import application code) plus the groupIds check, since that module's own self-test only
proves its own output is correct, not diagrams built or hand-edited outside it.

Fails open (never blocks) on anything outside this hook's concern: wrong tool, non-.excalidraw
file, unreadable file, or a JSON shape that isn't an Excalidraw file at all. Blocks only on
JSON syntax errors and actual binding problems, since both are exactly what this hook exists to
catch immediately instead of leaving them to be discovered by opening the app.
"""
import json
import sys
from pathlib import Path


def check_bindings(elements: list) -> list:
    by_id = {e.get("id"): e for e in elements if isinstance(e, dict)}
    problems = []

    for element in elements:
        if not isinstance(element, dict):
            continue

        if element.get("type") == "arrow":
            for side in ("startBinding", "endBinding"):
                binding = element.get(side)
                if not binding:
                    problems.append(f"{element.get('id')}.{side} is null")
                    continue
                target = by_id.get(binding.get("elementId"))
                if target is None:
                    problems.append(f"{element.get('id')}.{side} points at a missing element")
                    continue
                back_refs = target.get("boundElements") or []
                if not any(ref.get("id") == element.get("id") for ref in back_refs):
                    problems.append(
                        f"{binding.get('elementId')} is missing a reciprocal boundElements "
                        f"entry for arrow {element.get('id')}"
                    )

        if element.get("type") == "text" and element.get("containerId"):
            container = by_id.get(element["containerId"])
            if container is None:
                problems.append(f"{element.get('id')}.containerId points at a missing element")
                continue
            back_refs = container.get("boundElements") or []
            if not any(ref.get("id") == element.get("id") for ref in back_refs):
                problems.append(
                    f"{element['containerId']} is missing a reciprocal boundElements "
                    f"entry for text {element.get('id')}"
                )

    group_members = {}
    for element in elements:
        if not isinstance(element, dict):
            continue
        for group_id in element.get("groupIds") or []:
            group_members.setdefault(group_id, []).append(element.get("id"))
    for group_id, members in group_members.items():
        if len(members) < 2:
            problems.append(f"groupIds {group_id!r} is only used by one element ({members[0]})")

    return problems


def main():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if event.get("tool_name") not in ("Edit", "Write"):
        sys.exit(0)

    file_path = event.get("tool_input", {}).get("file_path", "")
    if not file_path.endswith(".excalidraw"):
        sys.exit(0)

    try:
        raw = Path(file_path).read_text(encoding="utf-8")
    except OSError:
        sys.exit(0)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"{file_path} is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, dict) or not isinstance(data.get("elements"), list):
        sys.exit(0)

    problems = check_bindings(data["elements"])
    if problems:
        print(
            f"{file_path} has {len(problems)} broken binding(s):\n"
            + "\n".join(f"  - {p}" for p in problems)
            + "\n\nRebuild the affected elements with "
            ".claude/skills/diagram-excalidraw/scripts/elements.py instead of hand-editing "
            "the JSON.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
