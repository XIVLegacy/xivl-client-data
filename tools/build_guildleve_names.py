#!/usr/bin/env python3
"""Build the complete guildleve ID to English/Japanese display-name join."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path

from _csv_reader import CsvRow, read_csv
from _csv_root import add_csv_dir_argument, validate_csv_dir

REPO = Path(__file__).resolve().parent.parent
OUTPUT = REPO / "derived/guildleve_names.csv"
MANIFEST = REPO / "manifests/guildleve_names.json"
FIELDS = [
    "guildleve_id",
    "name_en",
    "name_ja",
    "placeholder",
    "category",
    "source_sheet",
    "source_row",
]
NO_TRANSLATION = "\u7ffb\u8a33\u4e0d\u8981"
PLACEHOLDERS = ("x", "dummy", NO_TRANSLATION)
CATEGORIES = {1: "battlecraft", 2: "fieldcraft"}
SOURCE_LAYOUTS = {
    "guildleve.csv": (63, {1: "s32"}),
    "xtx_guildleve.csv": (89, {9: "str", 10: "str"}),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def load_source(path: Path) -> dict[int, CsvRow]:
    width, types = SOURCE_LAYOUTS[path.name]
    header, row_iterator = read_csv(path)
    rows = list(row_iterator)
    indexed = {}
    if (
        header.column_indices != [str(index) for index in range(width)]
        or len(header.column_types) != width
        or any(header.column_types[index] != value for index, value in types.items())
    ):
        raise ValueError(f"{path.name}: unexpected source layout")
    for row in rows:
        row_id = int(row.row_id)
        if row_id in indexed:
            raise ValueError(f"{path.name}: duplicate row id {row_id}")
        indexed[row_id] = row
    return indexed


def project(guildleves: dict[int, CsvRow], names: dict[int, CsvRow]) -> list[dict]:
    if guildleves.keys() != names.keys():
        raise ValueError("guildleve and xtx/guildleve row IDs must match exactly")
    output = []
    for row_id, row in sorted(guildleves.items()):
        text = names[row_id].values
        output.append(
            {
                "guildleve_id": row_id,
                "name_en": text[10],
                "name_ja": text[9],
                "placeholder": "true" if text[10] in PLACEHOLDERS else "false",
                "category": CATEGORIES.get(int(row.values[1]), "other"),
                "source_sheet": "xtx/guildleve",
                "source_row": row_id,
            }
        )
    return output


def render(rows: list[dict]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def id_ranges(ids: list[int]) -> list[list[int]]:
    ranges: list[list[int]] = []
    for row_id in sorted(ids):
        if ranges and row_id == ranges[-1][1] + 1:
            ranges[-1][1] = row_id
        else:
            ranges.append([row_id, row_id])
    return ranges


def build(csv_dir: Path) -> dict[Path, bytes]:
    validate_csv_dir(csv_dir)
    tables = {
        entry["name"]: entry
        for entry in json.loads(
            (REPO / "manifests/tables.json").read_text(encoding="utf-8")
        )
    }
    sources = []
    indexed = {}
    for name in SOURCE_LAYOUTS:
        data = (csv_dir / name).read_bytes()
        expected = tables[name]
        if len(data) != expected["bytes"] or digest(data) != expected["sha256"].upper():
            raise ValueError(f"{name}: source bytes differ from tables.json")
        indexed[name] = load_source(csv_dir / name)
        if len(indexed[name]) != expected["dataRowCount"]:
            raise ValueError(f"{name}: source row count differs from tables.json")
        sources.append(
            {
                "path": f"csv/{name}",
                "bytes": len(data),
                "sha256": digest(data),
                "rowCount": len(indexed[name]),
            }
        )
    rows = project(indexed["guildleve.csv"], indexed["xtx_guildleve.csv"])
    payload = render(rows)
    duplicates = defaultdict(list)
    for row in rows:
        if row["placeholder"] == "false":
            duplicates[(row["name_en"], row["name_ja"])].append(row["guildleve_id"])
    manifest = {
        "schemaVersion": 1,
        "extractionVersion": "2012.09.19.0001",
        "sourceEvidenceClass": "client_extraction",
        "sources": sources,
        "columnMappings": {
            "guildleve.csv": {"rowId": "guildleve_id", "1": "classType"},
            "xtx_guildleve.csv": {
                "rowId": "source_row",
                "9": "name_ja",
                "10": "name_en",
            },
        },
        "categoryRules": {"1": "battlecraft", "2": "fieldcraft", "otherwise": "other"},
        "output": {
            "path": "derived/guildleve_names.csv",
            "bytes": len(payload),
            "sha256": digest(payload),
            "rowCount": len(rows),
            "placeholderCount": sum(row["placeholder"] == "true" for row in rows),
            "categoryCounts": dict(
                sorted(Counter(row["category"] for row in rows).items())
            ),
        },
        "placeholderRanges": [
            {
                "nameEn": marker,
                "ranges": id_ranges(
                    [row["guildleve_id"] for row in rows if row["name_en"] == marker]
                ),
            }
            for marker in PLACEHOLDERS
        ],
        "duplicateNameGroups": [
            {"nameEn": en, "nameJa": ja, "guildleveIds": ids}
            for (en, ja), ids in sorted(duplicates.items())
            if len(ids) > 1
        ],
    }
    return {
        OUTPUT: payload,
        MANIFEST: (json.dumps(manifest, ensure_ascii=True, indent=2) + "\n").encode(
            "ascii"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_csv_dir_argument(parser)
    parser.add_argument(
        "--check", action="store_true", help="verify generated files without writing"
    )
    args = parser.parse_args()
    outputs = build(args.csv_dir)
    if args.check:
        stale = [
            path
            for path, data in outputs.items()
            if not path.is_file() or path.read_bytes() != data
        ]
        for path in stale:
            print(f"out of date: {path.relative_to(REPO)}")
        if stale:
            return 1
        print("verified guildleve names and manifest")
    else:
        for path, data in outputs.items():
            path.write_bytes(data)
            print(f"wrote {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
