#!/usr/bin/env python3
"""Build local guildleve titles from the journal's xtx/quest lookup."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

from _csv_reader import CsvRow, read_csv
from _csv_root import add_csv_dir_argument, default_csv_dir, validate_csv_dir

REPO = Path(__file__).resolve().parent.parent
OUTPUT = REPO / "derived/local_guildleve_names.csv"
MANIFEST = REPO / "manifests/local_guildleve_names.json"
FIELDS = ["guildleve_id", "name_en", "name_ja", "source_sheet", "source_row"]
SOURCE_WIDTHS = {"passiveGL_craft.csv": 44, "xtx_quest.csv": 57, "xtx__text_ui.csv": 5}
TITLE_CONTROLS = {
    "ja": "[@sheet:02280fff0a7874782f7175657374e8020203]",
    "en": "[@sheet:02280fff0a7874782f7175657374e8020303]",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def index_rows(rows: list[CsvRow], source: str) -> dict[int, CsvRow]:
    indexed = {}
    for row in rows:
        key = int(row.row_id)
        if key in indexed:
            raise ValueError(f"{source}: duplicate row id {key}")
        indexed[key] = row
    return indexed


def build_rows(driver: list[CsvRow], names: list[CsvRow]) -> list[list[object]]:
    local_rows = index_rows(driver, "passiveGL_craft.csv")
    name_rows = index_rows(names, "xtx_quest.csv")
    output = []
    for key in sorted(local_rows):
        if key not in name_rows:
            raise ValueError(f"local guildleve {key}: missing xtx/quest row")
        values = name_rows[key].values
        if len(values) < 3 or not values[1] or not values[2]:
            raise ValueError(f"local guildleve {key}: missing title field")
        output.append([key, values[2], values[1], "xtx/quest", key])
    return output


def check_title_controls(rows: list[CsvRow]) -> None:
    indexed = index_rows(rows, "xtx__text_ui.csv")
    if 4219 not in indexed:
        raise ValueError("xtx__text_ui.csv: missing title control 4219")
    title = indexed[4219].values
    if title[:2] != [TITLE_CONTROLS["ja"], TITLE_CONTROLS["en"]]:
        raise ValueError("xtx__text_ui.csv: title control 4219 changed")


def render_csv(rows: list[list[object]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(FIELDS)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def build(csv_dir: Path | None = None) -> dict[Path, bytes]:
    csv_dir = validate_csv_dir(csv_dir if csv_dir is not None else default_csv_dir())
    tables = {
        entry["name"]: entry
        for entry in json.loads(
            (REPO / "manifests/tables.json").read_text(encoding="utf-8")
        )
    }
    rows_by_source = {}
    sources = []
    for name, width in SOURCE_WIDTHS.items():
        path = csv_dir / name
        digest = sha256(path.read_bytes())
        if digest != tables[name]["sha256"].upper():
            raise ValueError(f"{name}: SHA-256 differs from tables.json")
        header, row_iterator = read_csv(path)
        rows = list(row_iterator)
        if header.column_indices != [str(i) for i in range(width)]:
            raise ValueError(f"{name}: column indices changed")
        if len(header.column_types) != width:
            raise ValueError(f"{name}: type header width changed")
        if name == "xtx_quest.csv" and header.column_types[1:3] != ["str", "str"]:
            raise ValueError(f"{name}: title field types changed")
        if len(rows) != tables[name]["dataRowCount"]:
            raise ValueError(f"{name}: row count differs from tables.json")
        rows_by_source[name] = rows
        sources.append(
            {
                "file": name,
                "sha256": digest,
                "dataRowCount": len(rows),
                "columnCount": width,
            }
        )
    check_title_controls(rows_by_source["xtx__text_ui.csv"])
    rows = build_rows(
        rows_by_source["passiveGL_craft.csv"], rows_by_source["xtx_quest.csv"]
    )
    output = render_csv(rows)
    manifest = {
        "schemaVersion": 1,
        "extractionVersion": "2012.09.19.0001",
        "sourceEvidenceClass": "client_extraction",
        "sources": sources,
        "columnMappings": {
            "guildleve_id": "passiveGL_craft row id",
            "name_en": "xtx/quest field 2",
            "name_ja": "xtx/quest field 1",
            "source_sheet": "xtx/quest",
            "source_row": "same row id as passiveGL_craft",
        },
        "titleControls": TITLE_CONTROLS,
        "product": {
            "path": "derived/local_guildleve_names.csv",
            "sha256": sha256(output),
            "bytes": len(output),
            "dataRowCount": len(rows),
            "columns": FIELDS,
        },
        "limitations": [
            "Covers every passiveGL_craft row, including test and dummy titles; names are preserved verbatim.",
            "The local journal title lookup is independent of passiveGL_craft columns 8-11.",
            "Client title data does not establish availability or server behavior.",
        ],
    }
    return {
        OUTPUT: output,
        MANIFEST: (json.dumps(manifest, ensure_ascii=True, indent=2) + "\n").encode(
            "utf-8"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_csv_dir_argument(parser)
    parser.add_argument(
        "--check", action="store_true", help="Verify tracked output without writing."
    )
    args = parser.parse_args()
    try:
        products = build(args.csv_dir)
        for path, content in products.items():
            if args.check:
                if not path.is_file() or path.read_bytes() != content:
                    raise ValueError(
                        f"{path.relative_to(REPO).as_posix()}: stale output"
                    )
            else:
                path.write_bytes(content)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"Local guildleve titles {'verified' if args.check else 'built'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
