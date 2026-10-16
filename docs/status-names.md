# Status names and typed sheet values

[`derived/status_names.csv`](../derived/status_names.csv) exports every row of
`status.csv`, joined by the exact row ID to `xtx_status.csv`. It contains 399
rows, including row 0. Extraction `2012.09.19.0001` and the exact source and
output identities are recorded in
[`manifests/retail_sheet_exports.json`](../manifests/retail_sheet_exports.json).
The source sheet IDs are `status` `0x01030198` and `xtx/status` `0x0B450073`
in [`sheet_inventory.csv`](../manifests/sheet_inventory.csv).

## Columns and limits

Column numbers are zero-based sheet positions after the CSV row ID.

| Output | Source |
|---|---|
| `status_id`, `source_row` | Exact row ID in both source sheets |
| `name_en` | `xtx_status.csv` column 3 |
| `name_ja` | `xtx_status.csv` column 1 |
| `icon_text` | Exact decoded control text in `xtx_status.csv` column 24 |
| `placeholder` | Exact English cell matches a declared placeholder marker |
| `status_col_N` | Unmodified typed `status.csv` column N |

The typed source columns are 25 and 42 (`s32`), 31, 47 and 53 (`float`),
55 (`s8`), and 51, 52, 54, 56, 57 and 58 (`bool`). Empty values remain empty.
The manifest records every selected position and its source type.

The export preserves flags and numeric values without assigning them category,
icon-ID, duration or effect semantics. Those names require a retained client
getter or another verified mapping. `icon_text` preserves the encoded icon
control, including duplicate/conflict controls, without decoding a numeric icon
identifier. It is separate from the unnamed numeric column 25.

There are 95 rows with English name `-`. These are the only rows classified as
placeholders in this corpus. The generator also recognizes exact empty,
`****`, `x`, `dummy` and the Japanese no-translation marker declared in the
manifest. Classification does not establish whether the client uses a row.
Duplicate names, Japanese source text and encoded controls remain unchanged.
The table establishes static names and values, not server effect formulas,
stacking, ticks, applied durations or retail availability.

## Selected name families

| Family | Status IDs and exact English names |
|---|---|
| Party bonuses | 223193 `Comradery`; 223194 `Strength in Numbers` |
| Party-bonus dummy labels | 223195 and 223196 have English `-` and Japanese dummy bonus names |
| Reraise | 223131 `Reraise` |
| Shell | 223130 `Shell` |
| Bio | 223135 `Bio` |
| Dia | 223136 `Dia` |
| Burn | 223148 `Burn`; 223272 `Deep Burn` |
| Choke | 223152 `Choke` |

The party-bonus descriptions in `xtx_status.csv` column 21 explicitly name a
light party of 4 to 7 members for row 223193 and a full party of 8 members for
row 223194. Rows 223195 and 223196 are included because their Japanese names
carry the corresponding dummy bonus labels. `Deep Burn` is listed by its
literal name; this does not make it the same effect as `Burn`.

Neither source sheet contains row 223995. No Japanese or English name or
description contains `level sync`, `level-sync` or the Japanese level-sync
label. This is a bounded sheet finding and does not establish whether another
client path or retail rule implements level sync. The separate
[status row absence finding](status-row-absence.md) covers row 230116.

## Reproduction

Run `python tools/build_retail_sheet_exports.py --csv-dir <root>` to regenerate
the status, rank, materia and materia-book products with their shared manifest.
Add `--check` to compare without writing. Inputs must match
[`tables.json`](../manifests/tables.json) exactly. Run
`python tools/test_retail_sheet_exports.py` for join, locale, source-identity
and mutation checks. Set `XIVL_CSV_DIR` to enable the complete corpus tests.

[`validate_corpus.py`](../tools/validate_corpus.py) checks public provenance,
hashes, counts and locators, and reproduces all products when the corpus is
present. The [SubStat crosswalk](substat-status-join.md) owns the wire-ID
translation and packed-word projections.
