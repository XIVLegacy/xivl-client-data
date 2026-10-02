#!/usr/bin/env python3
"""Build the authenticated localized-name crosswalk.

The product records CSV row keys and localized source fields.  It does not
infer an auto-translate wire token or select one zone/layout when a place name
has multiple candidates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from _csv_reader import CsvHeader, CsvRow, read_csv
from _csv_root import add_csv_dir_argument, default_csv_dir, validate_csv_dir


REPO = Path(__file__).resolve().parents[1]
TABLE_MANIFEST = REPO / "manifests" / "tables.json"
CORPUS_MANIFEST = REPO / "manifests" / "private_csv_corpus.json"
ZONE_PRODUCT = REPO / "manifests" / "zone_internal_names.json"
OUTPUT = REPO / "derived" / "autotranslate_name_crosswalk.json"

TABLES = (
    "xtx__fixedPhrase.csv",
    "_item.csv",
    "itemData.csv",
    "xtx_itemName.csv",
    "xtx_placeName.csv",
    "_zoneParam.csv",
    "_layout.csv",
    "zoneGroupParam.csv",
)

# zoneGroupParam's region code is column 0; the existing zones mapping treats
# columns 1-5 as independent zone memberships. Keep every occurrence.
ZONE_GROUP_MEMBERSHIP_COLUMNS = tuple(range(1, 6))

# These are raw field positions in the shipped sheets.  Several locale fields
# are retained per language because they contain grammatical or encoded forms.
LOCALE_COLUMNS = {
    "fixedPhrase": {
        "ja": (2, 3),
        "en": (4, 5),
        "de": (6, 7),
        "fr": (8, 9),
    },
    "itemName": {
        "ja": (4,),
        "en": (5, 6, 7),
        "de": (11, 12, 14),
        "fr": (19, 20, 21),
    },
    "placeName": {
        "ja": (0,),
        "en": (1, 2),
        "de": (4, 5),
        "fr": (6, 7),
    },
}

# These shipped fields are retained as raw values but are outside the required
# Japanese/English/German/French name index. No locale or grammatical meaning
# is assigned to them here.
UNSUPPORTED_LOCALE_COLUMNS = {
    "fixedPhrase": (10, 11),
    "itemName": (25, 26, 27, 28, 29, 30, 31, 32, 131, 132, 133, 134),
    "placeName": (8,),
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name}: expected an object")
    return value


def _load_table_manifest() -> dict[str, dict[str, Any]]:
    raw = json.loads(TABLE_MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("tables.json: expected a list")
    result: dict[str, dict[str, Any]] = {}
    for entry in raw:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            raise ValueError("tables.json: invalid entry")
        result[entry["name"]] = entry
    return result


def _load_source(
    csv_dir: Path, name: str, manifest: dict[str, Any]
) -> tuple[CsvHeader, list[CsvRow], dict[str, Any]]:
    path = csv_dir / name
    data = path.read_bytes()
    actual_hash = _sha256(data)
    expected_hash = str(manifest["sha256"]).upper()
    if len(data) != int(manifest["bytes"]) or actual_hash != expected_hash:
        raise ValueError(
            f"{name}: authenticated source mismatch "
            f"(bytes={len(data)}, sha256={actual_hash})"
        )
    header, iterator = read_csv(path)
    rows = list(iterator)
    if len(rows) != int(manifest["dataRowCount"]):
        raise ValueError(
            f"{name}: {len(rows)} rows != manifest {manifest['dataRowCount']}"
        )
    if len(header.column_indices) != len(header.column_types):
        raise ValueError(f"{name}: header width mismatch")
    seen: set[str] = set()
    for row in rows:
        if row.row_id in seen:
            raise ValueError(f"{name}: duplicate row id {row.row_id}")
        seen.add(row.row_id)
        if len(row.values) != len(header.column_indices):
            raise ValueError(f"{name}: row {row.row_id} width mismatch")
    source = {
        "sheet": name,
        "bytes": int(manifest["bytes"]),
        "dataRowCount": len(rows),
        "sha256": expected_hash,
        "columnTypes": header.column_types,
    }
    return header, rows, source


def _number(value: str) -> int:
    return int(value)


def _raw_fields(row: CsvRow) -> dict[str, str]:
    return {str(index): value for index, value in enumerate(row.values)}


def _localized_fields(row: CsvRow, family: str) -> dict[str, dict[str, str | None]]:
    result: dict[str, dict[str, str | None]] = {}
    for locale, columns in LOCALE_COLUMNS[family].items():
        result[locale] = {
            str(column): (row.values[column] or None) for column in columns
        }
    return result


def _unsupported_locale_fields(row: CsvRow, family: str) -> dict[str, str | None]:
    return {
        str(column): (row.values[column] or None)
        for column in UNSUPPORTED_LOCALE_COLUMNS[family]
    }


def _row_source(sheet: str, row: CsvRow) -> dict[str, Any]:
    # CSV rows are keyed by the extraction row id. Do not manufacture a line
    # locator after sorting: quoted multiline cells make physical lines lossy.
    return {"sheet": sheet, "rowId": row.row_id}


def _sort_rows(rows: list[CsvRow]) -> list[CsvRow]:
    return sorted(rows, key=lambda row: int(row.row_id))


def _group_memberships(
    rows: list[CsvRow],
) -> dict[str, list[tuple[CsvRow, int]]]:
    """Index every zone membership and its authoritative source column."""
    memberships: dict[str, list[tuple[CsvRow, int]]] = defaultdict(list)
    for row in rows:
        for column in ZONE_GROUP_MEMBERSHIP_COLUMNS:
            zone_id = row.values[column]
            if zone_id not in ("", "0"):
                memberships[zone_id].append((row, column))
    return memberships


def _ambiguity_groups(
    records: list[dict[str, Any]], family: str
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, int, str], list[tuple[str, int]]] = defaultdict(list)
    for record in records:
        key = record["id"]
        numeric_key = int(record["key"])
        for locale, fields in record["names"].items():
            for column, value in fields.items():
                if value is not None:
                    grouped[(locale, int(column), value)].append((key, numeric_key))

    output = []
    for (locale, column, value), members in sorted(
        grouped.items(), key=lambda item: (item[0][0], item[0][1], item[0][2])
    ):
        ids = sorted({item[0] for item in members})
        if len(ids) < 2:
            continue
        keys = sorted({item[1] for item in members})
        output.append(
            {
                "family": family,
                "locale": locale,
                "column": column,
                "name": value,
                "recordIds": ids,
                "keys": keys,
                "keyCount": len(keys),
            }
        )
    return output


def _family_presence(
    records: list[dict[str, Any]], family: str
) -> dict[str, dict[str, int]]:
    counts = {
        locale: {str(column): 0 for column in columns}
        for locale, columns in LOCALE_COLUMNS[family].items()
    }
    for record in records:
        for locale, fields in record["names"].items():
            for column, value in fields.items():
                if value is not None:
                    counts[locale][column] += 1
    return counts


def _unsupported_presence(records: list[dict[str, Any]], family: str) -> dict[str, int]:
    counts = {str(column): 0 for column in UNSUPPORTED_LOCALE_COLUMNS[family]}
    for record in records:
        for column, value in record["unsupportedLocaleFields"].items():
            if value is not None:
                counts[column] += 1
    return counts


def _load_zone_product() -> tuple[dict[str, Any], str]:
    data = ZONE_PRODUCT.read_bytes()
    product = json.loads(data.decode("utf-8"))
    if not isinstance(product, dict):
        raise ValueError("zone_internal_names.json: expected an object")
    return product, _sha256(data)


def build(csv_dir: Path = default_csv_dir()) -> dict[str, Any]:
    """Build the crosswalk from one fully authenticated CSV root."""
    csv_dir = validate_csv_dir(csv_dir)
    table_manifest = _load_table_manifest()
    loaded: dict[str, tuple[CsvHeader, list[CsvRow], dict[str, Any]]] = {}
    for name in TABLES:
        if name not in table_manifest:
            raise ValueError(f"tables.json: missing {name}")
        loaded[name] = _load_source(csv_dir, name, table_manifest[name])

    fixed_rows = _sort_rows(loaded["xtx__fixedPhrase.csv"][1])
    item_rows = _sort_rows(loaded["xtx_itemName.csv"][1])
    item_index = {row.row_id: row for row in item_rows}
    item_sheet_rows = {
        name: {row.row_id: row for row in _sort_rows(loaded[name][1])}
        for name in ("_item.csv", "itemData.csv")
    }
    if set(item_index) != set(item_sheet_rows["_item.csv"]) or set(item_index) != set(
        item_sheet_rows["itemData.csv"]
    ):
        raise ValueError("item name join is not complete and one-to-one")

    place_rows = _sort_rows(loaded["xtx_placeName.csv"][1])
    place_index = {row.row_id: row for row in place_rows}
    zone_rows = _sort_rows(loaded["_zoneParam.csv"][1])
    layout_rows = _sort_rows(loaded["_layout.csv"][1])
    group_rows = _sort_rows(loaded["zoneGroupParam.csv"][1])
    layouts_by_place: dict[str, list[CsvRow]] = defaultdict(list)
    for row in layout_rows:
        place_id = row.values[3]
        if place_id:
            layouts_by_place[place_id].append(row)
    groups_by_zone = _group_memberships(group_rows)

    zone_product, zone_product_hash = _load_zone_product()
    internal_by_zone: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for binding in zone_product.get("zoneBindings", []):
        if isinstance(binding, dict) and "zoneId" in binding:
            internal_by_zone[int(binding["zoneId"])].append(
                {
                    "zoneId": int(binding["zoneId"]),
                    "layoutId": int(binding["layoutId"]),
                    "zoneName": binding["zoneName"],
                    "basis": binding["basis"],
                }
            )

    fixed: list[dict[str, Any]] = []
    for row in fixed_rows:
        key = _number(row.row_id)
        fixed.append(
            {
                "id": f"fixedPhrase:{key}",
                "key": key,
                "field0": {"column": 0, "value": row.values[0] or None},
                "field1": {"column": 1, "value": row.values[1] or None},
                "names": _localized_fields(row, "fixedPhrase"),
                "unsupportedLocaleFields": _unsupported_locale_fields(
                    row, "fixedPhrase"
                ),
                "source": _row_source("xtx__fixedPhrase.csv", row),
            }
        )

    items: list[dict[str, Any]] = []
    for row in item_rows:
        key = _number(row.row_id)
        items.append(
            {
                "id": f"item:{key}",
                "key": key,
                "names": _localized_fields(row, "itemName"),
                "unsupportedLocaleFields": _unsupported_locale_fields(row, "itemName"),
                "joinRows": {
                    "_item": _row_source(
                        "_item.csv",
                        item_sheet_rows["_item.csv"][row.row_id],
                    ),
                    "itemData": _row_source(
                        "itemData.csv",
                        item_sheet_rows["itemData.csv"][row.row_id],
                    ),
                    "xtx_itemName": _row_source("xtx_itemName.csv", row),
                },
                "rawJoinFields": {
                    "_item.0": item_sheet_rows["_item.csv"][row.row_id].values[0]
                    or None
                },
            }
        )

    places: list[dict[str, Any]] = []
    for row in place_rows:
        key = _number(row.row_id)
        places.append(
            {
                "id": f"placeName:{key}",
                "key": key,
                "names": _localized_fields(row, "placeName"),
                "unsupportedLocaleFields": _unsupported_locale_fields(row, "placeName"),
                "source": _row_source("xtx_placeName.csv", row),
            }
        )

    zones: list[dict[str, Any]] = []
    for row in zone_rows:
        zone_id = _number(row.row_id)
        place_id = row.values[0] or None
        layouts = layouts_by_place.get(place_id, []) if place_id else []
        groups = groups_by_zone.get(row.row_id, [])
        zones.append(
            {
                "id": f"zone:{zone_id}",
                "key": zone_id,
                "placeNameId": int(place_id) if place_id else None,
                "placeNameRecordId": (
                    f"placeName:{place_id}" if place_id in place_index else None
                ),
                "zoneParam": {
                    "source": _row_source("_zoneParam.csv", row),
                    "columns": _raw_fields(row),
                },
                "zoneGroupParamCandidates": [
                    {
                        "membershipColumn": column,
                        "membershipValue": row.row_id,
                        "source": _row_source("zoneGroupParam.csv", group),
                        "columns": _raw_fields(group),
                    }
                    for group, column in groups
                ],
                "layoutCandidates": [
                    {
                        "source": _row_source("_layout.csv", layout),
                        "columns": _raw_fields(layout),
                    }
                    for layout in layouts
                ],
                "internalNameCandidates": internal_by_zone.get(zone_id, []),
            }
        )

    ambiguity = {
        "fixedPhrase": _ambiguity_groups(fixed, "fixedPhrase"),
        "itemName": _ambiguity_groups(items, "itemName"),
        "placeName": _ambiguity_groups(places, "placeName"),
    }
    source_tables = [loaded[name][2] for name in TABLES]
    corpus = _read_json(CORPUS_MANIFEST)
    source_archive = {
        "inputId": corpus["inputId"],
        "checkId": corpus["checkId"],
        "archiveBytes": corpus["archive"]["bytes"],
        "archiveSha256": str(corpus["archive"]["sha256"]).upper(),
        "expandedFileCount": corpus["expanded"]["fileCount"],
        "expandedTotalBytes": corpus["expanded"]["totalBytes"],
        "expandedTreeSha256": str(corpus["expanded"]["treeSha256"]).upper(),
    }
    return {
        "schemaVersion": 1,
        "extractionVersion": "2012.09.19.0001",
        "evidenceClass": "client_extraction",
        "method": (
            "Verify byte count and SHA-256 for eight authenticated source-row "
            "inputs; "
            "read fixedPhrase, item, place, zone, group, and layout row keys "
            "and localized cells; join item rows by equal row keys, join zone "
            "rows through _zoneParam field 0 and place-name row keys, retain "
            "all zoneGroupParam membership columns, and attach existing zone "
            "names only as source-product candidates."
        ),
        "confidence": {
            "scope": "source-cell/key equality",
            "level": "high",
            "boundary": (
                "No confidence is assigned to UI selection, wire tokens, token "
                "framing, or runtime zone/item selection."
            ),
        },
        "sourceArchive": source_archive,
        "sourceTables": source_tables,
        "sourceProducts": [
            {
                "path": "manifests/zone_internal_names.json",
                "sha256": zone_product_hash,
                "role": "existing zone-name candidates",
            }
        ],
        "localeColumns": LOCALE_COLUMNS,
        "unsupportedLocaleColumns": UNSUPPORTED_LOCALE_COLUMNS,
        "selectionBoundary": {
            "fixedPhraseToWire": "unproven",
            "wireTokenFormat": "unproven",
            "rowKeyVersusField0": "unproven",
            "statement": (
                "The CSV crosswalk does not select a wire token, decode a chat "
                "field, or choose one candidate from a duplicate localized name."
            ),
        },
        "statistics": {
            "fixedPhrase": {
                "recordCount": len(fixed),
                "localeFieldPresence": _family_presence(fixed, "fixedPhrase"),
                "unsupportedLocaleFieldPresence": _unsupported_presence(
                    fixed, "fixedPhrase"
                ),
                "ambiguityGroupCount": len(ambiguity["fixedPhrase"]),
            },
            "itemName": {
                "recordCount": len(items),
                "completeThreeSheetJoinCount": len(items),
                "localeFieldPresence": _family_presence(items, "itemName"),
                "unsupportedLocaleFieldPresence": _unsupported_presence(
                    items, "itemName"
                ),
                "ambiguityGroupCount": len(ambiguity["itemName"]),
            },
            "placeName": {
                "recordCount": len(places),
                "localeFieldPresence": _family_presence(places, "placeName"),
                "unsupportedLocaleFieldPresence": _unsupported_presence(
                    places, "placeName"
                ),
                "ambiguityGroupCount": len(ambiguity["placeName"]),
            },
            "zone": {
                "recordCount": len(zones),
                "placeNameJoinCount": sum(
                    zone["placeNameRecordId"] is not None for zone in zones
                ),
                "zonesWithMultipleLayouts": sum(
                    len(zone["layoutCandidates"]) > 1 for zone in zones
                ),
                "internalNameCandidateCount": sum(
                    len(zone["internalNameCandidates"]) for zone in zones
                ),
            },
        },
        "fixedPhrases": fixed,
        "items": items,
        "placeNames": places,
        "zones": zones,
        "ambiguityGroups": ambiguity,
    }


def render(product: dict[str, Any]) -> bytes:
    return (
        json.dumps(product, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode("ascii")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_csv_dir_argument(parser)
    parser.add_argument(
        "--check", action="store_true", help="verify the tracked output without writing"
    )
    args = parser.parse_args()
    try:
        rendered = render(build(Path(args.csv_dir)))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.check:
        try:
            current = OUTPUT.read_bytes()
        except OSError as exc:
            print(f"error: cannot read {OUTPUT}: {exc}", file=sys.stderr)
            return 1
        if current != rendered:
            print(f"error: {OUTPUT} is out of date", file=sys.stderr)
            return 1
        print(f"PASS: {OUTPUT} is deterministic")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(rendered)
    print(f"wrote {OUTPUT} ({len(rendered)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
