#!/usr/bin/env python3
"""Build and verify the exhaustive actor appearance packed-word census."""

from __future__ import annotations

import argparse
import csv
import io
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from _csv_reader import CsvHeader, CsvRow, read_csv
from mappings import actor_appearance


REPO = Path(__file__).resolve().parents[1]
CSV_DIR = REPO / "csv"
CENSUS_OUT = REPO / "derived" / "actor_appearance_census.csv"
DISTRIBUTIONS_OUT = REPO / "derived" / "actor_appearance_value_counts.csv"
FIELDS = (
    ("mainHand", 0x19, "s32"),
    ("offHand", 0x1A, "s32"),
    ("spMainHand", 0x1B, "s32"),
    ("spOffHand", 0x1C, "s32"),
    ("throwing", 0x1D, "s32"),
    ("pack", 0x1E, "s32"),
    ("pouch", 0x1F, "s32"),
)
LANES = (
    ("bits_31_30", 30, 0x3),
    ("bits_29_20", 20, 0x3FF),
    ("bits_19_10", 10, 0x3FF),
    ("bits_9_0", 0, 0x3FF),
)


@dataclass(frozen=True)
class CensusStats:
    source_row_count: int
    nonzero_row_count: int
    packed_occurrence_count: int
    distinct_counts: tuple[int, ...]


def unpack_2_10_10_10(value: int) -> tuple[int, int, int, int]:
    """Return the four packed components by bit range, without semantic names."""
    unsigned = value & 0xFFFFFFFF
    return (
        (unsigned >> 30) & 0x3,
        (unsigned >> 20) & 0x3FF,
        (unsigned >> 10) & 0x3FF,
        unsigned & 0x3FF,
    )


def _load_rows(path: Path) -> tuple[CsvHeader, list[CsvRow]]:
    header, rows = read_csv(path)
    return header, list(rows)


def _index(rows: list[CsvRow], source: str) -> dict[int, CsvRow]:
    indexed: dict[int, CsvRow] = {}
    for row in rows:
        row_id = int(row.row_id)
        if row_id in indexed:
            raise ValueError(f"{source}: duplicate row id {row_id}")
        indexed[row_id] = row
    return indexed


def _validate_graphic_header(header: CsvHeader) -> None:
    mapped = tuple(
        entry
        for entry in actor_appearance.COLUMNS
        if isinstance(entry[1], int) and 0x19 <= entry[1] <= 0x1F
    )
    if mapped != FIELDS:
        raise ValueError(f"actor appearance mapping drift: {mapped!r}")
    for name, position, csv_type in FIELDS:
        if header.column_indices[position] != str(position):
            raise ValueError(
                f"{name}: column 0x{position:02X} label is "
                f"{header.column_indices[position]!r}"
            )
        if header.column_types[position] != csv_type:
            raise ValueError(
                f"{name}: column 0x{position:02X} type is "
                f"{header.column_types[position]!r}"
            )


def _render_csv(header: list[str], rows: list[list[object]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def build(
    graphic_path: Path = CSV_DIR / "actorclass_graphic.csv",
    actorclass_path: Path = CSV_DIR / "actorclass.csv",
    display_name_path: Path = CSV_DIR / "xtx_displayName.csv",
) -> tuple[dict[Path, bytes], CensusStats]:
    graphic_header, graphic_rows = _load_rows(graphic_path)
    actorclass_header, actorclass_rows = _load_rows(actorclass_path)
    display_header, display_rows = _load_rows(display_name_path)
    _validate_graphic_header(graphic_header)
    if (
        actorclass_header.column_indices[5] != "5"
        or actorclass_header.column_types[5] != "s32"
    ):
        raise ValueError("actorclass.csv: display-name reference is not s32 column 5")
    if (
        display_header.column_indices[1] != "1"
        or display_header.column_types[1] != "str"
    ):
        raise ValueError("xtx_displayName.csv: English name is not str column 1")

    actorclasses = _index(actorclass_rows, actorclass_path.name)
    display_names = _index(display_rows, display_name_path.name)
    census_rows: list[list[object]] = []
    counters = [Counter[int]() for _field in FIELDS]
    packed_occurrences = 0
    graphic_ids: set[int] = set()

    for row in graphic_rows:
        row_id = int(row.row_id)
        if row_id in graphic_ids:
            raise ValueError(f"actorclass_graphic.csv: duplicate row id {row_id}")
        graphic_ids.add(row_id)
        if row_id not in actorclasses:
            raise ValueError(
                f"actorclass_graphic.csv row {row_id}: no actorclass.csv row"
            )
        actorclass = actorclasses[row_id]
        display_name_id = int(actorclass.values[5] or 0)
        if display_name_id not in display_names:
            raise ValueError(
                f"actorclass.csv row {row_id}: display name {display_name_id} is missing"
            )

        packed = [int(row.values[position] or 0) for _name, position, _type in FIELDS]
        for counter, value in zip(counters, packed, strict=True):
            counter[value] += 1
        packed_occurrences += sum(value != 0 for value in packed)
        if not any(packed):
            continue

        output: list[object] = [
            row_id,
            row_id,
            display_name_id,
            display_names[display_name_id].values[1],
        ]
        for value in packed:
            output.extend(
                [value, f"0x{value & 0xFFFFFFFF:08X}", *unpack_2_10_10_10(value)]
            )
        census_rows.append(output)

    census_header = [
        "actorclass_graphic_row_id",
        "actorclass_row_id",
        "display_name_id",
        "display_name_en",
    ]
    for name, _position, _type in FIELDS:
        census_header.extend(
            [
                f"{name}_packed_s32",
                f"{name}_packed_u32_hex",
                *(f"{name}_{lane_name}" for lane_name, _shift, _mask in LANES),
            ]
        )

    distribution_rows: list[list[object]] = []
    for (name, position, _type), counter in zip(FIELDS, counters, strict=True):
        for value in sorted(counter):
            distribution_rows.append(
                [
                    name,
                    f"0x{position:02X}",
                    value,
                    f"0x{value & 0xFFFFFFFF:08X}",
                    *unpack_2_10_10_10(value),
                    counter[value],
                ]
            )

    outputs = {
        CENSUS_OUT: _render_csv(census_header, census_rows),
        DISTRIBUTIONS_OUT: _render_csv(
            [
                "field",
                "source_column",
                "packed_s32",
                "packed_u32_hex",
                *(name for name, _shift, _mask in LANES),
                "row_count",
            ],
            distribution_rows,
        ),
    }
    stats = CensusStats(
        source_row_count=len(graphic_rows),
        nonzero_row_count=len(census_rows),
        packed_occurrence_count=packed_occurrences,
        distinct_counts=tuple(len(counter) for counter in counters),
    )
    return outputs, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated files")
    args = parser.parse_args()
    try:
        outputs, stats = build()
    except (IndexError, OSError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1

    if args.check:
        stale = [
            path
            for path, data in outputs.items()
            if not path.is_file() or path.read_bytes() != data
        ]
        if stale:
            for path in stale:
                print(f"FAIL: stale generated file: {path.relative_to(REPO)}")
            return 1
        action = "verified"
    else:
        for path, data in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            print(f"wrote {path.relative_to(REPO)}")
        action = "built"

    distinct = ",".join(str(count) for count in stats.distinct_counts)
    print(
        f"PASS: {action} {stats.nonzero_row_count}/{stats.source_row_count} rows; "
        f"{stats.packed_occurrence_count} nonzero words; distinct values {distinct}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
