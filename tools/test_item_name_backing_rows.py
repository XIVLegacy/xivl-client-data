"""Check signed item fields, opaque controls and trailing chs offset slots."""

from __future__ import annotations

import os
import struct
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import build_item_name_backing_rows as item
import build_place_name_backing_rows as backing


def framed(text: bytes) -> bytes:
    return struct.pack("<H", len(text) + 1) + text + b"\x00"


class ItemNameBackingRowsTests(unittest.TestCase):
    def test_signed_fields_keep_negative_values(self):
        values, details = backing.parse_row(
            framed(b"Authored") + b"\xff\x80\x7f", ["str", "s8", "s8", "s8"]
        )
        self.assertEqual(values, ["Authored", "-1", "-128", "127"])
        self.assertEqual(details[1], {"type": "s8"})
        with self.assertRaisesRegex(ValueError, "s8 column is truncated"):
            backing.parse_row(b"", ["s8"])

    def test_item_controls_remain_opaque_lossless_envelopes(self):
        raw = bytes.fromhex("021a020203021d0103022803010203")
        _, value, details = backing.parse_sheet_string(framed(raw))
        self.assertEqual(
            value,
            "[@italic:021a020203][@non-breaking-space:021d0103][@sheet:022803010203]",
        )
        self.assertEqual(details["tokenCount"], 3)

    def test_short_offset_policy_preserves_nonzero_keys_and_empty_slots(self):
        data = framed(b"Authored") + b"\xff"
        block = ET.Element("file", begin="1000000", count="3", enable="7", offset="8")
        block.text = "6"
        resources = {
            6: data,
            7: struct.pack("<II", 1000001, 1),
            8: struct.pack("<II", 0, len(data)),
        }
        arguments = (
            Path("unused"),
            "chs",
            1,
            block,
            ["str", "s8"],
            [0, 1],
            {1000001: SimpleNamespace(values=["Authored", "-1"])},
            {1000001: 0},
            5,
        )
        with mock.patch.object(
            backing, "_resource", side_effect=lambda _, key, __: resources[key]
        ):
            with self.assertRaisesRegex(ValueError, "entry count"):
                backing._block_report(*arguments)
            report, keys, anchors = backing._block_report(
                *arguments, anchor_keys=(1000001,), allow_short_offsets=True
            )
        self.assertEqual(keys, [1000001])
        self.assertEqual(report["fieldMatchesCsvCount"], 2)
        self.assertEqual(report["offsetEntryCount"], 2)
        self.assertEqual(anchors[0]["slotIndex"], 1)
        self.assertEqual(anchors[0]["enabledOrdinal"], 5)

    def test_authenticated_item_blocks_when_inputs_are_configured(self):
        client_root = os.environ.get("XIVL_CLIENT_ROOT")
        csv_dir = os.environ.get("XIVL_CSV_DIR")
        if not client_root or not csv_dir:
            self.skipTest("XIVL_CLIENT_ROOT and XIVL_CSV_DIR are not configured")
        report = item.build(Path(client_root), Path(csv_dir))
        self.assertEqual(report["csvRowCount"], 8403)
        for locale in report["locales"]:
            self.assertEqual(locale["fileBlockCount"], 50)
            self.assertEqual(
                locale["fieldMatchesCsvCount"],
                locale["enabledRowCount"] * len(locale["columns"]),
            )
        english = report["locales"][1]
        anchor = next(row for row in english["anchors"] if row["rowKey"] == 10009506)
        self.assertEqual(anchor["slotIndex"], 9506)
        self.assertEqual(anchor["enabledOrdinal"], 5614)
        self.assertEqual(anchor["cells"]["5"], "Bat Wing")


if __name__ == "__main__":
    unittest.main()
