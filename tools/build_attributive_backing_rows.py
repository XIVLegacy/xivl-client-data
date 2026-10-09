"""Authenticate xtx/attributive backing rows against the merged CSV."""

from __future__ import annotations

import argparse
import hashlib
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from _csv_root import add_csv_dir_argument, validate_csv_dir
from build_autotranslate_name_crosswalk import (
    _load_source,
    _load_table_manifest,
    render,
)
from build_fixed_phrase_backing_rows import identity, key_digest, read_ranges, row_spans
from compare_sheet_inventory import load_inventory, parse_document, resource_path


REPO = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "manifests" / "attributive_backing_rows.json"
SHEET = "xtx/attributive"
CSV = "xtx_attributive.csv"
LOCALES = ("ja", "en", "de", "fr", "chs")
ANCHORS = (1, 2, 5, 35)
UINT32_LIMIT = 1 << 32


def _attribute(element: ET.Element, name: str) -> str:
    value = element.get(name)
    if value is None:
        raise ValueError(f"missing SSD attribute {name}")
    return value


def _u32_attribute(element: ET.Element, name: str) -> int:
    value = _attribute(element, name)
    try:
        number = int(value, 10)
    except ValueError as exc:
        raise ValueError(f"SSD attribute {name} is not decimal") from exc
    if number < 0 or number >= UINT32_LIMIT:
        raise ValueError(f"SSD attribute {name} is outside u32")
    return number


def _resource(data_root: Path, resource_id: int, kind: str) -> bytes:
    try:
        path = resource_path(data_root, resource_id)
        return path.read_bytes()
    except (OSError, OverflowError, ValueError) as exc:
        raise ValueError(f"{kind} resource {resource_id} is unreadable") from exc


def parse_sheet_string(
    data: bytes, position: int = 0
) -> tuple[int, str, dict[str, Any]]:
    """Read one length-framed string while retaining only observed framing."""
    if position < 0 or position + 2 > len(data):
        raise ValueError("string length prefix is truncated")
    declared_length = struct.unpack_from("<H", data, position)[0]
    if declared_length == 0:
        raise ValueError("string declares zero bytes")
    body_start = position + 2
    body_end = body_start + declared_length
    if body_end > len(data):
        raise ValueError("string body is truncated")
    body = data[body_start:body_end]
    scrambled = body[0] == 0xFF
    terminator = 0x73 if scrambled else 0
    if body[-1] != terminator:
        raise ValueError("string has an invalid terminator")
    decoded = bytes(value ^ 0x73 for value in body[1:-1]) if scrambled else body[:-1]
    if any(value < 0x20 for value in decoded):
        raise ValueError("string contains an unsupported control byte")
    try:
        value = decoded.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("string body is not UTF-8") from exc
    value = value.replace("\\", "\\\\").replace("[", "\\[")
    return (
        body_end,
        value,
        {
            "start": position,
            "end": body_end,
            "declaredLength": declared_length,
            "scrambled": scrambled,
            "terminator": f"0x{terminator:02X}",
        },
    )


def parse_row(data: bytes, types: list[str]) -> tuple[list[str], list[dict[str, Any]]]:
    values: list[str] = []
    framing: list[dict[str, Any]] = []
    position = 0
    for type_name in types:
        if type_name == "s8":
            if position >= len(data):
                raise ValueError("s8 column is truncated")
            value = struct.unpack_from("<b", data, position)[0]
            values.append(str(value))
            framing.append({"type": "s8", "start": position, "end": position + 1})
            position += 1
        elif type_name == "str":
            position, value, detail = parse_sheet_string(data, position)
            values.append(value)
            framing.append({"type": "str", **detail})
        else:
            raise ValueError(f"unsupported attributive column type {type_name}")
    if position != len(data):
        raise ValueError("row has trailing bytes after its declared columns")
    return values, framing


def strict_row_spans(
    raw: bytes, data_size: int, begin: int, count: int
) -> dict[int, tuple[int, int]]:
    if len(raw) % 4 or len(raw) // 4 != count:
        raise ValueError("offset file entry count differs from block")
    return row_spans(raw, data_size, begin, count)


def _definition(sheet: ET.Element) -> tuple[list[str], list[int], dict[str, Any]]:
    locale = _attribute(sheet, "lang")
    types = [param.text or "" for param in sheet.findall("./type/param")]
    columns: list[int] = []
    for param in sheet.findall("./index/param"):
        try:
            column = int(param.text or "", 10)
        except ValueError as exc:
            raise ValueError(f"{locale}: index is not decimal") from exc
        if column < 0 or column >= UINT32_LIMIT:
            raise ValueError(f"{locale}: index is outside u32")
        columns.append(column)
    if len(types) != len(columns):
        raise ValueError(f"{locale}: type and index widths differ")
    if len(set(columns)) != len(columns):
        raise ValueError(f"{locale}: definition repeats a column index")
    if any(type_name not in {"s8", "str"} for type_name in types):
        raise ValueError(f"{locale}: unsupported attributive column type")
    column_max = _u32_attribute(sheet, "column_max")
    if not columns or column_max != max(columns) + 1:
        raise ValueError(f"{locale}: column_max does not bound its indexes")
    column_count = _u32_attribute(sheet, "column_count")
    if column_count != len(types):
        raise ValueError(f"{locale}: column_count differs from the type list")
    return (
        types,
        columns,
        {
            "locale": locale,
            "mode": _attribute(sheet, "mode"),
            "columnMax": column_max,
            "columnCount": column_count,
            "cache": _attribute(sheet, "cache"),
            "type": _attribute(sheet, "type"),
            "param": sheet.get("param", ""),
            "types": types,
            "columns": columns,
        },
    )


def _block_report(
    data_root: Path,
    locale: str,
    block_index: int,
    block: ET.Element,
    types: list[str],
    columns: list[int],
    csv_rows: dict[int, Any],
    csv_ordinals: dict[int, int],
) -> tuple[dict[str, Any], list[int], list[dict[str, Any]]]:
    begin = _u32_attribute(block, "begin")
    count = _u32_attribute(block, "count")
    if begin + count > UINT32_LIMIT:
        raise ValueError(f"{locale} block {block_index}: slot range is outside u32")
    resource_ids = {
        "enable": _u32_attribute(block, "enable"),
        "offsets": _u32_attribute(block, "offset"),
    }
    try:
        resource_ids["data"] = int((block.text or "").strip(), 10)
    except ValueError as exc:
        raise ValueError(
            f"{locale} block {block_index}: data id is not decimal"
        ) from exc
    if not 0 <= resource_ids["data"] < UINT32_LIMIT:
        raise ValueError(f"{locale} block {block_index}: data id is outside u32")
    resources = {
        kind: _resource(data_root, resource_id, f"{locale} {kind}")
        for kind, resource_id in resource_ids.items()
    }
    ranges, keys = read_ranges(resources["enable"], begin, count)
    spans = strict_row_spans(resources["offsets"], len(resources["data"]), begin, count)
    if keys != list(spans):
        raise ValueError(
            f"{locale} block {block_index}: enabled rows differ from spans"
        )

    range_by_key: dict[int, tuple[int, int, int]] = {}
    for range_index, (base, range_count) in enumerate(ranges):
        for key in range(base, base + range_count):
            range_by_key[key] = (range_index, base, range_count)
    field_matches = 0
    framing_count = 0
    anchors: list[dict[str, Any]] = []
    span_rows: list[tuple[int, int, int]] = []
    for enabled_ordinal, key in enumerate(keys):
        start, end = spans[key]
        values, framing = parse_row(resources["data"][start:end], types)
        if key not in csv_rows:
            raise ValueError(
                f"{locale}: backing row {key} is absent from the merged CSV"
            )
        for column, value in zip(columns, values):
            if value != csv_rows[key].values[column]:
                raise ValueError(
                    f"{locale}: row {key} column {column} differs from CSV"
                )
            field_matches += 1
        framing_count += len(framing)
        span_rows.append((key, start, end))
        if key in ANCHORS:
            range_index, range_base, range_count = range_by_key[key]
            anchors.append(
                {
                    "rowKey": key,
                    "blockIndex": block_index,
                    "slotIndex": key - begin,
                    "enabledOrdinal": enabled_ordinal,
                    "csvIterationIndex": csv_ordinals[key],
                    "rangeIndex": range_index,
                    "rangeBase": range_base,
                    "rangeCount": range_count,
                    "dataSpan": {"start": start, "end": end},
                    "cells": {
                        str(column): values[index]
                        for index, column in enumerate(columns)
                    },
                    "framing": framing,
                }
            )

    return (
        {
            "blockIndex": block_index,
            "begin": begin,
            "declaredSlotCount": count,
            "offsetEntryCount": len(resources["offsets"]) // 4,
            "enabledRangeCount": len(ranges),
            "enabledRowCount": len(keys),
            "enabledKeySha256": key_digest(keys),
            "rowSpanSha256": hashlib.sha256(
                b"".join(
                    struct.pack("<III", key, start, end)
                    for key, start, end in span_rows
                )
            )
            .hexdigest()
            .upper(),
            "enableMatchesNonemptySpans": True,
            "fieldCount": len(keys) * len(columns),
            "fieldMatchesCsvCount": field_matches,
            "framingFieldCount": framing_count,
            "sources": {
                kind: identity(raw, resource_ids[kind])
                for kind, raw in resources.items()
            },
        },
        keys,
        anchors,
    )


def build(client_root: Path, csv_dir: Path) -> dict[str, Any]:
    versions = {
        name: (client_root / name).read_text(encoding="ascii").strip()
        for name in ("game.ver", "patch.ver")
    }
    if versions != {"game.ver": "2012.09.19.0001", "patch.ver": "1.23b"}:
        raise ValueError("client version is not the catalog's 1.23b extraction")
    inventory = load_inventory(REPO / "manifests" / "sheet_inventory.csv")
    entry = next(row for row in inventory if row["name"] == SHEET)
    data_root = client_root / "data"
    master = resource_path(data_root, 0x01030000)
    references = parse_document(master).findall("sheet")
    named_references = [row for row in references if row.get("name") == SHEET]
    if len(named_references) != 1:
        raise ValueError(
            "game master does not name the attributive definition exactly once"
        )
    if named_references[0].get("infofile") != str(entry["resourceId"]):
        raise ValueError("game master names an unexpected attributive definition")
    schema_path = resource_path(data_root, entry["resourceId"])
    sheets = parse_document(schema_path).findall("sheet")
    if len(sheets) != len(LOCALES) or [sheet.get("lang") for sheet in sheets] != list(
        LOCALES
    ):
        raise ValueError("attributive locale definitions differ")

    # Validate the selected root before _load_source reads any CSV bytes.
    validated_csv_dir = validate_csv_dir(csv_dir)
    header, rows, source = _load_source(
        validated_csv_dir, CSV, _load_table_manifest()[CSV]
    )
    csv_keys: list[int] = []
    csv_rows: dict[int, Any] = {}
    for row in rows:
        try:
            key = int(row.row_id, 10)
        except ValueError as exc:
            raise ValueError(
                f"attributive CSV row id is not decimal: {row.row_id}"
            ) from exc
        if key < 0 or key >= UINT32_LIMIT or row.row_id != str(key):
            raise ValueError(
                f"attributive CSV row id is not canonical u32: {row.row_id}"
            )
        if key in csv_rows:
            raise ValueError(f"attributive CSV has duplicate numeric row id {key}")
        csv_keys.append(key)
        csv_rows[key] = row
    if csv_keys != sorted(csv_keys):
        raise ValueError("attributive CSV rows are not in ascending iteration order")
    csv_ordinals = {key: ordinal for ordinal, key in enumerate(csv_keys)}

    locale_reports = []
    definition_reports = []
    locale_keys: dict[str, list[int]] = {}
    for sheet in sheets:
        if sheet.get("name") != SHEET:
            raise ValueError("unexpected attributive definition name")
        types, columns, metadata = _definition(sheet)
        definition_reports.append(metadata)
        if any(column >= len(header.column_types) for column in columns):
            raise ValueError(
                f"{metadata['locale']}: definition column exceeds CSV width"
            )
        for column, type_name in zip(columns, types):
            if header.column_types[column] != type_name:
                raise ValueError(
                    f"{metadata['locale']}: column {column} type differs from CSV header"
                )
        groups = sheet.findall("./block")
        file_blocks: list[ET.Element] = []
        for group in groups:
            expected_files = _u32_attribute(group, "count")
            files = group.findall("./file")
            if expected_files != len(files):
                raise ValueError(f"{metadata['locale']}: block file count differs")
            file_blocks.extend(files)
        locale = metadata["locale"]
        if locale in locale_keys:
            raise ValueError(f"duplicate attributive locale {locale}")
        all_keys: list[int] = []
        block_reports = []
        anchors: list[dict[str, Any]] = []
        for file_block in file_blocks:
            block_report, block_keys, block_anchors = _block_report(
                data_root,
                locale,
                len(block_reports),
                file_block,
                types,
                columns,
                csv_rows,
                csv_ordinals,
            )
            block_reports.append(block_report)
            all_keys.extend(block_keys)
            anchors.extend(block_anchors)
        if not all_keys:
            raise ValueError(f"{locale}: definition has no enabled rows")
        if len(all_keys) != len(set(all_keys)) or all_keys != sorted(all_keys):
            raise ValueError(f"{locale}: block row keys are not unique and ordered")
        locale_keys[locale] = all_keys
        csv_only = sorted(set(csv_keys) - set(all_keys))
        if any(csv_rows[key].values[column] for key in csv_only for column in columns):
            raise ValueError(f"{locale}: CSV cells are nonempty where rows are absent")
        key_set = set(all_keys)
        if all_keys != [key for key in csv_keys if key in key_set]:
            raise ValueError(f"{locale}: backing row order differs from CSV iteration")
        locale_reports.append(
            {
                "locale": locale,
                "columns": columns,
                "types": types,
                "blockGroupCount": len(groups),
                "fileBlockCount": len(file_blocks),
                "enabledRowCount": len(all_keys),
                "enabledKeySha256": key_digest(all_keys),
                "csvOnlyKeys": csv_only,
                "csvOnlyKeyCount": len(csv_only),
                "csvOnlyCellsAreEmpty": True,
                "orderMatchesCsvIteration": True,
                "fieldMatchesCsvCount": sum(
                    report["fieldMatchesCsvCount"] for report in block_reports
                ),
                "blocks": block_reports,
                "anchors": anchors,
            }
        )

    union = set().union(*(set(keys) for keys in locale_keys.values()))
    if union != set(csv_keys):
        raise ValueError("attributive locale row union differs from merged CSV keys")
    if set(ANCHORS) - union:
        raise ValueError("attributive sparse anchor is absent from every locale")

    return {
        "schemaVersion": 1,
        "evidenceClass": "client_extraction",
        "clientVersion": versions,
        "extractionVersion": versions["game.ver"],
        "sheet": SHEET,
        "sourceMaster": identity(master.read_bytes(), 0x01030000),
        "masterReference": {
            "name": SHEET,
            "infofile": entry["resourceId"],
            "matchesDefinition": True,
        },
        "sourceDefinition": identity(schema_path.read_bytes(), entry["resourceId"]),
        "sourceCsv": source,
        "csvKeySha256": key_digest(csv_keys),
        "csvRowCount": len(csv_keys),
        "definitionLocales": definition_reports,
        "method": (
            "Verify the 1.23b version and decimal master-to-definition reference; "
            "follow every locale block's explicit data, enable and offset resource; "
            "derive typed field mappings from each definition and the merged CSV header; "
            "compare every supplied field, retain opaque string framing for finite anchors, "
            "and hash ordered row keys and row spans."
        ),
        "locales": locale_reports,
        "nativeBoundary": {
            "backingRowToCsv": "proven",
            "selectedInstanceAndLocale": "unobserved",
            "nativeSelection": "qualified",
            "statement": (
                "This report authenticates the named xtx/attributive definition and its "
                "backing rows against the merged CSV. It assigns no runtime token, "
                "selection, grammar or rendering behavior."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-root", required=True, type=Path)
    add_csv_dir_argument(parser)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        rendered = render(build(args.client_root, Path(args.csv_dir)))
        if args.check:
            if OUTPUT.read_bytes() != rendered:
                raise ValueError("attributive_backing_rows.json is out of date")
            print("PASS: attributive backing-row report is deterministic")
        else:
            OUTPUT.write_bytes(rendered)
            print(f"wrote {OUTPUT.name} ({len(rendered)} bytes)")
    except (OSError, ValueError, KeyError, StopIteration, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
