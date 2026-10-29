# Selected Grand Company quest reward offers

All six selected Grand Company quest IDs have same-key `quest_new_reward.csv`,
`quest.csv` and `xtx_quest.csv` records in retail 1.23b extraction
`2012.09.19.0001`. Their reward rows contain an EXP calculation input and
an item/count offer for 1,000 company seals. Historical EXP, gil and seal
receipt remains **UNESTABLISHED** for each quest. The client offer is a
separate fact from authoritative reward settlement.

## Selected quest rows

`Q51` is numeric column 51 of `quest.csv`; `R5`, `R55` and `R57` are numeric
columns 5, 55 and 57 of `quest_new_reward.csv`. Numeric header labels exclude
the separate leading row-key field. These selected cells are present,
nonblank `s32` values. Source identity, consumer locators and the finite
absence boundary follow the table. Confidence is high in the extracted
values and identified display arguments. No historical invocation or balance
change is inferred.

| Row / quest | Exact same-key source lines: quest / title; reward | EXP | Gil | Seals |
| --- | --- | --- | --- | --- |
| R1 / Alive `111427` | `quest.csv` and `xtx_quest.csv` line `452`; `quest_new_reward.csv` line `437` | Q51=`40`, R5=`7`; [expression established](#exp-expression-and-rounding); actual amount/receipt UNESTABLISHED | No type `-2` offer block; amount/receipt UNESTABLISHED | R55=`1000201`, R57=`1000`: Storm Seal item/count offer established; receipt UNESTABLISHED |
| R2 / Two Vans are Better than One `111627` | quest/title line `486`; reward line `466` | Q51=`40`, R5=`7`; [expression established](#exp-expression-and-rounding); actual amount/receipt UNESTABLISHED | No type `-2` offer block; amount/receipt UNESTABLISHED | R55=`1000202`, R57=`1000`: Serpent Seal item/count offer established; receipt UNESTABLISHED |
| R3 / Like Father, Like Son `111827` | quest/title line `520`; reward line `495` | Q51=`40`, R5=`7`; [expression established](#exp-expression-and-rounding); actual amount/receipt UNESTABLISHED | No type `-2` offer block; amount/receipt UNESTABLISHED | R55=`1000203`, R57=`1000`: Flame Seal item/count offer established; receipt UNESTABLISHED |
| R4 / Imperial Devices (Limsa Lominsa) `111410` | quest/title line `435`; reward line `425` | Q51=`25`, R5=`8`; [expression established](#exp-expression-and-rounding); actual amount/receipt UNESTABLISHED | No type `-2` offer block; amount/receipt UNESTABLISHED | R55=`1000201`, R57=`1000`: Storm Seal item/count offer established; receipt UNESTABLISHED |
| R5 / Imperial Devices (Gridania) `111610` | quest/title line `469`; reward line `454` | Q51=`25`, R5=`8`; [expression established](#exp-expression-and-rounding); actual amount/receipt UNESTABLISHED | No type `-2` offer block; amount/receipt UNESTABLISHED | R55=`1000202`, R57=`1000`: Serpent Seal item/count offer established; receipt UNESTABLISHED |
| R6 / Imperial Devices (Ul'dah) `111810` | quest/title line `503`; reward line `483` | Q51=`25`, R5=`8`; [expression established](#exp-expression-and-rounding); actual amount/receipt UNESTABLISHED | No type `-2` offer block; amount/receipt UNESTABLISHED | R55=`1000203`, R57=`1000`: Flame Seal item/count offer established; receipt UNESTABLISHED |

Line numbers identify the parsed records' physical lines. All selected records
occupy one line. The exact ID join uses `xtx_quest.csv` English title column 2
and the SAN class map in [Grand Company quest identities](grand-company-quest-identities.md).
The seal item names retain the separate catalog attribution in
[Grand Company reward rows](grand-company-reward-rows.md).

## Offer selection and gil boundary

`xivl-client-scripts:docs/quest-offer-reward-display.md#offer-row-selection`
owns the supplied-key lookup: `QuestDetailWidget.setRewardData` reads quest
and quest-new-reward sheets at the same supplied key. It advances by 13
numeric columns, processes marker `100` blocks and stops at marker `301`.
In each of these six rows, the only processed blocks are base `0`, type
`-13`, and base `52`, type `-14`; the first `301` is at base `65`.
The first block's icon `534` is not the EXP amount.

The authenticated `widget/ask/questdetailwidget.lua` source's type `-14`
branch at lines `698-716` sends base+3 as item ID and base+5 as count to
text key `5041`. These are R55 and R57 for base `52`, establishing the
1,000-seal item/count offer separately for each company. The type `-15`
branch at `717` is a different display path and is not a selected block.

The type `-2` branch at line `684` uses text key `5051`, whose English
numeric column 1 at `xtx__text_ui.csv:1726` identifies gil. None of the six
selected processed blocks uses type `-2`. This establishes an omitted gil
offer entry in this consumer,
not a zero-gil reward or a historical server decision. The type `-16` branch
at `781` is not the gil branch. Item/count key `5041` at line `1716` and
EXP key `5054` at line `1729` were checked separately in that sheet.

## EXP expression and rounding

The type `-13` branch calls `Player.calcSkillPoint(Q51,R5)` and passes its
result to UI text key `5054`, as established by
`xivl-client-scripts:docs/quest-offer-reward-display.md`.
The authenticated `chara/player/player_work.lua:675-689` divides the second
argument by 100, calls `getSkillPointMax` with the first argument, and applies
the named `_math.ceil` to their product.

The two selected entries in authenticated
`chara/charabaseclass_battle.lua:getSkillPointMax` are distinct:

| Quest IDs | Selected source entry | Retained expression | Exact arithmetic product |
| --- | --- | --- | ---: |
| `111427`, `111627`, `111827` | `<=40` table index `10` = `71000`; literal line `1982`, slot line `1992` | `_math.ceil(71000 * (7 / 100))` | 4970 |
| `111410`, `111610`, `111810` | `<=30` table index `5` = `27000`; literal line `1952`, slot line `1962` | `_math.ceil(27000 * (8 / 100))` | 2160 |

These products are exact-arithmetic reconstructions, not observed displayed
amounts. In an authored Python 3.12 binary64 reconstruction, the first product
is `4970.000000000001` and standard `math.ceil` returns `4971`; the second
product and standard ceil result are `2160`.

`xivl-decomp:docs/script/lua-math-ceil-paths.md#argument-and-result-carriers`
establishes binary64 argument/result storage for the registered native `ceil`
callback in the pinned executable. Its `#finite-rounding-conditions` section
qualifies the fallback by selected x87 control word and normal completion.
Neither fact determines actual Lua DIV/MUL intermediate precision or runtime
controls. The retained expressions therefore do not justify asserting `4970`
or `4971` as the retail display, or either product as an earned EXP grant.
Q51 is a calculation selector here, not a newly proved quest level requirement.

## Other reward-sheet keys

The complete authenticated `quest_reward.csv` has no exact row keyed by any
of these six IDs. Its 1,264 unique integer keys range from `11000101` to
`11077201`. This separate key domain is not interchangeable with the
same-key `quest_new_reward.csv` records. No runtime group/quest mapping or
semantic reward-field mapping is established for these six IDs in that
sheet. Missing exact rows do not mean blank cells or zero amounts.

The separate `_quest.csv` likewise has no exact selected key; it is not a
substitute for the present `quest.csv` records. No generic group, neighbouring
quest row or wiki amount supplies a missing reward or receipt join.

## Sources and remaining settlement join

The complete selected CSV members matched their byte sizes and SHA-256 pins
in [tables.json](../manifests/tables.json). Their containing archive matched
the size and SHA-256 in [private_csv_corpus.json](../manifests/private_csv_corpus.json).
Only these exact members and selected key projections were used:

| Member | SHA-256 |
| --- | --- |
| `quest_new_reward.csv` | `496d5e7d2e5057852f990e18f404524426d456c52cbcbd95544652494350ff66` |
| `quest.csv` | `bdadece1907b7050aaeee7c94a2a2d395fe76b504e47cbb1616b57ba380209dc` |
| `xtx_quest.csv` | `938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719` |
| `quest_reward.csv` | `c4165e2665823f3b1281ccaa5dffc022f79bb47e8c1fd063e3378a9d240474f7` |
| `_quest.csv` | `c0ca7e4783f45a785ab01ddb249252fb2c97e608a307fd9061175016ca2495c8` |
| `xtx__text_ui.csv` | `23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece` |

The three complete canonical Lua members matched
`xivl-client-scripts:manifests/scripts.json` inside the archive declared by
`xivl-client-scripts:manifests/private_lua_corpus.json`:

| Canonical source under `lua/scripts/` | SHA-256 |
| --- | --- |
| `widget/ask/questdetailwidget.lua` | `0d1474c6b43cce61d90a75ba0fe32e2b1d77504fd396024ee32a8876ebc8c8ce` |
| `chara/player/player_work.lua` | `be4e0575c015d537c0fbbe0d103e3d02e95a36a0b4f9c085825669e740e81b04` |
| `chara/charabaseclass_battle.lua` | `ca7d9bd52320e8aa62ecd853a0ce8d9e2e0ddc76fc504729b501b14b9bfcd959` |

Python 3.12 `zipfile`, `hashlib` and `csv` performed the bounded archive,
complete-member identity and header-derived cell checks. Source inspection
covered only the selected display branches and calculation entries. It did
not decode new LPBs, execute retail artifacts or infer native rounding from
a helper name.

For each exact quest, the remaining settlement join is a quest-attributed
successful completion and authoritative EXP/gil/seal transaction, with its
conditions and amounts. Client offer rows, dialogue completion and local
returns do not establish it. Encounter/item/victory/companion boundaries
remain in
`xivl-client-scripts:docs/grand-company-quest-step-contracts.md#encounter-outcome-and-reward-joins`.
