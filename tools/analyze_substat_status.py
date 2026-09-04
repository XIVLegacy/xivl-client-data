#!/usr/bin/env python3
"""Build the status-word crosswalk and resolve one 0x0179 wire status id."""

from __future__ import annotations

import argparse
import csv
import io
import json
from dataclasses import dataclass
from pathlib import Path

from _csv_reader import CsvRow, read_csv
from _csv_root import add_csv_dir_argument, default_csv_dir


REPO = Path(__file__).resolve().parents[1]
CSV_DIR = default_csv_dir()
STATUS_CSV = CSV_DIR / "status.csv"
STATUS_TEXT_CSV = CSV_DIR / "xtx_status.csv"
CROSSWALK = REPO / "derived" / "substat_status_crosswalk.csv"
WIRE_BASE = 200000
HIGH_WIRE_ADJUSTMENT = 0x4350


@dataclass(frozen=True)
class StatusJoin:
    wire_id: int
    row_id: int
    english_name: str

    @property
    def status_word(self) -> int:
        return self.row_id


def parse_wire_id(value: str) -> int:
    wire_id = int(value, 0)
    if not 0 <= wire_id <= 0xFFFF:
        raise argparse.ArgumentTypeError("wire status id must fit u16")
    return wire_id


def decode_wire_id(wire_id: int) -> int:
    """Apply FUN_008A3350's retail status-key transform."""
    if not 0 <= wire_id <= 0xFFFF:
        raise ValueError("wire status id must fit u16")
    if wire_id == 0:
        return 0
    adjustment = HIGH_WIRE_ADJUSTMENT if wire_id > 0x8000 else 0
    return WIRE_BASE + wire_id - adjustment


def wire_ids_for_row(row_id: int) -> tuple[int, ...]:
    candidates = (
        row_id - WIRE_BASE,
        row_id - WIRE_BASE + HIGH_WIRE_ADJUSTMENT,
    )
    return tuple(
        candidate
        for candidate in candidates
        if 0 < candidate <= 0xFFFF and decode_wire_id(candidate) == row_id
    )


def unpack_status_word(status_word: int) -> dict[str, int]:
    return {
        "chantKind1": (status_word >> 12) & 0xF,
        "chantKind2": (status_word >> 8) & 0xF,
        "objectBits8To11": (status_word >> 8) & 0xF,
        "objectBits14To15": (status_word >> 14) & 0x3,
        "objectBits12To13": (status_word >> 12) & 0x3,
    }


def _index(path: Path) -> dict[int, CsvRow]:
    _, rows = read_csv(path)
    indexed: dict[int, CsvRow] = {}
    for row in rows:
        row_id = int(row.row_id)
        if row_id in indexed:
            raise ValueError(f"{path.name}: duplicate row id {row_id}")
        indexed[row_id] = row
    return indexed


def resolve(wire_id: int, status_path: Path, text_path: Path) -> StatusJoin:
    row_id = decode_wire_id(wire_id)
    if row_id == 0:
        raise ValueError("wire status id zero is the empty sentinel")
    statuses = _index(status_path)
    names = _index(text_path)
    if row_id not in statuses:
        raise ValueError(f"status.csv has no translated row {row_id}")
    if row_id not in names:
        raise ValueError(f"xtx_status.csv has no translated row {row_id}")
    return StatusJoin(wire_id, row_id, names[row_id].values[3])


def build_crosswalk(status_path: Path) -> bytes:
    statuses = _index(status_path)
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(
        (
            "status_row_id",
            "status_word_hex",
            "low_wire_id_hex",
            "high_wire_id_hex",
            "chant_kind_1",
            "chant_kind_2",
            "object_bits_8_11",
            "object_bits_14_15",
            "object_bits_12_13",
        )
    )
    for row_id in sorted(statuses):
        fields = unpack_status_word(row_id)
        wire_ids = wire_ids_for_row(row_id)
        low_wire_id = next((value for value in wire_ids if value <= 0x8000), None)
        high_wire_id = next((value for value in wire_ids if value > 0x8000), None)
        writer.writerow(
            (
                row_id,
                f"0x{row_id:08X}",
                "" if low_wire_id is None else f"0x{low_wire_id:04X}",
                "" if high_wire_id is None else f"0x{high_wire_id:04X}",
                fields["chantKind1"],
                fields["chantKind2"],
                fields["objectBits8To11"],
                fields["objectBits14To15"],
                fields["objectBits12To13"],
            )
        )
    return output.getvalue().encode("ascii")


def report(join: StatusJoin) -> dict[str, object]:
    fields = unpack_status_word(join.status_word)
    return {
        "wireStatusIdHex": f"0x{join.wire_id:04X}",
        "allWireIdsForRowHex": [
            f"0x{wire_id:04X}" for wire_id in wire_ids_for_row(join.row_id)
        ],
        "statusRowId": join.row_id,
        "statusWordHex": f"0x{join.status_word:08X}",
        "englishName": join.english_name,
        **fields,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_csv_dir_argument(parser)
    parser.add_argument("--wire-id", type=parse_wire_id, default=0x5ADF)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    status_path = args.csv_dir / "status.csv"
    status_text_path = args.csv_dir / "xtx_status.csv"
    rendered = build_crosswalk(status_path)
    if args.check:
        if not CROSSWALK.is_file() or CROSSWALK.read_bytes() != rendered:
            raise SystemExit(f"{CROSSWALK}: stale or missing")
    else:
        CROSSWALK.parent.mkdir(parents=True, exist_ok=True)
        CROSSWALK.write_bytes(rendered)

    print(json.dumps(report(resolve(args.wire_id, status_path, status_text_path)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
