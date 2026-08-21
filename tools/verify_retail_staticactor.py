#!/usr/bin/env python3
"""Verify the fixed static-actor retail-input product contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _schema_check  # noqa: E402


REPO = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = REPO / "manifests" / "staticactor_class_paths.json"
DEFAULT_CHECK = REPO / "manifests" / "retail_staticactor_check.json"
DEFAULT_RETAIL_INPUTS = REPO / "manifests" / "retail_inputs.json"
DEFAULT_PRODUCT = REPO / "manifests" / "staticactor_class_paths.json"
DEFAULT_SCHEMA = REPO / "schemas" / "retail-evidence-attestation.schema.json"

CHECK_ID = "staticactor-class-paths-v1"
INPUT_ID = "staticactor-san-1.23b"
INPUT_FILENAME = "rq9q1797qvs.san"
INPUT_INSTALL_PATH = "client/script/rq9q1797qvs.san"
INPUT_SIZE = 108911
INPUT_SHA256 = "bb7306461b1728493242016a16d9dd5257d7512c60e423b017de5ec7aced3d14"
PRIVATE_REPOSITORY = "XIVLegacy/xivl-private-assets"
PRIVATE_COMMIT = "aeb52f6dbde95a793ee6d52be28de9f28a885b15"
PRIVATE_PATH = "client-data/ffxiv-1.23b/client/script/rq9q1797qvs.san"
PRODUCT_PATH = "manifests/staticactor_class_paths.json"
PRODUCT_SIZE = 248434
PRODUCT_SHA256 = "d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0"
PRODUCT_RECORD_COUNT = 2812
SCHEMA_VERSION = 1
TOOL_VERSIONS = {"python": "3.12", "verifier": "1.0"}

EXPECTED_RETAIL_INPUTS = {
    "schemaVersion": 1,
    "inputs": [{
        "id": INPUT_ID,
        "filename": INPUT_FILENAME,
        "installRelativePath": INPUT_INSTALL_PATH,
        "size": INPUT_SIZE,
        "sha256": INPUT_SHA256,
        "source": {
            "repository": PRIVATE_REPOSITORY,
            "commit": PRIVATE_COMMIT,
            "path": PRIVATE_PATH,
        },
        "allowedChecks": [CHECK_ID],
    }],
}
EXPECTED_CHECK = {
    "schemaVersion": 1,
    "checkId": CHECK_ID,
    "approvedInputId": INPUT_ID,
    "approvedInputSha256": INPUT_SHA256,
    "inputInstallRelativePath": INPUT_INSTALL_PATH,
    "generator": "tools/extract_staticactor_san.py",
    "expectedProduct": {
        "path": PRODUCT_PATH,
        "bytes": PRODUCT_SIZE,
        "sha256": PRODUCT_SHA256,
        "recordCount": PRODUCT_RECORD_COUNT,
    },
}


class VerificationError(Exception):
    """Malformed input that is safe to report without its contents."""


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise VerificationError("JSON input could not be read") from exc


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO, check=True,
            capture_output=True, text=True, timeout=10,
        )
        commit = result.stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise VerificationError("public commit unavailable") from exc
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None or commit == "0" * 40:
        raise VerificationError("public commit unavailable")
    return commit


def build_attestation(status: str) -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "publicRepositoryCommit": _git_commit(),
        "approvedInputSha256": INPUT_SHA256,
        "toolVersions": dict(TOOL_VERSIONS),
        "check": {"id": CHECK_ID, "version": 1},
        "result": {"status": status},
    }


def _product_errors(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        actual_size = path.stat().st_size
        actual_hash = _sha256(path)
        actual_bytes = path.read_bytes()
        expected_bytes = DEFAULT_PRODUCT.read_bytes()
    except (OSError, UnicodeError):
        return ["product could not be read"]
    if actual_size != PRODUCT_SIZE or actual_hash != PRODUCT_SHA256:
        errors.append("product size or SHA-256 differs")
    if actual_bytes != expected_bytes:
        errors.append("product bytes differ from the tracked result")
    try:
        document = json.loads(actual_bytes.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        return errors + ["product is not valid JSON"]
    if not isinstance(document, dict):
        return errors + ["product root is not an object"]
    if document.get("recordCount") != PRODUCT_RECORD_COUNT:
        errors.append("product record count differs")
    records = document.get("records")
    if not isinstance(records, list) or len(records) != PRODUCT_RECORD_COUNT:
        errors.append("product records are malformed")
    elif len({record.get("id") for record in records if isinstance(record, dict)}) != len(records):
        errors.append("product contains duplicate record IDs")
    return errors


def verify(
    input_path: Path = DEFAULT_INPUT,
    check_path: Path = DEFAULT_CHECK,
    retail_inputs_path: Path = DEFAULT_RETAIL_INPUTS,
) -> list[str]:
    errors = _product_errors(input_path)
    try:
        retail_inputs = _read_json(retail_inputs_path)
        check = _read_json(check_path)
    except VerificationError as exc:
        return errors + [str(exc)]
    if retail_inputs != EXPECTED_RETAIL_INPUTS:
        errors.append("retail input grant drifted")
    if check != EXPECTED_CHECK:
        errors.append("static-actor check manifest drifted")
    return errors


def _validate_retained_output(directory: Path) -> list[str]:
    try:
        entries = list(directory.iterdir())
    except OSError:
        return ["retained output directory is unavailable"]
    if len(entries) != 1:
        return ["retained output allowlist differs"]
    path = entries[0]
    if path.name != "retail-evidence-attestation.json" or not path.is_file() or path.is_symlink():
        return ["retained output allowlist differs"]
    try:
        document = _read_json(path)
        schema = _schema_check.load_schema(DEFAULT_SCHEMA)
    except (VerificationError, _schema_check.SchemaError):
        return ["retained attestation is unavailable"]
    return _schema_check.validate(document, schema)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, dest="input_path")
    parser.add_argument("--check", type=Path, default=DEFAULT_CHECK, dest="check_path")
    parser.add_argument("--retail-inputs", type=Path, default=DEFAULT_RETAIL_INPUTS)
    parser.add_argument("--validate-retained-output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.validate_retained_output is not None:
        errors = _validate_retained_output(args.validate_retained_output)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1 if errors else 0
    try:
        errors = verify(args.input_path, args.check_path, args.retail_inputs)
    except (OSError, KeyError, TypeError, ValueError, VerificationError):
        errors = ["verification input is malformed"]
    try:
        attestation = build_attestation("pass" if not errors else "fail")
    except VerificationError:
        print("ERROR: public commit unavailable", file=sys.stderr)
        return 1
    try:
        schema = _schema_check.load_schema(DEFAULT_SCHEMA)
        schema_errors = _schema_check.validate(attestation, schema)
    except _schema_check.SchemaError:
        schema_errors = ["schema unavailable"]
    if schema_errors:
        errors.append("attestation schema rejected output")
        try:
            attestation = build_attestation("fail")
        except VerificationError:
            print("ERROR: public commit unavailable", file=sys.stderr)
            return 1
    payload = json.dumps(
        attestation, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii") + b"\n"
    sys.stdout.buffer.write(payload)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
