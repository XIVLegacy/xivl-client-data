#!/usr/bin/env python3
"""Check local title joins, locale fields, and embedded title controls."""

from __future__ import annotations

import unittest

from _csv_reader import CsvRow
from build_local_guildleve_names import (
    TITLE_CONTROLS,
    build_rows,
    check_title_controls,
    render_csv,
)


class LocalGuildleveNamesTests(unittest.TestCase):
    def test_locale_fields_and_complete_driver_join(self):
        driver = [CsvRow("120005", []), CsvRow("120001", [])]
        names = [
            CsvRow("120001", ["ignored", "JA one", "Same title"]),
            CsvRow("120005", ["ignored", "JA two", "Same title"]),
            CsvRow("110001", ["ignored", "Other JA", "Other EN"]),
        ]
        self.assertEqual(
            build_rows(driver, names),
            [
                [120001, "Same title", "JA one", "xtx/quest", 120001],
                [120005, "Same title", "JA two", "xtx/quest", 120005],
            ],
        )

    def test_missing_join_is_an_error(self):
        with self.assertRaisesRegex(ValueError, "missing xtx/quest row"):
            build_rows([CsvRow("120005", [])], [])

    def test_duplicate_ids_are_an_error(self):
        row = CsvRow("120005", ["", "JA", "EN"])
        for driver, names in [([row, row], [row]), ([row], [row, row])]:
            with self.subTest(driver=len(driver), names=len(names)):
                with self.assertRaisesRegex(ValueError, "duplicate row id"):
                    build_rows(driver, names)

    def test_missing_title_is_an_error(self):
        for values in [[""], ["", "", "EN"], ["", "JA", ""]]:
            with self.subTest(values=values):
                with self.assertRaisesRegex(ValueError, "missing title field"):
                    build_rows([CsvRow("1", [])], [CsvRow("1", values)])

    def test_title_control_change_is_an_error(self):
        check_title_controls(
            [CsvRow("4219", [TITLE_CONTROLS["ja"], TITLE_CONTROLS["en"]])]
        )
        with self.assertRaisesRegex(ValueError, "title control 4219 changed"):
            check_title_controls(
                [CsvRow("4219", [TITLE_CONTROLS["en"], TITLE_CONTROLS["ja"]])]
            )

    def test_verbatim_text_and_deterministic_rendering(self):
        rows = [
            [
                120005,
                'Name, with "quotes"',
                "JA [@newline:02100103]",
                "xtx/quest",
                120005,
            ]
        ]
        self.assertEqual(
            render_csv(rows),
            b"guildleve_id,name_en,name_ja,source_sheet,source_row\n"
            b'120005,"Name, with ""quotes""",JA [@newline:02100103],xtx/quest,120005\n',
        )


if __name__ == "__main__":
    unittest.main()
