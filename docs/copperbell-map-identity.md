# Copperbell Mines map identity

The pinned `_zoneParam.csv` and `xtx_placeName.csv` rows join zone 178 to
place-name ID 3112, whose English text is Copperbell Mines. The zone catalog
also pairs zone 178 with layout 414 and place-name ID 3112. The client layout
census identifies layout 414 as `wil0Dungeon04`, Copperbell Mines.

Two `mapNavi_data.csv` rows share region 104, layout 414, offsets 1056 and 544
in columns 3 and 4, and scale 2 in column 5:

| Row | Page field, column 2 | Map piece ID, column 6 | Place-name IDs, columns 12-14 |
| ---: | ---: | ---: | --- |
| `1700` | 0 | `1131` | `3112`, `3113`, `1501` |
| `1720` | 20 | `1136` | `3112`, `3114`, `1501` |

Place-name ID 3112 is one of three references on each row. The matching
`2Dmap_piece.csv` rows 1131 and 1136 each declare dimensions 2560 by 2048.
These static joins associate Copperbell's zone and layout with two map-page
records. They do not establish server instance dispatch, active page selection,
or floor membership of a recorded position.

Sources in `manifests/tables.json`: `csv/_zoneParam.csv` row 178, SHA-256
`1e75e434217e8d99848ac1d690a9fcd93e43c9a2b00fc983e3ba7fb592d377f9`;
`csv/xtx_placeName.csv` row 3112, SHA-256
`81467ef42e8aeba82fe95f6c4249356550c02e41e6734abf9fdd194051dc1714`;
`csv/mapNavi_data.csv` rows 1700 and 1720, SHA-256
`a33f166fe9ec1ced44f2c614f849c295113352e9f8b7b03b7ecb818a53925a3f`;
and `csv/2Dmap_piece.csv` rows 1131 and 1136, SHA-256
`b08fdba7fc6ee1ad1780b3560cb75072030144ea49980946c0b6e7e74d8e5e88`.
The zone-to-layout pair is also present in
`manifests/zone_internal_names.json`. The layout name is listed in
`xivl-decomp:docs/resource/dungeon-layout-timeline-corpus.md:72`.
