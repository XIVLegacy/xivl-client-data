# derived/

Use these analysis artifacts alongside the as-imported CSV corpus. Repository
tools generate the owned products under `derived/`; the corpus manifest covers
only the source files under `csv/`.

## Derived vs imported

`csv/` is the extraction snapshot and nothing else: every file there is a
byte-for-byte import of extraction 2012.09.19.0001, pinned by sha256 in
`manifests/tables.json` and traceable to a `manifests/sheet_inventory.csv` row.
A file whose bytes this repo's own tools produce cannot satisfy either
invariant, so generated CSVs live here instead. The split is enforced, not just
convention: `tools/validate_corpus.py` fails on any `csv/` file absent from
`tables.json` or not derivable from a sheet-inventory row, and `manifest.json`
`tableCount`/`totalBytes` count `csv/` alone.

Consequence for consumers: a `csv/` row is client evidence; a `derived/` row is
this repo's interpretation of it, and is only as good as the finding doc named
in the table below.

| File | Built by | Source | Finding |
|---|---|---|---|
| `actor_appearance_census.csv` | `tools/build_actor_appearance_census.py` | `csv/actorclass_graphic.csv`, actor-class and display-name correlations | `docs/actor-appearance-crosswalk.md` |
| `actor_appearance_value_counts.csv` | `tools/build_actor_appearance_census.py` | `csv/actorclass_graphic.csv` | `docs/actor-appearance-crosswalk.md` |
| `command_battle_params.csv` | `tools/build_command_battle_params.py` | `csv/gameCommand.csv`, `csv/gameCommandBasic.csv`, `csv/xtx_command.csv` | `docs/command-battle-params.md` |
| `substat_status_crosswalk.csv` | `tools/analyze_substat_status.py` | `csv/status.csv` | `docs/substat-status-join.md` |
| `gc_seal_shop_catalog.csv` | `tools/build_shop_catalogs.py` | `csv/gcSealShopItem.csv`, item catalog | `docs/shop-catalogs.md` |
| `shop_catalog.csv` | `tools/build_shop_catalogs.py` | `csv/shopBase.csv`, `csv/shopItem.csv`, item catalog | `docs/shop-catalogs.md` |
| `map_marker_resource_crosswalk.csv` | `tools/build_map_marker_resources.py` | `csv/2Dmap_actor_data.csv`, `csv/2Dmap_marker.csv`, `csv/quest_marker.csv` | `docs/map-marker-resources.md` |
| `icons-1.23b/` | imported, not regenerable here | `archive/icons-1.23b/xiv-icons-1.23b.zip` | `derived/icons-1.23b/README.md` |

## command_battle_params.csv

One row per command id (1611), joining the command trio's gameplay sidecars with
client display names. Columns decode only what is verified against the client's
own command getter evidence, cited by `docs/command-battle-params.md`. Raw sheet
values are authoritative; speculative enum labels sit in separate `*_label`
columns and never overwrite the raw value. See the finding doc for the full
column -> getter:line map, the decoded element enum, and the list of quantities
that require retail-capture validation (primary damage potency, the C++ combine
step, native grow tables, and the 5-way command type).

Regenerate: `python tools/build_command_battle_params.py`.

## Shop catalogs

`gc_seal_shop_catalog.csv` is a lossless named projection of all 402
`gcSealShopItem` rows, joined to the item class and English name. It preserves
the raw rank, company, event, unresolved, and category values.

`shop_catalog.csv` expands each nonzero `shopBase` range against `shopItem`.
Overlapping ranges produce one association per owner. Source rows outside all
`shopBase` ranges remain in the source corpus and are not emitted here.

`manifests/shop_catalogs.json` records the seven-sheet fidelity audit, source
headers and hashes, output hashes, counts, column maps, and residual ceilings.
Regenerate both tables and the manifest with `python tools/build_shop_catalogs.py`.

## SubStat status crosswalk

`substat_status_crosswalk.csv` projects every status row id as the packed word
read by the retail SubStat and Object paths. It records only numeric bit
domains. No names for the nibble values are established by the source corpus.
Regenerate it with `python tools/analyze_substat_status.py`.

## Map-marker resource crosswalk

`map_marker_resource_crosswalk.csv` groups the complete marker-bearing sheet
rows by resource path, resource instance, UI class, and visibility. Its
manifest preserves raw column positions and claim limits so the grouped names
cannot be mistaken for a runtime call relationship or a wire-field map.
Regenerate it with `python tools/build_map_marker_resources.py`.

## icons-1.23b/

The 1.23b client icon export: four derived artifacts describing 9,960 decoded
PNGs, plus a gitignored 78 MB zip holding the images at
`archive/icons-1.23b/xiv-icons-1.23b.zip`. Unlike the row above, no tool here
rebuilds these; they were computed over the imported image archive and imported
with the corpus. `manifests/icons_1_23b.json` pins the zip's sha256 and records
one digest per artifact. What cannot be regenerated can at least be verified:
`tools/validate_corpus.py` re-checks every hash and recomputes the counts.
Orientation in [`icons-1.23b/README.md`](icons-1.23b/README.md).
