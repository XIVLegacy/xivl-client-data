"""Authenticate xtx/placeName backing rows against the merged CSV."""

from __future__ import annotations

import argparse
import collections
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
OUTPUT = REPO / "manifests" / "place_name_backing_rows.json"
SHEET = "xtx/placeName"
CSV = "xtx_placeName.csv"
LOCALES = ("ja", "en", "de", "fr", "chs")
ANCHORS = (1, 51, 1051, 2104, 2118, 3025, 8001)
CSV_TYPES = ["str", "str", "str", "u8", "str", "str", "str", "str", "str"]
UINT32_LIMIT = 1 << 32

# Authority: xivl-tools:docs/formats/ssd-sheet.md#rich-string-read-and-text-export-contract
# The payload is retained as raw token bytes; this report does not decode token
# expressions.
TOKEN_NAMES = {
    0x09: "switch",
    0x10: "newline",
    0x16: "soft-hyphen",
    0x1F: "hyphen",
}


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
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{kind} resource id is outside u32") from exc
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValueError(f"{kind} resource {resource_id} is unreadable") from exc
    return raw


def _escape_literal(raw: bytes) -> str:
    if any(value < 0x20 for value in raw):
        raise ValueError("literal string contains an unsupported control byte")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("literal string is not UTF-8") from exc
    return text.replace("\\", "\\\\").replace("[", "\\[")


def _token_end(data: bytes, start: int) -> tuple[int, int, int]:
    if start + 3 > len(data):
        raise ValueError("rich token header is truncated")
    code = data[start + 1]
    lead = data[start + 2]
    if lead == 0 or lead >= 0xF0:
        raise ValueError(f"rich token uses unsupported length lead 0x{lead:02X}")
    cursor = start + 3
    length = lead - 1
    end = cursor + length
    if end >= len(data) or data[end] != 0x03:
        raise ValueError("rich token has no matching terminator")
    if code not in TOKEN_NAMES:
        raise ValueError(f"rich token code 0x{code:02X} is unsupported")
    return end + 1, code, lead


def _render_rich(data: bytes) -> tuple[str, dict[str, Any]]:
    output: list[str] = []
    counts: collections.Counter[int] = collections.Counter()
    length_leads: collections.Counter[int] = collections.Counter()
    position = 0
    literal_start = 0
    while position < len(data):
        if data[position] != 0x02:
            position += 1
            continue
        output.append(_escape_literal(data[literal_start:position]))
        end, code, lead = _token_end(data, position)
        output.append(f"[@{TOKEN_NAMES[code]}:{data[position:end].hex()}]")
        counts[code] += 1
        length_leads[lead] += 1
        position = end
        literal_start = end
    output.append(_escape_literal(data[literal_start:]))
    return "".join(output), {
        "tokenCount": sum(counts.values()),
        "tokenCodes": {f"0x{code:02X}": counts[code] for code in sorted(counts)},
        "tokenLengthLeads": {
            f"0x{lead:02X}": length_leads[lead] for lead in sorted(length_leads)
        },
    }


def parse_sheet_string(
    data: bytes, position: int = 0
) -> tuple[int, str, dict[str, Any]]:
    """Read one bounded SSD string and export its lossless CSV text."""
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
    value, rich = _render_rich(decoded)
    return (
        body_end,
        value,
        {
            "scrambled": scrambled,
            **rich,
        },
    )


def parse_row(data: bytes, types: list[str]) -> tuple[list[str], list[dict[str, Any]]]:
    values: list[str] = []
    details: list[dict[str, Any]] = []
    position = 0
    for type_name in types:
        if type_name == "str":
            position, value, detail = parse_sheet_string(data, position)
            values.append(value)
            details.append(detail)
        elif type_name == "u8":
            if position >= len(data):
                raise ValueError("u8 column is truncated")
            values.append(str(data[position]))
            details.append({"type": "u8"})
            position += 1
        else:
            raise ValueError(f"unsupported placeName column type {type_name}")
    if position != len(data):
        raise ValueError("row has trailing bytes after its declared columns")
    return values, details


def span_digest(rows: list[tuple[int, int, int]]) -> str:
    encoded = b"".join(struct.pack("<III", key, start, end) for key, start, end in rows)
    return hashlib.sha256(encoded).hexdigest().upper()


def strict_row_spans(
    raw: bytes, data_size: int, begin: int, count: int
) -> dict[int, tuple[int, int]]:
    if len(raw) % 4 or len(raw) // 4 != count:
        raise ValueError("offset file entry count differs from block")
    return row_spans(raw, data_size, begin, count)


def _definition(sheet: ET.Element) -> tuple[list[str], list[int], dict[str, Any]]:
    locale = _attribute(sheet, "lang")
    type_params = sheet.findall("./type/param")
    index_params = sheet.findall("./index/param")
    types = [param.text or "" for param in type_params]
    columns: list[int] = []
    for param in index_params:
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
    for type_name in types:
        if type_name not in {"str", "u8"}:
            raise ValueError(f"{locale}: unsupported placeName column type {type_name}")
    column_max = _u32_attribute(sheet, "column_max")
    if not columns or column_max != max(columns) + 1:
        raise ValueError(f"{locale}: column_max does not bound its indexes")
    declared_count = _u32_attribute(sheet, "column_count")
    if declared_count != len(types):
        raise ValueError(f"{locale}: column_count differs from the type list")
    metadata = {
        "locale": locale,
        "mode": _attribute(sheet, "mode"),
        "columnMax": column_max,
        "columnCount": declared_count,
        "cache": _attribute(sheet, "cache"),
        "type": _attribute(sheet, "type"),
        "param": sheet.get("param", ""),
        "types": types,
        "columns": columns,
    }
    return types, columns, metadata


def _block_report(
    data_root: Path,
    locale: str,
    block_index: int,
    block: ET.Element,
    types: list[str],
    columns: list[int],
    csv_rows: dict[int, Any],
    csv_ordinals: dict[int, int],
    locale_ordinal_start: int,
) -> tuple[dict[str, Any], list[int], list[dict[str, Any]]]:
    begin = _u32_attribute(block, "begin")
    count = _u32_attribute(block, "count")
    if begin + count > UINT32_LIMIT:
        raise ValueError(f"{locale} block {block_index}: slot range is outside u32")
    resource_ids: dict[str, int] = {}
    for kind, attribute in (("enable", "enable"), ("offsets", "offset")):
        resource_ids[kind] = _u32_attribute(block, attribute)
    text = (block.text or "").strip()
    try:
        resource_ids["data"] = int(text, 10)
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
    try:
        spans = strict_row_spans(
            resources["offsets"], len(resources["data"]), begin, count
        )
    except ValueError as exc:
        raise ValueError(f"{locale} block {block_index}: {exc}") from exc
    if keys != list(spans):
        raise ValueError(
            f"{locale} block {block_index}: enabled rows differ from spans"
        )

    cell_matches = 0
    cell_count = 0
    string_count = 0
    scrambled_count = 0
    token_count = 0
    token_codes: collections.Counter[str] = collections.Counter()
    token_length_leads: collections.Counter[str] = collections.Counter()
    span_rows: list[tuple[int, int, int]] = []
    anchors: list[dict[str, Any]] = []
    range_by_key: dict[int, tuple[int, int, int]] = {}
    for range_index, (base, range_count) in enumerate(ranges):
        for key in range(base, base + range_count):
            range_by_key[key] = (range_index, base, range_count)

    for block_ordinal, key in enumerate(keys):
        start, end = spans[key]
        values, details = parse_row(resources["data"][start:end], types)
        if key not in csv_rows:
            raise ValueError(
                f"{locale}: backing row {key} is absent from the merged CSV"
            )
        for column, value, detail in zip(columns, values, details):
            expected = csv_rows[key].values[column]
            if value != expected:
                raise ValueError(
                    f"{locale}: row {key} column {column} differs from CSV"
                )
            cell_matches += 1
            cell_count += 1
            if detail.get("type") != "u8":
                string_count += 1
                scrambled_count += int(detail["scrambled"])
                token_count += int(detail["tokenCount"])
                for code, amount in detail["tokenCodes"].items():
                    token_codes[code] += amount
                for lead, amount in detail["tokenLengthLeads"].items():
                    token_length_leads[lead] += amount
        span_rows.append((key, start, end))
        if key in ANCHORS:
            range_index, range_base, range_count = range_by_key[key]
            anchors.append(
                {
                    "rowKey": key,
                    "blockIndex": block_index,
                    "slotIndex": key - begin,
                    "enabledOrdinal": locale_ordinal_start + block_ordinal,
                    "csvIterationIndex": csv_ordinals[key],
                    "rangeIndex": range_index,
                    "rangeBase": range_base,
                    "rangeCount": range_count,
                    "dataSpan": {"start": start, "end": end},
                    "cells": {
                        str(column): values[index]
                        for index, column in enumerate(columns)
                    },
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
            "rowSpanSha256": span_digest(span_rows),
            "enableMatchesNonemptySpans": True,
            "fieldCount": cell_count,
            "fieldMatchesCsvCount": cell_matches,
            "stringCount": string_count,
            "scrambledStringCount": scrambled_count,
            "tokenCount": token_count,
            "tokenCodes": dict(sorted(token_codes.items())),
            "tokenLengthLeads": dict(sorted(token_length_leads.items())),
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
    matching_references = [
        row
        for row in references
        if row.get("name") == SHEET and row.get("infofile") == str(entry["resourceId"])
    ]
    if len(matching_references) != 1:
        raise ValueError(
            "game master does not name the placeName definition exactly once"
        )
    schema_path = resource_path(data_root, entry["resourceId"])
    sheets = parse_document(schema_path).findall("sheet")
    if len(sheets) != len(LOCALES) or [sheet.get("lang") for sheet in sheets] != list(
        LOCALES
    ):
        raise ValueError("placeName locale definitions differ")

    header, rows, source = _load_source(
        validate_csv_dir(csv_dir), CSV, _load_table_manifest()[CSV]
    )
    if header.column_types != CSV_TYPES:
        raise ValueError("placeName CSV column types differ")
    csv_keys: list[int] = []
    csv_rows: dict[int, Any] = {}
    for row in rows:
        try:
            key = int(row.row_id, 10)
        except ValueError as exc:
            raise ValueError(
                f"placeName CSV row id is not decimal: {row.row_id}"
            ) from exc
        if key < 0 or key >= UINT32_LIMIT or row.row_id != str(key):
            raise ValueError(f"placeName CSV row id is not canonical u32: {row.row_id}")
        if key in csv_rows:
            raise ValueError(f"placeName CSV has duplicate numeric row id {key}")
        csv_keys.append(key)
        csv_rows[key] = row
    if csv_keys != sorted(csv_keys):
        raise ValueError("placeName CSV rows are not in ascending iteration order")
    csv_ordinals = {key: ordinal for ordinal, key in enumerate(csv_keys)}

    locale_reports = []
    locale_keys: dict[str, list[int]] = {}
    definition_reports = []
    for sheet in sheets:
        if sheet.get("name") != SHEET:
            raise ValueError("unexpected placeName definition name")
        types, columns, metadata = _definition(sheet)
        definition_reports.append(metadata)
        block_groups = sheet.findall("./block")
        file_blocks: list[ET.Element] = []
        for group in block_groups:
            expected_files = _u32_attribute(group, "count")
            files = group.findall("./file")
            if expected_files != len(files):
                raise ValueError(f"{metadata['locale']}: block file count differs")
            file_blocks.extend(files)
        locale = metadata["locale"]
        if locale in locale_keys:
            raise ValueError(f"duplicate placeName locale {locale}")
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
                len(all_keys),
            )
            block_reports.append(block_report)
            all_keys.extend(block_keys)
            anchors.extend(block_anchors)
        if not all_keys:
            raise ValueError(f"{locale}: definition has no blocks")
        keys = all_keys
        if len(keys) != len(set(keys)) or keys != sorted(keys):
            raise ValueError(f"{locale}: block row keys are not unique and ordered")
        locale_keys[locale] = keys
        csv_only = sorted(set(csv_keys) - set(keys))
        if any(csv_rows[key].values[column] for key in csv_only for column in columns):
            raise ValueError(
                f"{locale}: CSV cells are nonempty where backing rows are absent"
            )
        key_set = set(keys)
        expected_order = [key for key in csv_keys if key in key_set]
        if keys != expected_order:
            raise ValueError(f"{locale}: backing row order differs from CSV iteration")
        locale_reports.append(
            {
                "locale": locale,
                "columns": columns,
                "types": types,
                "blockGroupCount": len(block_groups),
                "fileBlockCount": len(file_blocks),
                "enabledRowCount": len(keys),
                "enabledKeySha256": key_digest(keys),
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
        raise ValueError("placeName locale row union differs from merged CSV keys")
    if any(set(keys) - set(csv_keys) for keys in locale_keys.values()):
        raise ValueError(
            "placeName backing rows contain keys absent from the merged CSV"
        )
    if set(ANCHORS) - union:
        raise ValueError("placeName sparse anchor is absent from every locale")

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
            "decode the established SSD string framing, XOR obfuscation and direct "
            "lossless rich-token envelope for the observed placeName token codes; "
            "compare exported cells to the authenticated merged CSV; hash ordered "
            "row keys and row spans."
        ),
        "tokenContract": {
            "source": (
                "xivl-tools:docs/formats/ssd-sheet.md#rich-string-read-and-"
                "text-export-contract"
            ),
            "supportedCodes": {
                "0x09": "switch",
                "0x10": "newline",
                "0x16": "soft-hyphen",
                "0x1F": "hyphen",
            },
            "lengthForm": "direct lead < 0xF0, length is lead - 1",
            "rejectedLengthForms": ["0x00", "0xF0", "0xF1", "0xF2", "0xF3-0xFF"],
        },
        "locales": locale_reports,
        "nativeBoundary": {
            "backingRowToCsv": "proven",
            "conditionalProducer": "proven",
            "conditionalProducerReference": (
                "xivl-client-structs:manifests/autotranslate_wire_format_study.json"
                "#AT-COMP-017"
            ),
            "conditionalProducerRevision": "ad17cb88572f831ebfffc96f3766c4df5733afa7",
            "historicalDeliveryAndLocale": "qualified",
            "textModuleOutputAndAdmission": "qualified",
            "selectedFamilyAndKey": "qualified",
            "render": "qualified",
            "statement": (
                "AT-COMP-017 proves conditional descriptor/category -> ExcelSheet -> "
                "ready CacheAll CB1990 -> C9DC80 -> C9C670 ordinary-record "
                "production; the category marker and target key remain separate. "
                "This backing-file and CSV report does not establish historical "
                "delivery or locale, TextModule output or admission, the selected "
                "family or key, or rendering."
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
                raise ValueError("place_name_backing_rows.json is out of date")
            print("PASS: place-name backing-row report is deterministic")
        else:
            OUTPUT.write_bytes(rendered)
            print(f"wrote {OUTPUT.name} ({len(rendered)} bytes)")
    except (OSError, ValueError, KeyError, StopIteration, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
