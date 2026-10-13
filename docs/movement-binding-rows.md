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
`0x01030169`, `0x010301D4` and `0x01030559`. This inventory does not by itself
identify which duplicate extraction product a particular native request uses.

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
