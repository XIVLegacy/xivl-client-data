"""Write generated corpus JSON with the repository's deterministic formatting."""

from __future__ import annotations

import json
from pathlib import Path


def write_json(path: Path, obj: object) -> None:
    """Write indent-2 UTF-8 JSON with a single trailing LF newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
