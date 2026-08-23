"""Compare the named sheet inventory with a retail client's SSD documents."""

from __future__ import annotations

import argparse
import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = ROOT / "manifests" / "sheet_inventory.csv"
MASTER_SOURCES = {
    "game_schema": 0x01030000,
    "var_schema": 0x03A70000,
}
TRAILER = 0xF1
KNOWN_PLAINTEXT_WORD = 0x6C6D
BYTE_ORDER_MARK = b"\xef\xbb\xbf"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-root", required=True, type=Path)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--output", type=Path, help="write JSON here instead of stdout")
    return parser.parse_args()


def resource_path(data_root: Path, resource_id: int) -> Path:
    parts = resource_id.to_bytes(4, "big")
    return data_root.joinpath(*(f"{part:02X}" for part in parts[:-1]), f"{parts[-1]:02X}.DAT")


def path_resource_id(path: Path) -> int:
    parts = path.parts
    return int("".join((parts[-4], parts[-3], parts[-2], path.stem)), 16)


def unscramble(buffer: bytearray) -> None:
    low, high = 0, len(buffer) - 1
    while low < high:
        buffer[low], buffer[high] = buffer[high], buffer[low]
        low += 2
        high -= 2


def decode_document(raw: bytes) -> bytes | None:
    """Decode the retail scrambled-XML container established by xivl-tools."""
    if not raw or raw[-1] != TRAILER or len(raw) - 1 < 8:
        return None
    encoded_length = len(raw) - 1
    buffer = bytearray(raw[:encoded_length])
    unscramble(buffer)
    key_a = (encoded_length * 7) & 0xFFFF
    key_b = int.from_bytes(buffer[6:8], "little") ^ KNOWN_PLAINTEXT_WORD
    for offset in range(0, encoded_length - 1, 4):
        word = int.from_bytes(buffer[offset : offset + 2], "little") ^ key_a
        buffer[offset : offset + 2] = word.to_bytes(2, "little")
    for offset in range(2, encoded_length - 1, 4):
        word = int.from_bytes(buffer[offset : offset + 2], "little") ^ key_b
        buffer[offset : offset + 2] = word.to_bytes(2, "little")
    if encoded_length % 4 == 1:
        buffer[-1] ^= (key_a & 0xFF) ^ (key_b & 0xFF)
    return bytes(buffer)


def parse_document(path: Path) -> ET.Element:
    raw = path.read_bytes()
    decoded = raw if raw.startswith(BYTE_ORDER_MARK) else decode_document(raw)
    if decoded is None:
        raise ValueError(f"{path}: not a plaintext or scrambled XML document")
    body = decoded[len(BYTE_ORDER_MARK) :] if decoded.startswith(BYTE_ORDER_MARK) else decoded
    return ET.fromstring(body.decode("utf-8"))


def sheet_entries(root: ET.Element) -> list[tuple[str, int | None]]:
    return [
        (sheet.get("name", ""), int(value) if (value := sheet.get("infofile")) else None)
        for sheet in root.findall("sheet")
    ]


def load_inventory(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [
        {
            "name": row["name"],
            "resourceId": int(row["resource_id"]),
            "source": row["source"],
        }
        for row in rows
    ]


def discover_documents(data_root: Path) -> dict[int, list[str]]:
    documents: dict[int, list[str]] = {}
    for path in data_root.rglob("*.DAT"):
        with path.open("rb") as handle:
            prefix = handle.read(3)
            if not prefix:
                continue
            handle.seek(-1, 2)
            trailer = handle.read(1)
        if prefix != BYTE_ORDER_MARK and trailer != bytes([TRAILER]):
            continue
        try:
            root = parse_document(path)
        except (UnicodeDecodeError, ET.ParseError, ValueError):
            continue
        documents[path_resource_id(path)] = [name for name, _ in sheet_entries(root)]
    return documents


def analyze(client_root: Path, inventory_path: Path) -> dict[str, Any]:
    data_root = client_root / "data"
    if not data_root.is_dir():
        raise ValueError(f"{client_root}: no data directory")
    inventory = load_inventory(inventory_path)
    inventory_ids = {row["resourceId"] for row in inventory}
    inventory_names = {row["name"] for row in inventory}

    master_results: dict[str, Any] = {}
    referenced_ids: set[int] = set()
    referenced_names: set[str] = set()
    for source, master_id in MASTER_SOURCES.items():
        entries = sheet_entries(parse_document(resource_path(data_root, master_id)))
        references = {(name, resource_id) for name, resource_id in entries if resource_id is not None}
        expected = {
            (row["name"], row["resourceId"])
            for row in inventory
            if row["source"] == source
        }
        referenced_ids.update(resource_id for _, resource_id in references)
        referenced_names.update(name for name, _ in references)
        master_results[source] = {
            "masterResourceId": master_id,
            "referenceCount": len(references),
            "missingFromInventory": sorted(
                [
                    {"name": name, "resourceId": resource_id}
                    for name, resource_id in references - expected
                ],
                key=lambda row: (row["name"], row["resourceId"]),
            ),
            "inventoryOnly": sorted(
                [
                    {"name": name, "resourceId": resource_id}
                    for name, resource_id in expected - references
                ],
                key=lambda row: (row["name"], row["resourceId"]),
            ),
        }

    name_mismatches = []
    for row in inventory:
        names = [name for name, _ in sheet_entries(parse_document(resource_path(data_root, row["resourceId"])))]
        if row["name"] not in names:
            name_mismatches.append({**row, "documentSheetNames": names})

    documents = discover_documents(data_root)
    master_ids = set(MASTER_SOURCES.values())
    extra_document_ids = sorted(set(documents) - inventory_ids - master_ids)
    extra_sheet_documents = [
        {
            "resourceId": resource_id,
            "resourceIdHex": f"0x{resource_id:08X}",
            "sheetNames": documents[resource_id],
            "novelSheetNames": sorted(set(documents[resource_id]) - inventory_names),
        }
        for resource_id in extra_document_ids
        if documents[resource_id]
    ]
    return {
        "inventoryCount": len(inventory),
        "inventoryDistinctNames": len(inventory_names),
        "inventoryDistinctResourceIds": len(inventory_ids),
        "masterComparisons": master_results,
        "masterReferencedIdsAbsentFromInventory": sorted(referenced_ids - inventory_ids),
        "masterReferencedNamesAbsentFromInventory": sorted(referenced_names - inventory_names),
        "inventoryDocumentNameMismatches": name_mismatches,
        "retailXmlDocumentCount": len(documents),
        "retailXmlDocumentsOutsideInventoryAndNamedMasters": len(extra_document_ids),
        "sheetDefiningDocumentsOutsideInventoryAndNamedMasters": extra_sheet_documents,
        "novelSheetNamesOutsideInventory": sorted(
            {
                name
                for document in extra_sheet_documents
                for name in document["novelSheetNames"]
            }
        ),
    }


def main() -> int:
    args = parse_args()
    report = analyze(args.client_root, args.inventory)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
