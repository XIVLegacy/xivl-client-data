#!/usr/bin/env python3
"""Build and verify the GC seal and generic shop catalogs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

from _csv_reader import CsvHeader, CsvRow, read_csv

REPO = Path(__file__).resolve().parent.parent
CSV_DIR = REPO / "csv"
DERIVED_DIR = REPO / "derived"
MANIFESTS = REPO / "manifests"
GC_OUT = DERIVED_DIR / "gc_seal_shop_catalog.csv"
SHOP_OUT = DERIVED_DIR / "shop_catalog.csv"
MANIFEST_OUT = MANIFESTS / "shop_catalogs.json"
EXTRACTION_VERSION = "2012.09.19.0001"

SHOP_SHEETS = {
    "gcSealShopItem.csv": (9, "GC seal inventory"),
    "populaceCompanyShop.csv": (5, "localized company-shop text"),
    "populaceGuildShop.csv": (5, "localized guild-shop text"),
    "populaceShopMateriaRemover.csv": (5, "localized materia-service text"),
    "populaceShopSalesman.csv": (5, "localized salesman text"),
    "shopBase.csv": (2, "generic shop item-key ranges"),
    "shopItem.csv": (3, "generic shop inventory"),
}


def load_table(path: Path) -> tuple[CsvHeader, list[CsvRow]]:
    header, rows = read_csv(path)
    return header, list(rows)


def index_rows(path: Path) -> dict[int, CsvRow]:
    _header, rows = load_table(path)
    indexed: dict[int, CsvRow] = {}
    for row in rows:
        row_id = int(row.row_id)
        if row_id in indexed:
            raise ValueError(f"{path.name}: duplicate row id {row_id}")
        indexed[row_id] = row
    return indexed


def render_csv(header: list[str], rows: list[list[object]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def build() -> dict[Path, bytes]:
    table_manifest = {
        entry["name"]: entry
        for entry in json.loads((MANIFESTS / "tables.json").read_text(encoding="utf-8"))
    }
    with (MANIFESTS / "sheet_inventory.csv").open(encoding="utf-8", newline="") as handle:
        sheet_inventory = {row["name"] + ".csv": row for row in csv.DictReader(handle)}

    audit = []
    source_headers: dict[str, dict[str, list[str]]] = {}
    for name, (width, role) in SHOP_SHEETS.items():
        header, rows = load_table(CSV_DIR / name)
        if len(header.column_indices) != width or len(header.column_types) != width:
            raise ValueError(f"{name}: declared width is not {width}")
        bad_rows = [row.row_id for row in rows if len(row.values) != width]
        if bad_rows:
            raise ValueError(f"{name}: truncated rows {bad_rows[:10]}")
        expected_rows = table_manifest[name]["dataRowCount"]
        if len(rows) != expected_rows:
            raise ValueError(f"{name}: {len(rows)} rows != manifest {expected_rows}")
        inventory = sheet_inventory[name]
        audit.append({
            "sheet": name,
            "evidenceClass": "client_extraction",
            "source": inventory["source"],
            "resourceId": int(inventory["resource_id"]),
            "resourceIdHex": inventory["resource_id_hex"],
            "dataRowCount": len(rows),
            "sheetColumnCount": width,
            "role": role,
            "verdict": "complete pinned extraction; no truncated rows",
            "sha256": table_manifest[name]["sha256"],
        })
        source_headers[name] = {
            "columnIndices": header.column_indices,
            "columnTypes": header.column_types,
        }

    item_rows = index_rows(CSV_DIR / "_item.csv")
    item_data_rows = index_rows(CSV_DIR / "itemData.csv")
    item_name_rows = index_rows(CSV_DIR / "xtx_itemName.csv")
    join_sources = []
    for name, rows in (
        ("_item.csv", item_rows),
        ("itemData.csv", item_data_rows),
        ("xtx_itemName.csv", item_name_rows),
    ):
        join_sources.append({
            "sheet": name,
            "dataRowCount": len(rows),
            "sha256": table_manifest[name]["sha256"],
        })

    gc_rows = index_rows(CSV_DIR / "gcSealShopItem.csv")
    gc_output: list[list[object]] = []
    for shop_row_id, row in sorted(gc_rows.items()):
        values = [int(value) for value in row.values]
        item_id = values[0]
        if item_id not in item_rows or item_id not in item_data_rows or item_id not in item_name_rows:
            raise ValueError(f"gcSealShopItem.csv row {shop_row_id}: item {item_id} has no complete item-catalog join")
        gc_output.append([
            shop_row_id,
            item_id,
            values[1],
            values[2],
            values[3],
            values[4],
            values[5],
            values[6],
            values[7],
            values[8],
            item_rows[item_id].values[0],
            item_name_rows[item_id].values[6],
        ])
    gc_bytes = render_csv([
        "shop_row_id",
        "item_id",
        "item_quality",
        "item_quantity",
        "seal_cost",
        "rank_requirement",
        "company_id",
        "event_flag_requirement",
        "reserved_zero",
        "item_category",
        "item_class_path",
        "item_name_en",
    ], gc_output)

    base_rows = index_rows(CSV_DIR / "shopBase.csv")
    shop_item_rows = index_rows(CSV_DIR / "shopItem.csv")
    owners: dict[int, list[int]] = {row_id: [] for row_id in shop_item_rows}
    shop_output: list[list[object]] = []
    for shop_id, row in sorted(base_rows.items()):
        start_id, end_id = (int(value) for value in row.values)
        if start_id == 0 and end_id == 0:
            continue
        for item_row_id in range(start_id, end_id + 1):
            item_row = shop_item_rows.get(item_row_id)
            if item_row is None:
                raise ValueError(f"shopBase.csv row {shop_id}: missing shopItem row {item_row_id}")
            owners[item_row_id].append(shop_id)
            item_id, quality, price = (int(value) for value in item_row.values)
            if item_id not in item_rows or item_id not in item_name_rows:
                raise ValueError(f"shopItem.csv row {item_row_id}: item {item_id} has no item-catalog join")
            shop_output.append([
                shop_id,
                item_row_id,
                item_id,
                quality,
                price,
                item_rows[item_id].values[0],
                item_name_rows[item_id].values[6],
            ])
    shop_bytes = render_csv([
        "shop_id",
        "shop_item_row_id",
        "item_id",
        "item_quality",
        "price",
        "item_class_path",
        "item_name_en",
    ], shop_output)

    unowned = sorted(row_id for row_id, row_owners in owners.items() if not row_owners)
    multiple = sorted(row_id for row_id, row_owners in owners.items() if len(row_owners) > 1)
    reserved_column7_nonzero_count = sum(
        int(row.values[7]) != 0 for row in gc_rows.values()
    )
    if reserved_column7_nonzero_count:
        raise ValueError("gcSealShopItem.csv column 7 is no longer uniformly zero")

    manifest = {
        "schemaVersion": 1,
        "generatedOn": "2026-08-15",
        "extractionVersion": EXTRACTION_VERSION,
        "sourceEvidenceClass": "client_extraction",
        "sheetAudit": audit,
        "sourceHeaders": source_headers,
        "joinSources": join_sources,
        "gcSealShop": {
            "source": "csv/gcSealShopItem.csv",
            "itemJoins": ["csv/_item.csv", "csv/itemData.csv", "csv/xtx_itemName.csv"],
            "output": "derived/gc_seal_shop_catalog.csv",
            "rowCount": len(gc_output),
            "distinctItemCount": len({row[1] for row in gc_output}),
            "reservedColumn7NonzeroCount": reserved_column7_nonzero_count,
            "sha256": sha256(gc_bytes),
        },
        "genericShop": {
            "sources": ["csv/shopBase.csv", "csv/shopItem.csv"],
            "itemJoins": ["csv/_item.csv", "csv/xtx_itemName.csv"],
            "output": "derived/shop_catalog.csv",
            "shopCount": sum(1 for row in base_rows.values() if row.values != ["0", "0"]),
            "associationCount": len(shop_output),
            "unownedShopItemRowCount": len(unowned),
            "multipleOwnerShopItemRowCount": len(multiple),
            "multipleOwnerShopItemRows": multiple,
            "sha256": sha256(shop_bytes),
        },
        "columnMappings": {
            "gcSealShopItem.csv": {
                "rowId": "shop_row_id",
                "0": "item_id",
                "1": "item_quality",
                "2": "item_quantity",
                "3": "seal_cost",
                "4": "rank_requirement",
                "5": "company_id",
                "6": "event_flag_requirement",
                "7": "reserved_zero",
                "8": "item_category",
            },
            "shopBase.csv": {"rowId": "shop_id", "0": "shop_item_start_id", "1": "shop_item_end_id"},
            "shopItem.csv": {"rowId": "shop_item_row_id", "0": "item_id", "1": "item_quality", "2": "price"},
        },
        "residualCeilings": [
            "The client getters do not assign a meaning to gcSealShopItem column 7; it is zero in all 402 rows.",
            "The 750 unowned shopItem rows are preserved in the source corpus but omitted from the range-expanded generic catalog.",
            "Eleven shopItem rows are intentionally emitted once for each of their two shopBase owners.",
        ],
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=True, indent=2) + "\n").encode("ascii")
    return {GC_OUT: gc_bytes, SHOP_OUT: shop_bytes, MANIFEST_OUT: manifest_bytes}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated files without writing")
    args = parser.parse_args()
    outputs = build()
    if args.check:
        mismatches = [path for path, data in outputs.items() if not path.is_file() or path.read_bytes() != data]
        if mismatches:
            for path in mismatches:
                print(f"out of date: {path.relative_to(REPO)}")
            return 1
        print(f"verified {len(outputs)} shop catalog artifact(s)")
        return 0
    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"wrote {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
