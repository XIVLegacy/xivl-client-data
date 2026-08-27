# Retail map-marker resource crosswalk

The decoded `2012.09.19.0001` corpus independently establishes a static
map-marker resource vocabulary. It does not establish that the proven s2c
`0x018D` consumer reads any one of these sheets or assigns any wire field to a
sheet column.

## Positive resource evidence

`2Dmap_marker.csv` contains 634 rows and joins each row to a resource path,
resource instance, UI class, property reference, and visibility value. Its four
resource paths are:

| Resource path | Rows |
|---|---:|
| `common/mapMarker.le.spk` | 442 |
| `common/mapMarkerAetheryte.le.spk` | 90 |
| `common/mapMarkerSymbol.le.spk` | 79 |
| `debug/mark_anime_sample.le.spk` | 23 |

The same sheet has nine UI-class values: `MapMarker`, `MapMarkerAetheryte`,
`MapMarkerAetheryteUnder`, `MapMarkerPoint`, `MapMarkerRight`,
`MapMarkerSymbol`, `MapMarkerSymbolLeft`, `MapMarkerSymbolUnder`, and
`MapMarkerUnder`. All 634 property references use the `@5204/i` prefix and are
distinct. Visibility is `Visible` in 304 rows and `Collapsed` in 330.

`quest_marker.csv` adds 7,889 rows using `common/mapMarker.le.spk`. Its resource
instances are `m00013`, `m00018`, and `m00029`; its UI classes are `MapMarker`
(6,497 rows), `MapMarkerQuest` (1,272), and `MapMarkerQuestArea` (120). All rows
are `Visible`. Of its property-reference cells, 7,886 use `@5208/i`; rows
`11000102`, `11000602`, and `11001002` carry the same non-ASCII blank sentinel
instead.

`2Dmap_actor_data.csv` adds 19 `common/mapMarker.le.spk` instances. The generated
[crosswalk](../derived/map_marker_resource_crosswalk.csv) groups the three
sheets by source, resource path, resource instance, UI class, and visibility.
The [manifest](../manifests/map_marker_resources.json) pins the source hashes,
resource ids, raw headers, value counts, property coverage, and coordinate
domains, plus the complete decoded-CSV vocabulary search. Regenerate both with:

```powershell
python tools/build_map_marker_resources.py
python tools/build_map_marker_resources.py --check
```

These are static string and resource relationships. No row contains
`MapMarkerParty`, and similarity between that runtime class name and this
sheet's `MapMarker*` classes is not a call edge.

## Vocabulary search

The generator searched the raw UTF-8 text of all 803 decoded CSVs using exact
case, Unicode case-folding, and a normalized form that removes every
non-ASCII-alphanumeric character. `MapScreenControl`, `group_marker_data`, and
`MapMarkerParty` are absent in all three domains. `Update` has 67 exact-case and
121 case-insensitive or normalized occurrences across seven sheets. Those are
localized updater, journal, timestamp, or general data strings; none occurs in
the three marker-resource sheets, so they do not corroborate the runtime
`Update` operation.

A prior tracked-tree search of paths, manifests, derived products, schemas,
tools, and public docs added no exact or normalized hit for the three absent
distinctive terms. The new analyzer and this finding necessarily name the
search terms and are not independent corpus evidence.
The sheet inventory does independently pin `2Dmap_actor_data`, `2Dmap_data`,
`2Dmap_marker`, `2Dmap_piece`, `aetheryte_2Dmap`, `mapNavi_data`, and
`quest_marker` to their client resource ids. This is inventory identity, not a
runtime consumer relationship.

## Coordinate boundary

The corpus types `2Dmap_marker.csv` columns 1 and 2 as `s32`; their observed
ranges are 312..6362 and 247..5653. In `quest_marker.csv`, columns 2 and 3 use
`float`; their observed ranges are -2584.95..2632.2 and
-2972.18..1825.51. `2Dmap_data.csv`, `2Dmap_piece.csv`, `mapNavi_data.csv`,
`aetheryte_2Dmap.csv`, `_layout.csv`, `_zoneParam.csv`, and `regionParam.csv`
carry further integer map, layout, and region values.

Several ID relationships are exact. Both `2Dmap_data` (307/307 rows) and
`mapNavi_data` (427/427) join their column 0 to `_region` and
`zoneGroupParam`, column 6 to `2Dmap_piece`, and columns 12..14 to
`xtx_placeName`. `aetheryte.csv` joins `aetheryte_2Dmap.csv` by all 118 row ids.
`2Dmap_marker` column 16 joins `xtx_placeName` for all 634 rows. These joins
establish region, piece, and display-name context, not a projection formula.

The rejected joins are equally important. `2Dmap_marker` column 17 resolves as
a place-name key for only 2/634 rows. `quest_marker` column 9 resolves to a
`2Dmap_data` row for 6,900/7,889 rows and to a place-name row for 6,877/7,889,
so it is not a universal direct key. The actor-data and map-marker instance
domains are disjoint despite sharing `common/mapMarker.le.spk`, and resource
path is not one-to-one with UI class.

No corpus record pairs a known world-coordinate tuple with its projected map
tuple, names a scale or origin for the float pair, or supplies a join that
proves such a transform. The static data therefore establishes coordinate
domains and map/layout context, but it cannot independently type the floats
selected by `0x018D` or assign them to X, Y, Z, scale, origin, or territory.
Navi map keys are not unique, so choosing one navi row per map pair would also
make heuristic transform counts selection-dependent. No candidate transform is
promoted.

## Research boundary

The remaining evidence requirement is a client-native consumer that connects
`MapMarkerParty` or `group_marker_data` to one of the static `.spk` instances
or UI classes, plus address-backed transform code or a paired retail
observation that maps a known world tuple to display coordinates. Static name
proximity, numeric column order, and unpaired ranges are insufficient.
