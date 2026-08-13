# Architectural Findings

Use these findings to interpret the FFXIV 1.23b static client CSV corpus and
its derived products.

## 1. The corpus is the 2012.09.19.0001 snapshot

The active corpus contains 803 CSV files extracted from FFXIV 1.23b on
2012-09-19. Later 1.x revisions are not represented. A later extraction needs
its own version anchor and reconciliation pass.

Treat `csv/` as immutable evidence. Do not re-emit or hand-edit rows. Changes
belong in manifests, derived products, or evidence notes.

## 2. Items use a three-CSV fan-in

`_item.csv` carries the base record, and `itemData.csv` carries typed game data.
`xtx_itemName.csv` carries localized display text. Joining all three is
required to reproduce a complete item record. Most other families are
single-source. The multi-CSV helper is the reusable join pattern for the
exceptions.

## 3. Mapping complexity describes the required transform

The CSV-to-SQL mappings range from partial single-sheet rows through large
single-sheet maps and multi-CSV joins to typed-column transformations. This
classification describes the evidence and transform needed for each mapping;
it is not a runtime contract.

## 4. Some families are structurally blocked

Some CSV tables cannot supply a useful promoted row because their data is sparse.
Others are client-only. These limits change only when new evidence supplies a
specific missing relationship.

## 5. Seed fragments have a separate consumer owner

This repo's `csv_to_sql.py` emits untracked fragments under `build/sql/`.
A downstream consumer owns its DDL, server SQL, and any import or splice of
those fragments.
The client-data pipeline does not write into a server checkout or treat a
server seed as its validation oracle.

## 6. The 1.23b item IDs align with later retail IDs where content overlaps

The retail inventory cross-check matched all 69 observed item IDs against
`_item.csv`, `xtx_itemName.csv`, and `itemData.csv`. The match supports using
the CSV item catalog as the lookup index for overlapping retail content. It
does not claim later-patch coverage.

## 7. Sheets ship a subset of their logical columns

The 2012.09.19.0001 corpus matches the shipped column set on all 798 inventoried
sheets, including string columns. Blank positions are structural gaps, not
decoder loss. Zone internal names and static-actor class paths are separate
manifested products, not missing sheet columns.

## 8. Zone region ids separate structural joins from curation

The region-id path in `tools/mappings/zones.py` follows the
`zoneGroupParam.csv` -> `regionParam.csv` -> `_region.csv` hierarchy. When a
zone appears under multiple group rows, the last non-empty child row wins. This
is intentional for zones 247, 258, and 259, where 103 is stale and 204 is the
effective group. Group 142 has no `_region.csv` inverse and remains unresolved.
The explicit table is a reconciliation layer for no-group placeholders,
battle instances, service and patch rows, and market or office rows whose
hierarchy finds a parent but whose target region deliberately overrides it.
These values are explicit curation, not additional client evidence.

## 9. Zone names are a separate non-sheet client product

`_zoneParam.csv` supplies place-name ids, not internal zone names. The
`MapLayoutResourceData` strings and `_layout.csv` series slots provide the
client-side name catalog in `manifests/zone_internal_names.json`. A binding is
client evidence only when one zone and one named layout share a place-name id.
Unshipped series layouts use the slot rule, while market, ocean, inn, and
related families contribute vocabulary without series bindings. The mapping's
explicit table is a separate reconciliation layer for ambiguous or absent
bindings and preserves SQL `NULL` for placeholder rows. Two catalog values
are fixed by dedicated shipped blobs: zone 139 is sea0Field05 (layout 105) and
zone 264 is lak0Dungeon01 (layout 511). Unresolved bindings remain maintainer
material, not client evidence. The generated catalog's provenance and
limitations stay with the manifest.
