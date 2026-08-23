"""Small strict JSON Schema checker for the retail attestation contract."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class SchemaError(Exception):
    """The schema cannot be interpreted by this checker."""


_SUPPORTED_KEYWORDS = frozenset({
    "type",
    "const",
    "enum",
    "pattern",
    "minLength",
    "minItems",
    "uniqueItems",
    "items",
    "required",
    "properties",
    "additionalProperties",
})
_ANNOTATION_KEYWORDS = frozenset({"$schema", "$id", "title", "description"})
_SUPPORTED_TYPES = frozenset({"object", "array", "string", "integer", "boolean", "null"})


def load_schema(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SchemaError("schema unavailable") from exc
    if not isinstance(document, dict):
        raise SchemaError("schema root is not an object")
    return document


def _check_schema_node(node: Any) -> None:
    if not isinstance(node, dict):
        raise SchemaError("schema node is not an object")
    unsupported = sorted(
        key for key in node
        if key not in _SUPPORTED_KEYWORDS and key not in _ANNOTATION_KEYWORDS
    )
    if unsupported:
        raise SchemaError(f"unsupported schema keyword {unsupported[0]!r}")

    if "type" in node:
        expected = node["type"]
        names = [expected] if isinstance(expected, str) else expected
        if (
            not isinstance(names, list)
            or not names
            or any(not isinstance(name, str) or name not in _SUPPORTED_TYPES for name in names)
        ):
            raise SchemaError("unsupported schema type")
    if "enum" in node and not isinstance(node["enum"], list):
        raise SchemaError("schema enum is not an array")
    if "pattern" in node and not isinstance(node["pattern"], str):
        raise SchemaError("schema pattern is not a string")
    for keyword in ("minLength", "minItems"):
        if keyword in node and (
            not isinstance(node[keyword], int) or isinstance(node[keyword], bool)
            or node[keyword] < 0
        ):
            raise SchemaError(f"schema {keyword} is not a non-negative integer")
    if "uniqueItems" in node and not isinstance(node["uniqueItems"], bool):
        raise SchemaError("schema uniqueItems is not a boolean")
    if "items" in node:
        _check_schema_node(node["items"])
    if "required" in node and (
        not isinstance(node["required"], list)
        or any(not isinstance(name, str) for name in node["required"])
    ):
        raise SchemaError("schema required is not a string array")
    properties = node.get("properties", {})
    if not isinstance(properties, dict):
        raise SchemaError("schema properties is not an object")
    for child in properties.values():
        _check_schema_node(child)
    if "additionalProperties" in node and not isinstance(node["additionalProperties"], bool):
        raise SchemaError("schema additionalProperties is not a boolean")


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
    _check_schema_node(schema)
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
