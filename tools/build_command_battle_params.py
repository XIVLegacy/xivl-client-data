"""Build getter-verified derived battle parameters from the CSV command trio."""

from __future__ import annotations

import csv
from pathlib import Path

from _csv_reader import read_csv

REPO = Path(__file__).resolve().parent.parent
CSV = REPO / "csv"
OUT = REPO / "derived" / "command_battle_params.csv"

# Getter evidence: xivl-client-scripts:lua/scripts/command/game/gamecommandbaseclass.lua
# Dispatch evidence: xivl-client-scripts:lua/scripts/command/game/battlecommandbaseclass.lua
# Status evidence: xivl-client-scripts:lua/scripts/status/statusbaseclass.lua

# Damage-element labels for gameCommand col 110, calibrated against named
# client actions.
ELEM_LABEL = {
    "-1": "None",
    "5": "Fire",
    "6": "Ice",
    "7": "Wind",
    "8": "Earth",
    "9": "Lightning",
    "10": "Water",
    "11": "Astral",
    "12": "Umbral",
    "13": "Unaspected",
}

# Damage-attribute labels for gameCommand col 108, from the client attribute
# names and command usage.
ATTR_LABEL = {
    "-1": "None",
    "1": "Slashing",
    "2": "Piercing",
    "3": "Blunt",
    "4": "Projectile",
    "11": "Sonic",
    "12": "Breath",
    "13": "Magical",
}

# Preserve the getter-verified effect block raw. Status timing is not in this sheet.
EFFECT_COLS = list(range(84, 117)) + [120]


def index(path: Path) -> dict[int, list[str]]:
    _header, rows = read_csv(path)
    out: dict[int, list[str]] = {}
    for row in rows:
        rid = row.row_id.strip()
        if rid == "":
            continue
        out[int(rid)] = row.values
    return out


def get(values: list[str], col: int) -> str:
    return values[col].strip() if col < len(values) else ""


def band(cid: int) -> str:
    return f"{cid // 1000}xxx"


def dmg_class(attr: str) -> str:
    if attr == "13":
        return "magical"
    if attr in ("1", "2", "3", "4", "11", "12"):
        return "physical"
    if attr in ("-1", ""):
        return "none"
    return "other"


def main() -> None:
    gc = index(CSV / "gameCommand.csv")
    gb = index(CSV / "gameCommandBasic.csv")
    xc = index(CSV / "xtx_command.csv")

    header = [
        "id", "name_en", "name_jp", "id_band",
        "class_job", "req_level", "compat_key", "caster_state_req",
        "dmg_attr", "dmg_attr_label", "dmg_attr_weight",
        "dmg_elem", "dmg_elem_label", "dmg_elem_weight", "dmg_class",
        "magnitude",
        "hp_cost", "mp_cost", "tp_cost", "cast_time", "recast_time",
        "action_gauge", "range", "best_range", "min_range", "effect_range",
        "recast_sep_hands", "target_state_gate",
        "p1_base", "p1_grow", "p2_base", "p2_grow",
        "p3_base", "p3_grow", "p4_base", "p4_grow",
        "effect_block_raw",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for cid in sorted(gc):
            g = gc[cid]
            b = gb.get(cid, [])
            x = xc.get(cid, [])
            attr = get(g, 108)
            elem = get(g, 110)
            effect = ";".join(
                f"{c}={get(g, c)}" for c in EFFECT_COLS if get(g, c) != ""
            )
            w.writerow([
                cid,
                get(x, 2), get(x, 1), band(cid),
                get(b, 38), get(b, 39), get(b, 40), get(g, 37),
                # Columns 109/111 are attribute/element weights. The poles use 0.33.
                attr, ATTR_LABEL.get(attr, ""), get(g, 109),
                elem, ELEM_LABEL.get(elem, ""), get(g, 111),
                dmg_class(attr),
                # Column 84 is client magnitude data. Its damage/HP scale is native.
                get(g, 84),
                # HP cost is absent from the sheet. The base getter returns 0.
                "0",
                get(b, 114), get(b, 115), get(b, 76), get(b, 79),
                get(g, 75), get(g, 64), get(g, 65), get(g, 66), get(g, 67),
                get(g, 82), get(g, 68),
                # Param1/2/4 are blank in extraction 2012.09.19.0001. Keep the shape.
                get(g, 43), get(g, 42), get(g, 48), get(g, 47),
                get(g, 53), get(g, 52), get(g, 58), get(g, 57),
                effect,
            ])

    print(f"wrote {OUT.relative_to(REPO)} ({len(gc)} rows)")


if __name__ == "__main__":
    main()
