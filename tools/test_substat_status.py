#!/usr/bin/env python3
"""Mutation tests for the SubStat status lookup and packed-word crosswalk."""

from __future__ import annotations

import csv
import io
import tempfile
from pathlib import Path

import analyze_substat_status as analyzer


PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(name)


def write_sheet(path: Path, width: int, rows: list[tuple[int, dict[int, str]]]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["", *(str(index) for index in range(width))])
        writer.writerow(["", *("" for _ in range(width))])
        for row_id, populated in rows:
            values = [""] * width
            for index, value in populated.items():
                values[index] = value
            writer.writerow([row_id, *values])
    return path


def raises_value_error(callable_) -> bool:
    try:
        callable_()
    except ValueError:
        return True
    return False


def main() -> int:
    check(
        "captured id translates to status row",
        analyzer.decode_wire_id(0x5ADF) == 223263,
    )
    check("zero remains the empty sentinel", analyzer.decode_wire_id(0) == 0)
    # xivl-decomp:docs/actor/status-wire-translation.md, constructor 0x008A3350.
    for wire_id, row_id in (
        (0x8000, 232768),
        (0x8001, 250001),
        (0x83E9, 251001),
        (0x9E2F, 257727),
        (0xFFFF, 282767),
    ):
        check(
            f"wire 0x{wire_id:04X} translates to literal row {row_id}",
            analyzer.decode_wire_id(wire_id) == row_id,
        )
    check(
        "captured row has only its low wire encoding",
        analyzer.wire_ids_for_row(223263) == (0x5ADF,),
    )
    for row_id, wire_id in (
        (232768, 0x8000),
        (250001, 0x8001),
        (251001, 0x83E9),
        (257727, 0x9E2F),
        (282767, 0xFFFF),
    ):
        check(
            f"row {row_id} has literal inverse 0x{wire_id:04X}",
            analyzer.wire_ids_for_row(row_id) == (wire_id,),
        )
    for row_id in (232769, 240000, 250000):
        check(f"gap row {row_id} has no wire id", not analyzer.wire_ids_for_row(row_id))
    check("empty sentinel has no wire id", not analyzer.wire_ids_for_row(0))
    check("unsupported row has no wire id", not analyzer.wire_ids_for_row(300000))
    check(
        "captured row decodes both reader domains",
        analyzer.unpack_status_word(223263)
        == {
            "chantKind1": 6,
            "chantKind2": 8,
            "objectBits8To11": 8,
            "objectBits14To15": 1,
            "objectBits12To13": 2,
        },
    )
    check(
        "out-of-range wire id fails",
        raises_value_error(lambda: analyzer.decode_wire_id(0x10000)),
    )
    check(
        "negative wire id fails",
        raises_value_error(lambda: analyzer.decode_wire_id(-1)),
    )

    with tempfile.TemporaryDirectory(prefix="substat-status-") as raw:
        directory = Path(raw)
        status = write_sheet(
            directory / "status.csv", 1, [(223263, {}), (240000, {}), (251001, {})]
        )
        text = write_sheet(directory / "xtx_status.csv", 4, [(223263, {3: "Resting"})])
        joined = analyzer.resolve(0x5ADF, status, text)
        check("status and text rows join", joined.english_name == "Resting")
        check(
            "zero cannot resolve a status row",
            raises_value_error(lambda: analyzer.resolve(0, status, text)),
        )
        first = analyzer.build_crosswalk(status)
        second = analyzer.build_crosswalk(status)
        check("crosswalk rendering is deterministic", first == second)
        check(
            "crosswalk is ASCII with literal LF",
            first.endswith(b"\n") and b"\r" not in first,
        )
        rendered = list(csv.DictReader(io.StringIO(first.decode("ascii"))))
        check(
            "crosswalk keeps literal low, gap and high wire columns",
            [
                (
                    row["status_row_id"],
                    row["low_wire_id_hex"],
                    row["high_wire_id_hex"],
                )
                for row in rendered
            ]
            == [
                ("223263", "0x5ADF", ""),
                ("240000", "", ""),
                ("251001", "", "0x83E9"),
            ],
        )

        missing = write_sheet(directory / "missing.csv", 1, [(223264, {})])
        check(
            "missing status row fails closed",
            raises_value_error(lambda: analyzer.resolve(0x5ADF, missing, text)),
        )
        check(
            "missing text row fails closed",
            raises_value_error(lambda: analyzer.resolve(0x5ADF, status, missing)),
        )
        duplicate = write_sheet(
            directory / "duplicate.csv", 1, [(223263, {}), (223263, {})]
        )
        check(
            "duplicate row fails closed",
            raises_value_error(lambda: analyzer.build_crosswalk(duplicate)),
        )

    for name in PASSED:
        print(f"PASS: {name}")
    for name in FAILED:
        print(f"FAIL: {name}")
    print(f"{len(PASSED)} passed; {len(FAILED)} failed")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
