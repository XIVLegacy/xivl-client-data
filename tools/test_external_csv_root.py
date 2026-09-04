#!/usr/bin/env python3
"""Regression checks for external CSV-root selection."""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from _csv_root import CsvRootError, validate_csv_dir
except ModuleNotFoundError:  # pragma: no cover - package import path
    from ._csv_root import CsvRootError, validate_csv_dir


REPO = Path(__file__).resolve().parents[1]
ANALYZER = REPO / "tools" / "analyze_item_graphics_candidates.py"
CSV_TO_SQL = REPO / "tools" / "csv_to_sql.py"
PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(name)


def write_sheet(
    path: Path,
    width: int,
    types: dict[int, str],
    rows: list[tuple[int, dict[int, object]]],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["", *(str(index) for index in range(width))])
        writer.writerow(["", *(types.get(index, "") for index in range(width))])
        for row_id, populated in rows:
            values = [""] * width
            for index, value in populated.items():
                values[index] = value
            writer.writerow([row_id, *values])


def run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
    )


def make_symlink(target: Path, link: Path, *, directory: bool = False) -> bool:
    try:
        os.symlink(target, link, target_is_directory=directory)
    except (NotImplementedError, OSError):
        return False
    return True


def rejected(path: Path) -> bool:
    try:
        validate_csv_dir(path)
    except CsvRootError:
        return True
    return False


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="external-csv-root-") as raw:
        root = Path(raw) / "corpus"
        root.mkdir()
        weapon_positions = list(range(92, 112)) + [135, 136, 141]
        equipment_positions = list(range(69, 91)) + [137, 138, 139]
        write_sheet(
            root / "weapon.csv",
            142,
            {position: "s32" for position in weapon_positions},
            [(1, {position: 1 for position in weapon_positions})],
        )
        write_sheet(
            root / "equipment.csv",
            140,
            {position: "s32" for position in equipment_positions},
            [(2, {position: 2 for position in equipment_positions})],
        )

        output = root / "report.json"
        external_env = os.environ.copy()
        external_env["XIVL_CSV_DIR"] = str(root)
        external_env.pop("XIVL_CORPUS_ABSENT", None)
        result = run(
            [sys.executable, str(ANALYZER), "--output", str(output)],
            external_env,
        )
        if result.returncode == 0:
            report = json.loads(output.read_text(encoding="utf-8"))
            check(
                "XIVL_CSV_DIR selects the external analyzer corpus",
                report["sheets"]["weapon.csv"]["rowCount"] == 1
                and report["sheets"]["equipment.csv"]["rowCount"] == 1,
            )
        else:
            check("XIVL_CSV_DIR selects the external analyzer corpus", False)

        explicit_env = os.environ.copy()
        explicit_env["XIVL_CSV_DIR"] = str(root / "does-not-exist")
        explicit_output = root / "explicit-report.json"
        result = run(
            [
                sys.executable,
                str(ANALYZER),
                "--csv-dir",
                str(root),
                "--output",
                str(explicit_output),
            ],
            explicit_env,
        )
        check(
            "--csv-dir overrides an invalid environment root",
            result.returncode == 0 and explicit_output.is_file(),
        )

        missing_env = os.environ.copy()
        missing_env["XIVL_CSV_DIR"] = str(root / "does-not-exist")
        result = run([sys.executable, str(CSV_TO_SQL), "--list"], missing_env)
        check(
            "metadata-only mapping listing does not require hydration",
            result.returncode == 0 and "items" in result.stdout.splitlines(),
        )

        check("plain external root is accepted", validate_csv_dir(root) == root)
        check("non-directory root is rejected", rejected(root / "weapon.csv"))

        linked_root = root.parent / "linked-root"
        linked_root_supported = make_symlink(root, linked_root, directory=True)
        check(
            "linked root is rejected when supported",
            not linked_root_supported or rejected(linked_root),
        )
        if linked_root_supported:
            linked_env = os.environ.copy()
            linked_env["XIVL_CSV_DIR"] = str(linked_root)
            linked_result = run(
                [sys.executable, str(ANALYZER), "--output", str(root / "linked.json")],
                linked_env,
            )
            check(
                "CLI rejects a linked environment root",
                linked_result.returncode != 0,
            )

        linked_descendant = root / "linked.csv"
        descendant_supported = make_symlink(root / "weapon.csv", linked_descendant)
        check(
            "linked descendant is rejected when supported",
            not descendant_supported or rejected(root),
        )
        if descendant_supported:
            descendant_result = run(
                [
                    sys.executable,
                    str(ANALYZER),
                    "--csv-dir",
                    str(root),
                    "--output",
                    str(root / "linked-descendant.json"),
                ],
                external_env,
            )
            check(
                "CLI rejects a linked descendant",
                descendant_result.returncode != 0,
            )

        nested = root / "nested"
        nested.mkdir()
        check("directory descendant is rejected", rejected(root))

    for name in PASSED:
        print(f"PASS: {name}")
    for name in FAILED:
        print(f"FAIL: {name}")
    print(f"{len(PASSED)} passed; {len(FAILED)} failed")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
