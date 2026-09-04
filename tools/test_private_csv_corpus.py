#!/usr/bin/env python3
"""Focused mutation tests for the private CSV corpus archive tool."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import private_csv_corpus as corpus


class PrivateCsvCorpusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="private-csv-corpus-")
        self.root = Path(self.temp.name)
        self.csv_dir = self.root / "csv"
        self.csv_dir.mkdir()
        self.files = {
            "a.csv": b"a,one\n1,alpha\n",
            "b.csv": b"b,two\n2,beta\n",
        }
        for name, data in self.files.items():
            (self.csv_dir / name).write_bytes(data)
        self.manifest = self.root / "manifest.json"
        self.tables = self.root / "tables.json"
        rows = []
        for name in sorted(self.files):
            data = self.files[name]
            rows.append(
                {
                    "name": name,
                    "relativePath": f"csv/{name}",
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
        self.manifest.write_text(
            json.dumps(
                {
                    "version": "fixture",
                    "tableCount": len(rows),
                    "totalBytes": sum(row["bytes"] for row in rows),
                }
            )
            + "\n",
            encoding="utf-8",
            newline="",
        )
        self.tables.write_text(json.dumps(rows) + "\n", encoding="utf-8", newline="")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _package(self, output: Path) -> dict:
        return corpus.package_archive(
            output,
            csv_dir=self.csv_dir,
            manifest_path=self.manifest,
            tables_path=self.tables,
        )

    def _verify(self, archive: Path) -> dict:
        return corpus.inspect_archive(
            archive, manifest_path=self.manifest, tables_path=self.tables
        )

    def _write_archive(self, output: Path, members: list[tuple[str, bytes]]) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
                for name, data in members:
                    archive.writestr(name, data)

    def test_package_is_deterministic_and_metadata_is_fixed(self) -> None:
        first = self.root / "first.zip"
        second = self.root / "second.zip"
        self._package(first)
        self._package(second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(
            hashlib.sha256(first.read_bytes()).hexdigest(),
            hashlib.sha256(second.read_bytes()).hexdigest(),
        )
        with zipfile.ZipFile(first) as archive:
            infos = archive.infolist()
            self.assertEqual([info.filename for info in infos], ["a.csv", "b.csv"])
            for info in infos:
                self.assertEqual(info.date_time, corpus.FIXED_DATE)
                self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                self.assertEqual(info.create_system, 3)
                self.assertEqual(info.external_attr, 0o100644 << 16)

    def test_hydrate_reproduces_manifest_identities(self) -> None:
        archive = self.root / "corpus.zip"
        destination = self.root / "hydrated"
        self._package(archive)
        shape = corpus.hydrate_archive(
            archive,
            destination,
            manifest_path=self.manifest,
            tables_path=self.tables,
        )
        self.assertEqual(shape["tableCount"], len(self.files))
        self.assertRegex(shape["treeSha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(
            {path.name for path in destination.iterdir()}, set(self.files)
        )
        for name, data in self.files.items():
            self.assertEqual((destination / name).read_bytes(), data)

    def test_traversal_member_is_rejected(self) -> None:
        archive = self.root / "traversal.zip"
        self._write_archive(archive, [("../a.csv", self.files["a.csv"]), ("b.csv", self.files["b.csv"])])
        with self.assertRaises(corpus.CorpusValidationError):
            self._verify(archive)

    def test_duplicate_member_is_rejected(self) -> None:
        archive = self.root / "duplicate.zip"
        self._write_archive(archive, [("a.csv", self.files["a.csv"]), ("a.csv", self.files["a.csv"])])
        with self.assertRaises(corpus.CorpusValidationError):
            self._verify(archive)

    def test_corrupt_member_is_rejected(self) -> None:
        archive = self.root / "corrupt.zip"
        self._write_archive(archive, [("a.csv", b"changed\n"), ("b.csv", self.files["b.csv"])])
        with self.assertRaises(corpus.CorpusValidationError):
            self._verify(archive)

    def test_unexpected_and_missing_members_are_rejected(self) -> None:
        unexpected = self.root / "unexpected.zip"
        self._write_archive(
            unexpected,
            [("a.csv", self.files["a.csv"]), ("unexpected.csv", self.files["b.csv"])],
        )
        with self.assertRaises(corpus.CorpusValidationError):
            self._verify(unexpected)

        missing = self.root / "missing.zip"
        self._write_archive(missing, [("a.csv", self.files["a.csv"])])
        with self.assertRaises(corpus.CorpusValidationError):
            self._verify(missing)

    def test_non_file_source_is_rejected(self) -> None:
        (self.csv_dir / "a.csv").unlink()
        (self.csv_dir / "a.csv").mkdir()
        with self.assertRaises(corpus.CorpusValidationError):
            self._package(self.root / "non-file.zip")

    def test_nonempty_destination_is_rejected_without_mutation(self) -> None:
        archive = self.root / "corpus.zip"
        destination = self.root / "nonempty"
        destination.mkdir()
        sentinel = destination / "keep.txt"
        sentinel.write_bytes(b"keep")
        self._package(archive)
        with self.assertRaises(corpus.CorpusValidationError):
            corpus.hydrate_archive(
                archive,
                destination,
                manifest_path=self.manifest,
                tables_path=self.tables,
            )
        self.assertEqual(sentinel.read_bytes(), b"keep")


if __name__ == "__main__":
    unittest.main()
