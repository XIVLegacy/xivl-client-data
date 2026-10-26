# Selected quest marker rows

The selected `quest_marker.csv` rows below preserve literal field values.
Columns 3/4 contain coordinates, not a complete world position. The rows do
not establish actor identity, quest activation, terrain height, or a route.

## Rows 11001601-11001606

| Row | Columns 3/4 | Column 5 | Column 8 | Columns 9/10 | Column 12 | Column 13 |
| ---: | --- | ---: | --- | --- | --- | --- |
| `11001601` | `-193`, `-1408` | `4000257` | `m00013` | `103`, `321` | `MapMarkerQuest` | `@5208/i11001601` |
| `11001602` | `-431`, `187` | `1600179` | `m00013` | `101`, `121` | `MapMarker` | `@5208/i11001602` |
| `11001603` | `-199.89`, `-162.06` | `1000392` | `m00013` | `103`, `321` | `MapMarkerQuest` | `@5208/i11001603` |
| `11001604` | `-431`, `187` | `1600179` | `m00013` | `101`, `121` | `MapMarker` | `@5208/i11001604` |
| `11001605` | `-235`, `51` | `4000257` | `m00013` | `104`, `421` | `MapMarkerQuest` | `@5208/i11001605` |
| `11001606` | `-193.46`, `-177.31` | `4000257` | `m00013` | `104`, `421` | `MapMarkerQuest` | `@5208/i11001606` |

## Rows 11001607-11001611

| Row | Columns 3/4 | Column 5 | Columns 9/10 | Column 13 |
| ---: | --- | ---: | --- | --- |
| `11001607` | `752.12`, `-374.22` | `4000257` | `105`, `501` | `@5208/i11001903` |
| `11001608` | `723.3`, `-381.08` | `4000257` | `105`, `501` | `@5208/i11001903` |
| `11001609` | `744.46`, `-307.34` | `4000257` | `105`, `501` | `@5208/i11001903` |
| `11001610` | `799.6`, `-214.43` | `4000257` | `105`, `501` | `@5208/i11001903` |
| `11001611` | `864.53`, `-298.03` | `4000257` | `105`, `501` | `@5208/i11001903` |

Each of these rows also has resource `m00013` in column 8 and `MapMarkerQuest`
in column 12.

## Rows 11001612-11001620

Each row has columns 3/4 `-431`, `187`; column 5 `1600179`; column 8
`m00013`; columns 9/10 `101`, `121`; and column 12 `MapMarker`.

| Rows | Column 13 |
| --- | --- |
| `11001612`-`11001620` | `@5208/i11000101` |

The property references in column 13 are literal values, not a universal
marker-row identity rule. The repeated destination-like fields and references
do not establish a quest route or associate any row with an actor class.

## Rows 11170401-11170406

| Row | Columns 3/4 | Column 5 | Columns 9/10 | Column 11 | Column 13 |
| ---: | --- | ---: | --- | ---: | --- |
| `11170401` | `-2166.42`, `-426.45` | `4000257` | `104`, `403` | `0` | `@5208/i11170401` |
| `11170402` | `-2189.01`, `-431.55` | `1000010` | `104`, `403` | `0` | `@5208/i11170402` |
| `11170403` | `-2179.86`, `-429.82` | `1200023` | `104`, `403` | `0` | `@5208/i11170403` |
| `11170404` | `169.1`, `-174.7` | `1000288` | `104`, `5014` | `0` | `@5208/i11170404` |
| `11170405` | `-105.3`, `194.83` | `4000257` | `104`, `421` | `50` | `@5208/i11170405` |
| `11170406` | `-113.22`, `209.95` | `1000010` | `104`, `421` | `50` | `@5208/i11170406` |

## Rows 11170501-11170506

| Row | Columns 3/4 | Column 5 | Columns 9/10 | Column 11 | Column 13 |
| ---: | --- | ---: | --- | ---: | --- |
| `11170501` | `-110`, `160` | `1900186` | `104`, `431` | `32` | `@5208/i11170501` |
| `11170502` | `-117`, `118` | `4000257` | `104`, `421` | `0` | `@5208/i11170502` |
| `11170503` | `-117`, `118` | `4000257` | `104`, `421` | `50` | `@5208/i11170503` |
| `11170504` | `-1597`, `251` | `4000257` | `104`, `403` | `0` | `@5208/i11170504` |
| `11170505` | `-115`, `153` | `2700004` | `104`, `431` | `32` | `@5208/i11170505` |
| `11170506` | `-119.84`, `127.86` | `4000257` | `104`, `431` | `32` | `@5208/i11170506` |

Each row in these two sections also has resource `m00013` in column 8 and
`MapMarkerQuest` in column 12. Column 11 is `0` in rows
`11001601`-`11001620`. The column 11 values are literal and carry no
assigned meaning here.

Source: `xivl-client-data:csv/quest_marker.csv`, rows `11001601`-`11001620`,
`11170401`-`11170406`, and `11170501`-`11170506`,
SHA-256
`920e93e6c1dd136ed758f22465bea3644f2bbe53a6ff46f7d938dd51e3b514be` in
`manifests/tables.json`. The source corpus is the pinned decoded
`2012.09.19.0001` snapshot; its archive identity is recorded in
`docs/ai_agents/retail-input-validation.md`.
