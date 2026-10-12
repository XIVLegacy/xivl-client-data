# Parley title rows

`xtx_negotiationTable.csv` holds row 0 and 62 nonzero row IDs. No row has a
value in columns 0-45; the localized text occupies columns 46-55, and column
48 holds the English title. The table therefore supplies no numeric
per-title value.

Fifteen English titles each match exactly one English quest title in
`xtx_quest.csv` column 2:

| Quest row | English title | Parley title rows |
| ---: | --- | --- |
| 110015 | Toll of the Warden | 5001, 5101 |
| 110017 | Lord Errant | 1401, 1501, 1601, 1701, 1801, 1901, 2001, 5301 |
| 110301 | Hide and Seek Shenanigans | 2101, 2201, 2301, 2302 |
| 110321 | Song of the Sirens | 4201, 4302, 4401, 4601, 4702, 4901 |
| 110360 | She Walks in Beauty | 4301, 4701, 4801 |
| 110361 | F'lhaminn's Flower | 3801 |
| 110362 | Struck Through the Heart | 5201 |
| 110381 | Designer Imposters | 1101 |
| 110382 | Head of the Class | 5401 |
| 110401 | Dance the Night Away | 2401, 2501, 2601, 2701, 2801, 2901 |
| 110421 | The Boy and the Dragon Gay | 1302, 1303, 1304 |
| 110441 | Mystery of the Gastronome Gone Home | 3001 |
| 110442 | Something in the Soup | 3101, 3201, 3301, 3401 |
| 110461 | Little Saboteurs | 1201 |
| 110481 | The Grass is Always Greener | 1301 |

The other nonzero rows, 1, 3501, 3511-3514, 3601, 3611-3613, 3701,
3711-3714, 3901, 4001, 4101, and 4501, match no quest title. Row 1's English
title is the single character U+00D7; the others carry item names such as "A Potion" and
"Hempen Inner Tunic".

A title-text match joins names only. These rows do not show which actor,
quest sequence, or event selects a title row, the order in which a quest
uses several rows, or Parley difficulty, turn count, or time limits.

Sources: `xivl-client-data:csv/xtx_negotiationTable.csv` physical lines
3-65, SHA-256
`8adbfac163e4f1c25c67549477f9dbc3195eeed2d93af6cfbe7b8107954003e6`
(`manifests/tables.json:6235-6240`); and
`xivl-client-data:csv/xtx_quest.csv` column 2 of the quest rows above,
physical lines 18, 20, 74, 80, 85-87, 92-93, 98, 104, 110-111, 116, and
122, SHA-256
`938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719`
(`manifests/tables.json:6267-6271`).

A prior external lead, `parley/title_resolutions_2026-09-27.md` at revision
`d5fb880e17f07f31ea7f8380ff813e5d71b6b678`, grouped the same title rows by
quest.
