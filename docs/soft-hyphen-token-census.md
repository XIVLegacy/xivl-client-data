# Soft hyphen token census

Every top-level `soft-hyphen` marker in a static sheet export carries the four
bytes `02 16 01 03`, the token of rich-text code `0x16`. This page counts those
markers, counts the same four bytes inside the hex of other rich tokens, and
records the longest cells without a token.

## Input and method

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. The instrument is `xivl extract` from `xivl-tools` at
revision `9c44b51f15c6e4ecef8e928145fc67f7633f1be7`. It wrote 803 CSV files
from 803 sheet documents with 183678 rows, and reported 639 missing trailing
values, 195 absent blocks and 57 conflicting values. The export writes each
rich-text token as `[@name:<token-hex>]` and names code `0x16` `soft-hyphen`.
The contract is in `xivl-tools:docs/formats/ssd-sheet.md`, Static-sheet CSV
export. No exported row text is distributed here.

The export of `xtx__text_ui.csv` is 1284564 bytes, 4355 data rows, SHA-256
`23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece`.
[local_guildleve_names.json](../manifests/local_guildleve_names.json) pins the
same digest and row count.

## Token form

A top-level marker is a `soft-hyphen` marker that the cell text holds itself.
The export holds 38421 of them, in 10571 cells of 428 files. Every one carries
the token hex `02160103`. No `[@duplicate:` alternate in the export, once its
hex is decoded, holds a `soft-hyphen` marker or those four bytes.

The same four bytes also occur 744 times inside the decoded token hex of other
rich tokens, which the export does not write as `soft-hyphen` markers. By the
name of the enclosing token, `if` holds 650, `switch` 93 and `sheet` 1. These
nested occurrences are in 171 cells of 84 files. 154 of those cells, in 75
files, hold no top-level marker. The search covers every token other than
`soft-hyphen` and `duplicate` markers and matches the four bytes at byte
boundaries. It does not parse the enclosing token, and it does not look for
another byte form of code `0x16`.

## Five-string-column sheets

676 files declare exactly five columns, each of type `str`. They hold 43797
rows, 24375 of the top-level markers and 599 of the nested occurrences. The
counts below are by column ordinal. The first table counts top-level markers
only.

| Ordinal | Rows with a marker | Markers | Files with a marker |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 |
| 1 | 10 | 30 | 1 |
| 2 | 2560 | 7460 | 336 |
| 3 | 4408 | 16885 | 376 |
| 4 | 0 | 0 | 0 |

The one file with a top-level marker at ordinal 1 is `xtx__text_ui.csv`.

The second table counts nested occurrences only. Its last column counts the
cells that hold a nested occurrence and no top-level marker.

| Ordinal | Rows with a nested occurrence | Occurrences | Files | Cells without a top-level marker |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 64 | 319 | 41 | 58 |
| 3 | 75 | 280 | 51 | 66 |
| 4 | 0 | 0 | 0 | 0 |

For the client's named language fields,
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, Default
table and named language fields, maps `ja`, `en`, `de` and `fr` to reference
fields 0 to 3. This census reports ordinals. It does not check the language
selection of each of the 676 definitions.

In `xtx__text_ui.csv` the rows with a top-level marker at ordinals 0 to 4
number 0, 10, 184, 172 and 0, with 0, 30, 660, 718 and 0 markers. Nested
occurrences number 0, 0, 19, 19 and 0, in 0, 0, 3, 3 and 0 cells that hold no
top-level marker. Row 1009 holds three top-level markers at ordinal 1 and none
at the other ordinals. The export also writes a second file,
`xtx__text_ui(2).csv`, which this paragraph does not count.

## Cells without a token

The lengths below are the UTF-8 byte lengths of cells in the 676 files that
hold no `[@` marker, after the export's backslash escapes are removed.

| Ordinal | Longest cell, bytes | Cells longer than 256 bytes |
| ---: | ---: | ---: |
| 0 | 750 | 318 |
| 1 | 902 | 1824 |
| 2 | 856 | 1028 |
| 3 | 751 | 443 |
| 4 | 529 | 146 |

One example is row 330 of `man0g1.csv`. Its ordinal 1 cell holds no marker and
is 295 bytes. That export is 222706 bytes with SHA-256
`e61129b46b468eef5f410966bd24d87e5317d6acb3db7f415b03bc389734e3a8`.

## Limits

A stored cell length is not a formatted length. These counts establish no
length bound of the client, no row that a script or server selects, and no line
break or glyph. The native handling of the token is in
`xivl-decomp:docs/resource/rich-text-soft-hyphen.md`.
