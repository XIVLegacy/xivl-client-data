# Soft hyphen token census

The installed sheets hold one byte form of the rich-text code `0x16`, the four
bytes `02 16 01 03`. This page counts it in a static sheet export and records
the longest cells without a token.

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

The export holds 38421 `soft-hyphen` markers, in 10571 cells of 428 files.
Every marker carries the token hex `02160103`. No `[@duplicate:` alternate in
the export, once its hex is decoded, holds a `soft-hyphen` marker or those four
bytes.

## Five-string-column sheets

676 files declare exactly five columns, each of type `str`. They hold 43797
rows and 24375 of the markers. The counts below are by column ordinal.

| Ordinal | Rows with a marker | Markers | Files with a marker |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 |
| 1 | 10 | 30 | 1 |
| 2 | 2560 | 7460 | 336 |
| 3 | 4408 | 16885 | 376 |
| 4 | 0 | 0 | 0 |

The one file with a marker at ordinal 1 is `xtx__text_ui.csv`.

For the client's named language fields,
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, Default
table and named language fields, maps `ja`, `en`, `de` and `fr` to reference
fields 0 to 3. This census reports ordinals. It does not check the language
selection of each of the 676 definitions.

In `xtx__text_ui.csv` the rows with a marker at ordinals 0 to 4 number 0, 10,
184, 172 and 0. Row 1009 holds three markers at ordinal 1 and none at the other
ordinals. The export also writes a second file, `xtx__text_ui(2).csv`, which
this paragraph does not count.

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
