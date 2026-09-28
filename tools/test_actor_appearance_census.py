#!/usr/bin/env python3
"""Mutation tests for the actor appearance packed-word census."""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

import build_actor_appearance_census as census


PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(name)


def _write_sheet(
    path: Path,
    width: int,
    types: dict[int, str],
    rows: list[tuple[int, dict[int, object]]],
) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["", *(str(index) for index in range(width))])
        writer.writerow(["", *(types.get(index, "") for index in range(width))])
        for row_id, populated in rows:
            values = [""] * width
            for position, value in populated.items():
                values[position] = value
            writer.writerow([row_id, *values])
    return path


def _fixtures(directory: Path) -> tuple[Path, Path, Path]:
    graphic = _write_sheet(
        directory / "actorclass_graphic.csv",
        47,
        {index: "s32" for index in range(6, 47)},
        [
            (1, {}),
            (2, {0x19: 1}),
            (3, {0x1A: -1, 0x1E: 0x0DD0003D}),
            (4, {0x1B: 0x38F00100, 0x1D: 0x38A01400}),
        ],
    )
    actorclass = _write_sheet(
        directory / "actorclass.csv",
        6,
        {5: "s32"},
        [(row_id, {5: 100 + row_id}) for row_id in range(1, 5)],
    )
    display = _write_sheet(
        directory / "xtx_displayName.csv",
        20,
        {index: "str" for index in (0, 1, 2, 6, 8, 13, 14, 19)},
        [(100 + row_id, {1: f"Actor {row_id}"}) for row_id in range(1, 5)],
    )
    return graphic, actorclass, display


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="actor-appearance-census-") as raw:
        directory = Path(raw)
        graphic, actorclass, display = _fixtures(directory)
        first, stats = census.build(graphic, actorclass, display)
        second, repeated_stats = census.build(graphic, actorclass, display)
        check("fixture has three nonzero rows", stats.nonzero_row_count == 3)
        check("fixture counts five nonzero words", stats.packed_occurrence_count == 5)
        check(
            "repeated build is byte-identical",
            first == second and stats == repeated_stats,
        )
        check(
            "all generated output uses literal LF",
            all(data.endswith(b"\n") and b"\r" not in data for data in first.values()),
        )
        check(
            "signed s32 decode is unsigned",
            census.unpack_2_10_10_10(-1) == (3, 1023, 1023, 1023),
        )

        original = graphic.read_bytes()
        with graphic.open(encoding="utf-8", newline="") as handle:
            graphic_records = list(csv.reader(handle))
        graphic_records[3][0x19 + 1] = "2"
        with graphic.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle, lineterminator="\n").writerows(graphic_records)
        mutated, _stats = census.build(graphic, actorclass, display)
        check("packed-value mutation changes census", mutated != first)
        graphic.write_bytes(original)

        lines = graphic.read_text(encoding="utf-8").splitlines()
        types = lines[1].split(",")
        types[0x19 + 1] = "u32"
        lines[1] = ",".join(types)
        graphic.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
        try:
            census.build(graphic, actorclass, display)
        except ValueError:
            type_mutation_failed = True
        else:
            type_mutation_failed = False
        check("packed-column type mutation fails", type_mutation_failed)
        graphic.write_bytes(original)

        actor_lines = actorclass.read_text(encoding="utf-8").splitlines()
        actorclass.write_text(
            "\n".join(actor_lines[:-1]) + "\n", encoding="utf-8", newline=""
        )
        try:
            census.build(graphic, actorclass, display)
        except ValueError:
            missing_join_failed = True
        else:
            missing_join_failed = False
        check("missing actorclass correlation fails", missing_join_failed)

    if FAILED:
        print("FAIL: " + "; ".join(FAILED))
        return 1
    print(f"PASS: {len(PASSED)} actor appearance census checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
