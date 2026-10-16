#!/usr/bin/env python3
"""Test complete sheet exports, locale fidelity, source pins and public checks."""

from __future__ import annotations

import csv
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from _csv_reader import CsvRow
import build_retail_sheet_exports as exports
import validate_corpus as corpus


def source_row(name: str, row_id: int, **values) -> CsvRow:
    row = [""] * exports.SOURCE_LAYOUTS[name][0]
    for column, value in values.items():
        row[int(column)] = value
    return CsvRow(str(row_id), row)


def fixture() -> dict:
    return {
        "status.csv": {
            223130: source_row("status.csv", 223130, **{"25": "10108", "47": "-1"})
        },
        "xtx_status.csv": {
            223130: source_row(
                "xtx_status.csv",
                223130,
                **{
                    "1": "\u30b7\u30a7\u30eb",
                    "2": "gain message",
                    "3": "Shell",
                    "24": "[@icon:021204f2277c03]",
                },
            )
        },
        "gcRank.csv": {
            11: source_row("gcRank.csv", 11, **{"0": "1", "1": "10000", "2": "1000"})
        },
        "xtx_gcRank.csv": {
            11: source_row(
                "xtx_gcRank.csv",
                11,
                **{
                    "3": "\u4e8c\u7b49\u7532\u5175",
                    "4": "\u4e8c\u7b49\u7259\u5175",
                    "5": "\u4e8c\u7b49\u95d8\u5175",
                    "9": "Storm Private Third Class",
                    "10": "Serpent Private Third Class",
                    "11": "Flame Private Third Class",
                },
            )
        },
        "materia.csv": {
            0: source_row("materia.csv", 0),
            1: source_row(
                "materia.csv", 1, **{"0": "10100001", "4": "-1", "42": "false"}
            ),
        },
        "materiaBook.csv": {
            1: source_row(
                "materiaBook.csv",
                1,
                **{"0": "\u66f8\u7269", "1": 'The tome, "quoted"\nline', "4": "\u4e66"},
            ),
            99: source_row("materiaBook.csv", 99, **{"1": "Unrelated key"}),
        },
    }


class RetailSheetExportTests(unittest.TestCase):
    def test_locale_columns_and_opaque_icon_control_are_exact(self):
        sources = fixture()
        rows = exports.project("status_names", sources)
        self.assertEqual(rows[0]["name_en"], "Shell")
        self.assertEqual(rows[0]["name_ja"], "\u30b7\u30a7\u30eb")
        self.assertEqual(rows[0]["icon_text"], "[@icon:021204f2277c03]")
        self.assertEqual(rows[0]["status_col_25"], "10108")
        self.assertEqual(rows[0]["status_col_47"], "-1")
        self.assertEqual(rows[0]["status_col_31"], "")
        self.assertEqual(rows[0]["source_row"], "223130")

    def test_names_join_only_exact_keys_and_preserve_placeholders(self):
        sources = fixture()
        sources["xtx_status.csv"][223130].values[3] = "-"
        self.assertEqual(
            exports.project("status_names", sources)[0]["placeholder"], "true"
        )
        sources["xtx_status.csv"][223130].values[3] = "Shell"
        sources["status.csv"][223131] = source_row("status.csv", 223131)
        with self.assertRaisesRegex(ValueError, "row IDs"):
            exports.project("status_names", sources)
        sources = fixture()
        sources["xtx_gcRank.csv"][13] = source_row("xtx_gcRank.csv", 13)
        with self.assertRaisesRegex(ValueError, "row IDs"):
            exports.project("gc_rank", sources)

    def test_gc_variants_preserve_all_names_without_company_id_inference(self):
        rows = exports.project("gc_rank", fixture())
        self.assertEqual(
            [r["name_en"] for r in rows],
            [
                "Storm Private Third Class",
                "Serpent Private Third Class",
                "Flame Private Third Class",
            ],
        )
        self.assertEqual([r["name_variant"] for r in rows], ["0", "1", "2"])
        self.assertEqual({r["company"] for r in rows}, {"unresolved"})
        self.assertEqual({r["seals_needed_next_rank"] for r in rows}, {"1000"})

    def test_verified_gc_fields_keep_each_distinct_source_column(self):
        sources = fixture()
        sources["gcRank.csv"][11].values = [
            "1",
            "10000",
            "1000",
            "",
            "",
            "",
            "641",
            "671",
            "701",
        ]
        for row in exports.project("gc_rank", sources):
            self.assertEqual(row["linear_rank"], "1")
            self.assertEqual(row["seal_maximum"], "10000")
            self.assertEqual(row["seals_needed_next_rank"], "1000")
            self.assertEqual(
                [row[f"icon_company_{company}"] for company in range(1, 4)],
                ["641", "671", "701"],
            )

    def test_materia_quality_boundaries_do_not_cross_parameter_or_icon_fields(self):
        sources = fixture()
        sources["materia.csv"][1].values = [str(i) for i in range(80)]
        row = exports.project("materia", sources)[1]
        self.assertEqual(row["parameter_1"], "4")
        self.assertEqual(row["parameter_2"], "21")
        for quality in range(16):
            self.assertEqual(row[f"value_1_quality_{quality}"], str(5 + quality))
            self.assertEqual(row[f"value_2_quality_{quality}"], str(22 + quality))
        for group in range(4):
            self.assertEqual(row[f"catalog_id_quality_group_{group}"], str(group))
            self.assertEqual(row[f"icon_quality_group_{group}"], str(38 + group))
        self.assertEqual(row["materia_col_42"], "42")
        self.assertEqual(row["materia_col_79"], "79")
        self.assertEqual(len(exports.TYPED_COLUMNS["materia"]), 80)
        self.assertEqual(set(exports.TYPED_COLUMNS["materia"].values()), set(range(80)))

    def test_materia_book_has_independent_keys_and_preserves_all_locales(self):
        sources = fixture()
        materia = exports.project("materia", sources)
        book = exports.project("materia_book", sources)
        self.assertEqual([r["materia_id"] for r in materia], ["0", "1"])
        self.assertEqual([r["text_id"] for r in book], ["1", "99"])
        self.assertEqual(materia[1]["catalog_id_quality_group_0"], "10100001")
        self.assertEqual(materia[1]["parameter_1"], "-1")
        self.assertEqual(materia[1]["materia_col_42"], "false")
        payload = exports.render("materia_book", book)
        round_trip = list(csv.DictReader(io.StringIO(payload.decode("utf-8"))))
        self.assertEqual(round_trip[0]["text_en"], 'The tome, "quoted"\nline')
        self.assertEqual(round_trip[0]["text_ja"], "\u66f8\u7269")
        self.assertEqual(round_trip[0]["text_zh"], "\u4e66")
        self.assertEqual(
            payload,
            exports.render("materia_book", exports.project("materia_book", sources)),
        )

    def test_layout_duplicate_width_and_type_failures(self):
        with tempfile.TemporaryDirectory(prefix="retail-sheets-") as raw:
            path = Path(raw) / "gcRank.csv"
            records = [
                ["", *map(str, range(9))],
                ["", "u8", "s32", "s32", "", "", "", "s32", "s32", "s32"],
                [11, 1, 10000, 1000, "", "", "", 641, 671, 701],
            ]

            def write():
                with path.open("w", encoding="utf-8", newline="") as handle:
                    csv.writer(handle).writerows(records)

            write()
            self.assertEqual(list(exports.load_source(path)), [11])
            records.append(records[-1])
            write()
            with self.assertRaisesRegex(ValueError, "duplicate"):
                exports.load_source(path)
            records.pop()
            records[-1].pop()
            write()
            with self.assertRaisesRegex(ValueError, "expected 9"):
                exports.load_source(path)
            records[-1].append(701)
            records[1][1] = "s32"
            write()
            with self.assertRaisesRegex(ValueError, "layout"):
                exports.load_source(path)
            records[1][1] = "u8"
            records[-1][1] = 256
            write()
            with self.assertRaisesRegex(ValueError, "out of range"):
                exports.load_source(path)

    def test_public_validator_rejects_product_and_provenance_mutations(self):
        with tempfile.TemporaryDirectory(prefix="retail-sheets-public-") as raw:
            root = Path(raw)
            (root / "derived").mkdir()
            (root / "manifests").mkdir()
            paths = [
                exports.MANIFEST,
                "manifests/tables.json",
                *[f"derived/{name}.csv" for name in exports.SPECS],
            ]
            for path in paths:
                (root / path).write_bytes((exports.REPO / path).read_bytes())
            exports.validate_public(root)
            path = root / "derived/status_names.csv"
            original = path.read_bytes()
            with (
                patch.object(corpus, "REPO_ROOT", root),
                patch.object(corpus, "CORPUS_ABSENT", True),
                patch.object(corpus, "errors", []),
            ):
                path.write_bytes(original.replace(b"Shell", b"Changed Shell"))
                corpus.validate_retail_sheet_exports()
                self.assertTrue(any("SHA-256" in error for error in corpus.errors))
                path.write_bytes(original.split(b"\n", 1)[0] + b"\n1\n")
                corpus.errors.clear()
                corpus.validate_retail_sheet_exports()
                self.assertTrue(any("row width" in error for error in corpus.errors))
                path.write_bytes(original)
                manifest_path = root / exports.MANIFEST
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["products"]["gc_rank"]["typedColumns"]["linear_rank"] = 1
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                corpus.errors.clear()
                corpus.validate_retail_sheet_exports()
                self.assertTrue(any("metadata" in error for error in corpus.errors))
                manifest["products"]["gc_rank"]["typedColumns"]["linear_rank"] = 0
                manifest["sources"][0]["sha256"] = "0" * 64
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                corpus.errors.clear()
                corpus.validate_retail_sheet_exports()
                self.assertTrue(any("identities" in error for error in corpus.errors))

    @unittest.skipUnless(os.environ.get("XIVL_CSV_DIR"), "requires selected corpus")
    def test_authenticated_exports_cover_every_raw_cell_and_named_anchor(self):
        root = Path(os.environ["XIVL_CSV_DIR"])
        outputs = exports.build(root)
        expected_counts = {
            "status_names": 399,
            "gc_rank": 66,
            "materia": 66,
            "materia_book": 52,
        }
        for name, spec in exports.SPECS.items():
            rows = list(
                csv.DictReader(
                    io.StringIO(
                        outputs[exports.REPO / f"derived/{name}.csv"].decode("utf-8")
                    )
                )
            )
            self.assertEqual(len(rows), expected_counts[name])
            source = exports.load_source(root / spec["source"])
            for row in rows:
                raw = source[int(row[spec["id"]])].values
                for field, column in exports.TYPED_COLUMNS[name].items():
                    self.assertEqual(
                        row[field].encode("utf-8"), raw[column].encode("utf-8")
                    )
            if "textSource" in spec:
                texts = exports.load_source(root / spec["textSource"])
                for row in rows:
                    raw = texts[int(row[spec["id"]])].values
                    for field, column in spec["textColumns"].items():
                        index = (
                            column[int(row["name_variant"])]
                            if isinstance(column, list)
                            else column
                        )
                        self.assertEqual(
                            row[field].encode("utf-8"), raw[index].encode("utf-8")
                        )
            if name == "status_names":
                indexed = {row["status_id"]: row for row in rows}
                self.assertEqual(sum(row["placeholder"] == "true" for row in rows), 95)
                self.assertEqual(indexed["223130"]["name_ja"], "\u30b7\u30a7\u30eb")
                self.assertEqual(indexed["223193"]["name_en"], "Comradery")
                self.assertEqual(indexed["223194"]["name_en"], "Strength in Numbers")
                self.assertNotIn("223995", indexed)
        with tempfile.TemporaryDirectory(prefix="retail-sheets-mutated-") as raw:
            altered = Path(raw)
            for name in exports.SOURCE_LAYOUTS:
                (altered / name).write_bytes((root / name).read_bytes())
            path = altered / "status.csv"
            path.write_bytes(path.read_bytes().replace(b"231", b"232", 1))
            with self.assertRaisesRegex(ValueError, "source bytes differ"):
                exports.build(altered)


if __name__ == "__main__":
    unittest.main()
