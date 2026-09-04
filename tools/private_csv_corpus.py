#!/usr/bin/env python3
"""Package, verify, and safely hydrate the private CSV corpus.

The CSV corpus is intentionally ignored by git. This tool gives maintainers
one reproducible ZIP representation without making the data part of the
repository's public surface. Archive members are the ASCII basenames from the
selected CSV root; the destination passed to ``hydrate`` is therefore the CSV
directory itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from _csv_root import default_csv_dir
except ModuleNotFoundError:  # pragma: no cover - package import path
    from ._csv_root import default_csv_dir

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV_DIR = default_csv_dir()
DEFAULT_MANIFEST = REPO_ROOT / "manifests" / "manifest.json"
DEFAULT_TABLES = REPO_ROOT / "manifests" / "tables.json"
CHUNK_SIZE = 1024 * 1024
FIXED_DATE = (1980, 1, 1, 0, 0, 0)


class CorpusValidationError(Exception):
    """A malformed corpus, manifest, archive, or hydration destination."""


# This name mirrors the archive verifier in xivl-captures and keeps callers
# from needing a repository-specific exception name.
ArchiveValidationError = CorpusValidationError


def _fail(message: str) -> None:
    raise CorpusValidationError(message)


def _is_reparse(path: Path) -> bool:
    """Return whether ``path`` is a link-like filesystem object."""
    try:
        return path.is_symlink() or os.path.isjunction(path)
    except OSError as exc:
        raise CorpusValidationError("filesystem entry cannot be inspected") from exc


def _regular_file(path: Path, label: str) -> os.stat_result:
    try:
        result = path.lstat()
    except OSError as exc:
        raise CorpusValidationError(f"{label} unreadable") from exc
    if _is_reparse(path) or not stat.S_ISREG(result.st_mode):
        _fail(f"{label} is not a regular file")
    return result


def _directory(path: Path, label: str) -> None:
    try:
        result = path.lstat()
    except OSError as exc:
        raise CorpusValidationError(f"{label} unavailable") from exc
    if _is_reparse(path) or not stat.S_ISDIR(result.st_mode):
        _fail(f"{label} is not a real directory")


def _read_json(path: Path, label: str) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                _fail(f"{label} has duplicate fields")
            result[key] = value
        return result

    try:
        raw = path.read_bytes()
        return json.loads(
            raw.decode("utf-8"), object_pairs_hook=reject_duplicates
        )
    except CorpusValidationError:
        raise
    except (OSError, UnicodeError, ValueError) as exc:
        raise CorpusValidationError(f"{label} unreadable") from exc


def _safe_member_name(name: str) -> None:
    """Require one safe ASCII filename, never a path supplied by an archive."""
    if not isinstance(name, str) or not name or "\x00" in name:
        _fail("archive member path invalid")
    try:
        name.encode("ascii")
    except UnicodeEncodeError as exc:
        raise CorpusValidationError("archive member path invalid") from exc
    if "\\" in name:
        _fail("archive member path invalid")
    path = PurePosixPath(name)
    if (
        path.is_absolute()
        or len(path.parts) != 1
        or path.as_posix() != name
        or path.parts[0] in {".", ".."}
        or ":" in path.parts[0]
        or not name.endswith(".csv")
    ):
        _fail("archive member path invalid")


def _manifest_identity(
    manifest_path: Path = DEFAULT_MANIFEST,
    tables_path: Path = DEFAULT_TABLES,
) -> tuple[dict[str, tuple[int, str]], int]:
    """Load and cross-check the two tracked corpus manifests."""
    manifest = _read_json(manifest_path, "manifest.json")
    tables = _read_json(tables_path, "tables.json")
    if not isinstance(manifest, dict) or not isinstance(tables, list):
        _fail("manifest shape invalid")

    table_count = manifest.get("tableCount")
    total_bytes = manifest.get("totalBytes")
    if (
        not isinstance(table_count, int)
        or isinstance(table_count, bool)
        or table_count < 0
        or not isinstance(total_bytes, int)
        or isinstance(total_bytes, bool)
        or total_bytes < 0
    ):
        _fail("manifest totals invalid")

    expected: dict[str, tuple[int, str]] = {}
    for row in tables:
        if not isinstance(row, dict):
            _fail("tables.json entry shape invalid")
        name = row.get("name")
        relative_path = row.get("relativePath")
        size = row.get("bytes")
        digest = row.get("sha256")
        if (
            not isinstance(name, str)
            or not isinstance(relative_path, str)
            or not isinstance(size, int)
            or isinstance(size, bool)
            or size < 0
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(char not in "0123456789abcdefABCDEF" for char in digest)
        ):
            _fail("tables.json entry invalid")
        _safe_member_name(name)
        if relative_path != f"csv/{name}":
            _fail("tables.json relativePath invalid")
        if name in expected:
            _fail("tables.json has duplicate entries")
        expected[name] = (size, digest.lower())

    if table_count != len(expected):
        _fail("manifest table count mismatch")
    if total_bytes != sum(size for size, _digest in expected.values()):
        _fail("manifest total bytes mismatch")
    return expected, total_bytes


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _tree_sha256(entries: list[dict[str, Any]]) -> str:
    """Hash the sorted filename, size, and content identity records."""
    digest = hashlib.sha256()
    for entry in entries:
        digest.update(entry["name"].encode("ascii"))
        digest.update(b"\0")
        digest.update(str(entry["bytes"]).encode("ascii"))
        digest.update(b"\0")
        digest.update(entry["sha256"].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _file_identity(path: Path, expected: tuple[int, str], label: str) -> None:
    expected_size, expected_digest = expected
    result = _regular_file(path, label)
    if result.st_size != expected_size:
        _fail(f"{label} size mismatch")
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
                digest.update(chunk)
    except OSError as exc:
        raise CorpusValidationError(f"{label} unreadable") from exc
    if digest.hexdigest() != expected_digest:
        _fail(f"{label} hash mismatch")


def _source_files(
    csv_dir: Path,
    expected: dict[str, tuple[int, str]],
) -> dict[str, Path]:
    """Return the exact allowlisted source files after a full directory scan."""
    _directory(csv_dir, "CSV source")
    found: dict[str, Path] = {}
    try:
        entries = sorted(csv_dir.iterdir(), key=lambda path: path.name)
    except OSError as exc:
        raise CorpusValidationError("CSV source unreadable") from exc
    for path in entries:
        name = path.name
        if name not in expected:
            _fail("CSV source has unexpected entry")
        _safe_member_name(name)
        if name in found:
            _fail("CSV source has duplicate entries")
        _regular_file(path, f"CSV source {name}")
        found[name] = path
    if set(found) != set(expected):
        _fail("CSV source is missing an expected entry")
    for name in sorted(found):
        _file_identity(found[name], expected[name], f"CSV source {name}")
    return found


def _new_zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(filename=name, date_time=FIXED_DATE)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.create_version = 20
    info.extract_version = 20
    info.flag_bits = 0
    info.volume = 0
    info.internal_attr = 0
    info.external_attr = 0o100644 << 16
    info.extra = b""
    info.comment = b""
    return info


def _output_path(path: Path) -> None:
    """Check an archive output without following a pre-existing link."""
    if not os.path.lexists(path):
        return
    _regular_file(path, "archive output")


def package_archive(
    output: Path,
    *,
    csv_dir: Path = DEFAULT_CSV_DIR,
    manifest_path: Path = DEFAULT_MANIFEST,
    tables_path: Path = DEFAULT_TABLES,
) -> dict[str, Any]:
    """Create a deterministic, stored ZIP of all manifest CSVs."""
    expected, total_bytes = _manifest_identity(manifest_path, tables_path)
    source = _source_files(csv_dir, expected)
    try:
        source_root = csv_dir.resolve(strict=True)
        resolved_output = output.resolve(strict=False)
    except OSError as exc:
        raise CorpusValidationError("archive output path unavailable") from exc
    if resolved_output == source_root or source_root in resolved_output.parents:
        _fail("archive output must be outside the CSV source")
    _output_path(output)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise CorpusValidationError("archive output directory unavailable") from exc

    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w+b",
            prefix=f".{output.name}.",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            with zipfile.ZipFile(
                temporary,
                mode="w",
                compression=zipfile.ZIP_STORED,
                allowZip64=True,
            ) as archive:
                archive.comment = b""
                for name in sorted(source):
                    data = source[name].read_bytes()
                    # Recheck after the source snapshot and before packaging.
                    if len(data) != expected[name][0] or _sha256_bytes(data) != expected[name][1]:
                        _fail(f"CSV source {name} changed during packaging")
                    archive.writestr(_new_zip_info(name), data)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, output)
        temporary_name = None
    except CorpusValidationError:
        raise
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        raise CorpusValidationError("archive packaging failed") from exc
    finally:
        if temporary_name is not None:
            try:
                Path(temporary_name).unlink()
            except OSError:
                pass

    shape = inspect_archive(output, manifest_path=manifest_path, tables_path=tables_path)
    if shape["totalBytes"] != total_bytes:
        _fail("packaged total bytes mismatch")
    return shape


def _regular_archive_member(info: zipfile.ZipInfo) -> None:
    if info.filename.endswith("/") or info.is_dir():
        _fail("archive directory member rejected")
    if info.flag_bits & 0x1:
        _fail("encrypted archive member rejected")
    mode = (info.external_attr >> 16) & 0xFFFF
    if mode and not stat.S_ISREG(mode):
        _fail("linked archive member rejected")
    if info.external_attr & 0x10:
        _fail("archive directory member rejected")
    if info.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
        _fail("archive compression method rejected")
    if info.file_size < 0 or info.compress_size < 0:
        _fail("archive member size invalid")


def _archive_file(path: Path) -> None:
    _regular_file(path, "archive")


def inspect_archive(
    archive_path: Path,
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    tables_path: Path = DEFAULT_TABLES,
) -> dict[str, Any]:
    """Read and verify every archive member without creating output files."""
    expected, total_bytes = _manifest_identity(manifest_path, tables_path)
    _archive_file(archive_path)
    seen: set[str] = set()
    actual: list[dict[str, Any]] = []
    actual_total = 0
    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            infos = archive.infolist()
            if len(infos) != len(expected):
                _fail("archive member count mismatch")
            for info in infos:
                _safe_member_name(info.filename)
                if info.filename not in expected:
                    _fail("archive has unexpected member")
                if info.filename in seen:
                    _fail("duplicate archive member rejected")
                seen.add(info.filename)
                _regular_archive_member(info)
                expected_size, expected_digest = expected[info.filename]
                if info.file_size != expected_size:
                    _fail("archive member size mismatch")
                digest = hashlib.sha256()
                read_size = 0
                try:
                    with archive.open(info, "r") as handle:
                        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
                            read_size += len(chunk)
                            digest.update(chunk)
                except (OSError, RuntimeError, NotImplementedError, EOFError) as exc:
                    raise CorpusValidationError("archive member unreadable") from exc
                if read_size != expected_size or digest.hexdigest() != expected_digest:
                    _fail("archive member identity mismatch")
                actual_total += read_size
                actual.append(
                    {
                        "name": info.filename,
                        "bytes": read_size,
                        "sha256": digest.hexdigest(),
                    }
                )
    except CorpusValidationError:
        raise
    except (OSError, RuntimeError, zipfile.BadZipFile, ValueError) as exc:
        raise CorpusValidationError("archive unreadable") from exc
    if seen != set(expected):
        _fail("archive member set mismatch")
    if actual_total != total_bytes:
        _fail("archive total bytes mismatch")
    actual.sort(key=lambda item: item["name"])
    return {
        "tableCount": len(actual),
        "totalBytes": actual_total,
        "treeSha256": _tree_sha256(actual),
        "tables": actual,
    }


def _destination_is_safe(path: Path) -> bool:
    """Return whether a safe hydration destination already exists."""
    if os.path.lexists(path):
        _directory(path, "hydration destination")
        try:
            if any(path.iterdir()):
                _fail("hydration destination is not empty")
        except OSError as exc:
            raise CorpusValidationError("hydration destination unreadable") from exc
        return True
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise CorpusValidationError("hydration destination parent unavailable") from exc
    _directory(path.parent, "hydration destination parent")
    return False


def _hydrated_files(
    destination: Path,
    expected: dict[str, tuple[int, str]],
) -> None:
    found: dict[str, Path] = {}
    try:
        entries = sorted(destination.iterdir(), key=lambda path: path.name)
    except OSError as exc:
        raise CorpusValidationError("hydration destination unreadable") from exc
    for path in entries:
        name = path.name
        if name not in expected:
            _fail("hydration produced an unexpected entry")
        _safe_member_name(name)
        if name in found:
            _fail("hydration produced duplicate entries")
        _regular_file(path, f"hydrated file {name}")
        found[name] = path
    if set(found) != set(expected):
        _fail("hydration is missing an expected entry")
    for name in sorted(found):
        _file_identity(found[name], expected[name], f"hydrated file {name}")


def hydrate_archive(
    archive_path: Path,
    destination: Path,
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    tables_path: Path = DEFAULT_TABLES,
) -> dict[str, Any]:
    """Validate an archive, then hydrate it into a new or empty directory."""
    expected, _total_bytes = _manifest_identity(manifest_path, tables_path)
    shape = inspect_archive(
        archive_path, manifest_path=manifest_path, tables_path=tables_path
    )
    destination_existed = _destination_is_safe(destination)
    staging: Path | None = None
    try:
        staging = Path(
            tempfile.mkdtemp(
                prefix=f".{destination.name}.",
                suffix=".tmp",
                dir=destination.parent,
            )
        )
        os.chmod(staging, 0o700)
        with zipfile.ZipFile(archive_path, "r") as archive:
            for info in archive.infolist():
                _safe_member_name(info.filename)
                target = staging / info.filename
                try:
                    with archive.open(info, "r") as source:
                        with target.open("xb") as sink:
                            shutil.copyfileobj(source, sink, CHUNK_SIZE)
                    os.chmod(target, 0o600)
                except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                    raise CorpusValidationError("archive hydration failed") from exc
        _hydrated_files(staging, expected)

        # Recheck after all writes. Publication renames the verified staging
        # directory; no archive member is ever written through the caller's
        # destination path.
        destination_now_exists = _destination_is_safe(destination)
        if destination_now_exists:
            destination.rmdir()
        os.replace(staging, destination)
        staging = None
    except CorpusValidationError:
        raise
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        raise CorpusValidationError("archive hydration failed") from exc
    finally:
        if staging is not None:
            shutil.rmtree(staging, ignore_errors=True)
        if destination_existed and not os.path.lexists(destination):
            try:
                destination.mkdir(mode=0o700)
            except OSError:
                pass
    return shape


# Short aliases make the read-only operations convenient for library callers.
package = package_archive
verify = inspect_archive
hydrate = hydrate_archive


def _path_option(parser: argparse.ArgumentParser, *flags: str, **kwargs: Any) -> None:
    parser.add_argument(*flags, type=Path, **kwargs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    package_parser = commands.add_parser("package", help="create the deterministic ZIP")
    _path_option(package_parser, "--output", "--archive", dest="output", required=True)
    _path_option(package_parser, "--csv-dir", default=default_csv_dir())
    _path_option(package_parser, "--manifest", default=DEFAULT_MANIFEST)
    _path_option(package_parser, "--tables", default=DEFAULT_TABLES)

    verify_parser = commands.add_parser("verify", help="read-only archive verification")
    verify_parser.add_argument("archive", type=Path, nargs="?")
    _path_option(verify_parser, "--archive", dest="archive_option")
    _path_option(verify_parser, "--manifest", default=DEFAULT_MANIFEST)
    _path_option(verify_parser, "--tables", default=DEFAULT_TABLES)

    hydrate_parser = commands.add_parser("hydrate", help="safely hydrate CSV files")
    hydrate_parser.add_argument("archive", type=Path, nargs="?")
    hydrate_parser.add_argument("destination", type=Path, nargs="?")
    _path_option(hydrate_parser, "--archive", dest="archive_option")
    _path_option(hydrate_parser, "--destination", "--output", dest="destination_option")
    _path_option(hydrate_parser, "--manifest", default=DEFAULT_MANIFEST)
    _path_option(hydrate_parser, "--tables", default=DEFAULT_TABLES)

    args = parser.parse_args(argv)
    if args.command == "verify":
        args.archive = args.archive or args.archive_option
        if args.archive is None:
            parser.error("verify requires an archive path")
    elif args.command == "hydrate":
        args.archive = args.archive or args.archive_option
        args.destination = args.destination or args.destination_option
        if args.archive is None or args.destination is None:
            parser.error("hydrate requires archive and destination paths")
    try:
        if args.command == "package":
            shape = package_archive(
                args.output,
                csv_dir=args.csv_dir,
                manifest_path=args.manifest,
                tables_path=args.tables,
            )
            print(
                f"PASS: packaged {shape['tableCount']} CSV files "
                f"({shape['totalBytes']} bytes)"
            )
        elif args.command == "verify":
            shape = inspect_archive(
                args.archive,
                manifest_path=args.manifest,
                tables_path=args.tables,
            )
            print(
                f"PASS: archive verified ({shape['tableCount']} members, "
                f"{shape['totalBytes']} bytes)"
            )
        else:
            shape = hydrate_archive(
                args.archive,
                args.destination,
                manifest_path=args.manifest,
                tables_path=args.tables,
            )
            print(
                f"PASS: hydrated {shape['tableCount']} CSV files "
                f"({shape['totalBytes']} bytes)"
            )
    except CorpusValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
