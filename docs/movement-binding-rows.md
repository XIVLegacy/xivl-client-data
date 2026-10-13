# Movement binding rows

The `key_config` CSV family pairs movement command names with axis and key
binding strings. These are `client_extraction` values from retail extraction
`2012.09.19.0001`, not observations of a player's active configuration.
The file identities are in [tables.json](../manifests/tables.json).

## Column and row identity

Column numbers below are the labels in the CSV's first header row. The leading
field is the row ID, so labeled column 8 is CSV field index 9. The second
header row types column 2 as `s32` and columns 3 and 8 as `str` in all four
files. Every selected row below has value 2 in labeled column 2.

Command values have the literal prefix `RaptureCommands.`. The table shows
the remainder of labeled column 8 and the initial text of labeled column 3.

| File | Row ID | Command suffix | Column 3 prefix |
|---|---|---|---|
| `key_config.csv` | 4 | `MoveCharacter` | `AxisL,,` |
| `key_config.csv` | 5 | `ShiftMoveCharacter` | `AxisL,RDown,` |
| `key_config2.csv` | 13 | `MoveCharacter` | `AxisL,,,,,,NumPad8,NumPad2,NumPad4,NumPad6,` |
| `key_config2.csv` | 12 | `ShiftMoveCharacter` | `AxisL,RDown,` |
| `key_config3.csv` | 4 | `MoveCharacter` | `AxisL,,` |
| `key_config3.csv` | 5 | `ShiftMoveCharacter` | `AxisL,RDown,` |
| `key_config(2).csv` | 2 | `MoveCharacter` | `AxisL,,` |
| `key_config(2).csv` | 1 | `ShiftMoveCharacter` | `AxisL,RDown,` |

The files remain distinct extraction products. In particular,
`key_config(2).csv` has different row IDs, binding strings and header width;
its rows are not aliases for the same-numbered rows in `key_config.csv`.
The [sheet inventory](../manifests/sheet_inventory.csv) identifies
`key_config`, `key_config2` and `key_config3` in `game_schema` as
`0x01030169`, `0x010301D4` and `0x01030559`. The retained source blocks below
authenticate the three same-named CSV products. A runtime request still needs
its native sheet-selection evidence.

## Retained source definitions

The retained retail `game.ver` and `patch.ver` identify `2012.09.19.0001` and
`1.23b`. Its game master resource `0x01030000` names each of the three definitions
exactly once through a decimal `infofile` reference. Each definition contains one sheet with `mode="client"`,
`type="all"`, `cache="0"`, `column_count="16"` and `column_max="16"`.
The `lang` attribute is absent. The declared column index map is the identity
map 0 through 15, and each sheet has one block with `begin="0"` and `count="1050"`.

| Sheet | Definition | Data | Enable | Offset | Enabled rows | CSV cells matched |
|---|---|---|---|---|---|---|
| `key_config` | `0x01030169` | `0x0103016A` | `0x0103016B` | `0x0103016C` | 310 | 4960 |
| `key_config2` | `0x010301D4` | `0x010302FE` | `0x010302FF` | `0x01030300` | 170 | 2720 |
| `key_config3` | `0x01030559` | `0x0103055A` | `0x0103055B` | `0x0103055C` | 310 | 4960 |

The enable resources contain little-endian `(base, count)` pairs. The ranges
are `(1, 262)` and `(1001, 48)` for `key_config` and `key_config3`, and
`(1, 142)` and `(1001, 28)` for `key_config2`. Each offset resource contains
1050 little-endian 32-bit cumulative row ends. Nonempty spans agree exactly
with the enabled keys. Decoding every supplied field using each definition's
types gives the same row-key set and all 16 field values as its same-named CSV.
The [XML decoder](../tools/compare_sheet_inventory.py) and
[backing-row format study](../tools/build_attributive_backing_rows.py)
describe the container and row-framing conventions.

These are source row keys, distinct from iteration positions in the CSV.
The selected source spans below are half-open byte offsets in the data resource.
The zero-based CSV ordinal counts data records after the two header records.

| Sheet | Row key | CSV ordinal | Data span |
|---|---|---|---|
| `key_config` | 4 | 3 | `[1908, 3061)` |
| `key_config` | 5 | 4 | `[3061, 3760)` |
| `key_config2` | 12 | 11 | `[1761, 1990)` |
| `key_config2` | 13 | 12 | `[1990, 2323)` |
| `key_config3` | 4 | 3 | `[2023, 3036)` |
| `key_config3` | 5 | 4 | `[3036, 3735)` |

The retained var master `0x03A70000` has no named entry for these three sheets.
The alternate master `0x27950000` names `key_config` through
`infofile="664076430"`, definition `0x2795008E`. That definition has
`mode="client"`, `type="all"`, `cache="0"`, absent `lang`, an empty `infofile`,
and `column_count="15"` and `column_max="15"`. Its index map is 0 through 14.
Its single block has `begin="0"` and `count="1012"`, with data `0x2795008F`,
enable `0x27950090` and offset `0x27950091`. Enable ranges `(1, 134)` and
`(1001, 8)` agree with the nonempty spans in its 1012-entry offset resource.
All 142 row keys and 2130 decoded fields exactly match `key_config(2).csv`.
The movement anchors are row 1, CSV ordinal 0, span `[0, 565)`, for
`ShiftMoveCharacter`, and row 2, CSV ordinal 1, span `[565, 1475)`, for
`MoveCharacter`.

Thus the two `key_config` CSV products have distinct retained source
definitions. Their 15-column and 16-column layouts, movement row keys and
binding strings must remain separate. This source association does not identify
which master a running client selected or prove delivery of its resources.

Resource IDs resolve to big-endian byte directory paths: `0x01030169` is
`data/01/03/01/69.DAT`. SHA-256 pins below identify the retained source bytes;
the CSV pins remain in [tables.json](../manifests/tables.json).

| Resource | Bytes | SHA-256 |
|---|---|---|
| `0x01030000` | 7044 | `860023878f9ad1e98fd1baa3e3380f971f86bf1f7747043cf0c3c7459cee2eb4` |
| `0x03A70000` | 218 | `6861b8c1b455fab0b6eafb3f74ea2aa2432cc67ef55e473a5a7b17d4c0461d99` |
| `0x01030169` | 1056 | `533f0f67266b21b245a0e1d47cb6c5e3c71839fb83270cbf981dbc5ddfa57fba` |
| `0x0103016A` | 67221 | `d9e380a32a0060c4db47ff22aa41ed21ed2672bc3e09cc14d75016d0f82a48b6` |
| `0x0103016B` | 16 | `c37ffebbfa8953dace4b22f6718212f2bca5b627b9f9fea32c130f45ee21733b` |
| `0x0103016C` | 4200 | `42dc9d1509f9c77eafb09a459b777e8c20f060d0278242b718a5fdedef2d07bb` |
| `0x010301D4` | 1057 | `7b8ab88f66003123891c9f4d5186083045a55e9a961a0d0b9e0cab01a461bdef` |
| `0x010302FE` | 22584 | `09ddaf554d1c37eb7103fd01d92c9ab4c260bafdbc695ace78272bd366bd2cd5` |
| `0x010302FF` | 16 | `d7df27cf464e684cf2ccfc2b87feedd5f4063bdd23293aa20a5bf221d7bcb235` |
| `0x01030300` | 4200 | `606e92d3eabb23c157b658d2e5a1fd5c59c0f42d88075bd04589f79e44ba299f` |
| `0x01030559` | 1057 | `33a24238b929ae5f8ef8361e13c8a42775b3baff91ef95ac383b4506ef7a1f66` |
| `0x0103055A` | 67536 | `8f94c591f27de6e4fb4d420809d2c345e64b2af776ec9327e1047aaf0257fd5a` |
| `0x0103055B` | 16 | `c37ffebbfa8953dace4b22f6718212f2bca5b627b9f9fea32c130f45ee21733b` |
| `0x0103055C` | 4200 | `b24dca19775be26346abf1489cf991bb4e457065e092f8f8fc118b19244b1368` |
| `0x27950000` | 293 | `246c4af86271f0d90475c8f73d67aaed5eae0cc6915995624e96aca2f9ba9251` |
| `0x2795008E` | 1132 | `9c8aa2516d87fcce5ed44268de209d5fc87f2e9611941190a6e120f3aae482e9` |
| `0x2795008F` | 22360 | `60a2de8b8212304b3136eac93542c26699c65a64e52ab23cbd620e8e7bdb3999` |
| `0x27950090` | 16 | `fe7d9253a6b6a42580f3e2eaed92568d3694985c49dbd6348315da0e6b97e3f8` |
| `0x27950091` | 4048 | `d4ee90fe19fac3d67abaa7f0c378c667bdfe4a774bf086cf6e46affb5d90a021` |

## Binding-string differences

In `key_config.csv` row 4, column 3 carries substitutions with defaults
W/S/A/D and NumPad8/NumPad2/NumPad4/NumPad6. Row 5 carries Q/E defaults in
the horizontal-movement substitutions. In `key_config3.csv`, the corresponding
primary defaults remain, while the secondary movement defaults are empty.
`key_config2.csv` row 13 instead carries literal numeric-keypad names.
These observations concern column 3; additional string columns contain
variants and must not be silently substituted for it.

The row values establish a static association between the command name and
binding text. They do not alone establish native column consumption, markup
parsing, successful object construction, configuration overrides, active
provider selection, a selected character, or command execution. Those joins
require the corresponding native consumer evidence.
