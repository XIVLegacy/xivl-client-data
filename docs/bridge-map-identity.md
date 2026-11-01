# The Bridge map identity

The pinned `_zoneParam.csv` row 140 carries place-name ID 1091, whose English
text is Sailors Ward. Zone 140 is the only `_zoneParam.csv` row with that ID.
It is the position-5 member of `zoneGroupParam.csv` row 101, the Limsa
Lominsa group listed in [zone-group place-key rows](zone-group-place-rows.md).

## Layout, map and marker rows

`_layout.csv` row 5005 holds `70` in column 2 and place-name ID 1517 in
column 3. `mapNavi_data.csv` row 70 is the only row with layout 5005 in
column 1. It has region 202 in column 0, page field 0 in column 2, offsets
512 and 448 in columns 3 and 4, and scale 4 in column 5:

| Row | Map piece ID, column 6 | Columns 10/11 | Place-name IDs, columns 12-14 | Columns 15/16 | Column 17 |
| ---: | ---: | --- | --- | --- | ---: |
| `70` | `1081` | `1536`, `1024` | `1051`, `1520`, `1501` | `768`, `512` | `1072` |

The matching `2Dmap_piece.csv` row 1081 declares dimensions 1536 by 1024.
Column 17 resolves to an `xtx_placeName.csv` row on all 427
`mapNavi_data.csv` rows.

| Place-name ID | English text, column 1 | Referenced by |
| ---: | --- | --- |
| 1051 | Limsa Lominsa | `mapNavi_data.csv` row 70, column 12 |
| 1072 | The Bridge | `mapNavi_data.csv` row 70, column 17 |
| 1091 | Sailors Ward | `_zoneParam.csv` row 140 |
| 1517 | Briefing Room | `_layout.csv` row 5005, column 3 |
| 1520 | Briefing Room | `mapNavi_data.csv` row 70, column 13 |

Row 1501 is a placeholder whose English cell is a single hyphen token. The
Japanese cell of row 1520 is the Japanese text of row 1072, a full-width
colon, and the Japanese text of row 1517.

`quest_marker.csv` row 11150405 has region 202 and map 5005 in columns
9/10, with coordinate cells `-333`, `-321`. It is the only marker row with
map 5005. Its other cells are listed in
[selected quest marker rows](quest-marker-rows.md#rows-11150401-11150410).

## Layout resource

[`zone_internal_names.json`](../manifests/zone_internal_names.json) lists
layout resource `0x72420007`, family `mkt_sea`, with primary name
`sea0Event01`. The resource is `data/72/42/00/07.DAT` in the retail 1.23b
install, game.ver `2012.09.19.0001`, 35552 bytes, SHA-256
`902cde4a009619b27161f578ed6fa3e659ab31f70c5ac2745b3d51abbce9c57b`.

Its scene layout name is `prv_s0_hal01`. The `LaySettingsObject` named
`prv_s0_hal01` has translation `(-320, 0, -320)`, zero rotation and unit
scale. `xivl export-zones <client-root> --layout 0x72420007` reports that
translation as the zone transform of every placement it exports.

Two `InstanceObject` nodes reference the `PositionMarkerBaseObject` named
`pomk_hal01`. Both have zero rotation and unit scale.

| Instance name | File offset | Translation |
| --- | ---: | --- |
| `ipomk_hall01` | `0x6AF0` | `(0, 0, 0)` |
| `ipomk_hall02` | `0x6B30` | `(0, 3.18, -10)` |

The layout's SEDB scene starts at file offset `0x11A0`, and its payload
starts at `0x11D0`. Node references are payload-relative. The field offsets
follow `xivl-tools:docs/formats/world-layout.md`, "Fields consumed by the
zone reader", at revision `fd4c97d89eab3bbbf657021297e3d78156c63319`.
`InstanceObject` translation is the inline `f32[3]` at `+0x20`, and the
`LaySettingsObject` translation is at `+0x40`. The `ipomk_hall02` Y value is
stored as the `f32` nearest 3.18.

## Limits

These static joins associate zone 140 with place name 1091, and layout 5005
with map row 70 and marker 11150405. No table joins zone 140 to layout 5005,
to resource `0x72420007` or to `sea0Event01`, and `zoneBindings` has no entry
for zone 140. The layout and marker translations are layout-space values.
They do not establish server coordinates, a map projection, instance dispatch
or an actor placement.

Sources in `manifests/tables.json`: `csv/_zoneParam.csv` row 140, SHA-256
`1e75e434217e8d99848ac1d690a9fcd93e43c9a2b00fc983e3ba7fb592d377f9`;
`csv/zoneGroupParam.csv` row 101, SHA-256
`e521adb118f8edc099fcf4171e905299b5b8c83c13c90fc62d46c646e80d8b23`;
`csv/_layout.csv` row 5005, SHA-256
`2fd242794ec24288b8d4f6f54878b6d8f9241a80eea7a4ce4f2e62df0286ba88`;
`csv/mapNavi_data.csv` row 70, SHA-256
`a33f166fe9ec1ced44f2c614f849c295113352e9f8b7b03b7ecb818a53925a3f`;
`csv/2Dmap_piece.csv` row 1081, SHA-256
`b08fdba7fc6ee1ad1780b3560cb75072030144ea49980946c0b6e7e74d8e5e88`;
`csv/xtx_placeName.csv` rows 1051, 1072, 1091, 1501, 1517 and 1520, SHA-256
`81467ef42e8aeba82fe95f6c4249356550c02e41e6734abf9fdd194051dc1714`; and
`csv/quest_marker.csv` row 11150405, SHA-256
`920e93e6c1dd136ed758f22465bea3644f2bbe53a6ff46f7d938dd51e3b514be`. All
are from extraction `2012.09.19.0001`.
