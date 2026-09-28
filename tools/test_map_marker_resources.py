#!/usr/bin/env python3
"""Mutation tests for the retail map-marker resource crosswalk."""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

import build_map_marker_resources as builder

PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(name)


def write_sheet(
    path: Path, width: int, types: dict[int, str], rows: list[list[str]]
) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["", *(str(index) for index in range(width))])
        writer.writerow(["", *(types.get(index, "") for index in range(width))])
        writer.writerows(rows)
    return path


def raises_value_error(callable_) -> bool:
    try:
        callable_()
    except ValueError:
        return True
    return False


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="map-marker-resources-") as raw:
        directory = Path(raw)
        write_sheet(
            directory / "2Dmap_actor_data.csv",
            3,
            {0: "s32", 1: "str", 2: "str"},
            [["1", "1", "common/mapMarker.le.spk", "m00001"]],
        )
        write_sheet(
            directory / "2Dmap_marker.csv",
            18,
            {1: "s32", 2: "s32", 8: "str", 9: "str", 13: "str", 14: "str", 15: "str"},
            [
                [
                    "2",
                    "",
                    "10",
                    "20",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "common/mapMarker.le.spk",
                    "m00022",
                    "",
                    "",
                    "",
                    "MapMarkerPoint",
                    "@5204/i2",
                    "Collapsed",
                    "",
                    "",
                ],
                [
                    "3",
                    "",
                    "30",
                    "40",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "common/mapMarker.le.spk",
                    "m00022",
                    "",
                    "",
                    "",
                    "MapMarkerPoint",
                    "@5204/i3",
                    "Collapsed",
                    "",
                    "",
                ],
            ],
        )
        write_sheet(
            directory / "quest_marker.csv",
            14,
            {
                2: "float",
                3: "float",
                6: "str",
                7: "str",
                11: "str",
                12: "str",
                13: "str",
            },
            [
                [
                    "4",
                    "",
                    "",
                    "1.5",
                    "-2.5",
                    "",
                    "",
                    "common/mapMarker.le.spk",
                    "m00013",
                    "",
                    "",
                    "",
                    "MapMarkerQuest",
                    "@5208/i4",
                    "Visible",
                ]
            ],
        )
        loaded = {
            name: builder.load_source(directory / name, spec)
            for name, spec in builder.SOURCE_SPECS.items()
        }
        grouped = builder.grouped_rows(loaded)
        check("all three source families are retained", len(grouped) == 3)
        point = next(row for row in grouped if row[3] == "MapMarkerPoint")
        check("identical resources group deterministically", point[5:] == [2, 2, 3])
        rendered = builder.render_crosswalk(grouped)
        check(
            "rendering is ASCII with literal LF",
            rendered.endswith(b"\n") and b"\r" not in rendered,
        )
        check(
            "rendering is deterministic", rendered == builder.render_crosswalk(grouped)
        )
        check(
            "property prefix coverage is exact",
            builder._property_summary(loaded["2Dmap_marker.csv"][1], 14, "@5204/i")[
                "matchingRowCount"
            ]
            == 2,
        )

        malformed = write_sheet(directory / "bad.csv", 2, {}, [["1", "a", "b"]])
        check(
            "header-width mutation fails closed",
            raises_value_error(
                lambda: builder.load_source(
                    malformed, builder.SOURCE_SPECS["2Dmap_actor_data.csv"]
                )
            ),
        )
        truncated = write_sheet(directory / "truncated.csv", 3, {}, [["1", "a", "b"]])
        check(
            "truncated-row mutation fails closed",
            raises_value_error(
                lambda: builder.load_source(
                    truncated, builder.SOURCE_SPECS["2Dmap_actor_data.csv"]
                )
            ),
        )
    for name in PASSED:
        print(f"PASS: {name}")
    for name in FAILED:
        print(f"FAIL: {name}")
    print(f"{len(PASSED)} passed; {len(FAILED)} failed")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
