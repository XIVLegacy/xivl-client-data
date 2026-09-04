"""Shared CSV-root selection for corpus-consuming tools."""

from __future__ import annotations

import argparse
import os
import stat
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_CSV_DIR = REPO_ROOT / "csv"
CSV_DIR_ENV = "XIVL_CSV_DIR"
REPARSE_POINT_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class CsvRootError(ValueError):
    """A selected CSV root is unsafe to inspect."""


def default_csv_dir() -> Path:
    """Return the explicit environment override or the legacy repo cache."""
    configured = os.environ.get(CSV_DIR_ENV)
    return Path(configured) if configured else REPO_CSV_DIR


def _lstat(path: Path, label: str) -> os.stat_result:
    try:
        info = path.lstat()
    except OSError as exc:
        raise CsvRootError(f"{label} is unavailable: {path}") from exc

    try:
        is_reparse = (
            path.is_symlink()
            or getattr(os.path, "isjunction", lambda _path: False)(path)
            or bool(getattr(info, "st_file_attributes", 0) & REPARSE_POINT_ATTRIBUTE)
        )
    except OSError as exc:
        raise CsvRootError(f"{label} cannot be inspected: {path}") from exc
    if is_reparse:
        raise CsvRootError(
            f"{label} must not be a symlink, junction, or reparse point: {path}"
        )
    return info


def validate_csv_dir(path: Path) -> Path:
    """Validate a CSV root and its direct descendants without reading bytes."""
    root = Path(path)
    info = _lstat(root, "CSV root")
    if not stat.S_ISDIR(info.st_mode):
        raise CsvRootError(f"CSV root is not a directory: {root}")

    try:
        children = sorted(root.iterdir(), key=lambda child: child.name)
    except OSError as exc:
        raise CsvRootError(f"CSV root descendants are unavailable: {root}") from exc
    for child in children:
        info = _lstat(child, "CSV root descendant")
        if not stat.S_ISREG(info.st_mode):
            raise CsvRootError(
                f"CSV root descendant is not a regular file: {child}"
            )
    return root


def _csv_dir_argument(value: str) -> Path:
    try:
        return validate_csv_dir(Path(value))
    except CsvRootError as exc:
        # Metadata-only operations such as csv_to_sql.py --list do not need a
        # hydrated corpus. Defer a missing root to the command that reads it,
        # while still rejecting every existing unsafe path before byte access.
        if not os.path.lexists(value):
            return Path(value)
        raise argparse.ArgumentTypeError(str(exc)) from exc


def add_csv_dir_argument(parser: argparse.ArgumentParser) -> None:
    """Add the common CSV-root option, honoring the environment by default."""
    parser.add_argument(
        "--csv-dir",
        type=_csv_dir_argument,
        default=str(default_csv_dir()),
        help=(
            "CSV corpus directory (default: XIVL_CSV_DIR or the repo-local "
            "csv/ compatibility cache)"
        ),
    )
