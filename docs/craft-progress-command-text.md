# Craft progress command name and help

The [CraftProgress Lua flow](https://github.com/XIVLegacy/xivl-client-scripts/blob/322f34dd2edccbc8b4634e4a1c7bfcc94f810956/docs/craft-progress-flow-contract.md#generated-row-and-button-command)
supplies a command ID as the only text argument to UI keys 3043 and 1105.
The first sets the generated command Button's Content. The second sets
TextBlock_CommandHelp.Text in the HD form. In the installed form pinned by
[Craft progress form declarations](craft-progress-form.md), the TextBlock
is at decoded line 44.

## UI keys

Both selected cells in each of the four languages below are one 0x28
named-sheet control. It takes literal `xtx/command`, integer argument 1
(0xE8 with literal index 1) as the row, and the literal logical field in
the table. There are no additional operands or text runs. The
[named-sheet control contract](https://github.com/XIVLegacy/xivl-decomp/blob/a580ee8c6cb2de2a4d130e44d799f32f36c760b1/docs/resource/rich-text-sheet-and-case-handlers.md)
owns evaluation. The sheet row argument is the command ID. The generated
Button's ordinal is a separate operand of the input route.

| Language | UI logical field | UI data / enable / offset | 3043 name field | 1105 help field |
| --- | ---: | --- | ---: | ---: |
| ja | 0 | `0x0B4502C1` / `0x0B4502C2` / `0x0B4502C3` | 1 | 22 |
| en | 1 | `0x0B4502B5` / `0x0B4502B6` / `0x0B4502B7` | 2 | 23 |
| de | 2 | `0x0B45029A` / `0x0B45029B` / `0x0B45029C` | 8 | 24 |
| fr | 3 | `0x0B4502A6` / `0x0B4502A7` / `0x0B4502A8` | 16 | 25 |

In each definition the UI column is the sole physical string column.
The selected block starts at row 0 and covers 13020 slots. The original
24-byte spans in each data file are half-open. Hashes are SHA-256 of the
20-byte decoded cell, after removing string framing.

| Language | 3043 span and hash | 1105 span and hash |
| --- | --- | --- |
| ja | [32949,32973) `68f25ccd8e31d75257e0dbb306640888024cc78516ea8a949d0de64c996d7da5` | [2417,2441) `6f163f101b77b2cb30d8f61a1786181ae2c8000dffe709a89ead3b4b363c3b68` |
| en | [25483,25507) `026825f826db5736cf30794fecb6e6d3ce12f1814f7280c40935b4ea97bbdd90` | [2264,2288) `dc349f7b60909c65bff9e1469e92e75dc5c9c88a6cf099e96391129059d200f5` |
| de | [30177,30201) `1621dfb7bdb79f471422fd3c1398cc3dd88e10ef82d3713b41a107c6452ab97d` | [2464,2488) `5ee28b76d08ed8b9f30fa4ec5fbbec075dbb494fd4caf83d7e85c3989f6d48cc` |
| fr | [29863,29887) `cf4a79c92456b6371783f638972ffd1fd4673d80036d566b7f8bb83ea33f2dbd` | [2968,2992) `9203cb72ad9a87a757a176791c29d6b8b207491afa588a1ecbe0ff73b21dced6` |

## Command sheet

The selected `xtx/command` block begins at row 22500 and covers 200 slots.
Its definition maps both selected logical fields in each language to
string columns. Physical columns below are zero-based.

| Language | Command data / enable / offset | Physical name / help | 22550 row span and SHA-256 |
| --- | --- | --- | --- |
| ja | `0x0B450223` / `0x0B450224` / `0x0B450225` | 0 / 1 | [438,521) `f1a492c411955c72270897a90af489ac027192910584a6c55da7bd27a81acc47` |
| en | `0x0B450066` / `0x0B450067` / `0x0B450068` | 0 / 6 | [541,653) `68784236e13fac4c9e97711641417dee81e96af955be7523cd67cb467fa598d4` |
| de | `0x0B450010` / `0x0B450011` / `0x0B450012` | 0 / 8 | [797,970) `af0d7f552afee24481b8a283c45bb6530c82c4934c3d77fad2b2767f463ffd53` |
| fr | `0x0B4500D6` / `0x0B4500D7` / `0x0B4500D8` | 0 / 6 | [594,713) `6fa96034f1598dc66261c823208aa9683b4f20a444345d9f0cf982587d65772d` |

English row 22550 field 2 is 18 bytes of plain UTF-8, SHA-256
`d514be58d23db744a9a45cd331f051dfa49fcd13664cd87851eac2cebcadfcaf`.
Field 23 is 44 bytes of plain UTF-8, SHA-256
`9176dd19360d8d1f06b8ade6e9b85c4200e9755928a95657c9a31ad066f9c209`.
Both agree with the [command catalog](../derived/command_battle_params.csv#L72).
The adjacent 22551 and 22552 rows select different names and help with the
same field indices. The English row 22580 span [4471,4583) matches row
22550 byte for byte.

## Source and reproduction

The source is the installed 1.23b build `2012.09.19.0001`.
The [named sheet inventory](../manifests/sheet_inventory.csv) identifies
the two definitions. The [SSD decoder recipe](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/docs/formats/ssd-sheet.md#the-scrambled-xml-container)
recovers each definition. Select the client sheet by exact language, locate
the row using the declared block and enable and offset files, then decode
the physical columns in definition order.

| Definition | Container bytes / SHA-256 | Decoded bytes / SHA-256 |
| --- | --- | --- |
| `0x0B450082` | 3099 / `27e50caf3d258e8eed2d9e70bc8355e2ab67f54f2dc8bf54e6cfcdf604e5e492` | 3098 / `2763f4ae79453b368b74f844f9a53647c6788e1c37a327258fd297327f799bac` |
| `0x0B450017` | 12993 / `99762442c38144d8ae82c83b24265c4b1afe3050aab769dc7ae2caddeb12b3e5` | 12992 / `46140f26d544e2302cee5a3e2bf2a2a1825f5bba1c1ec729726e0c34047011ca` |

These declarations establish the selected display data and argument join.
The chosen action and input delivery require the separate command flow.
