"""Build getter-verified derived battle parameters from the CSV command trio."""

from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

from _csv_reader import read_csv
from _csv_root import add_csv_dir_argument, default_csv_dir

REPO = Path(__file__).resolve().parent.parent
CSV = default_csv_dir()
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

HEADER = [
    "id", "name_en", "name_jp", "description_en", "description_jp", "id_band",
    "class_job", "req_level", "compat_key", "caster_state_req",
    "dmg_attr", "dmg_attr_label", "dmg_attr_weight",
    "dmg_elem", "dmg_elem_label", "dmg_elem_weight", "dmg_class",
    "magnitude",
    "hp_cost", "mp_cost", "tp_cost", "cast_time", "recast_time",
    "action_gauge", "range", "best_range", "min_range", "effect_range",
    "recast_sep_hands", "target_state_gate",
    "p1_base", "p1_grow", "p1_compat_adjust", "p1_tp_adjust",
    "p2_base", "p2_grow", "p2_compat_adjust", "p2_tp_adjust",
    "p3_base", "p3_grow", "p3_compat_adjust", "p3_tp_adjust",
    "p4_base", "p4_grow", "p4_compat_adjust", "p4_tp_adjust",
    "effect_block_raw",
]


def index(path: Path) -> dict[int, list[str]]:
    _header, rows = read_csv(path)
    out: dict[int, list[str]] = {}
    for row in rows:
        rid = row.row_id.strip()
        if rid == "":
            continue
        numeric_id = int(rid)
        if numeric_id in out:
            raise ValueError(f"{path}: duplicate row id {numeric_id}")
        out[numeric_id] = row.values
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


def render(csv_dir: Path) -> tuple[str, int]:
    gc = index(csv_dir / "gameCommand.csv")
    gb = index(csv_dir / "gameCommandBasic.csv")
    xc = index(csv_dir / "xtx_command.csv")
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(HEADER)
    for cid in sorted(gc):
        g = gc[cid]
        b = gb.get(cid, [])
        x = xc.get(cid, [])
        attr = get(g, 108)
        elem = get(g, 110)
        effect = ";".join(
            f"{column}={get(g, column)}"
            for column in EFFECT_COLS
            if get(g, column) != ""
        )
        writer.writerow([
            cid,
            get(x, 2), get(x, 1), get(x, 23), get(x, 22), band(cid),
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
            get(g, 43), get(g, 42), get(g, 44), get(g, 45),
            get(g, 48), get(g, 47), get(g, 49), get(g, 50),
            get(g, 53), get(g, 52), get(g, 54), get(g, 55),
            get(g, 58), get(g, 57), get(g, 59), get(g, 60),
            effect,
        ])
    return output.getvalue(), len(gc)


def check_output(expected: str, output_path: Path = OUT) -> None:
    if not output_path.is_file():
        raise SystemExit(f"missing generated output: {output_path}")
    if output_path.read_text(encoding="utf-8") != expected:
        display_path = (
            output_path.relative_to(REPO)
            if output_path.is_relative_to(REPO)
            else output_path
        )
        raise SystemExit(
            f"{display_path} is stale; regenerate it with "
            "tools/build_command_battle_params.py"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_csv_dir_argument(parser)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the tracked output without writing it",
    )
    args = parser.parse_args()

    content, row_count = render(args.csv_dir)
    if args.check:
        check_output(content)
        print(f"verified {OUT.relative_to(REPO)} ({row_count} rows)")
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8", newline="")
    print(f"wrote {OUT.relative_to(REPO)} ({row_count} rows)")


if __name__ == "__main__":
    main()
