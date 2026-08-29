#!/usr/bin/env python3
"""Mutation tests for the retail item/equipment column crosswalk."""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

import build_item_equipment_crosswalk as builder


PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(name)


def raises_value_error(callable_) -> bool:
    try:
        callable_()
    except ValueError:
        return True
    return False


def write_sheet(
    path: Path,
    width: int,
    types: dict[int, str],
    rows: list[tuple[int, dict[int, str]]],
) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["", *(str(index) for index in range(width))])
        writer.writerow(["", *(types.get(index, "") for index in range(width))])
        for row_id, populated in rows:
            values = [""] * width
            for column, value in populated.items():
                values[column] = value
            writer.writerow([row_id, *values])
    return path


def main() -> int:
    item_types = {column: "float" for column in (50, 53, 56, 59)}
    equipment_types = builder.EXPECTED_TYPES["equipment.csv"]
    with tempfile.TemporaryDirectory(prefix="item-equipment-crosswalk-") as raw:
        directory = Path(raw)
        item_rows = [
            (row_id, {50: "0", 53: "0", 56: "0", 59: "0"})
            for row_id in builder.KNOWN_GEAR
        ]
        equipment_rows = [
            (8030423, {71: "16007", 72: "2", 73: "-1", 74: "0", 75: "-1", 76: "0", 77: "-1", 78: "0", 79: "15001", 80: "4", 81: "-1", 82: "0", 83: "-1", 84: "0", 85: "-1", 86: "0", 87: "-1", 88: "0", 89: "-1", 90: "0"}),
            (8011608, {71: "-1", 72: "0", 73: "-1", 74: "0", 75: "-1", 76: "0", 77: "-1", 78: "5", 79: "1015001", 80: "3", 81: "-1", 82: "0", 83: "-1", 84: "0", 85: "-1", 86: "0", 87: "-1", 88: "0", 89: "-1", 90: "0"}),
            (4030013, {column: ("-1" if column % 2 else "0") for column in range(71, 91)}),
        ]
        item = write_sheet(directory / "itemData.csv", 141, item_types, item_rows)
        equipment = write_sheet(directory / "equipment.csv", 140, equipment_types, equipment_rows)
        write_sheet(
            directory / "xtx_text_paramName.csv",
            10,
            {column: "str" for column in range(10)},
            [(15001, {1: "HP"}), (16007, {1: "Storm gear"})],
        )
        write_sheet(
            directory / "xtx_itemName.csv",
            7,
            {column: "str" for column in range(7)},
            [(row_id, {6: label}) for row_id, label in builder.KNOWN_GEAR.items()],
        )
        inventory = directory / "sheet_inventory.csv"
        with inventory.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(["name", "resource_id", "resource_id_hex", "source"])
            for name, values in builder.EXPECTED_INVENTORY.items():
                writer.writerow([name, *values])

        header, rows = builder.load_sheet(item)
        builder.validate_requested_types("itemData.csv", header)
        blank = builder.summarize(builder.COLUMN_SPECS[0], header, rows)
        check("blank selector is not coerced to zero", blank.blank_count == 3 and blank.zero_count == 0)
        check("blank selector has no active values", blank.active_count == 0)
        check("direct parameter row-id join resolves", builder.parameter_join(15001, {15001: "HP"}) == ("direct row-id", 15001, "HP"))
        check("bounded offset join resolves", builder.parameter_join(1015001, {15001: "HP"}) == ("minus-1000000", 15001, "HP"))
        check("offset join does not generalize", builder.parameter_join(2015001, {1015001: "wrong"}) is None)
        pairs = builder.pair_audit(builder.load_sheet(equipment)[1])
        check(
            "pair audit distinguishes residual values beside -1",
            next(pair for pair in pairs if pair["idColumn"] == 77)[
                "minusOneNonzero"
            ]
            == 1,
        )

        first = builder.build(directory, inventory)
        second = builder.build(directory, inventory)
        check("document rendering is deterministic", first == second)
        check("document is ASCII with literal LF", first.endswith(b"\n") and b"\r" not in first)
        check("known gear anchors are rendered", all(f"row `{row_id}`".encode() in first for row_id in builder.KNOWN_GEAR))

        bad_types = dict(item_types)
        bad_types[49] = "s32"
        mutated = write_sheet(directory / "bad-type.csv", 141, bad_types, item_rows)
        bad_header, _bad_rows = builder.load_sheet(mutated)
        check("selector type mutation fails closed", raises_value_error(lambda: builder.validate_requested_types("itemData.csv", bad_header)))

        with equipment.open("a", encoding="utf-8", newline="") as handle:
            handle.write("999,-1\n")
        check("truncated row mutation fails closed", raises_value_error(lambda: builder.load_sheet(equipment)))

    for name in PASSED:
        print(f"PASS: {name}")
    for name in FAILED:
        print(f"FAIL: {name}")
    print(f"{len(PASSED)} passed; {len(FAILED)} failed")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
