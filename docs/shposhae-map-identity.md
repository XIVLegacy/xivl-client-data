# Shposhae map identity

The pinned client CSVs join zone 235 to place-name ID 1122, whose English
name is Shposhae. Five `mapNavi_data.csv` rows then associate that same
place-name ID with region 101 and layout 114:

| Map row | Page field | Map piece ID |
| ---: | ---: | ---: |
| `5000` | 0 | 1091 |
| `5002` | 2 | 1093 |
| `5003` | 3 | 1095 |
| `5004` | 4 | 1097 |
| `5005` | 5 | 1099 |

Each row has scale 2 and declared image dimensions 2560 by 2048.
`_layout.csv` row 114 points to map row 5000, while row 112 has no such
Shposhae page reference. The client layout catalog calls slot 114
`sea0Dungeon04`; its `placeNameId` 1501 is a placeholder, not the
Shposhae name. The direct map-page join supports Shposhae artwork/layout
association with 114, not a historical server zone-to-layout dispatch,
floor membership of recorded points, or a door placement.

Sources in `manifests/tables.json`: `csv/_zoneParam.csv` row 235 (SHA-256
`1e75e434217e8d99848ac1d690a9fcd93e43c9a2b00fc983e3ba7fb592d377f9`),
`csv/xtx_placeName.csv` row 1122 (SHA-256
`81467ef42e8aeba82fe95f6c4249356550c02e41e6734abf9fdd194051dc1714`),
`csv/mapNavi_data.csv` rows 5000 and 5002-5005 (SHA-256
`a33f166fe9ec1ced44f2c614f849c295113352e9f8b7b03b7ecb818a53925a3f`),
and `csv/_layout.csv` rows 112 and 114 (SHA-256
`2fd242794ec24288b8d4f6f54878b6d8f9241a80eea7a4ce4f2e62df0286ba88`).
The slot name and row-114 map reference are also in
`manifests/zone_internal_names.json`.
