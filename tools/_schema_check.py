"""Small strict JSON Schema checker for the retail attestation contract."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class SchemaError(Exception):
    """The schema cannot be interpreted by this checker."""


def load_schema(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SchemaError("schema unavailable") from exc
    if not isinstance(document, dict):
        raise SchemaError("schema root is not an object")
    return document


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise SchemaError(f"unsupported schema type {expected!r}")


def validate(value: Any, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def visit(current: Any, node: dict[str, Any], location: str) -> None:
        expected = node.get("type")
        if expected is not None:
            names = [expected] if isinstance(expected, str) else expected
            if not isinstance(names, list) or not any(
                _type_matches(current, name) for name in names
            ):
                errors.append(f"{location}: type mismatch")
                return
        if "const" in node and current != node["const"]:
            errors.append(f"{location}: const mismatch")
        if "enum" in node and current not in node["enum"]:
            errors.append(f"{location}: enum mismatch")
        if isinstance(current, str):
            if "pattern" in node and re.search(node["pattern"], current) is None:
                errors.append(f"{location}: pattern mismatch")
            if len(current) < node.get("minLength", 0):
                errors.append(f"{location}: string is too short")
        if isinstance(current, list):
            if len(current) < node.get("minItems", 0):
                errors.append(f"{location}: too few items")
            if node.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in current}) != len(current):
                errors.append(f"{location}: duplicate items")
            item_schema = node.get("items")
            if isinstance(item_schema, dict):
                for index, item in enumerate(current):
                    visit(item, item_schema, f"{location}[{index}]")
        if isinstance(current, dict):
            for name in node.get("required", []):
                if name not in current:
                    errors.append(f"{location}: missing property")
            properties = node.get("properties", {})
            for name, item in current.items():
                if name in properties:
                    visit(item, properties[name], f"{location}.{name}")
                elif node.get("additionalProperties") is False:
                    errors.append(f"{location}: unexpected property")

    visit(value, schema, "$")
    return errors
