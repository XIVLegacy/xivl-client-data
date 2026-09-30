"""Inspect one item/skill compatibility value without writing corpus products."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from _csv_reader import CsvHeader, CsvRow, coerce, read_csv
from _csv_root import add_csv_dir_argument, validate_csv_dir


ITEM_COMPATIBILITY_COLUMN = 48
FIRST_SKILL_COLUMN = 8
SKILL_COUNT = 44


@dataclass(frozen=True)
class CompatibilityResult:
    catalog_row_id: str
    item_data_row_id: str
    compatibility_row_id: str
    skill_id: int
    column: int
    stored_integer: int

    @property
    def client_factor(self) -> float:
        return self.stored_integer / 100


def _load_sheet(path: Path) -> tuple[CsvHeader, dict[str, CsvRow]]:
    header, rows = read_csv(path)
    indexed: dict[str, CsvRow] = {}
    for row in rows:
        if row.row_id in indexed:
            raise ValueError(f"{path.name}: duplicate row id {row.row_id!r}")
        indexed[row.row_id] = row
    return header, indexed


def _row(rows: dict[str, CsvRow], key: str, sheet: str) -> CsvRow:
    try:
        return rows[key]
    except KeyError as exc:
        raise ValueError(f"{sheet}: missing row {key!r}") from exc


def _integer_cell(
    sheet: str, header: CsvHeader, row: CsvRow, column: int, expected_type: str
) -> int:
    location = f"{sheet}: row {row.row_id!r}, column {column}"
    if column >= len(header.column_indices) or column >= len(header.column_types):
        raise ValueError(f"{location}: missing column or type declaration")
    actual_type = header.column_types[column]
    if actual_type != expected_type:
        raise ValueError(
            f"{location}: type {actual_type!r}; expected {expected_type!r}"
        )
    raw = row.values[column].strip()
    # Seed coercion maps blanks to zero; an inspection must retain the distinction.
    if raw == "":
        raise ValueError(f"{location}: blank cell")
    try:
        return int(coerce(raw, expected_type))
    except ValueError as exc:
        raise ValueError(
            f"{location}: invalid {expected_type} value {raw!r}: {exc}"
        ) from exc


def inspect(csv_dir: Path, catalog_id: int, skill_id: int) -> CompatibilityResult:
    if not 0 <= catalog_id <= 4294967295:
        raise ValueError("catalog ID must be a u32 integer")
    if not 1 <= skill_id <= SKILL_COUNT:
        raise ValueError(f"skill ID must be in [1, {SKILL_COUNT}]")
    csv_dir = validate_csv_dir(csv_dir)
    _catalog_header, catalog = _load_sheet(csv_dir / "_item.csv")
    catalog_row = _row(catalog, str(catalog_id), "_item.csv")
    item_header, items = _load_sheet(csv_dir / "itemData.csv")
    item_row = _row(items, catalog_row.row_id, "itemData.csv")
    key = _integer_cell(
        "itemData.csv", item_header, item_row, ITEM_COMPATIBILITY_COLUMN, "s32"
    )
    compatibility_header, compatibility = _load_sheet(csv_dir / "compatibility.csv")
    compatibility_row = _row(compatibility, str(key), "compatibility.csv")
    column = FIRST_SKILL_COLUMN + (skill_id - 1)
    stored = _integer_cell(
        "compatibility.csv", compatibility_header, compatibility_row, column, "s8"
    )
    return CompatibilityResult(
        catalog_row.row_id,
        item_row.row_id,
        compatibility_row.row_id,
        skill_id,
        column,
        stored,
    )


def render(result: CompatibilityResult) -> str:
    gate = (
        "Zero matches the observed canEquipSimple compatibility rejection."
        if result.stored_integer == 0
        else "Nonzero does not trigger the observed zero-compatibility rejection."
    )
    return (
        "\n".join(
            (
                f"_item.csv row {result.catalog_row_id} -> itemData.csv row {result.item_data_row_id}",
                f"itemData.csv column {ITEM_COMPATIBILITY_COLUMN} compatibility key: {result.compatibility_row_id}",
                f"compatibility.csv row {result.compatibility_row_id}, skill {result.skill_id}, column {result.column}",
                f"Stored integer (s8): {result.stored_integer}",
                f"Client factor (stored / 100): {result.client_factor:.2f}",
                gate,
                "Complete equipment eligibility is not determined: tribe and required-level checks,",
                "server policy, and item appearance are not evaluated.",
            )
        )
        + "\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_csv_dir_argument(parser)
    parser.add_argument(
        "catalog_id", type=int, help="item catalog row ID (decimal u32)"
    )
    parser.add_argument("skill_id", type=int, help="class/job skill ID (1 through 44)")
    args = parser.parse_args(argv)
    try:
        result = inspect(args.csv_dir, args.catalog_id, args.skill_id)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(render(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
