#!/usr/bin/env python3
"""Mutation tests for the static-actor retail-input contract."""

from __future__ import annotations

import copy
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _schema_check  # noqa: E402
import extract_staticactor_san as extractor  # noqa: E402
import verify_retail_staticactor as verifier  # noqa: E402


REPO = Path(__file__).resolve().parents[1]
CHECKS_WORKFLOW = REPO / ".github" / "workflows" / "checks.yml"
WORKFLOW = REPO / ".github" / "workflows" / "retail-checks.yml"
PRODUCT = REPO / "manifests" / "staticactor_class_paths.json"
CHECK = REPO / "manifests" / "retail_staticactor_check.json"
RETAIL_INPUTS = REPO / "manifests" / "retail_inputs.json"
SCHEMA = REPO / "schemas" / "retail-evidence-attestation.schema.json"
VERIFY = REPO / "tools" / "verify_retail_staticactor.py"
PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, condition: bool) -> None:
    (PASSED if condition else FAILED).append(name)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, document: object) -> Path:
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="",
    )
    return path


def _fails(
    directory: Path,
    product: bytes | None = None,
    expected: dict | None = None,
    retail_inputs: dict | None = None,
) -> bool:
    product_path = directory / "product.json"
    product_path.write_bytes(product if product is not None else PRODUCT.read_bytes())
    check_path = _write_json(directory / "check.json", expected or _load(CHECK))
    retail_path = _write_json(
        directory / "retail.json", retail_inputs or _load(RETAIL_INPUTS)
    )
    return bool(verifier.verify(product_path, check_path, retail_path))


def _run_cli(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFY), "--input", str(path)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def _san(records: list[tuple[int, bytes]], trailing: bytes = b"") -> bytes:
    decoded_tail = b"\x00" * 5 + struct.pack(">I", len(records))
    decoded_tail += b"".join(
        struct.pack(">I", actor_id) + class_path + b"\x00"
        for actor_id, class_path in records
    )
    decoded_tail += trailing
    return b"sane" + bytes(byte ^ extractor.XOR_KEY for byte in decoded_tail)


def main() -> int:
    parsed = extractor.parse_san(_san([(0xF0000001, b"/Command/Test")]))
    check(
        "SAN actor ids decode as unsigned u32",
        parsed == [{"id": 0xF0000001, "classPath": "/Command/Test"}],
    )
    try:
        extractor.parse_san(_san([(12002, b"/Command/Test")], trailing=b"\x01"))
    except ValueError as exc:
        trailing_rejected = "trailing bytes" in str(exc)
    else:
        trailing_rejected = False
    check("SAN trailing bytes fail closed", trailing_rejected)
    try:
        extractor.parse_san(b"sane")
    except ValueError as exc:
        short_header_rejected = "truncated san header" in str(exc)
    else:
        short_header_rejected = False
    check("SAN truncated header fails closed", short_header_rejected)

    checks_workflow = CHECKS_WORKFLOW.read_text(encoding="utf-8")
    check(
        "whitespace check uses event revision",
        "git diff --check" in checks_workflow
        and 'case "${GITHUB_EVENT_NAME}" in' in checks_workflow
        and "github.event.pull_request.base.sha" in checks_workflow
        and "github.event.before" in checks_workflow,
    )
    workflow = WORKFLOW.read_text(encoding="utf-8")
    check("retail preflight has a timeout", "timeout-minutes: 10" in workflow)
    check(
        "hosted Python patch is pinned",
        workflow.count('python-version: "3.12.14"') == 2,
    )
    check(
        "remote-main lookup is bounded",
        "timeout 30s git ls-remote origin refs/heads/main" in workflow,
    )
    shared_actions = [
        line.strip().removeprefix("uses: ")
        for line in workflow.splitlines()
        if line.strip().startswith(
            "uses: XIVLegacy/xivl-tools/.github/actions/"
        )
    ]
    shared_revisions = {action.rsplit("@", 1)[-1] for action in shared_actions}
    shared_revision = next(iter(shared_revisions), "")
    check(
        "shared retail actions use one immutable pin",
        len(shared_actions) == 2
        and len(shared_revisions) == 1
        and len(shared_revision) == 40
        and all(char in "0123456789abcdef" for char in shared_revision)
        and sum("/fetch-retail-input@" in action for action in shared_actions) == 1
        and sum(
            "/finalize-retail-attestation@" in action for action in shared_actions
        ) == 1,
    )
    check(
        "fetch passes the approved SAN identity",
        "commit: aeb52f6dbde95a793ee6d52be28de9f28a885b15" in workflow
        and "path: client-data/ffxiv-1.23b/client/script/rq9q1797qvs.san" in workflow
        and "size: 108911" in workflow
        and "sha256: bb7306461b1728493242016a16d9dd5257d7512c60e423b017de5ec7aced3d14" in workflow
        and "output-path: ${{ runner.temp }}/retail-evidence-private/game/client/script/rq9q1797qvs.san" in workflow,
    )
    check(
        "retail fetch selects only the SAN",
        all(name not in workflow for name in ("ffxivgame.exe", ".le.lpb", ".zip"))
        and "RETAIL_INPUTS_" + "REPOSITORY" not in workflow
        and "steps.fetch.outcome" in workflow
        and "id: finalize" in workflow
        and "steps.finalize.outcome" in workflow
        and "hashFiles" not in workflow,
    )
    python_commands = [
        line for line in workflow.splitlines()
        if "python" in line
        and "python-version" not in line
        and "setup-python" not in line
    ]
    check(
        "every hosted Python command is bounded",
        bool(python_commands) and all("timeout " in line for line in python_commands),
    )
    baseline = _load(PRODUCT)
    with tempfile.TemporaryDirectory(prefix="retail-staticactor-test-") as raw:
        directory = Path(raw)
        check("canonical product passes", not _fails(directory))
        check(
            "canonical product has 2,812 records",
            baseline.get("recordCount") == 2812
            and len(baseline.get("records", [])) == 2812,
        )

        mutated = copy.deepcopy(baseline)
        mutated["records"][0]["classPath"] = "/Mutation/Not/Approved"
        check(
            "mutated expected record fails",
            _fails(directory, product=json.dumps(mutated, ensure_ascii=False, indent=2).encode() + b"\n"),
        )

        original = PRODUCT.read_bytes()
        changed = bytearray(original)
        changed[-2] ^= 1
        check("mutated output byte fails", _fails(directory, product=bytes(changed)))

        expected = _load(CHECK)
        expected["expectedProduct"]["sha256"] = "0" * 64
        check("expected product hash drift fails", _fails(directory, expected=expected))

        retail = _load(RETAIL_INPUTS)
        retail["inputs"][0]["allowedChecks"].append("unapproved-check")
        check("retail grant expansion fails", _fails(directory, retail_inputs=retail))

        schema = _schema_check.load_schema(SCHEMA)
        attestation = verifier.build_attestation("pass")
        check("passing attestation satisfies schema", not _schema_check.validate(attestation, schema))
        try:
            _schema_check.validate("value", {"type": "string", "minimum": 1})
        except _schema_check.SchemaError:
            unsupported_keyword_fails_closed = True
        else:
            unsupported_keyword_fails_closed = False
        check("unsupported schema keyword fails closed", unsupported_keyword_fails_closed)
        try:
            _schema_check.validate("value", {"type": None})
        except _schema_check.SchemaError:
            invalid_type_fails_closed = True
        else:
            invalid_type_fails_closed = False
        check("invalid schema type fails closed", invalid_type_fails_closed)
        zero_commit = copy.deepcopy(attestation)
        zero_commit["publicRepositoryCommit"] = "0" * 40
        check(
            "all-zero public commit fails schema",
            bool(_schema_check.validate(zero_commit, schema)),
        )
        attestation["observations"] = []
        check("unexpected attestation field fails", bool(_schema_check.validate(attestation, schema)))

        failed_path = directory / "failed.json"
        failed = copy.deepcopy(baseline)
        failed["records"][0]["id"] = -1
        _write_json(failed_path, failed)
        result = _run_cli(failed_path)
        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError:
            output = {}
        check("failure invocation exits nonzero", result.returncode != 0)
        check(
            "failure output is sanitized",
            set(output)
            == {
                "schemaVersion",
                "publicRepositoryCommit",
                "approvedInputSha256",
                "toolVersions",
                "check",
                "result",
            }
            and output.get("result", {}).get("status") == "fail"
            and "client-data/" not in result.stdout
            and "rq9q1797qvs" not in result.stdout,
        )

        first = _run_cli(PRODUCT)
        second = _run_cli(PRODUCT)
        check(
            "repeated passing output is byte-identical",
            first.returncode == second.returncode == 0
            and first.stdout.encode() == second.stdout.encode(),
        )
        raw = subprocess.run(
            [sys.executable, str(VERIFY), "--input", str(PRODUCT)],
            cwd=REPO,
            capture_output=True,
            text=False,
            check=False,
            timeout=30,
        )
        check(
            "passing output has a literal LF terminator",
            raw.returncode == 0
            and raw.stdout.endswith(b"\n")
            and b"\r" not in raw.stdout,
        )

        retained = directory / "retained"
        retained.mkdir()
        _write_json(retained / "retail-evidence-attestation.json", verifier.build_attestation("pass"))
        check("retained pass attestation validates", not verifier._validate_retained_output(retained))
        (retained / "extra.json").write_text("{}\n", encoding="ascii")
        check("retained-file violation fails", bool(verifier._validate_retained_output(retained)))

    if FAILED:
        print("FAIL: " + "; ".join(FAILED))
        return 1
    print(f"PASS: {len(PASSED)} static-actor verification checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
