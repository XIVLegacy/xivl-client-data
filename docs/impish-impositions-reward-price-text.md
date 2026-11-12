# Impish Impositions reward price text

The installed English `spl0i2` row 23 uses supplied integer 3 for the displayed
price and supplied integer 1 for the prize item. Both of its cookie lookups use
literal item row 3010417. The script forwards 3010417 as supplied integer 2,
and the English resource contains no reference to that position. The same
row serves all four price calls.

## Quest source and typed arguments

The original `Spl0i2` member is
`client/script/tp5rq/r75w9s1v/ruy/ruyj1h.le.lpb`, 6840 bytes, SHA-256
`b30852b309ecb1f954dd220b7549ca5c22ec46f7091b3343e1e60d92a7c2caaa`.
The decoded chunk is 6827 bytes, SHA-256
`060506b25c19a40d7c6e194f9c875bf89480296f21992f25645632bc429d8eb8`.
Root PC9, decoded offset `0x44`, binds `initText` to proto0. Its PCs0-3,
offsets `0x214..0x220`, call `self:_loadTextDataPermanently(5699, "spl0i2")`.
Proto4 PCs151/162/173/184, offsets `0xF7F/0xFAB/0xFD7/0x1003`, call
`worldMaster:say(self, 23, prize, 3010417, count)`. The argument literals
are Lua numbers with exact signed 32-bit integer values. See the
[runner menu and callback values](https://github.com/XIVLegacy/xivl-client-scripts/blob/69f79bc1fda3a105811a266abf1e99a65afb7cff/docs/impish-impositions-client-contract.md#runner-menu-and-callback-values)
for selection and confirmation.

The ActorBase loader adds `0x03A20000` to 5699, requests definition
`0x03A21643` and can assign `spl0i2` to that same actor's source wrapper.
The WorldMaster route preserves the quest source, row and ordered tail through
`DesktopWidget._appendMessagePool` and `0x007702C0`. With integer capture,
the tail becomes three tag-0 formatter variants in order. The message lookup
uses field selector `0xFF`, which reads the loaded sheet's default field.
The installed English client definition has logical field 1 at physical
column 0, type `str`. See
[ActorBase text-source initialization](https://github.com/XIVLegacy/xivl-decomp/blob/054880e3638f864203764687e74c2b7ae187b218/docs/script/actor-base-text-source.md)
and the
[WorldMaster message-pool contract](https://github.com/XIVLegacy/xivl-decomp/blob/054880e3638f864203764687e74c2b7ae187b218/docs/script/worldmaster-message-pool.md).

## English row operations

Offsets are zero-based within the 393 decoded bytes. Integer selector
`0xE8` uses one-based positions in the supplied variant vector. Each
nested string expression `0xFF` formats its own control sequence.

| Offset | Control | Selected operation |
| --- | --- | --- |
| 0 | `0x2B` over nested `0x08` | Test integer 3 for inequality with zero, then signed less than or equal to 10 on the nonzero branch. Use a `0x09` switch with ten English word alternatives for the stock counts 3 and 10. Both zero and the greater-than-10 branch use signed decimal `0x20`. Apply first-letter capitalization to the result. |
| 108, 261 | `0x09` over `0x28` | Use `itemData` field 41 of cookie literal 3010417 and prize argument 1, respectively, to select the foreground color. The field is `s32` at physical column 4 and equals 1 for all five rows. Each selector chooses the first `0x13` alternative, `0xFFF3F3F3`. |
| 199, 350 | `0x14` | Emit edge color `0xFF262626` before each noun. |
| 208 | `0x31` | English noun for `xtx/itemName` row 3010417 with `xtx/attributive` row 3, literal quantity 2 and noun group 0. |
| 359 | `0x31` | English noun for `xtx/itemName` row from integer 1 with `xtx/attributive` row 2, literal quantity 1 and noun group 0. |
| 233, 238, 382, 387 | `0x14`, `0x13` | Emit the `0xEC` edge and foreground reset operands after each noun. |

The numeric color selectors cross the string decoder. The schema type-name
`s32` at VA `0x0110C580` initializes type-table slot 6 at
`0x00CAF46E..0x00CAF47D`. TextModule type case 6 selects `0x00CA0B37`
through the jump-table cell at `0x00CA0E0C`. It reads the dword and formats
it as signed decimal at `0x00CA0B5E..0x00CA0B6E`. Switch handler
`0x00C9F140` calls the integer decoder in mode 1 at `0x00C9F158`.
The decoder's `0xFF` fallback formats the nested string at `0x00CB3195`
and parses it through `0x004555A0` at `0x00CB31AA`. The result 1 takes the
first switch alternative at `0x00C9F16D..0x00C9F1AC`. This is a successful
lookup path with ready rows and the selected schema. See the
[entry count controls](https://github.com/XIVLegacy/xivl-decomp/blob/054880e3638f864203764687e74c2b7ae187b218/docs/resource/rich-string-entry-counts.md),
[named-sheet and capitalization handlers](https://github.com/XIVLegacy/xivl-decomp/blob/054880e3638f864203764687e74c2b7ae187b218/docs/resource/rich-text-sheet-and-case-handlers.md#rt-03-handler-0x28-named-sheet-text)
and [color token contract](https://github.com/XIVLegacy/xivl-decomp/blob/054880e3638f864203764687e74c2b7ae187b218/docs/resource/rich-text-colour-tokens.md#ct-01-formatter-handlers).

The English `xtx/itemName` definition's `NOUN` metadata maps group 0
`SGL/PLR/VOW/CNT/DEF` to logical fields 6/7/8/9/10. All five selected
rows have `DEF=0`. The cookie has `VOW=0`. With quantity 2 it uses
plural field 7 and an empty prefix from `xtx/attributive` row 3 field 5.
The prize uses singular field 6 and the prefix from row 2 field
`4 + 3*VOW`. Fields 4 and 7 of that row contain the same prefix.
Each noun control passes an empty nested variant vector. The selected
prefixes and noun cells contain no `[n]` placeholder or embedded control.
The displayed price comes from the leading count control. See the
[English noun handler](https://github.com/XIVLegacy/xivl-decomp/blob/054880e3638f864203764687e74c2b7ae187b218/docs/resource/battle-log-line-path.md#bl-08-token-0x31-the-english-actor-noun).

| Selection | Prize row | Count | Count form | Prize VOW | Prefix field in row 2 |
| --- | ---: | ---: | --- | ---: | ---: |
| 1 | 8013301 | 3 | Capitalized word | 0 | 4 |
| 2 | 8013302 | 10 | Capitalized word | 1 | 7 |
| 3 | 8013303 | 50 | Signed decimal | 0 | 4 |
| 4 | 8013304 | 99 | Signed decimal | 0 | 4 |

## Installed resources

The input is FFXIV 1.23b build `2012.09.19.0001`.
`ffxivgame.exe` is PE32 x86, 15996808 bytes, image base `0x00400000`,
SHA-256 `9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`.
The English quest definition is sheet ordinal 1, file ordinal 0, begin 0
and count 501. It explicitly names the data, enable and offset resources.
The quest row is the complete framed string at data span `[3632,4029)`.
After decoding its frame, SHA-256 is
`2a5747e669fbaea6a738b7e73656e975163f079424d0dfdcc2cc7fd76e3a7492`.

| Quest resource | Bytes | SHA-256 |
| --- | ---: | --- |
| Definition `0x03A21643` | 1664 | `e2e296bb9e6a43bb918c57a27e7a2dbf7d76e82ff856ac610ea9930e92975d17` |
| English data `0x03A2164A` | 17879 | `7567bac8669498885888b340dea8313411f0b1e3f96f03431f117885e7a520cf` |
| English enable `0x03A2164B` | 64 | `63592f88f993eae65dc17cd9301c2923be77e4c14c54d1c4892867831997f7c4` |
| English offsets `0x03A2164C` | 2004 | `d80bc66f084ba9e833b095f5617c2f67b635f5dbad9a14c082926ada76730f0a` |

Game master `0x01030000` names the three dependencies. All ordinals are
zero-based. The corresponding [sheet inventory](../manifests/sheet_inventory.csv)
records their definition keys.

| Sheet and selected rows | Definition, sheet/file ordinal | Data / enable / offsets | Selected data spans |
| --- | --- | --- | --- |
| `itemData` 3010417 | `0x01030129`, 0/3 | `0x010301D5/D6/D7` | `[7980,8075)` |
| `itemData` 8013301-8013304 | `0x01030129`, 0/32 | `0x01030160/61/62` | `[70585,70680)`, `[70680,70775)`, `[70775,70870)`, `[70870,70965)` |
| `xtx/itemName` 3010417 | `0x0B450027`, 1/3 | `0x0B4506F7/F8/F9` | `[13662,13872)` |
| `xtx/itemName` 8013301-8013304 | `0x0B450027`, 1/32 | `0x0B45038A/8B/8C` | `[71709,71773)`, `[71773,71867)`, `[71867,71949)`, `[71949,72037)` |
| `xtx/attributive` 2 and 3 | `0x0B4500CA`, 1/0 | `0x0B4500CE/CF/D0` | `[30,71)`, `[71,96)` |

The static evidence joins original LPB calls, PE instructions and the
installed English definition and rows. Reproduction checks the original
identities, exact Lua chunk end, schema types, monotonic row offsets,
agreement with enabled rows, complete row framing, and all selected
expressions. A bounded replay verifies the four price cases and repeats
them with a different integer 2. The interpretation requires successful
source initialization, a valid quest handle, English selection, ready
dependency rows and formatter completion. Original-client message delivery,
rendered pixels and server exchange behavior remain unobserved.
