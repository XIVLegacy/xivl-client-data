# Guildleve selected row values

The selected `passiveGL_craft.csv` and `guildleve.csv` values below use the
column positions defined by the existing mappings. Mapping names do not
establish how a client or server uses the values. These rows alone cannot
resolve eligibility, objective completion, rewards, or other runtime rules.

CSV positions below are zero-based after the row ID, matching the index
convention in `tools/mappings/passivegl_craft.py` and
`tools/mappings/guildleve.py`.

## Passive crafting guildleve

The retail `passiveGL_craft.csv` row `120214` stores these values in the four
mapped `recommendedLevel` fields:

| Row ID | Fields | CSV positions | Stored values |
| ---: | --- | --- | --- |
| 120214 | `recommendedLevel1` through `recommendedLevel4` | 16, 24, 32, 40 | 5, 15, 25, 40 |

## Guildleve rows

The `guildleve.csv` mapping names positions 39-42 `aimNum1` through `aimNum4`.
The selected rows contain these raw tuples:

| Row ID | Fields | Stored values |
| ---: | --- | --- |
| 12487 | `aimNum1` through `aimNum4` | 3, 3, 0, 0 |
| 11704 | `aimNum1` through `aimNum4` | 3, 4, 0, 0 |
| 13028 | `aimNum1` through `aimNum4` | 4, 0, 0, 0 |

The field labels above come from the existing mapping code. These tuples do not
by themselves define target counts, client display, objective completion, or
server policy.

## Objective, plate, and time-limit joins

Grouping all 624 `guildleve.csv` rows by position 17 (`objective`) gives the
position 1 (`classType`), position 7 (`plateId`), and position 21
(`timeLimit`) values below. Faction rows are listed in the next section, and
the 204 rows with objective 0 are omitted. Counts are rows.

| Objective | `classType` | Rows | `plateId` (rows) | `timeLimit` (rows) |
| ---: | ---: | ---: | --- | --- |
| 10011 | 1 | 61 | 20021 (59), 0 (1), 20032 (1) | 30 (54), 20 (5), 40 (1), 60 (1) |
| 10012 | 1 | 7 | 20021 | 30 |
| 10021 | 1 | 40 | 20025 (39), 20021 (1) | 30 (33), 40 (4), 20 (3) |
| 10031 | 1 | 44 | 20022 | 30 (41), 20 (3) |
| 10041 | 1 | 28 | 20028 | 30 (20), 20 (8) |
| 10042 | 1 | 1 | 20028 | 30 |
| 10051 | 1 | 30 | 20023 (20), 20021 (10) | 30 (20), 20 (10) |
| 10061 | 1 | 9 | 20027 | 30 |
| 10071 | 1 | 4 | 20024 | 30 |
| 10081 | 1 | 6 | 20026 | 30 |
| 11011, 11013, 11014 | 2 | 45 | 20029 | 30 |
| 11021 | 2 | 54 | 20044 (45), 20029 (9) | 30 |
| 13001 | 1 | 9 | 20051 | 15 |
| 13002 | 1 | 9 | 20036 | 15 |
| 13003 | 1 | 12 | 20049 | 20 |

The objective values equal objective row IDs of `xtx_guildleveText.csv`.
`guildleve_UI.csv` has no mapping module; its positions below use the same
zero-based convention. On every row, its positions 76, 77, and 78 equal
`guildleve.csv` positions 7, 8, and 6. Position
75 is 20011, 20012, 20013, or 20014 when `guildleve.csv` position 2
(`location`) is 1, 2, 3, or 4, and 0 on the two rows where it is 0. No text
sheet names a plate ID. The client reads of these `guildleve_UI` positions
and the client's scaling of `timeLimit` are recorded in
`xivl-client-scripts:docs/content-director-ui-contracts.md`.

A prior external lead, `Guildleves/10-battlecraft-regional.md` and
`Guildleves/20-fieldcraft.md` at revision
`d5fb880e17f07f31ea7f8380ff813e5d71b6b678`, describes eight battle plates, two
field plates, and fixed 30-minute timers. The rows above tie each battle
objective mainly to one of the eight plate IDs 20021-20028, with exceptions on
objectives 10011, 10021, and 10051, and store values other than 30 on 35 of
the 230 battle-objective rows.

## Faction guildleve rows

Exactly 65 rows have a nonzero position 4 (`factionCreditRequired`): IDs
1001-1025, 1101-1120, and 1201-1220. Position 20 (`authority`) is constant
within each block and equals an `xtx_guildleveText.csv` row whose English text
begins with the faction name. These 65 rows are also the only rows whose
position 8 (`borderId`) is 20002.

| IDs | `authority` | Faction text | `classType` | Objectives (rows) | `timeLimit` (rows) |
| --- | ---: | --- | ---: | --- | --- |
| 1001-1025 | 40019 | Brotherhood of the Broken Blade | 1 | 12001 (19), 12006 (3), 10021 (2), 12009 (1) | 40 (21), 10 (2), 11 (1), 12 (1) |
| 1101-1120 | 40020 | Azeyma's Shields | 1 | 12002 (9), 12006 (3), 10021 (2), 12007-12012 (1 each) | 40 (14), 10 (4), 15 (2) |
| 1201-1220 | 40021 | Horn and Hand | 4 | 12004 (12), 12005 (4), 12003 (3), 12013 (1) | 20 (16), 10 (3), 15 (1) |

A prior external lead, `Guildleves/40-faction-leves.md` at revision
`d5fb880e17f07f31ea7f8380ff813e5d71b6b678`, gives a 40-minute timer for every
faction guildleve. The stored value is 40 on 35 of the 65 rows, and on none of
the Horn and Hand block. The client talk routes keyed by these IDs are in
`xivl-client-scripts:docs/guildleve-journal-lifecycle.md`.

## Source identity

The files are pinned in `manifests/tables.json` for extraction
`2012.09.19.0001`. The selected row bytes were read from copies whose complete
file hashes match those pins:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `passiveGL_craft.csv` | 26972 | `2e2b68515f43ba2898bc3c4bf642332bd924687a4d771ba8d8d9733c539cd0ba` |
| `guildleve.csv` | 80881 | `74ee8061449bf538d504443017c776f994c06fd1bcd2fd008bbee18284d93b2d` |
| `guildleve_UI.csv` | 66847 | `956267ede9d4e488ee8b29e78e200a83536d3f9056e51e98090f2b1313e47af2` |

The hashes identify the complete source tables; the mapping code identifies
the stored column positions. Neither supplies a runtime consumer interpretation
for the `aimNum` tuple.
