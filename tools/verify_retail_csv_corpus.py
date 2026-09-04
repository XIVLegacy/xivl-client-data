#!/usr/bin/env python3
"""Verify the fixed private decoded-CSV corpus contract.

The archive is an input to the verifier, never an output.  Successful and
failed runs emit the same small, schema-checked attestation; archive member
names and bytes are intentionally absent from that output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _schema_check  # noqa: E402
import private_csv_corpus as corpus  # noqa: E402


REPO = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO / "manifests" / "private_csv_corpus.json"
DEFAULT_SCHEMA = REPO / "schemas" / "retail_csv_corpus_attestation.schema.json"
ATTESTATION_FILENAME = "retail-evidence-attestation.json"

CHECK_ID = "decoded-csv-corpus-v1"
INPUT_ID = "decoded-csv-corpus-1.23b"
PRIVATE_REPOSITORY = "XIVLegacy/xivl-private-assets"
PRIVATE_COMMIT = "db5f74e7480a162081820b2079f67bf0d6ddc5d4"
PRIVATE_PATH = "extracted/ffxiv-1.23b/client-data/csv.zip"
ARCHIVE_PATH = "csv.zip"
ARCHIVE_SIZE = 70110686
ARCHIVE_SHA256 = "006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0"
EXPANDED_FILE_COUNT = 803
EXPANDED_TOTAL_BYTES = 70029056
EXPANDED_TREE_SHA256 = "33e51c468b85b3d27b628ca4f5ff49e0bd10a8778812085f2bcdfdfd0cbd84bb"
TARGET = "csv"
SCHEMA_VERSION = 1
TOOL_VERSIONS = {"python": "3.12", "verifier": "1.0"}
COMMIT_LENGTH = 40

class VerificationError(Exception):
    """Malformed input that is safe to report without its contents."""


def _read_json(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise VerificationError("JSON duplicate field")
            result[key] = value
        return result

    try:
        return json.loads(
            path.read_text(encoding="ascii"), object_pairs_hook=reject_duplicates
        )
    except (OSError, UnicodeError, ValueError) as exc:
        raise VerificationError("JSON input unreadable") from exc


def _expected_manifest() -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "inputId": INPUT_ID,
        "checkId": CHECK_ID,
        "target": TARGET,
        "source": {
            "repository": PRIVATE_REPOSITORY,
            "commit": PRIVATE_COMMIT,
            "path": PRIVATE_PATH,
        },
        "archive": {
            "path": ARCHIVE_PATH,
            "bytes": ARCHIVE_SIZE,
            "sha256": ARCHIVE_SHA256,
        },
        "expanded": {
            "fileCount": EXPANDED_FILE_COUNT,
            "totalBytes": EXPANDED_TOTAL_BYTES,
            "treeSha256": EXPANDED_TREE_SHA256,
        },
    }


EXPECTED_MANIFEST = _expected_manifest()


def contract_errors(manifest_path: Path = DEFAULT_MANIFEST) -> list[str]:
    """Check the tracked grant without accessing the private archive."""
    try:
        manifest = _read_json(manifest_path)
    except VerificationError:
        return ["private CSV grant is unreadable"]
    if manifest != EXPECTED_MANIFEST:
        return ["private CSV grant drifted"]
    return []


def _is_reparse(path: Path) -> bool:
    try:
        is_junction = getattr(os.path, "isjunction", lambda value: False)
        return path.is_symlink() or is_junction(path)
    except OSError:
        return True


def _archive_identity_errors(archive_path: Path) -> list[str]:
    try:
        result = archive_path.lstat()
    except OSError:
        return ["private archive identity check failed"]
    if _is_reparse(archive_path) or not stat.S_ISREG(result.st_mode):
        return ["private archive identity check failed"]
    if result.st_size != ARCHIVE_SIZE:
        return ["private archive identity check failed"]

    digest = hashlib.sha256()
    try:
        with archive_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                digest.update(chunk)
    except OSError:
        return ["private archive identity check failed"]
    if digest.hexdigest() != ARCHIVE_SHA256:
        return ["private archive identity check failed"]
    return []


def _shape_errors(shape: Any) -> list[str]:
    if not isinstance(shape, dict):
        return ["private archive shape differs"]
    if (
        shape.get("tableCount") != EXPANDED_FILE_COUNT
        or shape.get("totalBytes") != EXPANDED_TOTAL_BYTES
        or shape.get("treeSha256") != EXPANDED_TREE_SHA256
    ):
        return ["private archive shape differs"]
    return []


def archive_errors(archive_path: Path) -> list[str]:
    """Verify archive bytes and expanded member identities read-only."""
    errors = _archive_identity_errors(archive_path)
    if errors:
        return errors
    try:
        shape = corpus.inspect_archive(archive_path)
    except (corpus.ArchiveValidationError, OSError, RuntimeError, ValueError):
        return ["private archive validation failed"]
    return _shape_errors(shape)


def verify_archive(
    archive_path: Path,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> list[str]:
    errors = contract_errors(manifest_path)
    return errors + archive_errors(archive_path)


def verify(
    archive_path: Path | None = None,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> list[str]:
    """Verify the grant, and the archive when one is supplied."""
    errors = contract_errors(manifest_path)
    if archive_path is not None:
        errors.extend(archive_errors(archive_path))
    return errors


def _git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise VerificationError("public commit unavailable") from exc
    commit = result.stdout.strip()
    if (
        len(commit) != COMMIT_LENGTH
        or any(char not in "0123456789abcdef" for char in commit)
        or commit == "0" * COMMIT_LENGTH
    ):
        raise VerificationError("public commit unavailable")
    return commit


def build_attestation(status: str, public_commit: str | None = None) -> dict[str, Any]:
    if status not in {"pass", "fail"}:
        raise ValueError("attestation status invalid")
    commit = public_commit if public_commit is not None else _git_commit()
    if (
        len(commit) != COMMIT_LENGTH
        or any(char not in "0123456789abcdef" for char in commit)
        or commit == "0" * COMMIT_LENGTH
    ):
        raise ValueError("public commit invalid")
    return {
        "schemaVersion": SCHEMA_VERSION,
        "publicRepositoryCommit": commit,
        "approvedInputSha256": ARCHIVE_SHA256,
        "toolVersions": dict(TOOL_VERSIONS),
        "check": {"id": CHECK_ID, "version": 1},
        "result": {"status": status},
    }


def _schema_errors(document: Any) -> bool:
    try:
        schema = _schema_check.load_schema(DEFAULT_SCHEMA)
        return bool(_schema_check.validate(document, schema))
    except _schema_check.SchemaError:
        return True


def retained_output_errors(directory: Path) -> list[str]:
    """Validate the exact one-file, canonical retained-output boundary."""
    try:
        if _is_reparse(directory) or not directory.is_dir():
            return ["retained output root invalid"]
        entries = list(directory.iterdir())
        if len(entries) != 1 or entries[0].name != ATTESTATION_FILENAME:
            return ["retained output allowlist differs"]
        path = entries[0]
        if _is_reparse(path) or not path.is_file() or path.stat().st_size > 4096:
            return ["retained attestation file invalid"]
        raw = path.read_bytes()
        if b"\r" in raw:
            return ["retained attestation line ending invalid"]
        text = raw.decode("ascii")
        document = json.loads(text)
        canonical = (
            json.dumps(document, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("ascii")
        if raw != canonical:
            return ["retained attestation serialization invalid"]
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return ["retained attestation unreadable"]
    return ["retained attestation schema rejected"] if _schema_errors(document) else []


# Keep the private helper spelling available to callers following the
# static-actor verifier contract.
_validate_retained_output = retained_output_errors


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=None)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check-contract", action="store_true")
    parser.add_argument("--validate-retained-output", type=Path)
    return parser.parse_args(argv)


def _emit_attestation(status: str) -> None:
    attestation = build_attestation(status)
    if _schema_errors(attestation):
        raise VerificationError("attestation schema rejected output")
    payload = (
        json.dumps(attestation, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    sys.stdout.buffer.write(payload)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.validate_retained_output is not None:
        errors = retained_output_errors(args.validate_retained_output)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1 if errors else 0

    if args.archive is None and not args.check_contract:
        errors = verify(None, args.manifest) + ["private archive is required"]
    elif args.archive is None:
        errors = verify(None, args.manifest)
    else:
        errors = verify_archive(args.archive, args.manifest)

    try:
        _emit_attestation("pass" if not errors else "fail")
    except (VerificationError, ValueError):
        print("ERROR: attestation could not be built", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
