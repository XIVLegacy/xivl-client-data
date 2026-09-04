#!/usr/bin/env python3
"""Build and verify the retail map-marker resource crosswalk."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from _csv_reader import CsvHeader, CsvRow, read_csv
from _csv_root import add_csv_dir_argument, default_csv_dir

REPO = Path(__file__).resolve().parent.parent
CSV_DIR = default_csv_dir()
DERIVED_OUT = REPO / "derived" / "map_marker_resource_crosswalk.csv"
MANIFEST_OUT = REPO / "manifests" / "map_marker_resources.json"
TABLES = REPO / "manifests" / "tables.json"
SHEET_INVENTORY = REPO / "manifests" / "sheet_inventory.csv"
EXTRACTION_VERSION = "2012.09.19.0001"
GENERATED_ON = "2026-08-27"
SEARCH_TERMS = (
    "MapScreenControl",
    "group_marker_data",
    "MapMarkerParty",
    "Update",
)


@dataclass(frozen=True)
class SourceSpec:
    width: int
    resource_path: int
    resource_instance: int
    ui_class: int | None
    visibility: int | None
    coordinate_columns: tuple[int, ...]


SOURCE_SPECS = {
    "2Dmap_actor_data.csv": SourceSpec(3, 1, 2, None, None, ()),
    "2Dmap_marker.csv": SourceSpec(18, 8, 9, 13, 15, (1, 2)),
    "quest_marker.csv": SourceSpec(14, 6, 7, 11, 13, (2, 3)),
}


def load_source(path: Path, spec: SourceSpec) -> tuple[CsvHeader, list[CsvRow]]:
    header, iterator = read_csv(path)
    rows = list(iterator)
    if len(header.column_indices) != spec.width:
        raise ValueError(f"{path.name}: label width is not {spec.width}")
    if len(header.column_types) != spec.width:
        raise ValueError(f"{path.name}: type width is not {spec.width}")
    bad_rows = [row.row_id for row in rows if len(row.values) != spec.width]
    if bad_rows:
        raise ValueError(f"{path.name}: truncated rows {bad_rows[:10]}")
    return header, rows


def grouped_rows(
    loaded: dict[str, tuple[CsvHeader, list[CsvRow]]],
) -> list[list[object]]:
    output: list[list[object]] = []
    for name, spec in SOURCE_SPECS.items():
        _header, rows = loaded[name]
        groups: dict[tuple[str, str, str, str], list[int]] = {}
        for row in rows:
            key = (
                row.values[spec.resource_path],
                row.values[spec.resource_instance],
                row.values[spec.ui_class] if spec.ui_class is not None else "",
                row.values[spec.visibility] if spec.visibility is not None else "",
            )
            groups.setdefault(key, []).append(int(row.row_id))
        for key, row_ids in sorted(groups.items()):
            output.append([name, *key, len(row_ids), min(row_ids), max(row_ids)])
    return output


def render_crosswalk(rows: list[list[object]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(
        [
            "source_sheet",
            "resource_path",
            "resource_instance",
            "ui_class",
            "visibility",
            "row_count",
            "first_row_id",
            "last_row_id",
        ]
    )
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def vocabulary_search(csv_dir: Path) -> tuple[int, list[dict[str, object]]]:
    paths = sorted(csv_dir.glob("*.csv"))
    texts = [(path.name, path.read_text(encoding="utf-8")) for path in paths]
    results = []
    for term in SEARCH_TERMS:
        normalized_term = _normalize(term)
        exact = sum(text.count(term) for _name, text in texts)
        casefolded = sum(
            text.casefold().count(term.casefold()) for _name, text in texts
        )
        normalized = sum(
            _normalize(text).count(normalized_term) for _name, text in texts
        )
        matching_files = sorted(
            name for name, text in texts if term.casefold() in text.casefold()
        )
        results.append(
            {
                "term": term,
                "exactSubstringCount": exact,
                "caseInsensitiveSubstringCount": casefolded,
                "normalizedTokenCount": normalized,
                "caseInsensitiveMatchingFiles": matching_files,
            }
        )
    return len(paths), results


def _property_summary(
    rows: list[CsvRow], column: int, expected_prefix: str
) -> dict[str, object]:
    values = [row.values[column] for row in rows]
    matches = [value for value in values if value.startswith(expected_prefix)]
    return {
        "column": str(column),
        "expectedPrefix": expected_prefix,
        "rowCount": len(values),
        "matchingRowCount": len(matches),
        "distinctValueCount": len(set(values)),
        "nonmatchingValues": sorted(set(values) - set(matches)),
    }


def _coordinate_summary(
    header: CsvHeader, rows: list[CsvRow], columns: tuple[int, ...]
) -> list[dict[str, object]]:
    output = []
    for column in columns:
        values = [float(row.values[column]) for row in rows]
        output.append(
            {
                "column": str(column),
                "declaredType": header.column_types[column],
                "nonemptyCount": len(values),
                "distinctValueCount": len(set(values)),
                "minimum": min(values),
                "maximum": max(values),
            }
        )
    return output


def build(csv_dir: Path = CSV_DIR) -> dict[Path, bytes]:
    tables = {
        entry["name"]: entry for entry in json.loads(TABLES.read_text(encoding="utf-8"))
    }
    with SHEET_INVENTORY.open(encoding="utf-8", newline="") as handle:
        inventory = {row["name"] + ".csv": row for row in csv.DictReader(handle)}

    loaded = {
        name: load_source(csv_dir / name, spec) for name, spec in SOURCE_SPECS.items()
    }
    crosswalk_rows = grouped_rows(loaded)
    crosswalk = render_crosswalk(crosswalk_rows)

    audits = []
    headers = {}
    resources = {}
    coordinates = {}
    for name, spec in SOURCE_SPECS.items():
        header, rows = loaded[name]
        table = tables[name]
        sheet = inventory[name]
        if len(rows) != table["dataRowCount"]:
            raise ValueError(
                f"{name}: {len(rows)} rows != manifest {table['dataRowCount']}"
            )
        audits.append(
            {
                "sheet": name,
                "source": sheet["source"],
                "resourceId": int(sheet["resource_id"]),
                "resourceIdHex": sheet["resource_id_hex"],
                "dataRowCount": len(rows),
                "sheetColumnCount": spec.width,
                "sha256": table["sha256"],
            }
        )
        headers[name] = {
            "columnIndices": header.column_indices,
            "columnTypes": header.column_types,
        }
        resources[name] = {
            "resourcePathColumn": str(spec.resource_path),
            "resourceInstanceColumn": str(spec.resource_instance),
            "uiClassColumn": (
                str(spec.ui_class) if spec.ui_class is not None else None
            ),
            "visibilityColumn": (
                str(spec.visibility) if spec.visibility is not None else None
            ),
            "resourcePaths": sorted(
                Counter(row.values[spec.resource_path] for row in rows).items()
            ),
            "resourceInstanceCount": len(
                {row.values[spec.resource_instance] for row in rows}
            ),
            "uiClasses": (
                sorted(Counter(row.values[spec.ui_class] for row in rows).items())
                if spec.ui_class is not None
                else []
            ),
            "visibilityValues": (
                sorted(Counter(row.values[spec.visibility] for row in rows).items())
                if spec.visibility is not None
                else []
            ),
        }
        coordinates[name] = _coordinate_summary(header, rows, spec.coordinate_columns)

    table_count, searches = vocabulary_search(csv_dir)
    manifest = {
        "schemaVersion": 1,
        "generatedOn": GENERATED_ON,
        "extractionVersion": EXTRACTION_VERSION,
        "sourceEvidenceClass": "client_extraction",
        "sheetAudit": audits,
        "sourceHeaders": headers,
        "resourceColumns": resources,
        "propertyReferences": {
            "2Dmap_marker.csv": _property_summary(
                loaded["2Dmap_marker.csv"][1], 14, "@5204/i"
            ),
            "quest_marker.csv": _property_summary(
                loaded["quest_marker.csv"][1], 12, "@5208/i"
            ),
        },
        "coordinateColumns": coordinates,
        "vocabularySearch": {
            "domain": "decoded csv/*.csv raw UTF-8 text",
            "tableCount": table_count,
            "normalization": "Unicode casefold, then remove non-ASCII-alphanumeric characters",
            "results": searches,
        },
        "output": {
            "path": "derived/map_marker_resource_crosswalk.csv",
            "rowCount": len(crosswalk_rows),
            "sha256": hashlib.sha256(crosswalk).hexdigest().upper(),
        },
        "claimLimits": [
            "The crosswalk establishes static resource and UI-property vocabulary, not a runtime call relationship to s2c 0x018D.",
            "Numeric source columns remain raw positions; their order does not assign any 0x018D wire offset.",
            "The corpus types coordinate-bearing columns but does not by itself identify a world-to-map transform.",
            "Generic localized uses of Update do not establish the exact runtime Update property operation.",
        ],
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=True, indent=2) + "\n").encode(
        "ascii"
    )
    return {DERIVED_OUT: crosswalk, MANIFEST_OUT: manifest_bytes}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_csv_dir_argument(parser)
    parser.add_argument(
        "--check", action="store_true", help="verify generated files without writing"
    )
    args = parser.parse_args()
    outputs = build(args.csv_dir)
    if args.check:
        mismatches = [
            path
            for path, data in outputs.items()
            if not path.is_file() or path.read_bytes() != data
        ]
        if mismatches:
            for path in mismatches:
                print(f"out of date: {path.relative_to(REPO)}")
            return 1
        print(f"verified {len(outputs)} map-marker resource artifact(s)")
        return 0
    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"wrote {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
