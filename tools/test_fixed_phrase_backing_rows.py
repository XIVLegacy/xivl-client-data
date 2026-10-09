"""Check sparse backing-row identities and bounded metadata reads."""

import unittest

import build_fixed_phrase_backing_rows as study


class BackingRowsTests(unittest.TestCase):
    def test_sparse_keys_are_not_dense_ordinals(self):
        ranges, keys = study.read_ranges(
            bytes.fromhex("64 00 00 00 02 00 00 00 37 01 00 00 01 00 00 00"),
            100,
            212,
        )
        self.assertEqual(ranges, [(100, 2), (311, 1)])
        self.assertEqual(keys, [100, 101, 311])

    def test_enable_pair_bounds(self):
        for raw in (
            bytes.fromhex("64 00 00 00 01 00 00"),
            bytes.fromhex("63 00 00 00 01 00 00 00"),
            bytes.fromhex("64 00 00 00 03 00 00 00"),
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                study.read_ranges(raw, 100, 2)

    def test_spans_keep_empty_slots(self):
        self.assertEqual(
            study.row_spans(
                bytes.fromhex("04 00 00 00 04 00 00 00 08 00 00 00"), 8, 100, 3
            ),
            {100: (0, 4), 102: (4, 8)},
        )

    def test_missing_trailing_empty_slots_are_explicit(self):
        self.assertEqual(
            study.row_spans(bytes.fromhex("04 00 00 00"), 4, 100, 3),
            {100: (0, 4)},
        )

    def test_invalid_spans_refuse(self):
        for raw in (
            bytes.fromhex("04 00 00"),
            bytes.fromhex("04 00 00 00 03 00 00 00"),
            bytes.fromhex("05 00 00 00"),
            bytes.fromhex("03 00 00 00"),
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                study.row_spans(raw, 4, 100, 2)

    def test_field0_and_literal_metadata_remain_separate(self):
        self.assertEqual(
            study.metadata_prefix(bytes.fromhex("09 00 00 00 05 00 23 5B 78 5D 00")),
            (9, "#[x]"),
        )
        self.assertEqual(
            study.metadata_prefix(bytes.fromhex("09 00 00 00 03 00 FF 33 73")),
            (9, "@"),
        )

    def test_truncated_metadata_refuses(self):
        for raw in (
            bytes.fromhex("09 00 00 00 01"),
            bytes.fromhex("09 00 00 00 05 00 40 00"),
            bytes.fromhex("09 00 00 00 01 00 40"),
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                study.metadata_prefix(raw)


if __name__ == "__main__":
    unittest.main()
