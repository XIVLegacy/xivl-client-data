#!/usr/bin/env python3
"""Mutation checks for curated and client-bound zone internal names."""

from __future__ import annotations

import json

from mappings import zones


PASSED: list[str] = []
FAILED: list[str] = []

REQUESTED_CURATED = {
    "192": "ocn1Battle01",
    "194": "ocn1Battle03",
    "195": "ocn1Battle04",
    "196": "ocn1Battle05",
    "198": "ocn1Battle06",
    "267": "roc1Field02",
    "268": "roc1Field03",
}
EXPECTED_VOCABULARY = {
    "ocn": {
        "ocn0Battle01",
        "ocn0Battle02",
        "ocn0Battle03",
        "ocn0Battle04",
        "ocn0Battle05",
    },
    "roc1": {"roc1Field01", "roc1Field01a", "roc1Field01b"},
}


def check(name: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(name)


def main() -> int:
    catalog = json.loads(zones._ZONE_NAME_CATALOG.read_text(encoding="utf-8"))
    bindings = {str(row["zoneId"]): row["zoneName"] for row in catalog["zoneBindings"]}
    vocabulary = {
        family: {
            name
            for blob in catalog["blobs"]
            if blob["family"] == family
            for name in blob["zoneNames"]
        }
        for family in EXPECTED_VOCABULARY
    }

    check(
        "requested rows are absent from generated bindings",
        not REQUESTED_CURATED.keys() & bindings.keys(),
    )
    check(
        "requested rows retain curated fallbacks",
        all(
            zones._EXPLICIT_ZONE_NAMES.get(zone_id) == zone_name
            for zone_id, zone_name in REQUESTED_CURATED.items()
        ),
    )
    check("client vocabulary is exact", vocabulary == EXPECTED_VOCABULARY)
    check(
        "resolver returns curated fallbacks",
        all(
            zones._resolve_zone_name(zone_id, {}) == zone_name
            for zone_id, zone_name in REQUESTED_CURATED.items()
        ),
    )

    zones._CATALOG_ZONE_NAMES = {"267": "roc1Field01a"}
    check(
        "generated binding supersedes curation",
        zones._resolve_zone_name("267", {}) == "roc1Field01a",
    )
    zones._CATALOG_ZONE_NAMES = {}
    zones._EXPLICIT_ZONE_NAMES = {
        key: value for key, value in zones._EXPLICIT_ZONE_NAMES.items() if key != "267"
    }
    try:
        zones._resolve_zone_name("267", {})
        missing_fails_closed = False
    except ValueError:
        missing_fails_closed = True
    check("missing evidence and curation fail closed", missing_fails_closed)

    for name in PASSED:
        print(f"PASS: {name}")
    for name in FAILED:
        print(f"FAIL: {name}")
    print(f"{len(PASSED)} passed; {len(FAILED)} failed")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
