# var_equip sound kind column

Column 110 of the `var_equip` sheet is a signed 32-bit number on every row.
The client reads it as the gear sound kind of a gear part. This
`client_extraction` finding records the column and its value distribution for
build `2012.09.19.0001`. The reader and the decode of the value are in
[xivl-decomp:docs/actor/gear-sound-kind-bytes.md](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/actor/gear-sound-kind-bytes.md).

## Column and shape

The extraction `var_equip.csv` has 32277 data rows below a header row and a
type row. Each row has its key in the first cell and 111 logical columns 0 to
110. Columns 108, 109 and 110 are all typed `s32`. The client reads the same
row object with the keys 108 for the texture path number, 109 for the texture
number and 110 for the sound kind. STATIC for the type row, INFERRED that the
accessor key equals the logical column index, which the equal tally below
supports for key 110.

## Value distribution

| Value | -1 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 or more |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Rows | 6 | 27947 | 2045 | 1169 | 82 | 171 | 370 | 487 | 0 |

The counts sum to 32277. MEASURED.

## Reproduction

Run `xivl extract <install> --output <dir>` from
[xivl-tools](https://github.com/XIVLegacy/xivl-tools), read
`var_equip.csv`, skip the first two rows and count the integer in the last
cell of each remaining row. The names of the kinds are not recorded in the
sheet or in this finding.
