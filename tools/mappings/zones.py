"""Explicit-only server_zones mapping with unresolved server fields zeroed."""

import json
from pathlib import Path

SQL_TABLE = "server_zones"
INCLUDE_IN_ALL = False
SOURCES = [
    "_zoneParam.csv",
    "xtx_placeName.csv",
    "zoneGroupParam.csv",
    "regionParam.csv",
    "_region.csv",
]

JOIN_KEYS = {
    # xtx_placeName.csv is joined via _zoneParam.csv col 0 (the placeName id).
    "xtx_placeName.csv": ("_zoneParam.csv", 0),
}

# Region-id exception policy and evidence classes: see docs/architectural-findings.md.
_EXPLICIT_REGION_IDS: dict[str, int] = {
    "138": 101, "146": 102, "156": 103, "179": 104,
    "248": 101, "260": 101, "261": 101,
    "164": 106, "165": 106, "166": 106, "167": 106, "168": 106,
    "184": 107, "185": 107, "186": 104, "187": 104, "188": 104,
    "192": 112, "193": 111, "194": 112, "195": 112, "196": 112, "198": 112,
    "134": 202, "160": 204, "180": 205, "232": 202, "233": 205, "234": 204,
    "177": 207, "201": 208, "244": 209,
    "139": 112, "200": 805, "257": 109, "267": 109, "268": 109,
    "0": 0,
}


_ZONE_NAME_CATALOG = (
    Path(__file__).resolve().parents[2] / "manifests" / "zone_internal_names.json"
)


def _load_catalog_zone_names() -> dict[str, str]:
    """Load deterministic client-bindable zone names from the manifest."""
    data = json.loads(_ZONE_NAME_CATALOG.read_text(encoding="utf-8"))
    return {str(b["zoneId"]): b["zoneName"] for b in data["zoneBindings"]}


_CATALOG_ZONE_NAMES = _load_catalog_zone_names()

# Zone-name evidence classes and ambiguity policy: see docs/architectural-findings.md.
_EXPLICIT_ZONE_NAMES: dict[str, str | None] = {
    "264": "lak0Dungeon01",
    "128": "sea0Field01", "129": "sea0Field02", "130": "sea0Field03",
    "133": "sea0Town01", "150": "fst0Field01", "152": "fst0Field03",
    "154": "fst0Field05", "155": "fst0Town01", "170": "wil0Field01",
    "171": "wil0Field02", "172": "wil0Field03", "175": "wil0Town01",
    "190": "lak0Field01", "238": "fst0Field04",
    "141": "sea0Field01a", "162": "fst0Field01a", "204": "sea0Field02a",
    "205": "sea0Field03a", "206": "fst0Town01a", "207": "fst0Field03a",
    "208": "fst0Field05a", "209": "wil0Town01a", "230": "sea0Town01a",
    "239": "roc0Field02a", "240": "wil0Field05a", "250": "roc0Field02a",
    "256": "roc0Field02a", "266": "lak0Field01a",
    "137": "sea0Dungeon06",
    "164": "fst0Battle01", "165": "fst0Battle02", "166": "fst0Battle03",
    "167": "fst0Battle04", "168": "fst0Battle05",
    "184": "wil0Battle01", "185": "wil0Battle01", "186": "wil0Battle02",
    "187": "wil0Battle03", "188": "wil0Battle04",
    "245": "roc0Dungeon04", "252": "roc0Dungeon04", "253": "roc0Dungeon04",
    "257": "roc1Field01",
    "134": "sea0Market01", "160": "fst0Market01", "180": "wil0Market01",
    "177": "_jail", "200": "sea1Cruise01", "201": "prv0Cottage00",
    "232": "sea0Office01", "233": "wil0Office01", "234": "fst0Office01",
    "236": "sea1Field01", "244": "prv0Inn01",
    # Names without a unique client binding remain explicit curation.
    "192": "ocn1Battle01", "193": "ocn0Battle02", "194": "ocn1Battle03",
    "195": "ocn1Battle04", "196": "ocn1Battle05", "198": "ocn1Battle06",
    "267": "roc1Field02", "268": "roc1Field03",
    "0": None, "138": None, "140": None, "146": None, "156": None,
    "161": None, "179": None, "181": None, "182": None, "210": None,
    "211": None, "235": None, "237": None, "246": None, "247": None,
    "248": None, "249": None, "251": None, "254": None, "255": None,
    "258": None, "259": None, "260": None, "261": None, "262": None,
    "263": None, "265": None, "269": None, "270": None,
}


def _resolve_zone_name(zone_id: str, sources) -> str | None:
    if zone_id in _CATALOG_ZONE_NAMES:
        return _CATALOG_ZONE_NAMES[zone_id]
    if zone_id in _EXPLICIT_ZONE_NAMES:
        return _EXPLICIT_ZONE_NAMES[zone_id]
    raise ValueError(
        f"zones: no zoneName derivation for zone {zone_id!r} (covered by "
        f"neither the client catalog nor _EXPLICIT_ZONE_NAMES)"
    )


def _mechanical_walk(sources):
    """Build structurally resolved zone ids. See docs/architectural-findings.md."""
    zone_group = sources["zoneGroupParam.csv"]
    region_param = sources["regionParam.csv"]
    region = sources["_region.csv"]

    zone_to_last_group: dict[str, str] = {}
    for group_id, row in zone_group.items():
        for child in row.values[1:6]:
            if child not in ("", "0"):
                zone_to_last_group[child] = group_id

    ranges: list[tuple[int, int, str]] = []
    for row in region_param.values():
        code, start, end = row.values[0], int(row.values[1]), int(row.values[2])
        ranges.append((start, end, code))

    # Reject duplicate region-code inverses before the walk.
    code_to_region_id: dict[str, str] = {}
    for row_id, row in region.items():
        value = row.values[1]
        if value in ("", "0"):
            continue
        if value in code_to_region_id:
            raise ValueError(
                f"_region.csv value {value} appears on rows "
                f"{code_to_region_id[value]} and {row_id}; inverse lookup is ambiguous"
            )
        code_to_region_id[value] = row_id

    result: dict[str, str] = {}
    for zone_id, group_id in zone_to_last_group.items():
        gid = int(group_id)
        for start, end, code in ranges:
            if start <= gid <= end:
                region_id = code_to_region_id.get(code)
                if region_id is not None:
                    result[zone_id] = region_id
                break
    return result


def _resolve_region_id(zone_id: str, sources) -> str:
    if zone_id in _EXPLICIT_REGION_IDS:
        return str(_EXPLICIT_REGION_IDS[zone_id])
    walked = _mechanical_walk(sources).get(zone_id)
    if walked is None:
        raise ValueError(
            f"zones: no regionId derivation for zone {zone_id!r} (covered by "
            f"neither the mechanical walk nor _EXPLICIT_REGION_IDS)"
        )
    return walked


COLUMNS = [
    ("id", "_zoneParam.csv", "row_id", "u32"),
    ("regionId", None, _resolve_region_id, "u16"),
    ("zoneName", None, _resolve_zone_name, "str"),
    ("placeName", "xtx_placeName.csv", 1, "str"),
    ("serverIp", None, "const:", "str"),
    ("serverPort", None, "const:0", "u32"),
    ("classPath", None, "const:", "str"),
    ("dayMusic", None, "const:0", "u16"),
    ("nightMusic", None, "const:0", "u16"),
    ("battleMusic", None, "const:0", "u16"),
    ("isIsolated", None, "const:0", "u8"),
    ("isInn", None, "const:0", "u8"),
    ("canRideChocobo", None, "const:0", "u8"),
    ("canStealth", None, "const:0", "u8"),
    ("isInstanceRaid", None, "const:0", "u8"),
    ("loadNavMesh", None, "const:0", "u8"),
]
