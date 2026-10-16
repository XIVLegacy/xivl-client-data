# Grand Company rank rows

[`derived/gc_rank.csv`](../derived/gc_rank.csv) preserves all 22 `gcRank.csv`
rows and three positional English/Japanese name variants per row, producing
66 records. The row IDs join exactly to `xtx_gcRank.csv`. Source sheet IDs are
`gcRank` `0x0103057E` and `xtx/gcRank` `0x0B450BA8` in
[`sheet_inventory.csv`](../manifests/sheet_inventory.csv).

[`manifests/retail_sheet_exports.json`](../manifests/retail_sheet_exports.json)
pins the source bytes, typed positions, text positions and output identity for
extraction `2012.09.19.0001`.

## Columns and name variants

Column numbers are zero-based sheet positions after the CSV row ID.

| Output | Source |
|---|---|
| `rank_id`, `source_row` | Exact row ID in both sheets |
| `name_variant` | Positional variant 0, 1 or 2 |
| `company` | `unresolved` |
| `name_en` | `xtx_gcRank.csv` column 9, 10 or 11 for variant 0, 1 or 2 |
| `name_ja` | `xtx_gcRank.csv` column 3, 4 or 5 for variant 0, 1 or 2 |
| `linear_rank` | `gcRank.csv` column 0 (`u8`), returned by `getGrandCompanyRankLinear` |
| `seal_maximum` | Column 1 (`s32`), returned by `getGrandCompanySealMax` |
| `seals_needed_next_rank` | Column 2 (`s32`), returned by `getGrandCompanyNeedSealNextRank` |
| `icon_company_1`, `icon_company_2`, `icon_company_3` | Columns 6, 7 and 8 (`s32`), selected by the status widget for companies 1, 2 and 3 |

For rank row 11, the English variants read `Storm Private Third Class`,
`Serpent Private Third Class` and `Flame Private Third Class`. The variant
number is an export position, not a company identifier. No verified client
consumer mapping binds these positions to numeric company IDs here.

All typed values are retained verbatim. For example, row 11 carries column 0
= `1`, column 1 = `10000`, column 2 = `1000`, and columns 6 to 8 =
`641,671,701`. The named fields describe the client getters and status display.
They do not prove that a promotion debits the reported next-rank seal value,
or that every exported rank is available. Row 0 and the remaining unusual
rank keys are retained rather than filtered into a presumed promotion ladder.

The mapping evidence is
`xivl-client-scripts:docs/gc-promotion-client-contract.md`, section
`Player state and sheet consumers`. `PlayerBaseClass` prototypes `0.13`,
`0.14` and `0.15` read columns 0, 1 and 2 at CALL PCs `25`, `12` and `12`
(decoded offsets `0x14C8`, `0x15A1` and `0x1660`). Status widget prototype
`0.8` selects columns 6 to 8 at arithmetic PCs `8-9` and data CALL PC `10`
(`0x10CA-0x10D2`). The source identity table in that contract pins the decoded
player payload to SHA-256
`1530dc2b53353888ccc6b47f78920ebd2c2d876335b9968196312153b0db464a`
and status payload to
`c28038e3c596621b0e87d7a9fd5d2857274a836fedaabd6a83ffaf4729e5b070`.
These are zero-based prototype PCs in the decoded Lua 5.1 chunks.

The manifest's `typedColumns` maps every named output field back to its exact
source position. The verified company-to-icon selection does not resolve
the separate company-to-name-variant join.

`memberRank.csv` is a separate five-row typed sheet with row IDs 0, 1, 4, 7 and
10, pinned by [`tables.json`](../manifests/tables.json). No join from that sheet
to Grand Company rank rows is established. The export does not apply it.

The data establishes static rank keys, name variants and values used by the
client getters and display. The cited client contract owns officer dialogue.
Server seal transactions, promotion requirements and rank availability remain
unestablished. The [rank/cap finding](rank-cap-findings.md)
owns the wider rank-sheet boundary.

## Reproduction

Run `python tools/build_retail_sheet_exports.py --csv-dir <root>` to regenerate
all four sheet products and the shared manifest. Add `--check` to verify
without writing. Run `python tools/test_retail_sheet_exports.py` for the
targeted checks, with `XIVL_CSV_DIR` set for complete source-cell fidelity and
source authentication tests. `tools/validate_corpus.py` verifies the public
products and reproduces them from a supplied corpus.
