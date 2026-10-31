# Tribe row domains

`tribe.csv` contains row IDs 0-15 and three `s32` columns. An exact row-ID
join to `xtx_tribe.csv` column 4 gives the English labels below. Positions
exclude the leading row ID; numeric source columns remain separate domains.

| Tribe row | English label | Column 0 | Column 1 | Column 2 |
| ---: | --- | ---: | ---: | ---: |
| 0 | Clanless | 0 | 0 | 2 |
| 1 | Midlander Male | 1 | 1 | 0 |
| 2 | Midlander Female | 2 | 1 | 1 |
| 3 | Highlander Male | 9 | 1 | 0 |
| 4 | Wildwood Male | 3 | 2 | 0 |
| 5 | Wildwood Female | 4 | 2 | 1 |
| 6 | Duskwight Male | 3 | 2 | 0 |
| 7 | Duskwight Female | 4 | 2 | 1 |
| 8 | Plainsfolk Male | 5 | 3 | 0 |
| 9 | Plainsfolk Female | 6 | 3 | 1 |
| 10 | Dunesfolk Male | 5 | 3 | 0 |
| 11 | Dunesfolk Female | 6 | 3 | 1 |
| 12 | Seeker of the Sun Female | 8 | 4 | 1 |
| 13 | Keeper of the Moon Female | 8 | 4 | 1 |
| 14 | Sea Wolf Male | 7 | 5 | 0 |
| 15 | Hellsguard Male | 7 | 5 | 0 |

Column 2 agrees with the explicit labels: 0 on the eight male-labeled rows,
1 on the seven female-labeled rows and 2 on Clanless. The independent title
selector uses female tribes 2, 5, 7, 9, 11, 12 and 13; its source and original
operands belong to `xivl-decomp:docs/script/player-achievement-titles.md`,
Display consumers and limits.

`xtx_text_raceName.csv` independently has paired noun keys 1/2 Hyur,
3/4 Elezen, 5/6 Lalafell, 7/8 Roegadyn and 9/10 Miqo'te. Those text keys
must not replace either tribe numeric column: tribe 3 has column-0 value 9,
while race-name row 9 labels Miqo'te. Column 1 groups the labeled tribes in
a different order, with Miqo'te at 4 and Roegadyn at 5.

These static rows do not establish a separate player-race wire field, a
complete appearance-model dictionary, historical availability or creation
selection rules. Complete source identities for the three named sheets are
pinned by [tables.json](../manifests/tables.json), extraction `2012.09.19.0001`.
