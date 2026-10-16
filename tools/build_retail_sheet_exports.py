#!/usr/bin/env python3
"""Export complete status, Grand Company rank, materia and materia-book rows."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

from _csv_reader import CsvRow, coerce, read_csv
from _csv_root import add_csv_dir_argument, validate_csv_dir

REPO = Path(__file__).resolve().parent.parent
MANIFEST = "manifests/retail_sheet_exports.json"
SOURCE_LAYOUTS = {
    "status.csv": (
        59,
        {
            25: "s32",
            31: "float",
            42: "s32",
            47: "float",
            51: "bool",
            52: "bool",
            53: "float",
            54: "bool",
            55: "s8",
            56: "bool",
            57: "bool",
            58: "bool",
        },
    ),
    "xtx_status.csv": (
        69,
        {
            1: "str",
            2: "str",
            3: "str",
            4: "str",
            5: "str",
            6: "s32",
            7: "s32",
            8: "str",
            9: "s32",
            10: "str",
            11: "s32",
            12: "s32",
            13: "s32",
            14: "s32",
            15: "str",
            16: "str",
            17: "s32",
            18: "s32",
            19: "s32",
            20: "str",
            21: "str",
            22: "str",
            23: "str",
            24: "str",
            67: "str",
            68: "str",
        },
    ),
    "gcRank.csv": (9, {0: "u8", 1: "s32", 2: "s32", 6: "s32", 7: "s32", 8: "s32"}),
    "xtx_gcRank.csv": (30, dict.fromkeys([3, 4, 5, *range(9, 30)], "str")),
    "materia.csv": (
        80,
        {
            **dict.fromkeys(range(5), "s32"),
            **dict.fromkeys(range(5, 21), "s16"),
            21: "s32",
            **dict.fromkeys(range(22, 38), "s16"),
            **dict.fromkeys(range(38, 42), "s32"),
            **dict.fromkeys(range(42, 80), "bool"),
        },
    ),
    "materiaBook.csv": (5, dict.fromkeys(range(5), "str")),
}
TYPED_COLUMNS = {
    "status_names": {f"status_col_{i}": i for i in SOURCE_LAYOUTS["status.csv"][1]},
    "gc_rank": {
        "linear_rank": 0,
        "seal_maximum": 1,
        "seals_needed_next_rank": 2,
        "icon_company_1": 6,
        "icon_company_2": 7,
        "icon_company_3": 8,
    },
    "materia": {
        **{f"catalog_id_quality_group_{group}": group for group in range(4)},
        "parameter_1": 4,
        **{f"value_1_quality_{quality}": 5 + quality for quality in range(16)},
        "parameter_2": 21,
        **{f"value_2_quality_{quality}": 22 + quality for quality in range(16)},
        **{f"icon_quality_group_{group}": 38 + group for group in range(4)},
        **{f"materia_col_{column}": column for column in range(42, 80)},
    },
    "materia_book": {},
}
PLACEHOLDERS = ("", "-", "****", "x", "dummy", "\u7ffb\u8a33\u4e0d\u8981")
SPECS = {
    "status_names": {
        "source": "status.csv",
        "id": "status_id",
        "multiplier": 1,
        "fields": [
            "status_id",
            "name_en",
            "name_ja",
            "placeholder",
            "icon_text",
            *TYPED_COLUMNS["status_names"],
            "source_row",
        ],
        "textColumns": {"name_en": 3, "name_ja": 1, "icon_text": 24},
        "textSource": "xtx_status.csv",
    },
    "gc_rank": {
        "source": "gcRank.csv",
        "id": "rank_id",
        "multiplier": 3,
        "fields": [
            "rank_id",
            "company",
            "name_variant",
            "name_en",
            "name_ja",
            *TYPED_COLUMNS["gc_rank"],
            "source_row",
        ],
        "textColumns": {"name_en": [9, 10, 11], "name_ja": [3, 4, 5]},
        "textSource": "xtx_gcRank.csv",
        "mappingEvidence": "xivl-client-scripts:docs/gc-promotion-client-contract.md#player-state-and-sheet-consumers",
    },
    "materia": {
        "source": "materia.csv",
        "id": "materia_id",
        "multiplier": 1,
        "fields": [
            "materia_id",
            *TYPED_COLUMNS["materia"],
            "source_row",
        ],
        "textColumns": {},
        "mappingEvidence": "xivl-client-scripts:docs/materia-meld-client-contract.md#sheet-getters",
    },
    "materia_book": {
        "source": "materiaBook.csv",
        "id": "text_id",
        "multiplier": 1,
        "fields": [
            "text_id",
            "text_ja",
            "text_en",
            "text_de",
            "text_fr",
            "text_zh",
            "source_row",
        ],
        "textColumns": {
            "text_ja": 0,
            "text_en": 1,
            "text_de": 2,
            "text_fr": 3,
            "text_zh": 4,
        },
        "textSource": "materiaBook.csv",
    },
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def load_source(path: Path) -> dict[int, CsvRow]:
    width, types = SOURCE_LAYOUTS[path.name]
    header, iterator = read_csv(path)
    rows = list(iterator)
    if (
        header.column_indices != list(map(str, range(width)))
        or len(header.column_types) != width
        or {i: t for i, t in enumerate(header.column_types) if t} != types
    ):
        raise ValueError(f"{path.name}: unexpected source layout")
    indexed = {}
    for row in rows:
        row_id = int(row.row_id)
        if row_id < 0 or row_id in indexed:
            raise ValueError(f"{path.name}: invalid or duplicate row id {row_id}")
        for column, type_name in types.items():
            coerce(row.values[column], type_name)
        indexed[row_id] = row
    return indexed


def project(name: str, sources: dict[str, dict[int, CsvRow]]) -> list[dict]:
    spec = SPECS[name]
    driver = sources[spec["source"]]
    text = sources.get(spec.get("textSource", ""))
    if text is not None and driver.keys() != text.keys():
        raise ValueError(f"{name}: source and text row IDs must match exactly")
    rows = []
    for row_id, row in sorted(driver.items()):
        for variant in range(spec["multiplier"]):
            result = {spec["id"]: str(row_id)}
            if name == "gc_rank":
                result.update(company="unresolved", name_variant=str(variant))
            if text is not None:
                for field, column in spec["textColumns"].items():
                    index = column[variant] if isinstance(column, list) else column
                    result[field] = text[row_id].values[index]
            if name == "status_names":
                result["placeholder"] = str(result["name_en"] in PLACEHOLDERS).lower()
            result.update(
                {
                    field: row.values[column]
                    for field, column in TYPED_COLUMNS[name].items()
                }
            )
            result["source_row"] = str(row_id)
            rows.append(result)
    return rows


def render(name: str, rows: list[dict]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=SPECS[name]["fields"], lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def source_metadata(tables: dict) -> list[dict]:
    return [
        {
            "path": f"csv/{name}",
            "bytes": tables[name]["bytes"],
            "sha256": tables[name]["sha256"].upper(),
            "rowCount": tables[name]["dataRowCount"],
            "columnTypes": {str(i): t for i, t in types.items()},
        }
        for name, (_, types) in SOURCE_LAYOUTS.items()
    ]


def product_metadata(name: str, payload: bytes, rows: list[dict]) -> dict:
    spec = SPECS[name]
    result = {
        "path": f"derived/{name}.csv",
        "bytes": len(payload),
        "sha256": digest(payload),
        "rowCount": len(rows),
        "source": f"csv/{spec['source']}",
        "fields": spec["fields"],
        "textColumns": spec["textColumns"],
        "typedColumns": TYPED_COLUMNS[name],
    }
    if "mappingEvidence" in spec:
        result["mappingEvidence"] = spec["mappingEvidence"]
    if "textSource" in spec:
        result["textSource"] = f"csv/{spec['textSource']}"
    if name == "status_names":
        result["placeholderCount"] = sum(row["placeholder"] == "true" for row in rows)
    return result


def build(csv_dir: Path) -> dict[Path, bytes]:
    validate_csv_dir(csv_dir)
    tables = {
        entry["name"]: entry
        for entry in json.loads(
            (REPO / "manifests/tables.json").read_text(encoding="utf-8")
        )
    }
    sources = {}
    for name in SOURCE_LAYOUTS:
        payload = (csv_dir / name).read_bytes()
        if (
            len(payload) != tables[name]["bytes"]
            or digest(payload) != tables[name]["sha256"].upper()
        ):
            raise ValueError(f"{name}: source bytes differ from tables.json")
        sources[name] = load_source(csv_dir / name)
        if len(sources[name]) != tables[name]["dataRowCount"]:
            raise ValueError(f"{name}: source row count differs from tables.json")
    outputs = {}
    products = {}
    for name in SPECS:
        rows = project(name, sources)
        payload = render(name, rows)
        outputs[REPO / f"derived/{name}.csv"] = payload
        products[name] = product_metadata(name, payload, rows)
    manifest = {
        "schemaVersion": 1,
        "extractionVersion": "2012.09.19.0001",
        "sourceEvidenceClass": "client_extraction",
        "sources": source_metadata(tables),
        "products": products,
        "placeholderMarkers": PLACEHOLDERS,
        "companyMapping": "unresolved; name_variant is the zero-based position within textColumns",
        "materiaBookJoin": "not established; exported independently",
    }
    outputs[REPO / MANIFEST] = (
        json.dumps(manifest, ensure_ascii=True, indent=2) + "\n"
    ).encode("ascii")
    return outputs


def validate_public(repo: Path) -> None:
    """Check source pins, product hashes, row coverage and locators without assets."""
    manifest = json.loads((repo / MANIFEST).read_text(encoding="utf-8"))
    tables = {
        entry["name"]: entry
        for entry in json.loads(
            (repo / "manifests/tables.json").read_text(encoding="utf-8")
        )
    }
    if manifest["sources"] != source_metadata(tables):
        raise ValueError("retail sheet exports: source identities or types differ")
    for name, spec in SPECS.items():
        payload = (repo / f"derived/{name}.csv").read_bytes()
        reader = csv.DictReader(io.StringIO(payload.decode("utf-8"), newline=""))
        rows = list(reader)
        if reader.fieldnames != spec["fields"] or any(
            None in row or None in row.values() for row in rows
        ):
            raise ValueError(f"{name}: product header or row width differs")
        if manifest["products"][name] != product_metadata(name, payload, rows):
            raise ValueError(f"{name}: product metadata or SHA-256 differs")
        if len(rows) != tables[spec["source"]]["dataRowCount"] * spec["multiplier"]:
            raise ValueError(f"{name}: product row count differs")
        keys = [(row[spec["id"]], row.get("name_variant", "")) for row in rows]
        if len(set(keys)) != len(keys) or keys != sorted(
            keys, key=lambda key: (int(key[0]), key[1])
        ):
            raise ValueError(f"{name}: product keys duplicate or unordered")
        for row in rows:
            if not row[spec["id"]].isdecimal() or row["source_row"] != row[spec["id"]]:
                raise ValueError(f"{name}: invalid source row")
            if (
                name == "status_names"
                and row["placeholder"] != str(row["name_en"] in PLACEHOLDERS).lower()
            ):
                raise ValueError(f"{name}: invalid placeholder")
            if name == "gc_rank" and (
                row["company"] != "unresolved"
                or row["name_variant"] not in {"0", "1", "2"}
            ):
                raise ValueError(f"{name}: invalid company or name variant")
        if name == "gc_rank":
            for rank_id in {row["rank_id"] for row in rows}:
                if {
                    row["name_variant"] for row in rows if row["rank_id"] == rank_id
                } != {"0", "1", "2"}:
                    raise ValueError("gc_rank: incomplete name variants")


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
        return bool(stale)
    for path, data in outputs.items():
        path.write_bytes(data)
        print(f"wrote {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
