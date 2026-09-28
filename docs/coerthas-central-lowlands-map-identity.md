# Coerthas Central Lowlands map identity

In the `2012.09.19.0001` corpus, `_zoneParam.csv` row 147 points to
place-name ID 4007, whose English text in `xtx_placeName.csv` is Coerthas
Central Lowlands. The client zone catalog associates zone 147 with layout 204
(`roc0Field04`) and the same place-name ID.

Four `mapNavi_data.csv` rows share region 102, layout 204, and a reference to
place-name ID 4007:

| Row | Page field |
| ---: | ---: |
| `3300` | 0 |
| `3320` | 20 |
| `3330` | 30 |
| `3340` | 40 |

Row `3000` is not part of this association: it has layout 201 and place-name
IDs 4004, 4009, and 1501. The static joins associate the Central Lowlands
name and layout with four map-navigation records. Row `4700` also references
place-name ID 4007, but has layout 214 and page field 100, so it is outside
the zone catalog's layout-204 association. These joins do not establish a
world-to-map coordinate transform, world units per grid cell, historical
server dispatch, or which record was selected for a particular point.

Sources in `manifests/tables.json`: `csv/_zoneParam.csv` row 147, SHA-256
`1e75e434217e8d99848ac1d690a9fcd93e43c9a2b00fc983e3ba7fb592d377f9`;
`csv/xtx_placeName.csv` row 4007, SHA-256
`81467ef42e8aeba82fe95f6c4249356550c02e41e6734abf9fdd194051dc1714`;
and `csv/mapNavi_data.csv` rows 3000, 3300, 3320-3340, and 4700, SHA-256
`a33f166fe9ec1ced44f2c614f849c295113352e9f8b7b03b7ecb818a53925a3f`.
The zone-to-layout association is in `manifests/zone_internal_names.json`.
