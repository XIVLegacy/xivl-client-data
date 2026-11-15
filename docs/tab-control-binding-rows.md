# Tab control binding rows

The three `key_config` sheets bind the `TabControl.NextTabItem` and
`TabControl.PreviousTabItem` commands, and the same keyboard gestures also
bind the target-cycle commands. The values below are decoded from the
retained source definitions of the retail install `2012.09.19.0001`, the
same resources as [Movement binding rows](movement-binding-rows.md). They
are not observations of a player's active configuration.

## Columns

Column numbers are the definition column indexes, which equal the labeled
columns of [Movement binding rows](movement-binding-rows.md). The
definitions type columns 0, 3, 4, 8, 10 and 12 to 15 as `str`, columns 1, 2,
5 and 9 as `s32`, and columns 6, 7 and 11 as `bool`. Column 8 is the
command and column 3 the binding string. Every selected row has 128 in
column 1, 0 in columns 5, 7 and 9, true in columns 6 and 11, and `**` in
column 10. Columns 12 to 15 repeat column 3. Column 4 is `**` except in
`key_config2` rows 48 and 1025, where it is `Shift`.

## `key_config` and `key_config3`

The two sheets agree on every row below.

| Row key | Column 2 | Column 3 | Command |
| ---: | ---: | --- | --- |
| 1037 | 0 | `[@KeyPrevTab1$=Tab Shift]` | `TabControl.PreviousTabItem` |
| 1038 | 0 | `[@KeyPrevTab2$=]` | `TabControl.PreviousTabItem` |
| 1039 | 0 | `[@KeyNextTab1$=Tab]` | `TabControl.NextTabItem` |
| 1040 | 0 | `[@KeyNextTab2$=]` | `TabControl.NextTabItem` |
| 1047 | 8 | `L2` | `TabControl.PreviousTabItem` |
| 1048 | 8 | `R2` | `TabControl.NextTabItem` |
| 67 | 0 | `[@KeyNextTarget1$=Tab]` | `RaptureCommands.ChangeTargetNext` |
| 69 | 0 | `[@KeyPrevTarget1$=Tab Shift]` | `RaptureCommands.ChangeTargetPrev` |

Column 0 of rows 1037 to 1040 is a Japanese label for moving the focus with
the Tab key, with a reverse suffix on rows 1037 and 1038 and a forward suffix
on rows 1039 and 1040. The binding strings are shown without the backslash
escape that `parse_sheet_string` adds before `[`.

`key_config` row 68 binds `RaptureCommands.ChangeTargetNext` to
`[@KeyNextTarget2$=NumPad0]` and `key_config3` row 68 leaves that slot
unbound. No other `TabControl` row exists in either sheet.

## `key_config2`

Column 3 holds the bare key name, with the modifier in column 4.

| Row key | Column 2 | Column 3 | Command |
| ---: | ---: | --- | --- |
| 1025 | 0 | `Tab` | `TabControl.PreviousTabItem` |
| 1026 | 0 | `Tab` | `TabControl.NextTabItem` |
| 1027 | 8 | `L2` | `TabControl.PreviousTabItem` |
| 1028 | 8 | `R2` | `TabControl.NextTabItem` |
| 46 | 0 | `Tab` | `RaptureCommands.ChangeTargetNext` |
| 48 | 0 | `Tab` | `RaptureCommands.ChangeTargetPrev` |

## Interpretation and limits

INFERRED. In `key_config` and `key_config3` one Tab press is bound both to
`TabControl.NextTabItem` and to `RaptureCommands.ChangeTargetNext`, and
Shift+Tab to the two previous commands.

UNKNOWN. Which control receives a `TabControl` command, the order in which
the client resolves a gesture bound to two commands, and which of the
three sheets the client selects at runtime.

## Source identity and reproduction

| Sheet | Resource | Kind | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| `key_config` | `0x0103016A` | data | 67221 | `d9e380a32a0060c4db47ff22aa41ed21ed2672bc3e09cc14d75016d0f82a48b6` |
| `key_config` | `0x0103016B` | enable | 16 | `c37ffebbfa8953dace4b22f6718212f2bca5b627b9f9fea32c130f45ee21733b` |
| `key_config` | `0x0103016C` | offset | 4200 | `42dc9d1509f9c77eafb09a459b777e8c20f060d0278242b718a5fdedef2d07bb` |
| `key_config2` | `0x010302FE` | data | 22584 | `09ddaf554d1c37eb7103fd01d92c9ab4c260bafdbc695ace78272bd366bd2cd5` |
| `key_config2` | `0x010302FF` | enable | 16 | `d7df27cf464e684cf2ccfc2b87feedd5f4063bdd23293aa20a5bf221d7bcb235` |
| `key_config2` | `0x01030300` | offset | 4200 | `606e92d3eabb23c157b658d2e5a1fd5c59c0f42d88075bd04589f79e44ba299f` |
| `key_config3` | `0x0103055A` | data | 67536 | `8f94c591f27de6e4fb4d420809d2c345e64b2af776ec9327e1047aaf0257fd5a` |
| `key_config3` | `0x0103055B` | enable | 16 | `c37ffebbfa8953dace4b22f6718212f2bca5b627b9f9fea32c130f45ee21733b` |
| `key_config3` | `0x0103055C` | offset | 4200 | `b24dca19775be26346abf1489cf991bb4e457065e092f8f8fc118b19244b1368` |

Read each definition with `decode_document` and `resource_path` in
[compare_sheet_inventory.py](../tools/compare_sheet_inventory.py), and the
enable ranges and row spans with `read_ranges` and `row_spans` in
[build_fixed_phrase_backing_rows.py](../tools/build_fixed_phrase_backing_rows.py).
Decode each row in column order with `parse_sheet_string` in
[build_attributive_backing_rows.py](../tools/build_attributive_backing_rows.py)
for `str`, little-endian 32-bit integers for `s32` and one byte for `bool`,
and require every row to consume its span exactly.
