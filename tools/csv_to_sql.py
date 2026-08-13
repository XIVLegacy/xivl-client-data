"""Generate repo-local CSV-to-SQL seed fragments for downstream consumers."""

from __future__ import annotations

import argparse
import importlib
import pkgutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV_DIR = REPO_ROOT / "csv"
DEFAULT_OUT_DIR = REPO_ROOT / "build" / "sql"

# Add tools/ to sys.path so mappings resolve from any working directory.
_TOOLS_DIR = str(REPO_ROOT / "tools")
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)


def discover_mappings() -> list[str]:
    import mappings  # noqa: PLC0415

    names: list[str] = []
    for module_info in pkgutil.iter_modules(mappings.__path__):
        if module_info.name.startswith("_"):
            continue
        names.append(module_info.name)
    return sorted(names)


def run_mapping(name: str, csv_dir: Path, out_dir: Path) -> Path:
    """Dispatch a declarative mapping to the single- or multi-source writer."""
    from _csv_reader import write_multi_csv_seed, write_single_csv_seed  # noqa: PLC0415

    module = importlib.import_module(f"mappings.{name}")
    if hasattr(module, "SOURCES"):
        return write_multi_csv_seed(
            module.SQL_TABLE, module.SOURCES,
            module.COLUMNS, csv_dir, out_dir,
            join_keys=getattr(module, "JOIN_KEYS", None),
            require_join_match=getattr(module, "REQUIRE_JOIN_MATCH", True),
        )
    return write_single_csv_seed(
        module.SQL_TABLE, module.SOURCE_CSV,
        module.COLUMNS, csv_dir, out_dir,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CSV-to-SQL seed fragment generator (writes into build/sql/)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--table", help="Mapping module name (e.g., accessory)")
    group.add_argument(
        "--all",
        action="store_true",
        help="Run complete CSV mappings",
    )
    group.add_argument("--list", action="store_true", help="List available mappings and exit")
    parser.add_argument("--csv-dir", type=Path, default=DEFAULT_CSV_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    available = discover_mappings()

    if args.list:
        for name in available:
            print(name)
        return 0

    if args.all:
        targets = []
        for name in available:
            module = importlib.import_module(f"mappings.{name}")
            if getattr(module, "INCLUDE_IN_ALL", True):
                targets.append(name)
            else:
                print(f"skipped {name}: partial mapping; run --table {name} explicitly")
    else:
        if args.table not in available:
            print(f"unknown table: {args.table}; available: {', '.join(available)}", file=sys.stderr)
            return 1
        targets = [args.table]

    for name in targets:
        out_path = run_mapping(name, args.csv_dir, args.out_dir)
        print(f"wrote {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
