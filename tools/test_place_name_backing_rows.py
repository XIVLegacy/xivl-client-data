"""Check placeName backing-row framing and sparse key handling."""

from __future__ import annotations

import os
import struct
import unittest
from pathlib import Path

import build_place_name_backing_rows as study


def framed(text: bytes, scrambled: bool = False) -> bytes:
    if scrambled:
        body = b"\xff" + bytes(value ^ 0x73 for value in text + b"\x00")[:-1] + b"\x73"
    else:
        body = text + b"\x00"
    return struct.pack("<H", len(body)) + body


class PlaceNameBackingRowsTests(unittest.TestCase):
    def test_actual_mixed_row_layout_decodes_all_columns(self):
        raw = framed(b"Limsa") + framed(b"limsa", scrambled=True) + b"\x01"
        values, details = study.parse_row(raw, ["str", "str", "u8"])
        self.assertEqual(values, ["Limsa", "limsa", "1"])
        self.assertTrue(details[1]["scrambled"])

    def test_rich_token_uses_lossless_csv_escape_without_expression_decode(self):
        token = bytes.fromhex("021f0103")
        end, value, detail = study.parse_sheet_string(framed(b"A" + token + b"[B"))
        self.assertEqual(end, len(framed(b"A" + token + b"[B")))
        self.assertEqual(value, r"A[@hyphen:021f0103]\[B")
        self.assertEqual(detail["tokenCodes"], {"0x1F": 1})
        self.assertEqual(detail["tokenLengthLeads"], {"0x01": 1})

    def test_zero_length_string_refuses(self):
        with self.assertRaisesRegex(ValueError, "zero bytes"):
            study.parse_sheet_string(b"\x00\x00")

    def test_truncated_string_prefix_refuses(self):
        with self.assertRaisesRegex(ValueError, "length prefix"):
            study.parse_sheet_string(b"\x01")

    def test_truncated_string_body_refuses(self):
        with self.assertRaisesRegex(ValueError, "string body"):
            study.parse_sheet_string(struct.pack("<H", 2) + b"\x00")

    def test_missing_string_terminator_refuses(self):
        with self.assertRaisesRegex(ValueError, "invalid terminator"):
            study.parse_sheet_string(struct.pack("<H", 2) + b"ab")

    def test_malformed_observed_token_envelope_refuses(self):
        with self.assertRaisesRegex(ValueError, "unsupported length lead"):
            study.parse_sheet_string(framed(bytes.fromhex("02090003")))

    def test_trailing_row_bytes_refuse(self):
        with self.assertRaisesRegex(ValueError, "trailing bytes"):
            study.parse_row(framed(b"x") + b"\x00", ["str"])

    def test_sparse_anchor_distinguishes_slot_and_enabled_ordinals(self):
        ranges, keys = study.read_ranges(
            bytes.fromhex("01000000010000001b04000001000000"), 0, 1100
        )
        self.assertEqual(ranges, [(1, 1), (1051, 1)])
        self.assertEqual(keys, [1, 1051])
        self.assertEqual(keys[1], 1051)
        self.assertNotEqual(keys[1], 1)

    def test_unknown_token_code_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported"):
            study.parse_sheet_string(framed(bytes.fromhex("02060103")))

    def test_unhandled_column_type_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unsupported placeName column type"):
            study.parse_row(framed(b"x"), ["s32"])

    def test_offset_slot_count_is_guarded(self):
        with self.assertRaises(ValueError):
            study.strict_row_spans(bytes.fromhex("04000000"), 4, 0, 2)

    def test_authenticated_client_cells_when_inputs_are_configured(self):
        client_root = os.environ.get("XIVL_CLIENT_ROOT")
        csv_dir = os.environ.get("XIVL_CSV_DIR")
        if not client_root or not csv_dir:
            self.skipTest("XIVL_CLIENT_ROOT and XIVL_CSV_DIR are not configured")
        report = study.build(Path(client_root), Path(csv_dir))
        self.assertEqual(report["csvRowCount"], 923)
        for locale in report["locales"]:
            self.assertEqual(
                locale["fieldMatchesCsvCount"],
                sum(block["fieldCount"] for block in locale["blocks"]),
            )
            anchor = next(item for item in locale["anchors"] if item["rowKey"] == 1051)
            self.assertEqual(anchor["slotIndex"], 1051)
            self.assertEqual(anchor["csvIterationIndex"], 101)


if __name__ == "__main__":
    unittest.main()
