"""Authenticate xtx/itemName backing blocks against the merged CSV."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from _csv_root import add_csv_dir_argument
from build_place_name_backing_rows import REPO, build_named, render

OUTPUT = REPO / "manifests" / "item_name_backing_rows.json"
ANCHORS = (1, 1000001, 1000002, 2000101, 10009506, 12000016, 13000001)


def build(client_root: Path, csv_dir: Path) -> dict[str, Any]:
    report = build_named(
        client_root,
        csv_dir,
        "xtx/itemName",
        "xtx_itemName.csv",
        None,
        ANCHORS,
        ("chs",),
    )
    report["tokenContract"]["supportedCodes"]["0x28"] = "sheet"
    report["tokenContract"]["supportedCodes"]["0x1A"] = "italic"
    report["tokenContract"]["supportedCodes"]["0x1D"] = "non-breaking-space"
    report["nativeBoundary"] = {
        "backingRowToCsv": "proven",
        "conditionalCacheKey": "proven",
        "conditionalCacheKeyReference": (
            "xivl-client-structs:docs/autotranslate-selection-contract.md"
            "#native-block-slots-and-conditional-csv-keys"
        ),
        "conditionalCacheKeyRevision": "143ff251b5e2d8ffc464207ccb097476cf17ad73",
        "statement": (
            "The generic AT-COMP-016 ready CacheAll mapping supplies a named "
            "block key as begin + slot, with storage index prior block counts + "
            "slot, strictly inside the block. This report authenticates those "
            "blocks and source cells. It does not establish historical cache "
            "state, selected item production, delivery or locale, TextModule "
            "output or admission, noun evaluation or rendering."
        ),
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-root", required=True, type=Path)
    add_csv_dir_argument(parser)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        rendered = render(build(args.client_root, Path(args.csv_dir)))
        if args.check:
            if OUTPUT.read_bytes() != rendered:
                raise ValueError("item_name_backing_rows.json is out of date")
            print("PASS: item-name backing-row report is deterministic")
        else:
            OUTPUT.write_bytes(rendered)
            print(f"wrote {OUTPUT.name} ({len(rendered)} bytes)")
    except (OSError, ValueError, KeyError, StopIteration, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
