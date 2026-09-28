"""SQL generation must distinguish missing cells from explicit empty values."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _csv_reader import write_multi_csv_seed, write_single_csv_seed


class CsvSeedTests(unittest.TestCase):
    def test_short_row_preserves_existing_seed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sample.csv").write_text(
                "id,0,1\ntype,u32,u32\n1,7\n", encoding="utf-8"
            )
            output = root / "sample.sql"
            output.write_bytes(b"existing seed\n")
            with self.assertRaisesRegex(
                ValueError, "row '1'.*expected 2 values, got 1"
            ):
                write_single_csv_seed(
                    "sample", "sample.csv", [("value", 1, "u32")], root, root
                )
            self.assertEqual(output.read_bytes(), b"existing seed\n")

    def test_short_joined_row_does_not_publish(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "driver.csv").write_text("id,0\ntype,u32\n1,7\n", encoding="utf-8")
            (root / "lookup.csv").write_text("id,0\ntype,u32\n1\n", encoding="utf-8")
            with self.assertRaisesRegex(
                ValueError, "lookup.csv.*expected 1 values, got 0"
            ):
                write_multi_csv_seed(
                    "sample",
                    ["driver.csv", "lookup.csv"],
                    [("value", "lookup.csv", 0, "u32")],
                    root,
                    root,
                )
            self.assertFalse((root / "sample.sql").exists())

    def test_explicit_empty_cell_keeps_zero(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sample.csv").write_text(
                "id,0,1\ntype,u32,u32\n1,7,\n", encoding="utf-8"
            )
            output = write_single_csv_seed(
                "sample",
                "sample.csv",
                [("id", "row_id", "u32"), ("a", 0, "u32"), ("b", 1, "u32")],
                root,
                root,
            )
            self.assertEqual(
                output.read_text().splitlines()[-1],
                "INSERT INTO sample VALUES (1, 7, 0);",
            )

    def test_declared_partial_join_keeps_zero(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "driver.csv").write_text("id,0\ntype,u32\n1,7\n", encoding="utf-8")
            (root / "lookup.csv").write_text("id,0\ntype,u32\n2,8\n", encoding="utf-8")
            output = write_multi_csv_seed(
                "sample",
                ["driver.csv", "lookup.csv"],
                [
                    ("id", "driver.csv", "row_id", "u32"),
                    ("value", "lookup.csv", 0, "u32"),
                ],
                root,
                root,
                require_join_match=False,
            )
            self.assertEqual(
                output.read_text().splitlines()[-1], "INSERT INTO sample VALUES (1, 0);"
            )


if __name__ == "__main__":
    unittest.main()
