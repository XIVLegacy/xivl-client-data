#!/usr/bin/env python3
"""Validate schemas, checksums, referential integrity, and the docs index."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = REPO_ROOT / "schemas"
MANIFESTS = REPO_ROOT / "manifests"
CSV_DIR = REPO_ROOT / "csv"
DOCS_DIR = REPO_ROOT / "docs"
CORPUS_ABSENT = os.environ.get("XIVL_CORPUS_ABSENT") == "1"
PERMITTED_TOP_LEVEL_GROUPS = {
    "root",
    ".github",
    "data",
    "derived",
    "docs",
    "manifests",
    "schemas",
    "tools",
}
REQUIRED_AGENT_TOOLING_IGNORE_LINES = {
    "# Agent / AI tooling",
    ".claude/",
    ".agents/",
    "AGENTS.md",
    "CLAUDE.md",
    "docs/ai_agents/local/",
}
ABSOLUTE_MAINTAINER_PATH_RE = re.compile(
    rb"(?:[A-Za-z]:\\" + rb"Users\\|/" + rb"Users/|/" + rb"home/)",
    re.IGNORECASE,
)

try:
    import jsonschema  # noqa: PLC0415

    _HAVE_JSONSCHEMA = True
except ImportError:
    _HAVE_JSONSCHEMA = False

errors: list[str] = []


def _tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    return sorted(path for path in result.stdout.decode("utf-8").split("\0") if path)


def validate_repository_boundary() -> int:
    """Enforce the tracked public surface and reject private or binary inputs."""
    paths = _tracked_paths()
    for path in paths:
        group = path.split("/", 1)[0] if "/" in path else "root"
        if group not in PERMITTED_TOP_LEVEL_GROUPS:
            errors.append(f"unexpected top-level tracked group: {path}")

    for path in paths:
        if path.lower().startswith("csv/"):
            errors.append(f"forbidden tracked CSV corpus path: {path}")
        data = (REPO_ROOT / path).read_bytes()
        if data[:2] == b"MZ":
            errors.append(f"PE MZ magic in tracked file: {path}")
        if ABSOLUTE_MAINTAINER_PATH_RE.search(data):
            errors.append(f"absolute maintainer path in tracked file: {path}")

    ignore_text = (
        (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        .replace("\r\n", "\n")
    )
    ignore_lines = set(ignore_text.split("\n"))
    for required in sorted(REQUIRED_AGENT_TOOLING_IGNORE_LINES):
        if required not in ignore_lines:
            errors.append(f".gitignore missing required line: {required}")
    return len(paths)


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_json_tree() -> int:
    """Parse every repository JSON file outside ignored build metadata."""
    count = 0
    for root, directories, filenames in os.walk(REPO_ROOT, followlinks=False):
        root_path = Path(root)
        directories[:] = sorted(
            name
            for name in directories
            if name != ".git"
            and not (
                CORPUS_ABSENT and root_path == REPO_ROOT and name == CSV_DIR.name
            )
            and not os.path.isjunction(root_path / name)
        )
        for filename in sorted(filenames):
            if not filename.endswith(".json"):
                continue
            path = root_path / filename
            relative = path.relative_to(REPO_ROOT)
            count += 1
            try:
                _load(path)
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                errors.append(f"{relative.as_posix()}: invalid JSON ({exc})")
    return count


def validate_csv_contract() -> None:
    """Check corpus metadata and, when present, the CSV layout and totals."""
    if not CORPUS_ABSENT and CSV_DIR.is_dir():
        subdirectories = sorted(
            path.relative_to(REPO_ROOT).as_posix()
            for path in CSV_DIR.rglob("*")
            if path.is_dir()
        )
        if subdirectories:
            errors.append(
                "canonical CSVs must live directly under csv; found "
                f"subdirectories: {', '.join(subdirectories)}"
            )

    manifest_path = MANIFESTS / "manifest.json"
    tables_path = MANIFESTS / "tables.json"
    if not (manifest_path.is_file() and tables_path.is_file()):
        return

    manifest = _load(manifest_path)
    tables = _load(tables_path)
    if not isinstance(manifest, dict) or not isinstance(tables, list):
        return  # schema validation reports the malformed top-level shape

    if manifest.get("sourceType") != "decoded_csv":
        errors.append("manifest.sourceType must stay decoded_csv")
    if CORPUS_ABSENT:
        return

    csv_files = sorted(CSV_DIR.glob("*.csv"))
    csv_count = len(csv_files)
    total_bytes = sum(path.stat().st_size for path in csv_files)

    if len(tables) != csv_count:
        errors.append(
            f"tables.json has {len(tables)} entries != {csv_count} CSV files on disk"
        )
    if manifest.get("tableCount") != csv_count:
        errors.append(
            f"manifest.tableCount {manifest.get('tableCount')} != "
            f"{csv_count} CSV files on disk"
        )
    if manifest.get("totalBytes") != total_bytes:
        errors.append(
            f"manifest.totalBytes {manifest.get('totalBytes')} != "
            f"{total_bytes} CSV bytes on disk"
        )


def _sha256_hexdigest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validator_for(schema_path: Path):
    return jsonschema.Draft202012Validator(_load(schema_path))


def _check(instance, validator, label: str) -> None:
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        errors.append(f"{label}: schema violation at {loc}: {err.message}")


def validate_schemas() -> None:
    pairs = [
        (MANIFESTS / "manifest.json", "manifest.schema.json", "manifest.json"),
        (MANIFESTS / "tables.json", "tables.schema.json", "tables.json"),
        (
            MANIFESTS / "zone_internal_names.json",
            "zone_internal_names.schema.json",
            "zone_internal_names.json",
        ),
        (
            MANIFESTS / "staticactor_class_paths.json",
            "staticactor_class_paths.schema.json",
            "staticactor_class_paths.json",
        ),
        (
            MANIFESTS / "icons_1_23b.json",
            "icons_1_23b.schema.json",
            "icons_1_23b.json",
        ),
        (
            MANIFESTS / "shop_catalogs.json",
            "shop_catalogs.schema.json",
            "shop_catalogs.json",
        ),
        (
            MANIFESTS / "retail_inputs.json",
            "retail_inputs.schema.json",
            "retail_inputs.json",
        ),
        (
            MANIFESTS / "retail_staticactor_check.json",
            "retail_staticactor_check.schema.json",
            "retail_staticactor_check.json",
        ),
    ]
    for inst_path, schema_name, label in pairs:
        schema_path = SCHEMAS / schema_name
        if not inst_path.is_file():
            errors.append(f"{label}: file missing")
            continue
        if not schema_path.is_file():
            errors.append(f"{label}: schema {schema_name} missing")
            continue
        _check(_load(inst_path), _validator_for(schema_path), label)


def _check_row_counts(name: str, data: bytes, entry: dict) -> None:
    """Recompute a table's lineCount and dataRowCount from disk bytes."""
    if "lineCount" not in entry or "dataRowCount" not in entry:
        return  # schema validation already reported the missing key
    # Match build-manifest.ps1's CR/LF/CRLF line-terminator convention.
    folded = data.replace(b"\r\n", b"\n")
    line_count = folded.count(b"\n") + folded.count(b"\r")
    if data and data[-1] not in (10, 13):
        line_count += 1
    if entry["lineCount"] != line_count:
        errors.append(
            f"{name}: lineCount {entry['lineCount']} != {line_count} lines on disk"
        )
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{name}: not valid UTF-8 ({exc})")
        return
    try:
        records = sum(1 for _ in csv.reader(io.StringIO(text, newline="")))
    except csv.Error as exc:
        errors.append(f"{name}: unparseable as CSV ({exc})")
        return
    expected = max(0, records - 2)  # drop the label and type header rows
    if entry["dataRowCount"] != expected:
        errors.append(
            f"{name}: dataRowCount {entry['dataRowCount']} != {expected} "
            f"({records} CSV records minus the two header rows)"
        )


def validate_checksums() -> None:
    tables_path = MANIFESTS / "tables.json"
    if not tables_path.is_file():
        errors.append("tables.json: file missing")
        return
    tables = _load(tables_path)
    by_name: dict[str, dict] = {}
    for position, entry in enumerate(tables):
        # Report malformed entries so one schema error cannot abort the gate.
        if not isinstance(entry, dict) or "name" not in entry:
            errors.append(f"tables.json: entry {position} has no 'name' key")
            continue
        name = entry["name"]
        by_name[name] = entry
        if CORPUS_ABSENT:
            continue
        csv_path = CSV_DIR / name
        if not csv_path.is_file():
            errors.append(f"tables.json: {name} listed but missing under csv/")
            continue
        data = csv_path.read_bytes()
        if "bytes" not in entry or "sha256" not in entry:
            errors.append(f"tables.json: {name} is missing a bytes/sha256 key")
        else:
            if len(data) != entry["bytes"]:
                errors.append(f"{name}: bytes {len(data)} != manifest {entry['bytes']}")
            digest = hashlib.sha256(data).hexdigest()
            if digest.lower() != entry["sha256"].lower():
                errors.append(
                    f"{name}: sha256 mismatch (file {digest} != manifest {entry['sha256']})"
                )
        _check_row_counts(name, data, entry)

    if not CORPUS_ABSENT:
        for csv_path in sorted(CSV_DIR.glob("*.csv")):
            if csv_path.name not in by_name:
                errors.append(
                    f"csv/{csv_path.name}: present on disk but absent from tables.json"
                )

    manifest_path = MANIFESTS / "manifest.json"
    if manifest_path.is_file():
        manifest = _load(manifest_path)
        if manifest.get("tableCount") != len(tables):
            errors.append(
                f"manifest.tableCount {manifest.get('tableCount')} != "
                f"{len(tables)} table entries"
            )
        total = sum(e.get("bytes", 0) for e in tables if isinstance(e, dict))
        if manifest.get("totalBytes") != total:
            errors.append(
                f"manifest.totalBytes {manifest.get('totalBytes')} != {total}"
            )


def validate_sheet_inventory() -> None:
    """Validate inventory rows and, when present, correspondence with csv/."""
    inv_path = MANIFESTS / "sheet_inventory.csv"
    if not inv_path.is_file():
        errors.append("sheet_inventory.csv: file missing")
        return
    with inv_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        expected_header = ["name", "resource_id", "resource_id_hex", "source"]
        if reader.fieldnames != expected_header:
            errors.append(
                f"sheet_inventory.csv: header {reader.fieldnames} != {expected_header}"
            )
            return
        rows = list(reader)

    schema_path = SCHEMAS / "sheet_inventory.schema.json"
    if not schema_path.is_file():
        errors.append(
            "sheet_inventory.csv: schema sheet_inventory.schema.json missing"
        )
    else:
        _check(rows, _validator_for(schema_path), "sheet_inventory.csv")

    for row in rows:
        try:
            if int(row["resource_id_hex"], 16) != int(row["resource_id"]):
                errors.append(
                    f"sheet_inventory.csv: {row['name']}: resource_id_hex "
                    f"{row['resource_id_hex']} != resource_id {row['resource_id']}"
                )
        except (TypeError, ValueError):
            errors.append(
                f"sheet_inventory.csv: {row['name']}: unparseable resource id "
                f"({row['resource_id']!r} / {row['resource_id_hex']!r})"
            )

    names = [row["name"] for row in rows]
    if len(set(names)) != len(names):
        errors.append("sheet_inventory.csv: duplicate sheet names")
    if names != sorted(names):
        errors.append("sheet_inventory.csv: rows are not sorted by name")

    if CORPUS_ABSENT:
        return

    expected_files = {name.replace("/", "_") + ".csv" for name in names}
    on_disk = {p.name for p in CSV_DIR.glob("*.csv")}
    for missing in sorted(expected_files - on_disk):
        errors.append(f"sheet_inventory.csv: {missing} expected under csv/ but missing")
    for extra in sorted(on_disk - expected_files):
        if (
            extra.endswith("(2).csv")
            and extra[: -len("(2).csv")] + ".csv" in expected_files
        ):
            continue
        errors.append(
            f"csv/{extra}: present on disk but not derivable from any "
            f"sheet_inventory.csv row"
        )


def validate_derived_counts() -> None:
    """Validate generator-reported counts against their payloads."""
    actors_path = MANIFESTS / "staticactor_class_paths.json"
    if actors_path.is_file():
        actors = _load(actors_path)
        records = actors.get("records", [])
        if actors.get("recordCount") != len(records):
            errors.append(
                f"staticactor_class_paths.json: recordCount "
                f"{actors.get('recordCount')} != {len(records)} records"
            )
        ids = [r["id"] for r in records]
        if len(set(ids)) != len(ids):
            errors.append("staticactor_class_paths.json: duplicate record ids")

    shop_builder = REPO_ROOT / "tools" / "build_shop_catalogs.py"
    if shop_builder.is_file() and not CORPUS_ABSENT:
        result = subprocess.run(
            [sys.executable, str(shop_builder), "--check"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            detail = (result.stdout + result.stderr).strip()
            errors.append(f"shop catalog artifacts are not reproducible: {detail}")


def validate_zone_catalog() -> None:
    """Validate cross-references in the zone-name catalog."""
    catalog_path = MANIFESTS / "zone_internal_names.json"
    if not catalog_path.is_file():
        return
    catalog = _load(catalog_path)
    families = set(catalog.get("families", {}))

    for blob in catalog.get("blobs", []):
        if blob["family"] not in families:
            errors.append(
                f"zone_internal_names.json: blob {blob['resourceIdHex']} names "
                f"family {blob['family']!r} with no entry in families"
            )
        primary = blob.get("primaryName")
        if primary is not None and primary not in blob["zoneNames"]:
            errors.append(
                f"zone_internal_names.json: blob {blob['resourceIdHex']}: "
                f"primaryName {primary!r} is not among its zoneNames"
            )

    layouts: dict[int, dict] = {}
    for layout in catalog.get("layouts", []):
        layout_id = layout["layoutId"]
        if layout_id in layouts:
            errors.append(f"zone_internal_names.json: duplicate layoutId {layout_id}")
        layouts[layout_id] = layout
        if layout["family"] not in families:
            errors.append(
                f"zone_internal_names.json: layout {layout_id} names family "
                f"{layout['family']!r} with no entry in families"
            )

    for binding in catalog.get("zoneBindings", []):
        layout = layouts.get(binding["layoutId"])
        if layout is None:
            errors.append(
                f"zone_internal_names.json: zone {binding['zoneId']} binds "
                f"layoutId {binding['layoutId']} with no entry in layouts"
            )
            continue
        if binding["placeNameId"] != layout["placeNameId"]:
            errors.append(
                f"zone_internal_names.json: zone {binding['zoneId']}: "
                f"placeNameId {binding['placeNameId']} != layout "
                f"{layout['layoutId']} placeNameId {layout['placeNameId']}"
            )
        if binding["zoneName"] != layout["slotName"]:
            errors.append(
                f"zone_internal_names.json: zone {binding['zoneId']}: zoneName "
                f"{binding['zoneName']!r} != layout {layout['layoutId']} "
                f"slotName {layout['slotName']!r}"
            )


def validate_icon_corpus() -> None:
    """Re-verify the icon manifest against described files and counts."""
    manifest_path = MANIFESTS / "icons_1_23b.json"
    if not manifest_path.is_file():
        errors.append("icons_1_23b.json: file missing")
        return
    manifest = _load(manifest_path)
    label = "icons_1_23b.json"

    def _verify(entry: dict, required: bool) -> None:
        path = REPO_ROOT / entry["path"]
        if not path.is_file():
            if required:
                errors.append(f"{label}: {entry['path']} listed but missing on disk")
            return
        size = path.stat().st_size
        if size != entry["bytes"]:
            errors.append(
                f"{label}: {entry['path']} bytes {size} != manifest {entry['bytes']}"
            )
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                digest.update(chunk)
        if digest.hexdigest() != entry["sha256"]:
            errors.append(
                f"{label}: {entry['path']} sha256 mismatch "
                f"(file {digest.hexdigest()} != manifest {entry['sha256']})"
            )

    archive = manifest.get("archive")
    if isinstance(archive, dict) and {"path", "bytes", "sha256"} <= archive.keys():
        _verify(archive, required=False)
    for entry in manifest.get("derivedArtifacts", []):
        if isinstance(entry, dict) and {"path", "bytes", "sha256"} <= entry.keys():
            _verify(entry, required=True)

    inventory = REPO_ROOT / "derived" / "icons-1.23b" / "file-inventory.csv"
    if not inventory.is_file():
        errors.append(f"{label}: derived/icons-1.23b/file-inventory.csv missing")
        return
    with inventory.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    placeholders = sum(1 for row in rows if row.get("placeholder") == "1")
    for key, actual in (
        ("fileCount", len(rows)),
        ("placeholderCount", placeholders),
        ("realIconCount", len(rows) - placeholders),
    ):
        if manifest.get(key) != actual:
            errors.append(
                f"{label}: {key} {manifest.get(key)} != {actual} from file-inventory.csv"
            )

    by_folder: dict[str, list[dict]] = {}
    for row in rows:
        by_folder.setdefault(row.get("folder", ""), []).append(row)
    for band in manifest.get("bands", []):
        folder = str(band.get("folder"))
        band_rows = by_folder.get(folder, [])
        if len(band_rows) != band.get("files"):
            errors.append(
                f"{label}: band {folder} files {band.get('files')} != "
                f"{len(band_rows)} inventory rows"
            )
        band_placeholders = sum(1 for row in band_rows if row.get("placeholder") == "1")
        if band_placeholders != band.get("placeholderFiles"):
            errors.append(
                f"{label}: band {folder} placeholderFiles "
                f"{band.get('placeholderFiles')} != {band_placeholders} on disk"
            )
        if not band_rows:
            continue
        try:
            icon_ids = [int(row["icon_id"]) for row in band_rows]
            pixel_sizes = sorted({int(row["width"]) for row in band_rows})
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"{label}: band {folder} has malformed inventory data ({exc})")
            continue
        for key, actual in (
            ("realIcons", len(band_rows) - band_placeholders),
            ("idMin", min(icon_ids)),
            ("idMax", max(icon_ids)),
            ("pixelSizes", pixel_sizes),
        ):
            if band.get(key) != actual:
                errors.append(
                    f"{label}: band {folder} {key} {band.get(key)} != "
                    f"{actual} from file-inventory.csv"
                )
    unlisted = sorted(
        set(by_folder) - {str(b.get("folder")) for b in manifest.get("bands", [])}
    )
    for folder in unlisted:
        errors.append(f"{label}: inventory folder {folder} has no band entry")


def validate_vendor_provenance() -> None:
    """Verify vendored inputs under docs/ai_agents/verification.md."""
    vendor_dir = REPO_ROOT / "data" / "vendor"
    if not vendor_dir.is_dir():
        return
    vendor_groups = sorted(path for path in vendor_dir.iterdir() if path.is_dir())
    for group_dir in vendor_groups:
        prov_path = group_dir / "PROVENANCE.json"
        if not prov_path.is_file():
            label = group_dir.relative_to(REPO_ROOT).as_posix()
            errors.append(f"{label}: vendor directory has no PROVENANCE.json")
            continue
        label = prov_path.relative_to(REPO_ROOT).as_posix()
        try:
            manifest = _load(prov_path)
        except (OSError, ValueError) as exc:
            errors.append(f"{label}: failed to parse ({exc})")
            continue
        entries = manifest.get("files")
        if not isinstance(entries, list) or not entries:
            errors.append(f"{label}: no files[] entries to verify")
            continue
        listed_files: set[str] = set()
        for entry in entries:
            name = entry.get("file") if isinstance(entry, dict) else None
            expected = entry.get("sha256") if isinstance(entry, dict) else None
            if not name or not expected:
                errors.append(f"{label}: an entry is missing its file/sha256 key")
                continue
            for field in ("sourceLicense", "sourceLicenseUrl"):
                if not isinstance(entry.get(field), str) or not entry[field]:
                    errors.append(f"{label}: {name} is missing {field}")
            listed_files.add(Path(name).as_posix())
            target = prov_path.parent / name
            if not target.is_file():
                errors.append(f"{label}: {name} listed but missing on disk")
                continue
            digest = _sha256_hexdigest(target)
            if digest.lower() != expected.lower():
                errors.append(
                    f"{label}: {name} sha256 mismatch "
                    f"(file {digest} != manifest {expected})"
                )
        actual_files = {
            path.relative_to(group_dir).as_posix()
            for path in group_dir.rglob("*")
            if path.is_file() and path != prov_path
        }
        for name in sorted(actual_files - listed_files):
            errors.append(f"{label}: {name} exists but has no files[] entry")


def validate_retail_staticactor_contract() -> None:
    """Check the asset-free static-actor retail contract and product hash."""
    try:
        import verify_retail_staticactor as verifier

        contract_errors = verifier.verify()
    except (ImportError, OSError, TypeError, ValueError):
        errors.append("retail static-actor verifier could not run")
        return
    for detail in contract_errors:
        errors.append(f"retail static-actor contract: {detail}")


def validate_docs_index() -> None:
    """Ensure each tracked docs shelf indexes its sibling Markdown files."""
    for docs_dir in (DOCS_DIR, DOCS_DIR / "ai_agents"):
        readme = docs_dir / "README.md"
        label = readme.relative_to(REPO_ROOT).as_posix()
        if not readme.is_file():
            errors.append(f"{label}: file missing")
            continue
        linked: set[str] = set()
        for target in re.findall(r"\]\(([^)]+)\)", readme.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0]  # drop any '#anchor'
            if "/" in target or not target.endswith(".md") or target == "README.md":
                continue  # cross-dir link, non-md, or self-reference
            linked.add(target)
        on_disk = {p.name for p in docs_dir.glob("*.md")} - {"README.md"}
        directory = docs_dir.relative_to(REPO_ROOT).as_posix()
        for missing in sorted(linked - on_disk):
            errors.append(
                f"{label}: indexes {missing} but no such file under {directory}/"
            )
        for orphan in sorted(on_disk - linked):
            errors.append(f"{directory}/{orphan}: present but unindexed in {label}")


def main() -> int:
    tracked_count = validate_repository_boundary()
    json_count = validate_json_tree()
    if errors:
        print(f"corpus validation FAILED ({len(errors)} problem(s)):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    if not _HAVE_JSONSCHEMA:
        print(
            "error: jsonschema not installed; schema validation is a required "
            "part of this gate and cannot be skipped. pip install jsonschema",
            file=sys.stderr,
        )
        return 1
    validate_csv_contract()
    validate_schemas()
    validate_checksums()
    validate_sheet_inventory()
    validate_derived_counts()
    validate_zone_catalog()
    validate_icon_corpus()
    validate_vendor_provenance()
    validate_retail_staticactor_contract()
    validate_docs_index()
    if errors:
        print(f"corpus validation FAILED ({len(errors)} problem(s)):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    corpus_check = "manifest metadata" if CORPUS_ABSENT else "checksums"
    print(
        f"repository boundary + corpus validation OK ({tracked_count} tracked files, "
        f"{json_count} JSON files, schemas, {corpus_check}, "
        "sheet-inventory "
        "referential integrity, derived counts, zone-catalog cross-references, "
        "icon corpus, vendor provenance + docs-index sync)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
