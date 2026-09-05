"""Mutation tests for the command battle-parameter catalog."""

from __future__ import annotations

import csv
import io
import json
import tempfile
from pathlib import Path

import build_command_battle_params as subject


def write_sheet(path: Path, width: int, rows: list[tuple[int, dict[int, str]]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["id", *(str(index) for index in range(width))])
        writer.writerow(["type", *("str" for _ in range(width))])
        for row_id, cells in rows:
            values = [""] * width
            for index, value in cells.items():
                values[index] = value
            writer.writerow([row_id, *values])


def parse_rendered(content: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(content)))


def compatibility_cells(first: int = 40) -> dict[int, str]:
    return {column: str(first + column - 8) for column in range(8, 52)}


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="xivl-command-params-") as raw_root:
        root = Path(raw_root)
        paths = root / "class_paths.json"
        paths.write_text(json.dumps({"recordCount": 2, "records": [
            {"id": 20, "classPath": "/Command/Game/SyntheticMagic"},
            {"id": 30001, "classPath": "/Command/Game/WrongColumnJoin"},
        ]}), encoding="utf-8")
        write_sheet(
            root / "gameCommand.csv",
            121,
            [
                (20, {37: "2", 42: "7", 43: "11", 44: "1", 45: "3",
                      47: "8", 48: "12", 49: "4", 50: "5", 52: "9",
                      53: "13", 54: "0", 55: "1", 57: "10", 58: "14",
                      59: "6", 60: "2", 64: "20", 67: "8", 75: "250",
                      82: "true", 84: "950", 108: "13", 109: "1",
                      110: "5", 111: "0"}),
                (10, {84: "100"}),
            ],
        )
        write_sheet(
            root / "gameCommandBasic.csv",
            116,
            [(20, {36: "30001", 38: "22", 39: "10", 40: "3", 76: "3", 79: "8",
                   114: "105", 115: "1000"}), (10, {})],
        )
        write_sheet(
            root / "compatibility.csv",
            52,
            [(3, compatibility_cells())],
        )
        write_sheet(
            root / "xtx_command.csv",
            26,
            [(20, {1: "Fire JP", 2: "Fire", 22: "JP description",
                   23: "EN description"})],
        )

        content, count = subject.render(root, paths)
        assert count == 2
        rows = parse_rendered(content)
        assert [row["id"] for row in rows] == ["10", "20"]
        fire = rows[1]
        assert fire["lua_class_path"] == "/Command/Game/SyntheticMagic"
        assert rows[0]["lua_class_path"] == ""
        assert fire["name_en"] == "Fire"
        assert fire["description_en"] == "EN description"
        assert fire["description_jp"] == "JP description"
        assert [fire[f"p{index}_compat_adjust"] for index in range(1, 5)] == [
            "1", "4", "0", "6"
        ]
        assert [fire[f"p{index}_tp_adjust"] for index in range(1, 5)] == [
            "3", "5", "1", "2"
        ]
        assert fire["effect_block_raw"].startswith("84=950")
        assert fire["compatibility_percent_by_skill"] == ";".join(
            f"{skill_id}={39 + skill_id}" for skill_id in range(1, 45)
        )
        assert rows[0]["compatibility_percent_by_skill"] == ""
        assert subject.render(root, paths) == (content, count)

        output = root / "generated.csv"
        output.write_text(content, encoding="utf-8", newline="")
        subject.check_output(content, output)
        output.write_text(content.replace("Fire", "Fira", 1), encoding="utf-8")
        try:
            subject.check_output(content, output)
        except SystemExit as exc:
            assert "is stale" in str(exc)
        else:
            raise AssertionError("stale output was accepted")

        (root / "compatibility.csv").unlink()
        try:
            subject.render(root, paths)
        except FileNotFoundError as exc:
            assert "compatibility.csv" in str(exc)
        else:
            raise AssertionError("missing compatibility source was accepted")

        write_sheet(root / "compatibility.csv", 52, [])
        try:
            subject.render(root, paths)
        except ValueError as exc:
            assert "missing compatibility row" in str(exc)
        else:
            raise AssertionError("missing compatibility row was accepted")

        blank_cells = compatibility_cells()
        del blank_cells[17]
        write_sheet(root / "compatibility.csv", 52, [(3, blank_cells)])
        try:
            subject.render(root, paths)
        except ValueError as exc:
            assert "skill 10" in str(exc) and "blank" in str(exc)
        else:
            raise AssertionError("blank compatibility cell was accepted")

        malformed_cells = compatibility_cells()
        malformed_cells[16] = "not-an-integer"
        write_sheet(root / "compatibility.csv", 52, [(3, malformed_cells)])
        try:
            subject.render(root, paths)
        except ValueError as exc:
            assert "skill 9" in str(exc) and "non-integer" in str(exc)
        else:
            raise AssertionError("non-integer compatibility cell was accepted")

        out_of_range_cells = compatibility_cells()
        out_of_range_cells[8] = "128"
        write_sheet(root / "compatibility.csv", 52, [(3, out_of_range_cells)])
        try:
            subject.render(root, paths)
        except ValueError as exc:
            assert "skill 1" in str(exc) and "out-of-range" in str(exc)
        else:
            raise AssertionError("out-of-range compatibility cell was accepted")

        write_sheet(
            root / "compatibility.csv",
            51,
            [(3, {column: str(40 + column - 8) for column in range(8, 51)})],
        )
        try:
            subject.render(root, paths)
        except ValueError as exc:
            assert "skill 44" in str(exc) and "blank" in str(exc)
        else:
            raise AssertionError("incomplete compatibility row was accepted")

        write_sheet(root / "gameCommand.csv", 121, [(20, {}), (20, {})])
        try:
            subject.render(root, paths)
        except ValueError as exc:
            assert "duplicate row id 20" in str(exc)
        else:
            raise AssertionError("duplicate command id was accepted")

        paths.write_text(json.dumps({"recordCount": 2, "records": [
            {"id": 20, "classPath": "/Command/Game/First"},
            {"id": 20, "classPath": "/Command/Game/Second"},
        ]}), encoding="utf-8")
        try:
            subject.command_class_paths(paths)
        except ValueError as exc:
            assert "duplicate static-actor id 20" in str(exc)
        else:
            raise AssertionError("ambiguous static-actor identity was accepted")

    print("command battle-parameter tests passed")


if __name__ == "__main__":
    main()
