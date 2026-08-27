"""Decode the client's static-actor class-path catalog into a manifest."""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from _json_io import write_json  # noqa: E402

SAN_RELATIVE = Path("client/script/rq9q1797qvs.san")
DEFAULT_OUT = REPO_ROOT / "manifests" / "staticactor_class_paths.json"
XOR_KEY = 0x73


def parse_san(raw: bytes) -> list[dict]:
    if raw[:4] != b"sane":
        raise ValueError(f"bad magic {raw[:4]!r}; expected b'sane'")
    if len(raw) < 13:
        raise ValueError(f"truncated san header: {len(raw)} bytes")
    decoded = bytes(b ^ XOR_KEY for b in raw)
    count = struct.unpack(">I", decoded[9:13])[0]
    records: list[dict] = []
    pos = 13
    for index in range(count):
        if pos + 4 > len(decoded):
            raise ValueError(f"truncated actor id for record {index} at offset {pos}")
        actor_id = struct.unpack(">I", decoded[pos:pos + 4])[0]
        end = decoded.find(b"\x00", pos + 4)
        if end == -1:
            raise ValueError(f"unterminated classPath string at offset {pos}")
        class_path = decoded[pos + 4:end].decode("ascii")
        if not class_path.startswith("/"):
            raise ValueError(f"malformed classPath {class_path!r} at offset {pos}")
        records.append({"id": actor_id, "classPath": class_path})
        pos = end + 1
    if pos != len(decoded):
        raise ValueError(f"unexpected trailing bytes at offset {pos}")
    if len({r["id"] for r in records}) != len(records):
        raise ValueError("duplicate actor ids in san table")
    records.sort(key=lambda r: r["id"])
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Build manifests/staticactor_class_paths.json from the client install")
    parser.add_argument("game_dir", type=Path, help="FFXIV 1.x install root (parent of client/)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    san_path = args.game_dir / SAN_RELATIVE
    if not san_path.is_file():
        print(f"static-actor table not found: {san_path}", file=sys.stderr)
        return 1

    records = parse_san(san_path.read_bytes())
    write_json(args.out, {
        "_provenance": {
            "source_path": SAN_RELATIVE.as_posix(),
            "method": (
                "XOR-0x73 decode of the sane-magic static-actor table; "
                "records are [u32 BE actor id][NUL-terminated classPath]. "
                "Record count cross-checked against the header count field."
            ),
            "evidence_class": "client_extraction",
            "limitations": [
                "Covers script actors only (/Command, /Quest, /Status, "
                "/Judge); NPC actor classes (ids 1000001+) are bound "
                "server-side and are absent from the client install.",
            ],
            "generator": "tools/extract_staticactor_san.py",
        },
        "recordCount": len(records),
        "records": records,
    })
    print(f"wrote {args.out} ({len(records)} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
