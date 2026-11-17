# Text command sheet rows

`xtx/_textCommand` is the sheet that the chat line parser matches a leading
`/word` against. This `client_extraction` finding records the row shape the
parser reads. Facts marked `STATIC` are decoded static client data for build
`2012.09.19.0001`. The parser that consumes the cells is documented in
[xivl-decomp:docs/input/text-command-parser.md](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/input/text-command-parser.md).

## Sheet identity

The sheet inventory row is `xtx/_textCommand`, resource id 189073651
(`0x0B4508F3`), in
[`manifests/sheet_inventory.csv`](../manifests/sheet_inventory.csv). The
extraction writes it as `xtx__textCommand.csv` with 125 data rows. The first
data key is 101 and the last is 334. The key is the first CSV cell. The
header row lists the logical columns 0 to 19. The type row reads
`u8`, `u8`, `s8`, `s8`, `s8`, then `str` in columns 5, 6, 7, 9, 10, 12, 13,
15, 16, 18 and 19, with an empty type in columns 8, 11, 14 and 17. STATIC.

## Numeric columns

The parser reads the three leading numbers through its row accessor. Column 0
is the token budget, column 1 is the count of leading numeric words, and
columns 2, 3 and 4 are the resolver kind of numeric word 0, 1 and 2.

| Column 0 | Column 1 | Columns 2, 3, 4 | Rows | Keys named |
| ---: | ---: | --- | ---: | --- |
| 1 | 0 | 0, 0, 0 | 23 | 101 `/say`, 102 `/shout`, 104 `/party` |
| 2 | 0 | 0, 0, 0 | 5 | 223, 224, 227, 240, 330 |
| 2 | 1 | 0, 0, 0 | 2 | 322 `/random`, 326 `/countdown` |
| 2 | 1 | 1, 0, 0 | 1 | 201 `/?` |
| 2 | 1 | 2, 0, 0 | 1 | 228 `/recast` |
| 2 | 1 | 3, 0, 0 | 84 | 213 `/names`, the emote words |
| 3 | 0 | 0, 0, 0 | 1 | 103 `/tell` |
| 3 | 1 | -1, 0, 0 | 1 | 230 `/item` |
| 3 | 1 | 0, 0, 0 | 1 | 219 `/marking` |
| 3 | 1 | 2, 0, 0 | 1 | 216 `/action` |
| 3 | 1 | 3, 0, 0 | 1 | 210 `/partycmd` |
| 3 | 2 | 0, 2, 0 | 1 | 231 `/equipaction` |
| 3 | 2 | 3, -1, 0 | 1 | 232 `/equip` |
| 3 | 2 | 3, 3, 0 | 1 | 296 `/display` |

The 125th row, key 297 `/textclear`, carries the extractor marker
`[@duplicate:N]` on the first four numeric cells. Its values are not read
here. STATIC, with the conflict count of the extraction log as the only
statement on it.

The keys 322 and 326 are the only rows with budget 2, count 1 and kind 0, a
numeric word that the parser resolves as a plain base 10 number.

## Text columns

In the rows named above, column 5 and column 9 hold the full word and column
10 holds the short alias in the same language set. Key 101 reads `/say` and
`/s`, key 103 `/tell` and `/t`, key 326 `/countdown` and `/count`, key 322
`/random` and `/dice`. Columns 5 and 9 are equal on 121 of the 125 rows. They
differ on keys 259, 295, 299 and 334. STATIC.

## Reproduction

Run `xivl extract <install> --output <dir>` from
[xivl-tools](https://github.com/XIVLegacy/xivl-tools), open
`xtx__textCommand.csv` and read the type row, the numeric cells and the text
cells of the keys above. Count the data rows below the type row.
