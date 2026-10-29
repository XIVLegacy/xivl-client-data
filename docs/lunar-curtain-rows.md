# Lunar Curtain item and status rows

The retail extraction identifies an item and a status named Lunar Curtain.
The status description says damage from supreme spells derived from Dalamud
is reduced by half. This is client text, not an observed item use or a proved
server damage formula. The item-to-status application edge is unestablished.

## Item identity and local use contract

Extraction `2012.09.19.0001` gives these same-key item joins. Column numbers
are zero-based sheet positions after the row ID.

| Source | Row / physical line | Column | Observation |
| --- | --- | --- | --- |
| `csv/_item.csv` | 3020538 / 496 | 0 | `Normal/CmnGoodStatusItem` |
| `csv/xtx_itemName.csv` | 3020538 / 496 | 5 | `Lunar Curtain` |
| `csv/xtx_itemName.csv` | 3020538 / 496 | 26 | Describes a powder forming a magical barrier from aetherial particles. |
| `csv/itemData.csv` | 3020538 / 496 | 50,53,56,59 | Raw float parameter values `0.5,0,0,15`. |

The grow-selector and compatibility cells at itemData columns
49/51,52/54,55/57,58/60 are empty. The
[item-column crosswalk](item-equipment-columns.md) owns their generic
parameter roles; neither `0.5` nor `15` is assigned a damage or time unit here.

`CmnGoodStatusItem` defines two local methods. For catalog 3020538,
`canUseForRelation` returns `(true,false,false)`. This records the tuple
without assigning target-category names to its positions. `canUseDetail`
returns `(true,0)`. These are local use checks, not a success receipt.
The two methods contain no status application or item settlement.

Source: `xivl-client-scripts:lua/scripts/item/normal/cmngoodstatusitem.lua`,
catalog getter at line 14, method bindings at lines 58 and 68. Original Lua
5.1 `root/proto0` compares the catalog with 3020538 at PC 42 / payload
`0x1BA` and returns the three booleans at PC 47 / `0x1CE`.
`root/proto1` returns `(true,0)` at PC 2 / `0x28C`.
PCs are zero-based; offsets address the decoded payload. The original root's
closure bindings establish which prototype implements each named method.

## Status identity and effect-text limit

`csv/xtx_status.csv:292`, row 223273, column 3 names Lunar Curtain.
Column 21 says damage from supreme spells derived from Dalamud is reduced
by half. `csv/status.csv:292` has the same row key. Its raw typed columns
31 and 47 (`float`) are `0.5` and `15`; these matching scalars are not an
independent item-to-status binding or an established applied duration.
The [status export](status-names.md#columns-and-limits) owns the typed-column
boundary, and `derived/status_names.csv:291` retains the named row.

The selected command-name sheet contains no Lunar Curtain label. The
positive item/status identities do not establish a separate battle-command
ID. Name equality alone does not prove that using item 3020538 applies
status 223273, which spells qualify, the authoritative reduction, duration,
stacking, quality effects or completion packet.

An attributable retained item invocation joined to its status update and
damage/result state, or an exact authoritative application producer, would
close those edges. No such retail transaction is established by these rows
and local checks.

## Source identity and reproduction

Python 3.12.0 `csv`, `zipfile` and `hashlib` authenticated the decoded CSV
archive against `manifests/private_csv_corpus.json`, then each selected member
against `manifests/tables.json` before selecting exact keys. Source pins:

| Member | SHA-256 |
| --- | --- |
| `csv/_item.csv` | `f41dba38473a8a4014826c5b0cd639e12c6652700c9f760660fcb241d7469dda` |
| `csv/itemData.csv` | `f17193d832b375761cd01a37b25ff7d2c2947967ddc5ba4c2b16c0507d422912` |
| `csv/xtx_itemName.csv` | `917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2` |
| `csv/status.csv` | `3b09a76123b0fd8aba320dc5513e8182820fef409cf9d40f0b522b10b11d02ec` |
| `csv/xtx_status.csv` | `60eca3b76d1d9799589d9059adeb1e7c3d142e07609a1ad0a053c5e75d9b96ee` |
| `csv/xtx_command.csv` | `2aa0b20822df0b2270918d9ac5525c86a34a941d7c66d17a106add1b2d6567d3` |

The exact Lua member matched
`xivl-client-scripts:manifests/scripts.json`, SHA-256
`c394327594278277509f63e7076a32454f059e0c43aaab70883fa7cd6273d4d1`.
Its original resource is `1q5x/wvsx9y/7xw3vv6rq9qpr1q5x.le.lpb`,
714 bytes, SHA-256
`304c54ea1a454f4a7d9fa4bd2812d599dd6f0c396aee7e9624a146a6109670dd`;
decoded payload is 701 bytes, SHA-256
`a72ab556988721e97983cfaba204d7fcdd1a01c870248b89fca3654f5f69b318`.
These identities matched `manifests/retail_lua_coverage.json` in the scripts
repository. Original closure bindings, catalog comparisons and return values
were checked in memory using `tools/retail_script.py:decode_lpb` and
`tools/build_quest_contracts.py:ChunkReader/states_for/instruction` there.
Bounded path evaluation for catalog 3020538 checked the selected return;
it was static analysis, not a retail runtime test.
