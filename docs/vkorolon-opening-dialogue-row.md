# V'korolon opening dialogue row

Installed FFXIV 1.23b build `2012.09.19.0001`, English `etc5g0` row 4
contains a color switch, an English item noun and two color resets. The
source call passes no formatter arguments.
`xivl-client-scripts:docs/quest-event-client-contracts.md`,
"V'korolon opening dialogue row 4", records the quest text source and call.

## English row controls

The definition `0x03A22384` selects English sheet ordinal 1 and file ordinal
0, begin 0 and count 501. Its one `str` column has logical field 1. Row 4
occupies `[0x168,0x28C)` in the data file. The decoded string is 288 bytes,
SHA-256
`e8d81d1f554d354da1c21e1843270f473984a88528f1a956122335a70fa9e5c7`.
All control offsets below are zero-based in that decoded string.

| Offset | Control | Operands |
| --- | --- | --- |
| `0x1D` | `0x09` Switch | A nested `0x28` reads `itemData` row 11000224, logical field 41. Six nested `0x13` foreground alternatives in order hold `0xFFF3F3F3`, `0xFFC0FFA0`, `0xFF60C8FF`, `0xFFB38CFF`, `0xFFFFA666` and `0xFFE5DD7E`. |
| `0x78` | `0x14` EdgeColor | Literal `0xFF262626`. |
| `0x81` | `0x31` EnglishNoun | `xtx/itemName`, attributive row 1, item row 11000224, quantity 1, group selector 1. No remaining operands. |
| `0x9A`, `0x9F` | `0x14`, `0x13` | `0xEC` edge and foreground reset operands, respectively. |

Field 41 of the item row is `s32` at physical column 4 and contains 1.
The traced numeric-sheet and Switch handlers therefore select the first
foreground alternative. The English noun handler converts selector 1 to
metadata group 0. The English `xtx/itemName` definition maps
`SGL/PLR/VOW/CNT/DEF` to logical fields 6/7/8/9/10. Fields 8 and 10 of
the item row both contain signed byte 0. With quantity 1 the noun joins
`xtx/attributive` row 1 field 4 to item-name field 6. The cells are 2 and
13 decoded bytes, respectively, and contain no control or `[n]`
placeholder. The same handler contracts are cited in
[Impish Impositions reward price text](impish-impositions-reward-price-text.md)
and the [English noun handler](https://github.com/XIVLegacy/xivl-decomp/blob/054880e3638f864203764687e74c2b7ae187b218/docs/resource/battle-log-line-path.md#bl-08-token-0x31-the-english-actor-noun).

## Installed resource locators

The [sheet inventory](../manifests/sheet_inventory.csv) maps the sheet names
to their definitions. All ordinals and data spans are zero-based. The item
blocks begin at 11000000 and have 1000 slots. The attributive block begins
at 1 and has 35 slots.

| Sheet and row | Definition, sheet/file ordinal | Data / enable / offsets | Data span |
| --- | --- | --- | --- |
| `etc5g0` 4 | `0x03A22384`, 1/0 | `0x03A2238B/8C/8D` | `[0x168,0x28C)` |
| `itemData` 11000224 | `0x01030129`, 0/47 | `0x0103017E/7F/80` | `[21185,21280)` |
| `xtx/itemName` 11000224 | `0x0B450027`, 1/47 | `0x0B4506CD/CE/CF` | `[21941,22012)` |
| `xtx/attributive` 1 | `0x0B4500CA`, 1/0 | `0x0B4500CE/CF/D0` | `[0,30)` |

| Resource | Bytes | SHA-256 |
| --- | ---: | --- |
| `0x03A22384` | 1664 | `144a9d8c682893d2773e2548b6b15e132bae0b839e876f0ee12aaad300f65258` |
| `0x03A2238B` | 7362 | `0536e1335159246268550bd8b0875799f66a8a1f1cf290381e45a2f4aa7d978c` |
| `0x03A2238C` | 32 | `48f4aa3ad8f59416bd4a8cc4867299195a14e1235fce91186a614982abc9e130` |
| `0x03A2238D` | 2004 | `b20532209c99fce7235632b4fa282ba5140fb15ec9bfdcb3819d7a1ee1889226` |
| `0x01030129` | 5906 | `8cbcc49bb37e6ecb3aad4763804f5566aa5e9987721bd32a524dd120a8a85f4a` |
| `0x0103017E` | 94905 | `aefd7401fd1e7579e0556407c6b8f1e6c1fd281a1e4d15ed34945e38f85f6998` |
| `0x0B450027` | 26125 | `15a3ddf5259b62dc706d914618c39415167c77c5cc408cefcb365caec2200ab6` |
| `0x0B4506CD` | 61016 | `b0141bf636bf868c536e9f9d607bffa731b1776505009c5984209a8ba1a7ad38` |
| `0x0B4500CA` | 3516 | `e292f595d63e2f1002ddaf3be5248e8f8561259a0df50ec85b0eab299b30e6cb` |
| `0x0B4500CE` | 896 | `174978c81481669878759f3113c8181fd23a5d6c90bbe9b7fb0b8cea11b4c8b6` |

For each resource ID, use its four hex byte pairs as
`data/AA/BB/CC/DD.DAT`. Decode the definition, select the named sheet
ordinal and verify the declared block. Interpret the offsets as little-endian
row ends and verify that the nonempty spans match the enable ranges. Decode
the selected span by the definition's typed fields and consume the complete
span. Strip the `str` frame before reading the control offsets. The
[SSD format](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/docs/formats/ssd-sheet.md)
and
[read-only sheet scanner](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/tools/research/census_sheet_stack.py)
describe the schema, frame and path operations.

This is an extraction of one English row and its selected dependencies.
The formatted result follows from the cited handlers with ready sheets and a
valid quest source. Original-client rendering and message delivery remain
unobserved.
