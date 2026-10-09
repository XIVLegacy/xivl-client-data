"""Check attributive backing-row framing and sparse locale handling."""

from __future__ import annotations

import os
import struct
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest import mock

import build_attributive_backing_rows as study


def framed(text: bytes, scrambled: bool = False) -> bytes:
    if scrambled:
        body = b"\xff" + bytes(value ^ 0x73 for value in text) + b"\x73"
    else:
        body = text + b"\x00"
    return struct.pack("<H", len(body)) + body


class AttributiveBackingRowsTests(unittest.TestCase):
    def test_mixed_row_layout_decodes_s8_and_strings(self):
        values, framing = study.parse_row(
            b"\x63" + framed(b"a ") + framed(b"[n]", scrambled=True),
            ["s8", "str", "str"],
        )
        self.assertEqual(values, ["99", "a ", r"\[n]"])
        self.assertEqual(framing[0], {"type": "s8", "start": 0, "end": 1})
        self.assertTrue(framing[2]["scrambled"])

    def test_string_framing_is_retained_without_token_interpretation(self):
        end, value, detail = study.parse_sheet_string(framed(b"A[B"))
        self.assertEqual(end, len(framed(b"A[B")))
        self.assertEqual(value, r"A\[B")
        self.assertEqual(detail["declaredLength"], 4)
        self.assertEqual(detail["terminator"], "0x00")

    def test_sparse_enable_ranges_keep_key_and_ordinal_separate(self):
        ranges, keys = study.read_ranges(
            bytes.fromhex("01000000010000000500000001000000"), 1, 35
        )
        self.assertEqual(ranges, [(1, 1), (5, 1)])
        self.assertEqual(keys, [1, 5])
        self.assertEqual(keys[1], 5)
        self.assertNotEqual(keys[1], 1)

    def test_zero_length_string_refuses(self):
        with self.assertRaisesRegex(ValueError, "zero bytes"):
            study.parse_sheet_string(b"\x00\x00")

    def test_truncated_string_body_refuses(self):
        with self.assertRaisesRegex(ValueError, "string body"):
            study.parse_sheet_string(struct.pack("<H", 2) + b"\x00")

    def test_control_bytes_refuse_opaque_string_guessing(self):
        with self.assertRaisesRegex(ValueError, "control byte"):
            study.parse_sheet_string(framed(bytes.fromhex("4102")))

    def test_unknown_column_type_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported attributive"):
            study.parse_row(b"x", ["u16"])

    def test_offset_slot_count_is_guarded(self):
        with self.assertRaisesRegex(ValueError, "entry count"):
            study.strict_row_spans(bytes.fromhex("04000000"), 4, 1, 2)

    def test_ambiguous_named_master_reference_fails_through_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            client_root = Path(temporary)
            (client_root / "game.ver").write_text("2012.09.19.0001", encoding="ascii")
            (client_root / "patch.ver").write_text("1.23b", encoding="ascii")
            master = ET.Element("ssd")
            ET.SubElement(master, "sheet", name=study.SHEET, infofile="7")
            ET.SubElement(master, "sheet", name=study.SHEET, infofile="8")
            with (
                mock.patch.object(
                    study,
                    "load_inventory",
                    return_value=[
                        {"name": study.SHEET, "resourceId": 7, "source": "game_schema"}
                    ],
                ),
                mock.patch.object(
                    study, "resource_path", return_value=client_root / "master"
                ),
                mock.patch.object(study, "parse_document", return_value=master),
            ):
                with self.assertRaisesRegex(ValueError, "exactly once"):
                    study.build(client_root, client_root / "missing-csv")

    def test_authenticated_client_cells_when_inputs_are_configured(self):
        client_root = os.environ.get("XIVL_CLIENT_ROOT")
        csv_dir = os.environ.get("XIVL_CSV_DIR")
        if not client_root or not csv_dir:
            self.skipTest("XIVL_CLIENT_ROOT and XIVL_CSV_DIR are not configured")
        report = study.build(Path(client_root), Path(csv_dir))
        self.assertEqual(report["csvRowCount"], 35)
        self.assertEqual(report["sourceDefinition"]["resourceId"], "0x0B4500CA")
        for locale in report["locales"]:
            self.assertEqual(
                locale["fieldMatchesCsvCount"],
                sum(block["fieldCount"] for block in locale["blocks"]),
            )
        english = next(item for item in report["locales"] if item["locale"] == "en")
        anchor = next(item for item in english["anchors"] if item["rowKey"] == 5)
        self.assertEqual(anchor["slotIndex"], 4)
        self.assertEqual(anchor["enabledOrdinal"], 4)
        self.assertEqual(anchor["csvIterationIndex"], 4)
        simplified = next(item for item in report["locales"] if item["locale"] == "chs")
        self.assertEqual(simplified["enabledRowCount"], 1)
        self.assertIn(5, simplified["csvOnlyKeys"])


if __name__ == "__main__":
    unittest.main()
