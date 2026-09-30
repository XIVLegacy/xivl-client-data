"""Synthetic joins and failure cases for the read-only compatibility inspector."""

from __future__ import annotations

import csv
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import inspect_item_compatibility as subject


INSPECTOR = Path(__file__).with_name("inspect_item_compatibility.py")


def write_sheet(
    root: Path,
    name: str,
    width: int,
    types: dict[int, str],
    rows: list[tuple[int, dict[int, str]]],
) -> None:
    with (root / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["id", *map(str, range(width))])
        writer.writerow(["type", *(types.get(column, "") for column in range(width))])
        for row_id, cells in rows:
            writer.writerow(
                [row_id, *(cells.get(column, "0") for column in range(width))]
            )


class ItemCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="item-compatibility-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.fixture()

    def fixture(self, key: str = "2119", stored: str = "45") -> None:
        write_sheet(self.root, "_item.csv", 4, {0: "str"}, [(7001, {0: "9009"})])
        write_sheet(
            self.root,
            "itemData.csv",
            49,
            {48: "s32"},
            [(9009, {48: "999"}), (7001, {47: "999", 48: key})],
        )
        write_sheet(
            self.root,
            "compatibility.csv",
            52,
            dict.fromkeys(range(8, 52), "s8"),
            [
                (7001, {22: "33"}),
                (999, {22: "80"}),
                (2119, {8: "0", 21: "99", 22: stored, 23: "60", 51: "100"}),
            ],
        )

    def run_cli(self, *args: str, env_root: Path | None = None):
        environment = os.environ.copy()
        environment["XIVL_CSV_DIR"] = str(env_root or self.root)
        return subprocess.run(
            [sys.executable, str(INSPECTOR), *args],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

    def test_actual_row_chain_and_selected_column(self) -> None:
        result = subject.inspect(self.root, 7001, 15)
        self.assertEqual(
            result, subject.CompatibilityResult("7001", "7001", "2119", 15, 22, 45)
        )
        self.assertEqual(result.client_factor, 0.45)
        text = subject.render(result)
        self.assertIn("_item.csv row 7001 -> itemData.csv row 7001", text)
        self.assertIn("column 48 compatibility key: 2119", text)
        self.assertIn("row 2119, skill 15, column 22", text)
        self.assertIn("Stored integer (s8): 45", text)
        self.assertIn("stored / 100): 0.45", text)

    def test_signed_values_and_zero_gate(self) -> None:
        for stored in (-128, -1, 0, 1, 45, 100, 127):
            with self.subTest(stored=stored):
                self.fixture(stored=str(stored))
                result = subject.inspect(self.root, 7001, 15)
                self.assertEqual(result.stored_integer, stored)
                self.assertEqual(result.client_factor, stored / 100)
                text = subject.render(result)
                self.assertEqual("Zero matches" in text, stored == 0)
                self.assertIn("Complete equipment eligibility is not determined", text)
                self.assertIn("tribe and required-level checks", text)
                self.assertIn("server policy, and item appearance", text)

    def test_first_and_last_supported_skills(self) -> None:
        for skill, column, value in ((1, 8, 0), (44, 51, 100)):
            with self.subTest(skill=skill):
                result = subject.inspect(self.root, 7001, skill)
                self.assertEqual(
                    (result.column, result.stored_integer), (column, value)
                )

    def test_missing_source_rows(self) -> None:
        for sheet in ("_item.csv", "itemData.csv", "compatibility.csv"):
            with self.subTest(sheet=sheet):
                self.fixture()
                path = self.root / sheet
                header = path.read_text(encoding="utf-8").splitlines()[:2]
                path.write_text("\n".join(header) + "\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, sheet + ": missing row"):
                    subject.inspect(self.root, 7001, 15)

    def test_missing_file(self) -> None:
        (self.root / "itemData.csv").unlink()
        with self.assertRaises(FileNotFoundError):
            subject.inspect(self.root, 7001, 15)

    def test_zero_key_is_a_row_lookup(self) -> None:
        self.fixture(key="0")
        with self.assertRaisesRegex(ValueError, "compatibility.csv: missing row '0'"):
            subject.inspect(self.root, 7001, 15)
        write_sheet(self.root, "compatibility.csv", 52, {22: "s8"}, [(0, {22: "10"})])
        self.assertEqual(subject.inspect(self.root, 7001, 15).stored_integer, 10)

    def test_blank_cells_are_not_zero(self) -> None:
        for key, stored, sheet, column in (
            ("", "45", "itemData.csv", 48),
            ("2119", "", "compatibility.csv", 22),
            ("2119", " ", "compatibility.csv", 22),
        ):
            with self.subTest(sheet=sheet, stored=stored):
                self.fixture(key=key, stored=stored)
                with self.assertRaisesRegex(
                    ValueError, f"{sheet}.*column {column}: blank cell"
                ):
                    subject.inspect(self.root, 7001, 15)

    def test_malformed_and_out_of_range_integers(self) -> None:
        for value in ("abc", "1.0", "true", "2147483648"):
            with self.subTest(key=value):
                self.fixture(key=value)
                with self.assertRaisesRegex(ValueError, "itemData.csv.*invalid s32"):
                    subject.inspect(self.root, 7001, 15)
        for value in ("abc", "100.0", "true", "128", "-129"):
            with self.subTest(stored=value):
                self.fixture(stored=value)
                with self.assertRaisesRegex(
                    ValueError, "compatibility.csv.*invalid s8"
                ):
                    subject.inspect(self.root, 7001, 15)

    def test_wrong_type_or_missing_column(self) -> None:
        for width, types, message in (
            (52, {22: "u8"}, "expected 's8'"),
            (22, {}, "missing column or type declaration"),
        ):
            with self.subTest(width=width):
                write_sheet(self.root, "compatibility.csv", width, types, [(2119, {})])
                with self.assertRaisesRegex(ValueError, message):
                    subject.inspect(self.root, 7001, 15)
        self.fixture()
        write_sheet(self.root, "itemData.csv", 49, {48: "str"}, [(7001, {48: "2119"})])
        with self.assertRaisesRegex(ValueError, "expected 's32'"):
            subject.inspect(self.root, 7001, 15)

    def test_row_width_and_duplicate_rows(self) -> None:
        path = self.root / "compatibility.csv"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("123,1\n")
        with self.assertRaisesRegex(ValueError, "expected 52 values, got 1"):
            subject.inspect(self.root, 7001, 15)
        for sheet in ("_item.csv", "itemData.csv", "compatibility.csv"):
            with self.subTest(sheet=sheet):
                self.fixture()
                path = self.root / sheet
                duplicate = path.read_text(encoding="utf-8").splitlines()[-1]
                with path.open("a", encoding="utf-8") as handle:
                    handle.write(duplicate + "\n")
                with self.assertRaisesRegex(ValueError, "duplicate row id"):
                    subject.inspect(self.root, 7001, 15)

    def test_invalid_catalog_or_skill(self) -> None:
        for catalog, skill in ((-1, 1), (4294967296, 1), (7001, 0), (7001, 45)):
            with self.subTest(catalog=catalog, skill=skill):
                with self.assertRaises(ValueError):
                    subject.inspect(self.root, catalog, skill)
        result = self.run_cli("not-an-id", "15")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_cli_selection_read_only_and_errors(self) -> None:
        before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        result = self.run_cli("7001", "15")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout, subject.render(subject.inspect(self.root, 7001, 15))
        )
        explicit = self.run_cli(
            "7001", "15", "--csv-dir", str(self.root), env_root=self.root / "absent"
        )
        self.assertEqual(explicit.returncode, 0, explicit.stderr)
        self.assertEqual(
            before, {path.name: path.read_bytes() for path in self.root.iterdir()}
        )
        self.fixture(stored="")
        failure = self.run_cli("7001", "15")
        self.assertNotEqual(failure.returncode, 0)
        self.assertEqual(failure.stdout, "")
        self.assertIn("blank cell", failure.stderr)

    def test_unsafe_root_is_rejected(self) -> None:
        (self.root / "nested").mkdir()
        with self.assertRaisesRegex(ValueError, "not a regular file"):
            subject.inspect(self.root, 7001, 15)


if __name__ == "__main__":
    unittest.main()
