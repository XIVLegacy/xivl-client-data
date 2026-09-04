#!/usr/bin/env python3
"""Mutation tests for the private decoded-CSV corpus retail contract."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _schema_check  # noqa: E402
import verify_retail_csv_corpus as verifier  # noqa: E402


REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "manifests" / "private_csv_corpus.json"
SCHEMA = REPO / "schemas" / "private_csv_corpus.schema.json"
ATTESTATION_SCHEMA = REPO / "schemas" / "retail_csv_corpus_attestation.schema.json"
VERIFY = REPO / "tools" / "verify_retail_csv_corpus.py"
WORKFLOW = REPO / ".github" / "workflows" / "retail-checks.yml"
PASSED: list[str] = []
FAILED: list[str] = []


def check(label: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(label)


def write_json(path: Path, value: object, *, canonical: bool = False) -> None:
    if canonical:
        raw = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"
    else:
        raw = json.dumps(value, ensure_ascii=True, indent=2) + "\n"
    path.write_text(raw, encoding="ascii", newline="")


def run_verifier(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFY), *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )


def contract_tests(root: Path) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="ascii"))
    schema = _schema_check.load_schema(SCHEMA)
    check("public CSV grant satisfies schema", not _schema_check.validate(manifest, schema))
    check("public grant passes", not verifier.contract_errors())

    for field, label in (
        (("source", "commit"), "source commit"),
        (("archive", "bytes"), "archive size"),
        (("archive", "sha256"), "archive hash"),
        (("expanded", "fileCount"), "expanded file count"),
        (("expanded", "totalBytes"), "expanded byte count"),
        (("expanded", "treeSha256"), "expanded tree hash"),
    ):
        mutated = copy.deepcopy(manifest)
        current = mutated[field[0]][field[1]]
        mutated[field[0]][field[1]] = (current + 1) if isinstance(current, int) else "0" * len(current)
        path = root / f"mutated-{label.replace(' ', '-')}.json"
        write_json(path, mutated)
        check(f"mutated {label} grant fails", bool(verifier.contract_errors(path)))


def archive_logic_tests(root: Path) -> None:
    expected = {
        "tableCount": verifier.EXPANDED_FILE_COUNT,
        "totalBytes": verifier.EXPANDED_TOTAL_BYTES,
        "treeSha256": verifier.EXPANDED_TREE_SHA256,
    }
    check("canonical archive shape passes", not verifier._shape_errors(expected))
    for field, label in (
        ("tableCount", "content count"),
        ("totalBytes", "content bytes"),
        ("treeSha256", "content tree"),
    ):
        mutated = dict(expected)
        mutated[field] = mutated[field] + 1 if isinstance(mutated[field], int) else "0" * 64
        check(f"mutated {label} fails", bool(verifier._shape_errors(mutated)))

    short_archive = root / "short.zip"
    short_archive.write_bytes(b"x")
    check("archive size failure is reported", bool(verifier.archive_errors(short_archive)))
    original_size = verifier.ARCHIVE_SIZE
    try:
        verifier.ARCHIVE_SIZE = 1
        check("archive hash failure is reported", bool(verifier.archive_errors(short_archive)))
    finally:
        verifier.ARCHIVE_SIZE = original_size

    original_identity = verifier._archive_identity_errors
    original_inspect = verifier.corpus.inspect_archive
    try:
        verifier._archive_identity_errors = lambda _path: []

        def reject(_path: Path) -> dict:
            raise verifier.corpus.ArchiveValidationError("member content rejected")

        verifier.corpus.inspect_archive = reject
        check("archive content failure is reported", bool(verifier.archive_errors(Path("private.csv.zip"))))

        verifier.corpus.inspect_archive = lambda _path: dict(expected)
        check("archive content baseline passes", not verifier.archive_errors(Path("private.csv.zip")))
        bad_tree = dict(expected, treeSha256="0" * 64)
        verifier.corpus.inspect_archive = lambda _path: bad_tree
        check("archive tree failure is reported", bool(verifier.archive_errors(Path("private.csv.zip"))))
    finally:
        verifier._archive_identity_errors = original_identity
        verifier.corpus.inspect_archive = original_inspect


def output_tests(root: Path) -> None:
    schema = _schema_check.load_schema(ATTESTATION_SCHEMA)
    attestation = verifier.build_attestation("pass", "1" * 40)
    check("passing attestation satisfies schema", not _schema_check.validate(attestation, schema))
    mutated = copy.deepcopy(attestation)
    mutated["archive"] = "forbidden"
    check("attestation additional field fails", bool(_schema_check.validate(mutated, schema)))
    mutated = copy.deepcopy(attestation)
    mutated["approvedInputSha256"] = "0" * 64
    check("attestation input hash mutation fails", bool(_schema_check.validate(mutated, schema)))
    mutated = copy.deepcopy(attestation)
    mutated["publicRepositoryCommit"] = "0" * 40
    check("attestation zero commit fails", bool(_schema_check.validate(mutated, schema)))

    failed = run_verifier("--archive", str(root / "missing-private-archive.zip"))
    try:
        document = json.loads(failed.stdout)
    except json.JSONDecodeError:
        document = {}
    check("failure invocation exits nonzero", failed.returncode != 0)
    check(
        "failure output is sanitized",
        set(document)
        == {
            "schemaVersion",
            "publicRepositoryCommit",
            "approvedInputSha256",
            "toolVersions",
            "check",
            "result",
        }
        and document.get("result", {}).get("status") == "fail"
        and "private-archive" not in failed.stdout
        and "private-archive" not in failed.stderr,
    )

    first = run_verifier("--check-contract")
    second = run_verifier("--check-contract")
    check(
        "repeated attestations are byte-identical",
        first.returncode == second.returncode == 0 and first.stdout == second.stdout,
    )
    check("attestation output has LF terminator", first.stdout.endswith("\n") and "\r" not in first.stdout)

    retained = root / "retained"
    retained.mkdir()
    write_json(retained / verifier.ATTESTATION_FILENAME, attestation, canonical=True)
    check("single retained attestation passes", not verifier.retained_output_errors(retained))
    (retained / "extra.log").write_text("forbidden\n", encoding="ascii")
    check("extra retained file fails", bool(verifier.retained_output_errors(retained)))
    (retained / "extra.log").unlink()
    (retained / "nested").mkdir()
    check("nested retained entry fails", bool(verifier.retained_output_errors(retained)))
    (retained / "nested").rmdir()
    (retained / verifier.ATTESTATION_FILENAME).write_bytes(b"{}\r\n")
    check("CRLF retained attestation fails", bool(verifier.retained_output_errors(retained)))


def private_archive_test() -> None:
    configured = os.environ.get("XIVL_PRIVATE_CSV_ARCHIVE")
    if not configured:
        check("private archive optional in asset-free test", True)
        return
    result = run_verifier("--archive", configured)
    check("private archive passes when available", result.returncode == 0)


def workflow_tests() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    artifact_paths = [
        line.strip()
        for line in workflow.splitlines()
        if line.strip().startswith("path:")
    ]
    check("CSV corpus job is present", "csv-corpus:" in workflow)
    check(
        "CSV fetch pins the approved archive",
        f"commit: {verifier.PRIVATE_COMMIT}" in workflow
        and f"path: {verifier.PRIVATE_PATH}" in workflow
        and f"size: {verifier.ARCHIVE_SIZE}" in workflow
        and f"sha256: {verifier.ARCHIVE_SHA256}" in workflow,
    )
    check(
        "CSV corpus stays in disposable storage",
        'hydrated="${private_root}/csv"' in workflow
        and 'XIVL_CSV_DIR="${hydrated}"' in workflow
        and "path: _retail-staging/retail-evidence-attestation.json" in workflow,
    )
    check(
        "CSV workflow retains no private archive or hydrated files",
        "RETAIL_INPUTS_" + "REPOSITORY" not in workflow
        and "upload-artifact" in workflow
        and all("runner.temp" not in line for line in artifact_paths),
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="retail-csv-corpus-test-") as raw:
        root = Path(raw)
        contract_tests(root)
        archive_logic_tests(root)
        output_tests(root)
    workflow_tests()
    private_archive_test()
    if FAILED:
        print("FAIL: " + "; ".join(FAILED))
        return 1
    print(f"PASS: {len(PASSED)} retail CSV corpus verification checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
