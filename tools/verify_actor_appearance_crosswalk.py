#!/usr/bin/env python3
"""Verify the bounded actorclass_graphic packed-word crosswalk."""

from __future__ import annotations

import sys
from pathlib import Path

from _csv_reader import read_csv
from mappings import actor_appearance


REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "csv" / actor_appearance.SOURCE_CSV
TARGET_IDS = tuple(range(0x5A0700, 0x5A0704))
EXPECTED_COLUMNS = (
    ("mainHand", 0x19, "s32"),
    ("offHand", 0x1A, "s32"),
    ("spMainHand", 0x1B, "s32"),
    ("spOffHand", 0x1C, "s32"),
    ("throwing", 0x1D, "s32"),
    ("pack", 0x1E, "s32"),
    ("pouch", 0x1F, "s32"),
)


def unpack_2_10_10_10(value: int) -> tuple[int, int, int, int]:
    """Return bits 31:30, 29:20, 19:10, and 9:0 without naming lanes."""
    unsigned = value & 0xFFFFFFFF
    return (
        (unsigned >> 30) & 0x3,
        (unsigned >> 20) & 0x3FF,
        (unsigned >> 10) & 0x3FF,
        unsigned & 0x3FF,
    )


def verify() -> list[tuple[int, list[int]]]:
    mapping = tuple(
        entry for entry in actor_appearance.COLUMNS if isinstance(entry[1], int)
    )
    mapped = tuple(entry for entry in mapping if 0x19 <= entry[1] <= 0x1F)
    if mapped != EXPECTED_COLUMNS:
        raise ValueError(f"actor appearance mapping drift: {mapped!r}")

    header, rows = read_csv(SOURCE)
    for name, position, csv_type in EXPECTED_COLUMNS:
        if header.column_indices[position] != str(position):
            raise ValueError(
                f"{name}: CSV position 0x{position:02X} has label "
                f"{header.column_indices[position]!r}"
            )
        if header.column_types[position] != csv_type:
            raise ValueError(
                f"{name}: CSV position 0x{position:02X} has type "
                f"{header.column_types[position]!r}"
            )

    wanted = {str(row_id) for row_id in TARGET_IDS}
    found: dict[int, list[int]] = {}
    for row in rows:
        if row.row_id not in wanted:
            continue
        found[int(row.row_id)] = [
            int(row.values[position]) for _name, position, _type in EXPECTED_COLUMNS
        ]

    missing = [row_id for row_id in TARGET_IDS if row_id not in found]
    if missing:
        rendered = ", ".join(f"0x{row_id:06X}" for row_id in missing)
        raise ValueError(f"missing actorclass_graphic rows: {rendered}")

    for row_id, values in found.items():
        if values != [0] * len(EXPECTED_COLUMNS):
            raise ValueError(f"0x{row_id:06X}: expected seven zero words, got {values}")
        if any(unpack_2_10_10_10(value) != (0, 0, 0, 0) for value in values):
            raise ValueError(f"0x{row_id:06X}: zero-word unpack invariant failed")

    return [(row_id, found[row_id]) for row_id in TARGET_IDS]


def main() -> int:
    try:
        rows = verify()
    except (IndexError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    fields = ", ".join(
        f"0x{position:02X}={name}:{csv_type}"
        for name, position, csv_type in EXPECTED_COLUMNS
    )
    print(f"columns: {fields}")
    for row_id, values in rows:
        print(f"0x{row_id:06X} ({row_id}): {','.join(map(str, values))}")
    print("PASS: 4 rows x 7 packed appearance words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
