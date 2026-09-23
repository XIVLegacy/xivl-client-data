# Grand Company quest reward-row values

The pinned `quest_new_reward.csv` has SHA-256
`496d5e7d2e5057852f990e18f404524426d456c52cbcbd95544652494350ff66`.
At the following quest-ID rows, CSV column 55 contains a company-seal item
ID and column 57 contains a count-shaped integer. The item names come from
the separately pinned [item catalog](inventory-cross-check.md), not from
the reward sheet itself.

| Quest row | Column 55 item / catalog name | Column 57 value |
| ---: | --- | ---: |
| 111402 | 1000201 / Storm Seal | 250 |
| 111602 | 1000202 / Serpent Seal | 250 |
| 111802 | 1000203 / Flame Seal | 250 |
| 111407 | 1000201 / Storm Seal | 1000 |
| 111607 | 1000202 / Serpent Seal | 1000 |
| 111807 | 1000203 / Flame Seal | 1000 |
| 111420 | 1000201 / Storm Seal | 700 |
| 111620 | 1000202 / Serpent Seal | 700 |
| 111820 | 1000203 / Flame Seal | 700 |

These are literal decoded client-data values. The sheet's integer fields
do not identify the historical server grant, reward acceptance condition,
or actual seal balance. In particular, the 250 displayed by the separate
`Com0*2` status-widget methods is not independent proof of a transaction.
