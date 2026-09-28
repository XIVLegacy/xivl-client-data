# Mor Dhona map identity

In the `2012.09.19.0001` corpus, `_zoneParam.csv` rows 190 and 266 both
point to place-name ID 106, whose English text in `xtx_placeName.csv` is Mor
Dhona. The zone-name catalog lists layout 501 as `lak0Field01` with the same
place-name ID. Because both zone rows share that name, these records do not
identify a unique zone ID for the layout.

Four `mapNavi_data.csv` rows use region 105 and layout 501 and reference
place-name ID 106:

| Row | Page field | Map piece ID |
| ---: | ---: | ---: |
| `3500` | 0 | `1401` |
| `3520` | 20 | `1401` |
| `3530` | 30 | `1401` |
| `3540` | 40 | `1401` |

These static records associate Mor Dhona's name and layout with four
map-navigation entries. They do not establish which zone ID uses the layout,
a world-to-map coordinate formula, units per grid cell, or the map selection
and spawn behavior of a historical encounter.

Sources in `manifests/tables.json`: `csv/_zoneParam.csv` rows 190 and 266,
SHA-256
`1e75e434217e8d99848ac1d690a9fcd93e43c9a2b00fc983e3ba7fb592d377f9`;
`csv/xtx_placeName.csv` row 106, SHA-256
`81467ef42e8aeba82fe95f6c4249356550c02e41e6734abf9fdd194051dc1714`;
and `csv/mapNavi_data.csv` rows 3500 and 3520-3540, SHA-256
`a33f166fe9ec1ced44f2c614f849c295113352e9f8b7b03b7ecb818a53925a3f`.
The layout name and place-name association are in
`manifests/zone_internal_names.json`.
