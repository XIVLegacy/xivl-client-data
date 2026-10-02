#!/usr/bin/env python3
"""Focused tests for the localized-name crosswalk."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import build_autotranslate_name_crosswalk as builder
from _csv_reader import CsvRow


PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(name)


def main() -> int:
    # Literal source-shaped row: field 0 and the row key are deliberately
    # different, and every required locale has an explicit missing value.
    phrase = CsvRow(
        "974",
        [
            "9",
            "",
            "\u30de\u30c3\u30d7",
            "",
            "Map",
            "",
            "Karte",
            "",
            "Carte",
            "",
            "\u5730\u56fe",
            "",
        ],
    )
    phrase_names = builder._localized_fields(phrase, "fixedPhrase")
    check("fixed phrase keeps row key separate from field 0", phrase.row_id == "974")
    check("fixed phrase keeps literal field 0", phrase.values[0] == "9")
    check("fixed phrase keeps literal field 1", phrase.values[1] == "")
    check(
        "fixed phrase keeps four locale anchors",
        (
            phrase_names["ja"]["2"] == "\u30de\u30c3\u30d7"
            and phrase_names["en"]["4"] == "Map"
            and phrase_names["de"]["6"] == "Karte"
            and phrase_names["fr"]["8"] == "Carte"
        ),
    )
    check("missing fixed phrase fields are explicit", phrase_names["ja"]["3"] is None)
    check(
        "source locators use exact row ids without lossy line numbers",
        builder._row_source("xtx__fixedPhrase.csv", phrase)
        == {"sheet": "xtx__fixedPhrase.csv", "rowId": "974"},
    )

    memberships = builder._group_memberships(
        [CsvRow("101", ["1051", "133", "230", "134", "232", "140"])]
    )
    check(
        "zone-group membership keeps every source column",
        [(row.row_id, column) for row, column in memberships["133"]]
        + [(row.row_id, column) for row, column in memberships["230"]]
        == [("101", 1), ("101", 2)],
    )

    configured = os.environ.get("XIVL_CSV_DIR")
    scratch_parent = os.environ.get("XIVL_TEST_SCRATCH")
    if scratch_parent is None and configured:
        scratch_parent = str(Path(configured).parent)
    temp_kwargs = {"dir": scratch_parent} if scratch_parent else {}
    with tempfile.TemporaryDirectory(
        prefix="autotranslate-name-crosswalk-", **temp_kwargs
    ) as raw:
        path = Path(raw) / "fixture.csv"
        path.write_text(",0\n,s32\n9,1\n", encoding="utf-8", newline="")
        bad_manifest = {
            "bytes": path.stat().st_size,
            "sha256": "0" * 64,
            "dataRowCount": 1,
        }
        try:
            builder._load_source(path.parent, "fixture.csv", bad_manifest)
        except ValueError:
            authenticated_failure = True
        else:
            authenticated_failure = False
    check("source hash mutation fails closed", authenticated_failure)

    item_rows = [
        {
            "id": "item:1",
            "key": 1,
            "names": {
                "ja": {"4": "\u540c\u540d"},
                "en": {"5": "Same", "6": "same", "7": "Sames"},
                "de": {"11": "Gleich", "12": "gleich", "14": "Gleiche"},
                "fr": {"19": "Meme", "20": "meme", "21": "memes"},
            },
        },
        {
            "id": "item:2",
            "key": 2,
            "names": {
                "ja": {"4": "\u5225\u540d"},
                "en": {"5": "Same", "6": "other", "7": "others"},
                "de": {"11": "Anders", "12": "anders", "14": "Andere"},
                "fr": {"19": "Autre", "20": "autre", "21": "autres"},
            },
        },
    ]
    groups = builder._ambiguity_groups(item_rows, "itemName")
    check(
        "duplicate localized names preserve both item keys",
        groups
        == [
            {
                "family": "itemName",
                "locale": "en",
                "column": 5,
                "name": "Same",
                "recordIds": ["item:1", "item:2"],
                "keys": [1, 2],
                "keyCount": 2,
            }
        ],
    )
    check(
        "grammatical form fields remain separate",
        all(group["column"] == 5 for group in groups),
    )

    first = builder.render({"z": "\u8a00\u8449", "a": 1})
    second = builder.render({"a": 1, "z": "\u8a00\u8449"})
    check(
        "rendering is deterministic and ASCII escaped",
        first == second and b"\\u8a00" in first,
    )
    check("rendering uses a final LF", first.endswith(b"\n") and b"\r" not in first)

    # When a hydrated corpus is supplied, assert literal anchors and the
    # many-to-many Limsa place/layout boundary independently of the renderer.
    if configured:
        product = builder.build(Path(configured))
        fixed = next(row for row in product["fixedPhrases"] if row["key"] == 974)
        fixed_header = next(row for row in product["fixedPhrases"] if row["key"] == 100)
        item = next(row for row in product["items"] if row["key"] == 1000001)
        place = next(row for row in product["placeNames"] if row["key"] == 1051)
        limsa = [row for row in product["zones"] if row["placeNameId"] == 1051]
        check("authenticated fixed phrase anchor", fixed["field0"]["value"] == "9")
        check("fixed phrase field 1 stays raw", fixed["field1"]["value"] is None)
        check(
            "fixed phrase header marker stays raw",
            fixed_header["field1"]["value"] == "@",
        )
        check("authenticated item anchor", item["names"]["en"]["5"] == "Gil")
        check(
            "three item source rows preserve one key",
            {
                (name, row["sheet"], row["rowId"])
                for name, row in item["joinRows"].items()
            }
            == {
                ("_item", "_item.csv", "1000001"),
                ("itemData", "itemData.csv", "1000001"),
                ("xtx_itemName", "xtx_itemName.csv", "1000001"),
            },
        )
        bat_wing = [
            row for row in product["items"] if row["key"] in {10009506, 12000016}
        ]
        check(
            "Bat Wing duplicate keeps both keys and raw item fields",
            {
                (row["key"], row["names"]["en"]["5"], row["rawJoinFields"]["_item.0"])
                for row in bat_wing
            }
            == {
                (10009506, "Bat Wing", "Normal/StandardItem"),
                (12000016, "Bat Wing", "Normal/DummyItem"),
            },
        )
        check(
            "authenticated place anchor", place["names"]["en"]["1"] == "Limsa Lominsa"
        )
        check("Limsa keeps both zone ids", [row["key"] for row in limsa] == [133, 230])
        check(
            "Limsa keeps all three layout candidates",
            sorted(
                {
                    entry["source"]["rowId"]
                    for row in limsa
                    for entry in row["layoutCandidates"]
                }
            )
            == ["121", "131", "171"],
        )
        check(
            "Limsa keeps both group membership columns",
            sorted(
                {
                    (entry["source"]["rowId"], entry["membershipColumn"])
                    for row in limsa
                    for entry in row["zoneGroupParamCandidates"]
                }
            )
            == [("101", 1), ("101", 2)],
        )
        check(
            "Limsa has no selected internal name",
            all(not row["internalNameCandidates"] for row in limsa),
        )
        check(
            "Limsa text is absent from fixed phrases",
            not any(
                value == "Limsa Lominsa"
                for row in product["fixedPhrases"]
                for fields in (
                    row["names"],
                    {"unsupported": row["unsupportedLocaleFields"]},
                )
                for locale_fields in fields.values()
                for value in locale_fields.values()
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
