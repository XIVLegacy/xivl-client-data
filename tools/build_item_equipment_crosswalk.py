#!/usr/bin/env python3
"""Build and verify the retail item/equipment column crosswalk."""

from __future__ import annotations

import argparse
import csv
import io
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from _csv_reader import CsvHeader, CsvRow, read_csv
from _csv_root import add_csv_dir_argument, default_csv_dir


REPO = Path(__file__).resolve().parents[1]
CSV_DIR = default_csv_dir()
OUTPUT = REPO / "docs" / "item-equipment-columns.md"
INVENTORY = REPO / "manifests" / "sheet_inventory.csv"
EXPECTED_INVENTORY = {
    "equipment": ("16973991", "0x010300A7", "game_schema"),
    "itemData": ("16974121", "0x01030129", "game_schema"),
    "xtx/text_paramName": ("189071483", "0x0B45007B", "game_schema"),
}

KNOWN_GEAR = {
    8030423: "body capture 0x007A88D7",
    8011608: "helm capture 0x007A3F58",
    4030013: "weapon capture 0x003D7E3D",
}


@dataclass(frozen=True)
class ColumnSpec:
    sheet: str
    column: int
    role: str
    value_kind: str


@dataclass(frozen=True)
class ColumnSummary:
    spec: ColumnSpec
    declared_type: str
    row_count: int
    blank_count: int
    zero_count: int
    minus_one_count: int
    active_count: int
    domain: str
    examples: str


def _specs() -> tuple[ColumnSpec, ...]:
    specs: list[ColumnSpec] = []
    for number, start in enumerate((49, 52, 55, 58), 1):
        specs.extend(
            (
                ColumnSpec("itemData.csv", start, f"parameter {number} grow selector", "blank"),
                ColumnSpec("itemData.csv", start + 1, f"parameter {number} base value", "scalar"),
                ColumnSpec(
                    "itemData.csv",
                    start + 2,
                    f"parameter {number} compatibility adjustment",
                    "blank",
                ),
            )
        )
    equipment_roles = {
        71: "condition-parameter scalar 1; data-shaped parameter ID",
        72: "condition-parameter scalar 2; data-shaped value",
        73: "condition-parameter scalar 3; data-shaped parameter ID",
        74: "condition-parameter scalar 4; data-shaped value",
        75: "base append-parameter ID",
        76: "base append-parameter value",
        77: "quality-gated parameter ID",
        78: "quality-gated parameter value",
    }
    for column in range(79, 91):
        pair = (column - 79) // 2 + 1
        equipment_roles[column] = (
            f"append-parameter pair {pair} "
            + ("ID" if column % 2 else "value")
        )
    for column in range(71, 91):
        specs.append(
            ColumnSpec(
                "equipment.csv",
                column,
                equipment_roles[column],
                "id" if column % 2 else "scalar",
            )
        )
    return tuple(specs)


COLUMN_SPECS = _specs()
ID_COLUMNS = tuple(
    spec.column
    for spec in COLUMN_SPECS
    if spec.sheet == "equipment.csv" and spec.value_kind == "id"
)
FORMULA_ID_COLUMNS = tuple(column for column in ID_COLUMNS if column >= 75)
EXPECTED_TYPES = {
    "itemData.csv": {
        column: ("float" if column in (50, 53, 56, 59) else "")
        for column in range(49, 61)
    },
    "equipment.csv": {
        71: "s16",
        72: "s16",
        73: "s16",
        74: "s16",
        75: "s32",
        76: "s16",
        77: "s32",
        78: "s16",
        79: "s32",
        80: "s16",
        81: "s32",
        82: "s16",
        83: "s32",
        84: "s16",
        85: "s32",
        86: "s16",
        87: "s32",
        88: "s16",
        89: "s32",
        90: "s16",
    },
}


def load_sheet(path: Path) -> tuple[CsvHeader, list[CsvRow]]:
    header, iterator = read_csv(path)
    rows = list(iterator)
    width = len(header.column_indices)
    if len(header.column_types) != width:
        raise ValueError(f"{path.name}: label/type header widths differ")
    if header.column_indices != [str(index) for index in range(width)]:
        raise ValueError(f"{path.name}: column labels are not contiguous zero-based indices")
    seen: set[str] = set()
    for row in rows:
        if len(row.values) != width:
            raise ValueError(f"{path.name}: row {row.row_id} has width {len(row.values)} != {width}")
        if row.row_id in seen:
            raise ValueError(f"{path.name}: duplicate row id {row.row_id}")
        seen.add(row.row_id)
    return header, rows


def _numeric_key(value: str) -> tuple[float, str]:
    return float(value), value


def _domain(values: list[str]) -> str:
    counts = Counter(values)
    if len(counts) <= 12:
        ordered = sorted(counts, key=lambda value: (-1, "") if value == "" else _numeric_key(value))
        return ", ".join(("blank" if value == "" else value) + f" ({counts[value]})" for value in ordered)
    numeric = [value for value in counts if value != ""]
    low = min(numeric, key=_numeric_key)
    high = max(numeric, key=_numeric_key)
    frequent = sorted(counts.items(), key=lambda item: (-item[1], _numeric_key(item[0])))[:4]
    top = ", ".join(f"{value} ({count})" for value, count in frequent)
    return f"{low}..{high}; {len(counts)} distinct; top {top}"


def _examples(rows: list[CsvRow], column: int, value_kind: str) -> str:
    candidates = [
        row
        for row in rows
        if row.values[column] != ""
        and not (value_kind == "id" and row.values[column] == "-1")
        and not (value_kind == "scalar" and row.values[column] == "0")
    ]
    if not candidates:
        return "none"
    by_value = sorted(candidates, key=lambda row: (_numeric_key(row.values[column]), int(row.row_id)))
    chosen = [by_value[0], by_value[-1]]
    first = min(candidates, key=lambda row: int(row.row_id))
    chosen.append(first)
    unique: list[CsvRow] = []
    for row in chosen:
        if row.row_id not in {item.row_id for item in unique}:
            unique.append(row)
    return ", ".join(f"{row.row_id}={row.values[column]}" for row in unique)


def summarize(spec: ColumnSpec, header: CsvHeader, rows: list[CsvRow]) -> ColumnSummary:
    values = [row.values[spec.column] for row in rows]
    counts = Counter(values)
    if spec.value_kind == "id":
        active_count = len(values) - counts["-1"]
    elif spec.value_kind == "blank":
        active_count = len(values) - counts[""]
    else:
        active_count = len(values) - counts["0"] - counts["-1"]
    return ColumnSummary(
        spec=spec,
        declared_type=header.column_types[spec.column] or "untyped",
        row_count=len(rows),
        blank_count=counts[""],
        zero_count=counts["0"],
        minus_one_count=counts["-1"],
        active_count=active_count,
        domain=_domain(values),
        examples=_examples(rows, spec.column, spec.value_kind),
    )


def validate_requested_types(sheet: str, header: CsvHeader) -> None:
    for column, expected in EXPECTED_TYPES[sheet].items():
        actual = header.column_types[column]
        if actual != expected:
            label = expected or "untyped"
            actual_label = actual or "untyped"
            raise ValueError(
                f"{sheet}: column {column} type {actual_label!r} != {label!r}"
            )


def load_param_names(path: Path) -> dict[int, str]:
    header, rows = load_sheet(path)
    if header.column_types != ["str"] * 10:
        raise ValueError(f"{path.name}: expected ten string columns")
    return {int(row.row_id): row.values[1] for row in rows}


def parameter_join(parameter_id: int, names: dict[int, str]) -> tuple[str, int, str] | None:
    if parameter_id in names:
        return "direct row-id", parameter_id, names[parameter_id]
    base_id = parameter_id - 1_000_000
    if base_id in names and 1_015_000 <= parameter_id <= 1_016_999:
        return "minus-1000000", base_id, names[base_id]
    return None


def _active_ids(rows: list[CsvRow], columns: tuple[int, ...]) -> list[int]:
    return [
        int(row.values[column])
        for row in rows
        for column in columns
        if row.values[column] != "-1"
    ]


def join_audit(
    rows: list[CsvRow],
    names: dict[int, str],
    columns: tuple[int, ...] = ID_COLUMNS,
) -> list[dict[str, object]]:
    bands = (
        ("15xxx", 15_000, 15_999, "direct row-id"),
        ("16xxx", 16_000, 16_999, "direct row-id"),
        ("20xxx", 20_000, 20_999, "direct row-id"),
        ("1015xxx", 1_015_000, 1_015_999, "minus-1000000"),
        ("1016xxx", 1_016_000, 1_016_999, "minus-1000000"),
    )
    active = _active_ids(rows, columns)
    output = []
    for label, low, high, rule in bands:
        values = [value for value in active if low <= value <= high]
        distinct = sorted(set(values))
        matched = [
            value
            for value in distinct
            if (joined := parameter_join(value, names)) is not None
            and joined[0] == rule
        ]
        if len(matched) != len(distinct):
            raise ValueError(
                f"{label}: parameter-name join mismatch for "
                f"{sorted(set(distinct) - set(matched))}"
            )
        output.append(
            {
                "band": label,
                "occurrences": len(values),
                "distinct": len(distinct),
                "rule": rule,
                "matched": len(matched),
            }
        )
    covered = sum(int(row["occurrences"]) for row in output)
    if covered != len(active):
        unsupported = sorted(set(active) - {value for value in active if parameter_join(value, names)})
        raise ValueError(f"unsupported equipment parameter ids: {unsupported}")
    return output


def pair_audit(rows: list[CsvRow]) -> list[dict[str, int]]:
    output = []
    for id_column in ID_COLUMNS:
        value_column = id_column + 1
        output.append(
            {
                "idColumn": id_column,
                "valueColumn": value_column,
                "minusOneZero": sum(
                    row.values[id_column] == "-1"
                    and row.values[value_column] == "0"
                    for row in rows
                ),
                "minusOneNonzero": sum(
                    row.values[id_column] == "-1"
                    and row.values[value_column] not in ("0", "")
                    for row in rows
                ),
                "liveIdZero": sum(
                    row.values[id_column] != "-1"
                    and row.values[value_column] == "0"
                    for row in rows
                ),
            }
        )
    return output


def _tuple(rows: dict[int, CsvRow], columns: range, row_id: int) -> str:
    row = rows[row_id]
    return "(" + ", ".join(row.values[column] or "blank" for column in columns) + ")"


def _inventory_search(path: Path) -> tuple[int, list[str], list[str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    indexed = {row["name"]: row for row in rows}
    for name, expected in EXPECTED_INVENTORY.items():
        row = indexed.get(name)
        actual = (
            row["resource_id"],
            row["resource_id_hex"],
            row["source"],
        ) if row else None
        if actual != expected:
            raise ValueError(f"sheet inventory mismatch for {name}: {actual!r}")
    names = list(indexed)
    grow = sorted(name for name in names if "grow" in name.casefold())
    parameter = sorted(name for name in names if "param" in name.casefold())
    return len(rows), grow, parameter


def render(
    summaries: list[ColumnSummary],
    sheets: dict[str, list[CsvRow]],
    joins: list[dict[str, object]],
    formula_id_counts: tuple[int, int],
    pairs: list[dict[str, int]],
    inventory_result: tuple[int, list[str], list[str]],
    item_names: dict[int, str],
) -> bytes:
    inventory_count, grow_names, parameter_names = inventory_result
    out = io.StringIO(newline="")
    out.write("# Retail item/equipment column crosswalk\n\n")
    out.write(
        "This is the canonical extraction `2012.09.19.0001` crosswalk for the "
        "`itemDataSheet` columns used by the promoted client formulas. It joins "
        "operational roles from `xivl-client-scripts:docs/equipment-parameter-formulas.md` "
        "to the repository-local `itemData.csv` and `equipment.csv` schemas. Column "
        "numbers are zero-based. Regenerate or verify it with "
        "`python tools/build_item_equipment_crosswalk.py [--check]`.\n\n"
    )
    out.write(
        "The canonical sheet inventory identifies `itemData` as game-schema "
        "resource `0x01030129`, `equipment` as `0x010300A7`, and the localized "
        "parameter-name sheet `xtx/text_paramName` as `0x0B45007B`. The source CSV "
        "type rows, rather than inferred runtime widths, supply the stored types "
        "below.\n\n"
    )
    out.write("## Column census\n\n")
    out.write(
        "`Active` means nonblank for untyped columns, neither `0` nor `-1` for "
        "scalar columns, and not `-1` for data-shaped ID columns. `Examples` are deterministic "
        "`row_id=value` locators, not semantic labels.\n\n"
    )
    out.write("| Sheet.column | Consumer role | Stored type | Blank | Zero | -1 | Active | Domain | Examples |\n")
    out.write("|---|---|---:|---:|---:|---:|---:|---|---|\n")
    for summary in summaries:
        spec = summary.spec
        out.write(
            f"| `{spec.sheet[:-4]}.{spec.column}` | {spec.role} | `{summary.declared_type}` | "
            f"{summary.blank_count} | {summary.zero_count} | {summary.minus_one_count} | "
            f"{summary.active_count} | {summary.domain} | {summary.examples} |\n"
        )

    out.write("\n## Parameter-ID joins\n\n")
    out.write(
        "The odd equipment columns have an alternating ID/value data shape. This "
        "does not override the formula contract: columns 71-74 remain four returned "
        "condition scalars there, while columns 75-90 have the explicit combination "
        "roles shown above. Every observed non-`-1` odd-column ID resolves to the "
        "localized English name in `csv/xtx_text_paramName.csv` by one of two "
        "data-supported key rules:\n\n"
    )
    formula_occurrences, formula_distinct = formula_id_counts
    all_occurrences = sum(int(row["occurrences"]) for row in joins)
    all_distinct = sum(int(row["distinct"]) for row in joins)
    out.write(
        f"The eight formula-defined ID columns 75, 77, 79, 81, 83, 85, 87, "
        f"and 89 contain {formula_occurrences} non-sentinel occurrences and "
        f"{formula_distinct} distinct IDs. Including the two data-shaped condition "
        f"columns 71 and 73 yields {all_occurrences} occurrences and {all_distinct} "
        "distinct IDs across the five bands below.\n\n"
    )
    out.write("| ID band | Occurrences | Distinct IDs | Join rule | Named IDs |\n")
    out.write("|---|---:|---:|---|---:|\n")
    for row in joins:
        out.write(
            f"| `{row['band']}` | {row['occurrences']} | {row['distinct']} | "
            f"{row['rule']} | {row['matched']} |\n"
        )
    out.write(
        "\nThe direct join is an exact row-ID match. The offset join is limited to "
        "the observed 1015xxx and 1016xxx bands and removes 1,000,000 before the "
        "same row-ID lookup. It is supported by the retail item-table audit in "
        "`xivl-captures:studies/gamerescape-tables/derived/client-column-map-notes.md`; "
        "the analyzer does not generalize it to another band. The join supplies a "
        "localized parameter label only. It does not establish value units, a "
        "parameter category, equipment eligibility, or a mapping to actor "
        "`generalParameter` indices.\n\n"
    )
    out.write("### Pair sentinel audit\n\n")
    out.write(
        "No requested equipment cell is blank. The pair census distinguishes the "
        "canonical `(-1, 0)` shape from residual values beside `-1`; it must not be "
        "used to invent a skip rule where the promoted consumer does not have one.\n\n"
    )
    out.write("| Pair | `(-1, 0)` | `(-1, nonzero)` | `(live ID, 0)` |\n")
    out.write("|---|---:|---:|---:|\n")
    for pair in pairs:
        out.write(
            f"| `{pair['idColumn']}/{pair['valueColumn']}` | "
            f"{pair['minusOneZero']} | {pair['minusOneNonzero']} | "
            f"{pair['liveIdZero']} |\n"
        )
    out.write(
        "\nThe client formula explicitly skips `-1` for column 75 and the six IDs "
        "in columns 79, 81, 83, 85, 87, and 89. It does not establish that skip "
        "rule for quality-gated column 77, and it returns columns 71-74 directly. "
        "Accordingly, `-1` is a proven consumer sentinel only for the seven "
        "skip-tested ID columns.\n\n"
    )
    out.write(
        f"The {inventory_count}-sheet inventory has these parameter-bearing names: "
        f"`{', '.join(parameter_names)}`. Only `xtx/text_paramName` is a parameter "
        "label sheet; the others are geographic parameter sheets. No inventory "
        "sheet name identifies a parameter-unit or parameter-category table. The "
        "two unit values returned by the client `desktopWidget` consumer therefore "
        "remain a native/UI boundary rather than a corpus join.\n\n"
    )

    out.write("## Retail gear anchors\n\n")
    out.write(
        "The three catalog IDs retained by the equipment-property correlation study "
        "are all present in both source sheets. Their tuples keep the requested "
        "columns in source order and do not assign meaning to the observed "
        "`generalParameter[18]` changes.\n\n"
    )
    out.write("| Evidence anchor | Client item name | itemData 49-60 | equipment 71-90 |\n")
    out.write("|---|---|---|---|\n")
    item_rows = {int(row.row_id): row for row in sheets["itemData.csv"]}
    equipment_rows = {int(row.row_id): row for row in sheets["equipment.csv"]}
    for row_id, anchor in KNOWN_GEAR.items():
        out.write(
            f"| {anchor} / row `{row_id}` | {item_names[row_id]} | "
            f"`{_tuple(item_rows, range(49, 61), row_id)}` | "
            f"`{_tuple(equipment_rows, range(71, 91), row_id)}` |\n"
        )
    out.write(
        "\nSource: `xivl-captures:studies/equipment-property-correlation/derived/evidence-map.md`. "
        "The packet study proves item/equipment-slot linkage and actor-property "
        "chronology, not a particular parameter noun.\n\n"
    )

    out.write("## Grow-selector and rejected-join boundary\n\n")
    out.write(
        "All four grow-selector columns (49, 52, 55, 58) and all four compatibility "
        "columns (51, 54, 57, 60) are untyped and blank on every `itemData.csv` row. "
        "The corpus therefore has no stored selector values from which to recover a "
        "domain. The formula's negative-selector-to-nil behavior is a client-consumer "
        "contract, not a sentinel observed in this extraction.\n\n"
    )
    out.write(
        f"A normalized `grow` search over all {inventory_count} canonical sheet names "
        f"returns {len(grow_names)} matches"
        + (f" (`{', '.join(grow_names)}`)" if grow_names else "")
        + ". This is a bounded sheet-inventory negative only: it does not rule out "
        "native tables behind `getGrowData` or `judgeGrowColumn`. No grow-table join "
        "can be promoted from this data corpus.\n\n"
    )
    out.write(
        "Rejected joins are: treating the offset IDs as direct `paramName` row IDs; "
        "mapping parameter IDs to actor `generalParameter` indices; assigning units "
        "or categories from numeric magnitude; and treating blank grow or "
        "compatibility cells as zero. The corpus also does not establish public "
        "field names for these numeric columns, the four condition names, HQ "
        "semantics, server authority, or equipment eligibility.\n"
    )
    return out.getvalue().encode("ascii")


def build(csv_dir: Path = CSV_DIR, inventory: Path = INVENTORY) -> bytes:
    loaded = {
        name: load_sheet(csv_dir / name)
        for name in ("itemData.csv", "equipment.csv", "xtx_text_paramName.csv", "xtx_itemName.csv")
    }
    sheets = {name: rows for name, (_header, rows) in loaded.items()}
    headers = {name: header for name, (header, _rows) in loaded.items()}
    for sheet in EXPECTED_TYPES:
        validate_requested_types(sheet, headers[sheet])
    summaries = [summarize(spec, headers[spec.sheet], sheets[spec.sheet]) for spec in COLUMN_SPECS]
    names = load_param_names(csv_dir / "xtx_text_paramName.csv")
    joins = join_audit(sheets["equipment.csv"], names)
    formula_ids = _active_ids(sheets["equipment.csv"], FORMULA_ID_COLUMNS)
    item_names = {int(row.row_id): row.values[6] for row in sheets["xtx_itemName.csv"]}
    for row_id in KNOWN_GEAR:
        for sheet in ("itemData.csv", "equipment.csv"):
            if row_id not in {int(row.row_id) for row in sheets[sheet]}:
                raise ValueError(f"{sheet}: missing retail gear anchor {row_id}")
        if row_id not in item_names:
            raise ValueError(f"xtx_itemName.csv: missing retail gear anchor {row_id}")
    return render(
        summaries,
        sheets,
        joins,
        (len(formula_ids), len(set(formula_ids))),
        pair_audit(sheets["equipment.csv"]),
        _inventory_search(inventory),
        item_names,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_csv_dir_argument(parser)
    parser.add_argument("--check", action="store_true", help="verify the canonical document")
    args = parser.parse_args()
    rendered = build(args.csv_dir)
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != rendered:
            print(f"out of date: {OUTPUT.relative_to(REPO)}")
            return 1
        print("verified retail item/equipment column crosswalk")
        return 0
    OUTPUT.write_bytes(rendered)
    print(f"wrote {OUTPUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
