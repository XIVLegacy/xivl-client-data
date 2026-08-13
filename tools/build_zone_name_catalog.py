"""Build zone internal-name bindings from client layout blobs and CSVs."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from _json_io import write_json  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "manifests" / "zone_internal_names.json"

# Zone-name evidence method and family roles: see docs/architectural-findings.md.
FAMILIES: dict[str, str] = {
    "sea": "29/D9/00",
    "fst": "29/B0/00",
    "roc": "28/D9/00",
    "wil": "61/5A/00",
    "lak": "03/E7/00",
    "mkt_sea": "72/42/00",
    "mkt_fst": "72/9F/00",
    "mkt_wil": "72/A6/00",
    "ocn": "2B/03/00",
    "inn": "A0/9B/00",
    "roc1": "AB/F4/00",
}

SERIES_FAMILY = {1: "sea", 2: "roc", 3: "fst", 4: "wil", 5: "lak"}

MAGIC = b"MapLayoutResourceData"
RESIDENT = b"Bk_resident\x00"
NAME_RE = re.compile(rb"(?:sea|fst|wil|roc|lak|ocn|prv|jal|cru)\d[A-Z][a-zA-Z]+\d+[a-z]?")
PLACEHOLDER_PLACE_NAME = 1501


def read_corpus_csv(csv_dir: Path, name: str) -> list[list[str]]:
    """Return data rows of a corpus CSV (header + type rows skipped)."""
    with (csv_dir / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.reader(fh))[2:]


def family_base_hex(subdir: str) -> str:
    a, b, c = subdir.split("/")
    return f"0x{a}{b}{c}00"


def scan_blobs(game_dir: Path) -> list[dict]:
    blobs: list[dict] = []
    for family, subdir in FAMILIES.items():
        directory = game_dir / "data" / Path(*subdir.split("/"))
        if not directory.is_dir():
            raise SystemExit(f"missing layout family directory: {directory}")
        for dat in sorted(directory.glob("*.DAT")):
            data = dat.read_bytes()
            if not data.startswith(MAGIC):
                continue
            names = sorted({m.group().decode() for m in NAME_RE.finditer(data)})
            primary = None
            i = data.find(RESIDENT)
            if i != -1:
                j = i + len(RESIDENT)
                raw = data[j:data.find(b"\x00", j)].decode(errors="replace")
                if NAME_RE.fullmatch(raw.encode()):
                    primary = raw
            if primary is None and len(names) == 1:
                # A stage-alias resident label is usable only when the blob contains exactly one zone name.
                primary = names[0]
            if primary is None and not names:
                continue  # divider / shared-object blob, no zone evidence
            blobs.append({
                "resourceIdHex": f"0x{subdir.replace('/', '')}{dat.stem}",
                "family": family,
                "primaryName": primary,
                "zoneNames": names,
            })
    return blobs


def slot_name(layout_id: int, usage: int) -> str | None:
    family = SERIES_FAMILY.get(layout_id // 100)
    if family is None or layout_id >= 600:
        return None
    slot = layout_id % 100
    if 1 <= slot <= 9 and usage == 1:
        return f"{family}0Field{slot:02d}"
    if 11 <= slot <= 19 and usage == 2:
        return f"{family}0Dungeon{slot - 10:02d}"
    if slot == 21:
        return f"{family}0Town01"
    if slot == 31:
        return f"{family}0Town01a"
    return None


def build(game_dir: Path, csv_dir: Path) -> dict:
    blobs = scan_blobs(game_dir)
    primaries: dict[str, set[str]] = {}
    for blob in blobs:
        if blob["primaryName"]:
            primaries.setdefault(blob["family"], set()).add(blob["primaryName"])

    layout_rows = read_corpus_csv(csv_dir, "_layout.csv")
    layouts: list[dict] = []
    for row in layout_rows:
        layout_id, usage, place_name_id = int(row[0]), int(row[2]), int(row[4])
        name = slot_name(layout_id, usage)
        if name is None:
            continue
        family = SERIES_FAMILY[layout_id // 100]
        layouts.append({
            "layoutId": layout_id,
            "family": family,
            "usage": usage,
            "placeNameId": place_name_id,
            "slotName": name,
            "blobShipped": name in primaries.get(family, set()),
        })

    zone_place = {
        int(r[0]): int(r[1])
        for r in read_corpus_csv(csv_dir, "_zoneParam.csv")
        if r[1]
    }
    zones_by_place: dict[int, list[int]] = {}
    for zone_id, place_id in zone_place.items():
        zones_by_place.setdefault(place_id, []).append(zone_id)
    layouts_by_place: dict[int, list[dict]] = {}
    for layout in layouts:
        layouts_by_place.setdefault(layout["placeNameId"], []).append(layout)

    bindings: list[dict] = []
    for place_id, zone_ids in sorted(zones_by_place.items()):
        if place_id == PLACEHOLDER_PLACE_NAME or len(zone_ids) != 1:
            continue
        candidates = layouts_by_place.get(place_id, [])
        if len(candidates) != 1:
            continue
        layout = candidates[0]
        bindings.append({
            "zoneId": zone_ids[0],
            "layoutId": layout["layoutId"],
            "zoneName": layout["slotName"],
            "placeNameId": place_id,
            "basis": "blob_primary" if layout["blobShipped"] else "layout_slot",
        })
    bindings.sort(key=lambda b: b["zoneId"])

    return {
        "_provenance": {
            "source_path": "FFXIV 1.x client install, game.ver 2012.09.19.0001",
            "method": (
                "MapLayoutResourceData blob string pools (Bk_resident primaries) "
                "joined to zone ids via _layout.csv region-series slot positions "
                "and bijective _zoneParam.csv placeName ids; a sole zone name "
                "stands in when Bk_resident is a stage alias, while shared "
                "placeName ids remain unbound."
            ),
            "evidence_class": "client_extraction",
            "limitations": [
                "zoneBindings covers only placeName-bijective zones; instanced "
                "copies and sub-area variants sharing a placeName with a "
                "sibling are not client-discriminable and stay unbound.",
                "Slot names for unshipped layouts (blobShipped false) come from "
                "the series slot rule, not from a blob string.",
                "Market/ocn/inn/roc1 family blobs carry name evidence but no "
                "series slots, so they contribute vocabulary only.",
            ],
            "generator": "tools/build_zone_name_catalog.py",
        },
        "families": {
            name: {"dataSubdir": subdir, "resourceBaseHex": family_base_hex(subdir)}
            for name, subdir in FAMILIES.items()
        },
        "blobs": blobs,
        "layouts": layouts,
        "zoneBindings": bindings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build manifests/zone_internal_names.json from the client install")
    parser.add_argument("game_dir", type=Path, help="FFXIV 1.x install root (parent of data/)")
    parser.add_argument("--csv-dir", type=Path, default=REPO_ROOT / "csv")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    if not (args.game_dir / "data").is_dir():
        print(f"not a 1.x install root (no data/): {args.game_dir}", file=sys.stderr)
        return 1

    catalog = build(args.game_dir, args.csv_dir)
    write_json(args.out, catalog)
    print(
        f"wrote {args.out} ({len(catalog['blobs'])} blobs, "
        f"{len(catalog['layouts'])} layouts, "
        f"{len(catalog['zoneBindings'])} zone bindings)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
