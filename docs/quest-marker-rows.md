# Selected quest marker rows

This page records literal fields from selected `quest_marker.csv` rows.
Coordinates below are the stored values in columns 3/4, not a complete world
position. The table does not establish actor identity, quest activation,
terrain height, or a route.

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

Source: `xivl-client-data:csv/quest_marker.csv`, rows `11001601`-`11001620`,
SHA-256
`920e93e6c1dd136ed758f22465bea3644f2bbe53a6ff46f7d938dd51e3b514be` in
`manifests/tables.json`. The source corpus is the pinned decoded
`2012.09.19.0001` snapshot; its archive identity is recorded in
`docs/ai_agents/retail-input-validation.md`.
