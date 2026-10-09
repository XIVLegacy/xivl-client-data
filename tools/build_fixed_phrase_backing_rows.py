"""Compare fixed-phrase backing rows with the authenticated merged CSV."""

from __future__ import annotations

import argparse
import hashlib
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from _csv_root import add_csv_dir_argument, validate_csv_dir
from build_autotranslate_name_crosswalk import (
    _load_source,
    _load_table_manifest,
    render,
)
from compare_sheet_inventory import load_inventory, parse_document, resource_path

REPO = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "manifests" / "fixed_phrase_backing_rows.json"
SHEET = "xtx/_fixedPhrase"
CSV = "xtx__fixedPhrase.csv"
LOCALES = ("ja", "en", "de", "fr", "chs")
ANCHORS = (100, 311, 430, 974, 1255, 2104, 2106, 2115, 2118, 2133, 3025)


def identity(raw: bytes, resource_id: int) -> dict:
    return {
        "resourceId": f"0x{resource_id:08X}",
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest().upper(),
    }


def read_ranges(
    raw: bytes, begin: int, count: int
) -> tuple[list[tuple[int, int]], list[int]]:
    if len(raw) % 8:
        raise ValueError("enable file has an incomplete pair")
    ranges = list(struct.iter_unpack("<II", raw))
    keys = []
    previous_end = begin
    for base, length in ranges:
        if not length or base < previous_end or base + length > begin + count:
            raise ValueError("enable range is empty, unordered or outside the block")
        keys.extend(range(base, base + length))
        previous_end = base + length
    return ranges, keys


def row_spans(
    raw: bytes, data_size: int, begin: int, count: int
) -> dict[int, tuple[int, int]]:
    if len(raw) % 4 or len(raw) // 4 > count:
        raise ValueError("offset file has an incomplete or extra entry")
    spans = {}
    start = 0
    for slot, (end,) in enumerate(struct.iter_unpack("<I", raw)):
        if end < start or end > data_size:
            raise ValueError("row offset is decreasing or outside the data file")
        if end > start:
            spans[begin + slot] = (start, end)
        start = end
    if start != data_size:
        raise ValueError("offset file does not consume the data file")
    return spans


def metadata_prefix(row: bytes) -> tuple[int, str]:
    if len(row) < 6:
        raise ValueError("row is shorter than its metadata prefix")
    field0, length = struct.unpack_from("<IH", row)
    if not length or 6 + length > len(row):
        raise ValueError("metadata string is truncated")
    body = row[6 : 6 + length]
    if body[0] == 0xFF:
        body = bytes(value ^ 0x73 for value in body[1:])
    if not body or body[-1] != 0:
        raise ValueError("metadata string lacks its terminator")
    return field0, body[:-1].decode("utf-8")


def key_digest(keys: list[int]) -> str:
    return (
        hashlib.sha256(b"".join(struct.pack("<I", key) for key in keys))
        .hexdigest()
        .upper()
    )


def build(client_root: Path, csv_dir: Path) -> dict:
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
    if not any(
        row.get("name") == SHEET and row.get("infofile") == str(entry["resourceId"])
        for row in references
    ):
        raise ValueError(
            "game master does not name the inventory's fixed-phrase resource"
        )
    schema_path = resource_path(data_root, entry["resourceId"])
    sheets = parse_document(schema_path).findall("sheet")
    if [sheet.get("lang") for sheet in sheets] != list(LOCALES):
        raise ValueError("fixed-phrase locale definitions differ")
    header, rows, source = _load_source(
        validate_csv_dir(csv_dir), CSV, _load_table_manifest()[CSV]
    )
    if header.column_types != ["u32", *(["str"] * 11)]:
        raise ValueError("fixed-phrase CSV column types differ")
    csv_keys = [int(row.row_id) for row in rows]
    csv_rows = {int(row.row_id): row for row in rows}
    csv_ordinals = {key: index for index, key in enumerate(csv_keys)}
    locale_reports = []
    metadata_by_key: dict[int, dict[str, str]] = {}
    union: set[int] = set()
    for sheet in sheets:
        locale = sheet.get("lang")
        if sheet.get("name") != SHEET:
            raise ValueError("unexpected sheet name")
        columns = [int(param.text) for param in sheet.findall("./index/param")]
        if [param.text for param in sheet.findall("./type/param")] != [
            "u32",
            "str",
            "str",
            "str",
        ] or columns[:2] != [0, 1]:
            raise ValueError("fixed-phrase backing columns differ")
        blocks = sheet.findall("./block/file")
        if len(blocks) != 1:
            raise ValueError("fixed-phrase definition does not have one block")
        block = blocks[0]
        begin, count = int(block.get("begin")), int(block.get("count"))
        resource_ids = {
            "data": int(block.text),
            "enable": int(block.get("enable")),
            "offsets": int(block.get("offset")),
        }
        resources = {
            kind: resource_path(data_root, rid).read_bytes()
            for kind, rid in resource_ids.items()
        }
        ranges, keys = read_ranges(resources["enable"], begin, count)
        spans = row_spans(resources["offsets"], len(resources["data"]), begin, count)
        if keys != list(spans):
            raise ValueError(f"{locale}: enable ranges differ from nonempty row spans")
        if not set(keys) <= csv_rows.keys():
            raise ValueError(f"{locale}: backing rows are absent from the merged CSV")
        union.update(keys)
        anchors = []
        for ordinal, key in enumerate(keys):
            start, end = spans[key]
            field0, field1 = metadata_prefix(resources["data"][start:end])
            if str(field0) != csv_rows[key].values[0]:
                raise ValueError(f"{locale}: row {key} field 0 differs from the CSV")
            metadata_by_key.setdefault(key, {})[locale] = field1
            if key in ANCHORS:
                range_index, pair = next(
                    (index, pair)
                    for index, pair in enumerate(ranges)
                    if pair[0] <= key < pair[0] + pair[1]
                )
                anchors.append(
                    {
                        "csvRecordId": f"fixedPhrase:{key}",
                        "rowKey": key,
                        "enabledOrdinal": ordinal,
                        "csvIterationIndex": csv_ordinals[key],
                        "rangeIndex": range_index,
                        "rangeBase": pair[0],
                        "rangeCount": pair[1],
                        "dataSpan": {"start": start, "end": end},
                        "field0": field0,
                        "field1": field1,
                    }
                )
        locale_reports.append(
            {
                "locale": locale,
                "nameColumns": columns[2:],
                "declaredSlotCount": count,
                "offsetEntryCount": len(resources["offsets"]) // 4,
                "enabledRangeCount": len(ranges),
                "enabledRowCount": len(keys),
                "enabledKeySha256": key_digest(keys),
                "enableMatchesNonemptySpans": True,
                "field0MatchesCsvCount": len(keys),
                "csvOnlyKeys": sorted(set(csv_keys) - set(keys)),
                "sources": {
                    kind: identity(raw, resource_ids[kind])
                    for kind, raw in resources.items()
                },
                "anchors": anchors,
            }
        )
    if union != csv_rows.keys():
        raise ValueError("locale row union differs from merged CSV keys")
    differences = []
    for key, values in sorted(metadata_by_key.items()):
        csv_cell = csv_rows[key].values[1]
        if any(
            value.replace("\\", "\\\\").replace("[", "\\[") != csv_cell
            for value in values.values()
        ):
            differences.append(
                {
                    "rowKey": key,
                    "csvField1": csv_cell,
                    "backingField1ByLocale": values,
                }
            )
    return {
        "schemaVersion": 1,
        "evidenceClass": "client_extraction",
        "extractionVersion": versions["game.ver"],
        "sheet": SHEET,
        "sourceMaster": identity(master.read_bytes(), 0x01030000),
        "sourceDefinition": identity(schema_path.read_bytes(), entry["resourceId"]),
        "sourceCsv": source,
        "csvKeySha256": key_digest(csv_keys),
        "method": "Compare enabled keys, nonempty offset spans and field 0 against the merged CSV; retain sparse backing-row metadata and locale column locators. Key digests hash ordered little-endian u32 values.",
        "locales": locale_reports,
        "metadataDifferences": differences,
        "nativeBoundary": {
            "reference": "xivl-client-structs:manifests/autotranslate_wire_format_study.json, AT-COMP-010/011 and AT-CHAT-001/002/003",
            "revision": "6b53147c8afca1a13bd9c753b39662aaa964da3b",
            "enableRangesToNativeBackend": "unproved",
            "selectedInstanceAndLocale": "unobserved",
            "nativeKeyEqualsCsvRowId": "unproved",
            "statement": "Backing-file ordinals are not observed Completion indices. No selected native key, category, control or receive/render lookup is assigned a CSV row identity.",
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
                raise ValueError("fixed_phrase_backing_rows.json is out of date")
            print("PASS: fixed-phrase backing-row report is deterministic")
        else:
            OUTPUT.write_bytes(rendered)
            print(f"wrote {OUTPUT.name} ({len(rendered)} bytes)")
    except (OSError, ValueError, KeyError, StopIteration, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
