"""Profile typed item columns for possible graphics-model encodings."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from _csv_root import add_csv_dir_argument, default_csv_dir
except ModuleNotFoundError:  # pragma: no cover - package import path
    from ._csv_root import add_csv_dir_argument, default_csv_dir

CSV_ROOT = default_csv_dir()

CANDIDATES = {
    "weapon.csv": list(range(92, 112)) + [135, 136, 141],
    "equipment.csv": list(range(69, 91)) + [137, 138, 139],
}

INTEGER_TYPES = {"s8": 8, "u8": 8, "s16": 16, "u16": 16, "s32": 32, "u32": 32}
GRAPHICS_FIELDS = ("weaponId", "equipmentId", "variantId", "colorId")
GRAPHICS_ROW = re.compile(
    r"\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    add_csv_dir_argument(parser)
    parser.add_argument(
        "--graphics-sql",
        type=Path,
        help="optional historical graphics SQL used only for correlation",
    )
    parser.add_argument("--output", type=Path, help="write JSON here instead of stdout")
    return parser.parse_args()


def parse_value(raw: str, type_name: str) -> int | float | None:
    if raw == "":
        return None
    if type_name == "bool":
        return int(raw.lower() not in {"0", "false"})
    if type_name == "float":
        return float(raw)
    return int(raw)


def read_candidates(
    filename: str,
    csv_dir: Path = CSV_ROOT,
) -> tuple[dict[int, str], dict[int, dict[int, int | float | None]]]:
    path = csv_dir / filename
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        labels = next(reader)[1:]
        types = next(reader)[1:]
        wanted = CANDIDATES[filename]
        type_map = {column: types[column] for column in wanted}
        rows: dict[int, dict[int, int | float | None]] = {}
        for raw_row in reader:
            if not raw_row:
                continue
            row_id = int(raw_row[0])
            values = raw_row[1:]
            rows[row_id] = {
                column: parse_value(values[column] if column < len(values) else "", type_map[column])
                for column in wanted
            }
    if labels != [str(index) for index in range(len(labels))]:
        raise ValueError(f"{path}: non-canonical numeric column labels")
    return type_map, rows


def entropy(counter: Counter[int], count: int) -> float:
    if not count:
        return 0.0
    return -sum((n / count) * math.log2(n / count) for n in counter.values())


def packed_profile(values: list[int], bits: int) -> dict[str, Any]:
    mask = (1 << bits) - 1
    encoded = [value & mask for value in values]
    byte_count = bits // 8
    lanes = []
    for lane in range(byte_count):
        frequencies = Counter((value >> (lane * 8)) & 0xFF for value in encoded)
        lanes.append(
            {
                "lane": lane,
                "distinct": len(frequencies),
                "zeroCount": frequencies[0],
                "entropyBits": round(entropy(frequencies, len(encoded)), 6),
            }
        )
    return {
        "valueCount": len(encoded),
        "bitwiseOrHex": f"0x{_bitwise_or(encoded):0{bits // 4}X}",
        "nonzeroUpperByteCount": sum(value >> 8 != 0 for value in encoded),
        "byteLanesLeastSignificantFirst": lanes,
    }


def _bitwise_or(values: list[int]) -> int:
    result = 0
    for value in values:
        result |= value
    return result


def pearson(pairs: list[tuple[float, float]]) -> float | None:
    if len(pairs) < 2:
        return None
    xs, ys = zip(*pairs)
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    xx = sum((x - mean_x) ** 2 for x in xs)
    yy = sum((y - mean_y) ** 2 for y in ys)
    if xx == 0 or yy == 0:
        return None
    return sum((x - mean_x) * (y - mean_y) for x, y in pairs) / math.sqrt(xx * yy)


def column_profile(values: list[int | float | None], type_name: str) -> dict[str, Any]:
    present = [value for value in values if value is not None]
    frequencies = Counter(present)
    profile: dict[str, Any] = {
        "type": type_name,
        "rowCount": len(values),
        "blankCount": len(values) - len(present),
        "zeroCount": frequencies[0],
        "minusOneCount": frequencies[-1],
        "minimum": min(present) if present else None,
        "maximum": max(present) if present else None,
        "distinctCount": len(frequencies),
        "nonSentinelDistinctCount": len({value for value in present if value not in {0, -1}}),
        "frequencies": {str(key): frequencies[key] for key in sorted(frequencies)},
    }
    if type_name in INTEGER_TYPES:
        packed_values = [int(value) for value in present if value not in {0, -1}]
        profile["packedProfileExcludingZeroAndMinusOne"] = packed_profile(
            packed_values, INTEGER_TYPES[type_name]
        )
    return profile


def parse_graphics_sql(path: Path) -> dict[int, dict[str, int]]:
    text = path.read_text(encoding="utf-8", errors="strict")
    result: dict[int, dict[str, int]] = {}
    for match in GRAPHICS_ROW.finditer(text):
        catalog_id, *payload = (int(value) for value in match.groups())
        result[catalog_id] = dict(zip(GRAPHICS_FIELDS, payload, strict=True))
    if not result:
        raise ValueError(f"{path}: no five-field graphics rows found")
    return result


def reference_profile(
    rows: dict[int, dict[int, int | float | None]], graphics: dict[int, dict[str, int]]
) -> dict[str, Any]:
    overlap = sorted(rows.keys() & graphics.keys())
    correlations: dict[str, Any] = {}
    for column in next(iter(rows.values())):
        correlations[str(column)] = {}
        for field in GRAPHICS_FIELDS:
            pairs = [
                (float(rows[row_id][column]), float(graphics[row_id][field]))
                for row_id in overlap
                if rows[row_id][column] is not None
            ]
            exact = sum(left == right for left, right in pairs)
            non_sentinel_pairs = [
                (left, right) for left, right in pairs if left not in {0, -1} and right not in {0, -1}
            ]
            correlations[str(column)][field] = {
                "pairCount": len(pairs),
                "exactCount": exact,
                "nonSentinelPairCount": len(non_sentinel_pairs),
                "nonSentinelExactCount": sum(left == right for left, right in non_sentinel_pairs),
                "pearson": None if (value := pearson(pairs)) is None else round(value, 6),
            }
    return {"overlapCount": len(overlap), "correlations": correlations}


def analyze(
    graphics_path: Path | None,
    csv_dir: Path = CSV_ROOT,
) -> dict[str, Any]:
    graphics = parse_graphics_sql(graphics_path) if graphics_path else None
    report: dict[str, Any] = {
        "scope": {name: CANDIDATES[name] for name in CANDIDATES},
        "graphicsSqlRole": "historical-target-correlation-only" if graphics else None,
        "sheets": {},
    }
    for filename in CANDIDATES:
        type_map, rows = read_candidates(filename, csv_dir)
        ids = sorted(rows)
        columns = {
            str(column): column_profile([rows[row_id][column] for row_id in ids], type_map[column])
            for column in CANDIDATES[filename]
        }
        correlations: dict[str, dict[str, float | None]] = {}
        for left in CANDIDATES[filename]:
            correlations[str(left)] = {}
            for right in CANDIDATES[filename]:
                pairs = [
                    (float(rows[row_id][left]), float(rows[row_id][right]))
                    for row_id in ids
                    if rows[row_id][left] is not None and rows[row_id][right] is not None
                ]
                value = pearson(pairs)
                correlations[str(left)][str(right)] = None if value is None else round(value, 6)
        sheet: dict[str, Any] = {
            "rowCount": len(rows),
            "columns": columns,
            "pearsonCorrelations": correlations,
        }
        if graphics is not None:
            sheet["historicalGraphicsCrosscheck"] = reference_profile(rows, graphics)
        report["sheets"][filename] = sheet
    return report


def main() -> int:
    args = parse_args()
    report = analyze(args.graphics_sql, args.csv_dir)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
