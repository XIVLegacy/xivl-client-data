#!/usr/bin/env python3
"""Test guildleve name joins, locale fidelity, placeholders, and input failures."""

from __future__ import annotations

import csv
import io
import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from _csv_reader import CsvRow
import build_guildleve_names as names
import validate_corpus as corpus


def fixture():
    guildleves = {}
    texts = {}
    for row_id, category, en, ja in [
        (10801, 1, "My Very First Adventure", "\u99c6\u3051\u51fa\u3057"),
        (10802, 1, "My Very First Adventure", "\u99c6\u3051\u51fa\u3057"),
        (2, 1, names.NO_TRANSLATION, "\u30c9\u30fc\u30c9\u30fc"),
        (11602, 1, "dummy", "dummy"),
        (10829, 1, "x", "x"),
        (3200, 2, "Meet the Flint Stones", "\u539f\u77f3"),
        (1201, 4, "Collecting Sea Shells", "\u8c9d"),
    ]:
        values = [""] * 63
        values[1] = str(category)
        guildleves[row_id] = CsvRow(str(row_id), values)
        text = [""] * 89
        text[9:11] = [ja, en]
        text[13:15] = ["description JA", "description EN"]
        texts[row_id] = CsvRow(str(row_id), text)
    return guildleves, texts


class GuildleveNamesTests(unittest.TestCase):
    def test_complete_sorted_join_preserves_duplicate_names(self):
        guildleves, texts = fixture()
        rows = names.project(guildleves, texts)
        self.assertEqual([r["guildleve_id"] for r in rows], sorted(guildleves))
        self.assertEqual(rows[-4]["guildleve_id"], 10801)
        self.assertEqual(rows[-4]["name_en"], rows[-3]["name_en"])
        self.assertEqual(len(rows), len(guildleves))

    def test_exact_locale_cells_and_csv_round_trip(self):
        guildleves, texts = fixture()
        texts[10801].values[9] = '\u304b\u3099,"quoted"\nline'
        rows = names.project(guildleves, texts)
        output = names.render(rows)
        reread = list(csv.DictReader(io.StringIO(output.decode("utf-8"))))
        self.assertEqual(
            next(r for r in reread if r["guildleve_id"] == "10801")["name_ja"],
            texts[10801].values[9],
        )
        self.assertEqual(output, names.render(names.project(guildleves, texts)))
        self.assertNotIn(b"\r", output)

    def test_placeholder_markers_are_exact_english_cells(self):
        guildleves, texts = fixture()
        rows = names.project(guildleves, texts)
        self.assertEqual(
            {r["guildleve_id"] for r in rows if r["placeholder"] == "true"},
            {2, 10829, 11602},
        )
        texts[10801].values[10] = "Dummy"
        texts[10801].values[9] = names.NO_TRANSLATION
        self.assertEqual(
            next(
                r
                for r in names.project(guildleves, texts)
                if r["guildleve_id"] == 10801
            )["placeholder"],
            "false",
        )

    def test_category_uses_class_type_and_source_locator(self):
        guildleves, texts = fixture()
        rows = {r["guildleve_id"]: r for r in names.project(guildleves, texts)}
        self.assertEqual(rows[10801]["category"], "battlecraft")
        self.assertEqual(rows[3200]["category"], "fieldcraft")
        self.assertEqual(rows[1201]["category"], "other")
        self.assertEqual(rows[3200]["source_sheet"], "xtx/guildleve")
        self.assertEqual(rows[3200]["source_row"], 3200)

    def test_missing_or_extra_name_rows_fail(self):
        guildleves, texts = fixture()
        del texts[10801]
        with self.assertRaisesRegex(ValueError, "row IDs"):
            names.project(guildleves, texts)
        guildleves, texts = fixture()
        texts[99999] = texts[10801]
        with self.assertRaisesRegex(ValueError, "row IDs"):
            names.project(guildleves, texts)

    def test_source_layout_duplicate_and_width_failures(self):
        with tempfile.TemporaryDirectory(prefix="guildleve-names-") as raw:
            path = Path(raw) / "guildleve.csv"
            records = [
                ["", *map(str, range(63))],
                ["", "", "s32", *([""] * 61)],
                [1, *(["0"] * 63)],
            ]

            def write():
                with path.open("w", encoding="utf-8", newline="") as handle:
                    csv.writer(handle).writerows(records)

            write()
            self.assertEqual(list(names.load_source(path)), [1])
            records.append(records[-1])
            write()
            with self.assertRaisesRegex(ValueError, "duplicate"):
                names.load_source(path)
            records.pop()
            records[-1].pop()
            write()
            with self.assertRaisesRegex(ValueError, "expected 63"):
                names.load_source(path)
            records[-1].append("0")
            records[1][2] = "str"
            write()
            with self.assertRaisesRegex(ValueError, "layout"):
                names.load_source(path)

    def test_ranges_keep_gaps(self):
        self.assertEqual(names.id_ranges([7, 2, 3, 8, 11]), [[2, 3], [7, 8], [11, 11]])

    def test_public_validator_rejects_tampering_and_short_rows(self):
        with tempfile.TemporaryDirectory(prefix="guildleve-names-product-") as raw:
            root = Path(raw)
            (root / "derived").mkdir()
            (root / "manifests").mkdir()
            for source in (
                names.OUTPUT,
                names.MANIFEST,
                names.REPO / "manifests/tables.json",
            ):
                (root / source.relative_to(names.REPO)).write_bytes(source.read_bytes())
            product = root / "derived/guildleve_names.csv"
            original = product.read_bytes()
            with (
                patch.object(corpus, "REPO_ROOT", root),
                patch.object(corpus, "MANIFESTS", root / "manifests"),
                patch.object(corpus, "CORPUS_ABSENT", True),
                patch.object(corpus, "errors", []),
            ):
                corpus.validate_guildleve_names()
                self.assertEqual(corpus.errors, [])
                product.write_bytes(
                    original.replace(b"Official Behest", b"Changed Behest!")
                )
                corpus.validate_guildleve_names()
                self.assertTrue(
                    any("SHA-256 mismatch" in error for error in corpus.errors)
                )
                corpus.errors.clear()
                product.write_bytes(original.split(b"\n", 1)[0] + b"\n1\n")
                corpus.validate_guildleve_names()
                self.assertTrue(any("row width" in error for error in corpus.errors))

    @unittest.skipUnless(os.environ.get("XIVL_CSV_DIR"), "requires selected corpus")
    def test_authenticated_corpus_matches_every_locale_cell(self):
        root = Path(os.environ["XIVL_CSV_DIR"])
        outputs = names.build(root)
        rows = list(csv.DictReader(io.StringIO(outputs[names.OUTPUT].decode("utf-8"))))
        source = names.load_source(root / "xtx_guildleve.csv")
        self.assertEqual(len(rows), 624)
        self.assertEqual(sum(row["placeholder"] == "true" for row in rows), 262)
        for row in rows:
            text = source[int(row["guildleve_id"])].values
            self.assertEqual(row["name_en"].encode("utf-8"), text[10].encode("utf-8"))
            self.assertEqual(row["name_ja"].encode("utf-8"), text[9].encode("utf-8"))
        with tempfile.TemporaryDirectory(prefix="guildleve-names-source-") as raw:
            altered = Path(raw)
            for name in names.SOURCE_LAYOUTS:
                (altered / name).write_bytes((root / name).read_bytes())
            path = altered / "xtx_guildleve.csv"
            path.write_bytes(
                path.read_bytes().replace(b"Official Behest", b"Changed Behest!")
            )
            with self.assertRaisesRegex(ValueError, "source bytes differ"):
                names.build(altered)


if __name__ == "__main__":
    unittest.main()
