"""Build getter-verified derived battle parameters from the CSV command trio."""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path

from _csv_reader import read_csv
from _csv_root import add_csv_dir_argument, default_csv_dir

REPO = Path(__file__).resolve().parent.parent
CSV = default_csv_dir()
OUT = REPO / "derived" / "command_battle_params.csv"
CLASS_PATHS = REPO / "manifests" / "staticactor_class_paths.json"

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
COMPATIBILITY_COLS = range(8, 52)
COMPATIBILITY_MIN = -128
COMPATIBILITY_MAX = 127

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
    "effect_block_raw", "lua_class_path",
    "compatibility_percent_by_skill",
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


def command_class_paths(path: Path) -> dict[int, str]:
    document = json.loads(path.read_text(encoding="utf-8"))
    records = document["records"]
    if document["recordCount"] != len(records):
        raise ValueError("static-actor record count differs")
    result: dict[int, str] = {}
    for record in records:
        actor_id, class_path = record["id"], record["classPath"]
        if actor_id in result:
            raise ValueError(f"duplicate static-actor id {actor_id}")
        result[actor_id] = class_path
    return result


def compatibility_percent_by_skill(
    compatibility: dict[int, list[str]], key: str, path: Path
) -> str:
    """Render the selected compatibility row as skill-id percentages."""
    try:
        row_id = int(key)
    except ValueError as exc:
        raise ValueError(f"{path}: non-integer compatibility key {key!r}") from exc

    values = compatibility.get(row_id)
    if values is None:
        raise ValueError(f"{path}: missing compatibility row for key {key!r}")

    rendered: list[str] = []
    for skill_id, column in enumerate(COMPATIBILITY_COLS, start=1):
        value = get(values, column)
        if value == "":
            raise ValueError(
                f"{path}: compatibility row {row_id} has blank skill {skill_id} "
                f"at column {column}"
            )
        try:
            numeric_value = int(value)
        except ValueError as exc:
            raise ValueError(
                f"{path}: compatibility row {row_id} has non-integer skill "
                f"{skill_id} value {value!r} at column {column}"
            ) from exc
        if not COMPATIBILITY_MIN <= numeric_value <= COMPATIBILITY_MAX:
            raise ValueError(
                f"{path}: compatibility row {row_id} has out-of-range skill "
                f"{skill_id} value {value!r} at column {column}; expected "
                f"signed s8 range [{COMPATIBILITY_MIN}, {COMPATIBILITY_MAX}]"
            )
        rendered.append(f"{skill_id}={value}")
    return ";".join(rendered)


def render(csv_dir: Path, class_paths: Path = CLASS_PATHS) -> tuple[str, int]:
    gc = index(csv_dir / "gameCommand.csv")
    gb = index(csv_dir / "gameCommandBasic.csv")
    xc = index(csv_dir / "xtx_command.csv")
    compatibility_path = csv_dir / "compatibility.csv"
    compatibility = index(compatibility_path)
    paths = command_class_paths(class_paths)
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(HEADER)
    for cid in sorted(gc):
        g = gc[cid]
        b = gb.get(cid, [])
        x = xc.get(cid, [])
        compatibility_key = get(b, 40)
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
            paths.get(cid, "") if paths.get(cid, "").startswith("/Command/") else "",
            compatibility_percent_by_skill(
                compatibility, compatibility_key, compatibility_path
            )
            if compatibility_key != ""
            else "",
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
