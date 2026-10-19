# Regional dungeon layout associations

The retail FFXIV 1.23b extraction `2012.09.19.0001` contains 24 regional
`Dungeon01` through `Dungeon06` layout slots across the `sea`, `roc`, `fst`,
and `wil` families. The layout catalog, place-name rows, map-reference rows,
and zone-group rows establish the static associations below. They do not
select a historical server instance or its environment policy.

## Layout and place-name joins

`_layout.csv` position 3 supplies the place-name ID. Matching
`_zoneParam.csv` position 0 gives the listed zone rows. Position numbers
exclude the row key. Place 1501 carries the placeholder hyphen token and
supplies no named association. English display text below comes from
`xtx_placeName.csv` position 1, with its hyphen token displayed as `-`.

The catalog column reports only existing `zoneBindings` in
[`zone_internal_names.json`](../manifests/zone_internal_names.json).
Its generator requires one zone and one layout for a non-placeholder place
ID across the complete catalog. A shared place is not enough to select a
zone copy. The eight bindings below are static catalog derivations.

| Layout row / internal name | Layout place ID / English text | Zones sharing layout place | Catalog zone binding | Layout map reference |
| --- | --- | --- | --- | ---: |
| 111 / `sea0Dungeon01` | 1101 / Mistbeard Cove | 131 | 131 | 600 |
| 112 / `sea0Dungeon02` | 1501 / - | none | none | 1 |
| 113 / `sea0Dungeon03` | 1113 / Cassiopeia Hollow | 132 | 132 | 700 |
| 114 / `sea0Dungeon04` | 1501 / - | none | none | 5000 |
| 115 / `sea0Dungeon05` | 1501 / - | none | none | 1 |
| 116 / `sea0Dungeon06` | 1501 / - | none | none | 4900 |
| 211 / `roc0Dungeon01` | 4102 / Dzemael Darkhold | 231 | 231 | 2900 |
| 212 / `roc0Dungeon02` | 1501 / - | none | none | 1 |
| 213 / `roc0Dungeon03` | 1501 / - | none | none | 1 |
| 214 / `roc0Dungeon04` | 4104 / The Aurum Vale | 245, 252-253 | none | 5500 |
| 215 / `roc0Dungeon05` | 1501 / - | none | none | 1 |
| 216 / `roc0Dungeon06` | 1501 / - | none | none | 1 |
| 311 / `fst0Dungeon01` | 2101 / The Mun-Tuy Cellars | 157 | 157 | 2500 |
| 312 / `fst0Dungeon02` | 2113 / The Tam-Tara Deepcroft | 158 | 158 | 2600 |
| 313 / `fst0Dungeon03` | 2123 / The Thousand Maws of Toto-Rak | 159 | 159 | 3600 |
| 314 / `fst0Dungeon04` | 1501 / - | none | none | 3800 |
| 315 / `fst0Dungeon05` | 1501 / - | none | none | 4000 |
| 316 / `fst0Dungeon06` | 1501 / - | none | none | 4200 |
| 411 / `wil0Dungeon01` | 1501 / - | none | none | 1 |
| 412 / `wil0Dungeon02` | 3101 / Nanawa Mines | 176 | 176 | 1600 |
| 413 / `wil0Dungeon03` | 3002 / Eastern Thanalan | 171, 210, 249, 262-263 | none | 4400 |
| 414 / `wil0Dungeon04` | 3112 / Copperbell Mines | 178 | 178 | 1700 |
| 415 / `wil0Dungeon05` | 3123 / Cutter's Cry | 246, 254-255 | none | 5400 |
| 416 / `wil0Dungeon06` | 1501 / - | none | none | 1 |

Zones 159 and 231 have the direct place joins to layouts 313 and 211 through
place IDs 2123 and 4102 respectively. Aurum Vale's place 4104 instead joins
zones 245, 252 and 253. Cutter's Cry's place 3123 joins zones 246, 254 and
255. Eastern Thanalan's place 3002 joins zones 171, 210, 249, 262 and 263.
These shared-place cases have no catalog binding. Layout 413's place text
does not identify a dungeon duty.

## Map-reference context

Every row below is selected by `mapNavi_data.csv` position 1 equaling the
layout ID. The complete row set includes different page-field values, so
the count is a count of references rather than distinct artwork or floors.
The final column follows any non-placeholder place label at positions
12-14 to `_zoneParam.csv` position 0. It is a context union, not another
zone-to-layout binding.

| Layout | Map-reference count | Exact map-reference rows | Zones matching any map place label: context only |
| ---: | ---: | --- | --- |
| 111 | 11 | 600-601, 611-619 | 131 |
| 112 | 0 | none | none |
| 113 | 8 | 700-701, 711-716 | 132 |
| 114 | 12 | 5000, 5002-5005, 5011-5017 | 235 |
| 115 | 1 | 4800 | none |
| 116 | 7 | 4900, 4911-4916 | 137 |
| 211 | 15 | 2900, 2902, 2911-2923 | 231 |
| 212 | 0 | none | none |
| 213 | 0 | none | none |
| 214 | 11 | 4600, 4700, 5500-5503, 5511-5515 | 147, 245, 252-253 |
| 215 | 0 | none | none |
| 216 | 0 | none | none |
| 311 | 11 | 2500, 2511-2520 | 157 |
| 312 | 9 | 2600, 2611-2617, 2620 | 158 |
| 313 | 16 | 3600, 3611-3624, 3700 | 154, 159, 208 |
| 314 | 2 | 3800, 3900 | 151 |
| 315 | 2 | 4000, 4100 | 152, 207, 247, 258-259 |
| 316 | 2 | 4200, 4300 | 153 |
| 411 | 0 | none | none |
| 412 | 10 | 1600, 1611-1619 | 176 |
| 413 | 2 | 4400, 4500 | 171, 210, 249, 262-263 |
| 414 | 9 | 1700, 1711-1717, 1720 | 178 |
| 415 | 17 | 5400-5404, 5411-5422 | 246, 254-255 |
| 416 | 0 | none | none |

Map row 3700 uses layout 313 but labels place IDs 2011 and 2034, adding
zones 154 and 208 to the map-label context. The direct Toto-Rak layout-place
join remains zone 159. Likewise, row 4700 labels place IDs 4007 and 4012
under layout 214, adding zone 147 to Aurum Vale's context without selecting
it as an Aurum Vale instance.

Placeholder layouts 314, 315 and 316 have field-place map labels. Their
context zones therefore do not name those dungeon layouts. Layout 114's
Shposhae map association and layout 116's U'Ghamaro Mines map association
also remain separate from their placeholder layout place 1501. Shposhae's
named map pages and Copperbell's page references are detailed in
[Shposhae map identity](shposhae-map-identity.md) and
[Copperbell Mines map identity](copperbell-map-identity.md).

## Region and zone-group context

Map region IDs come from `mapNavi_data.csv` position 0. `_region.csv`
position 1 gives each region's place key, which matches `regionParam.csv`
position 0. The latter's positions 1-2 bound the zone-group row range.
These number spaces are distinct: map region 101 uses region-place key
102 and regionParam row 1, while zone-group row 101 describes a capital
group.
For layouts without map-reference rows, this is regional family context,
not a direct map-region row for that individual layout.

| Layout family | Map region ID / region name | `_region` row: position 1 | `regionParam` row: positions 0, 1, 2 |
| --- | --- | --- | --- |
| `sea` | 101 / La Noscea | 101: 102 | 1: 102, 101, 113 |
| `roc` | 102 / Coerthas | 102: 105 | 4: 105, 401, 408 |
| `fst` | 103 / The Black Shroud | 103: 104 | 2: 104, 201, 209 |
| `wil` | 104 / Thanalan | 104: 103 | 3: 103, 301, 309 |

Zone-group positions 1-5 list zone IDs under the place key at position 0.
Rows 209 and 406 list zone 159 under place 2123 and zone 231 under place
4102. Rows 407 and 309 list the three Aurum Vale and three Cutter's Cry
zone IDs respectively. Row 303 lists the five Eastern Thanalan IDs. These
rows corroborate place grouping without discriminating a selected instance.
See [Zone-group place-key rows](zone-group-place-rows.md) for the wider
shared-place boundary.

## Sources and selection boundary

The layout vocabulary is in
[`zone_internal_names.json`](../manifests/zone_internal_names.json), with
selection semantics in
[`build_zone_name_catalog.py`](../tools/build_zone_name_catalog.py).
The catalog SHA-256 is
`076a890f2ba9bf4cb3f38ec94982b64407400a01378873ea0d4155fee44e253e`;
the generator was inspected at revision
`9ca24cf5aecd33c4f2753c0d75887ac6e96516cc`. Python 3.12 `csv` reads checked
the seven member identities and the selected row/position joins.
Published resource identity is recorded in
`xivl-decomp:docs/resource/dungeon-layout-timeline-corpus.md#per-layout-coverage`.
That corpus establishes shipped layout resources, including layouts whose
catalog binding basis is `layout_slot`. It does not supply zone dispatch.

All CSV row keys and column positions above refer to the extraction pinned
by [`tables.json`](../manifests/tables.json):

| Member | Data rows | SHA-256 |
| --- | ---: | --- |
| `_layout.csv` | 173 | `2fd242794ec24288b8d4f6f54878b6d8f9241a80eea7a4ce4f2e62df0286ba88` |
| `_zoneParam.csv` | 111 | `1e75e434217e8d99848ac1d690a9fcd93e43c9a2b00fc983e3ba7fb592d377f9` |
| `mapNavi_data.csv` | 427 | `a33f166fe9ec1ced44f2c614f849c295113352e9f8b7b03b7ecb818a53925a3f` |
| `zoneGroupParam.csv` | 42 | `e521adb118f8edc099fcf4171e905299b5b8c83c13c90fc62d46c646e80d8b23` |
| `xtx_placeName.csv` | 923 | `81467ef42e8aeba82fe95f6c4249356550c02e41e6734abf9fdd194051dc1714` |
| `regionParam.csv` | 6 | `720ae958fd38d53721b6ddce380b82a5cddecb111157291ca29f9465c56bc147` |
| `_region.csv` | 61 | `7dc1f9b9657dc302e8ba341181233455149e57ad12291cc1c2bd6483455f666d` |

The archive identity is recorded in
[`private_csv_corpus.json`](../manifests/private_csv_corpus.json): 70,110,686
bytes, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.

No join here identifies which shared-place zone was selected for a duty,
the runtime instance discriminator, active map-page selection, entry or
spawn coordinates, NPC or encounter use, music, weather, or environment
defaults. Those require a direct binding or a paired retail observation
at the corresponding boundary. Place or map-label equality does not
supply that missing selection evidence.
