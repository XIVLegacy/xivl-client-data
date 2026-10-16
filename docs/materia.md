# Materia sheet rows and instructional text

[`derived/materia.csv`](../derived/materia.csv) preserves all 66 rows and all
80 typed columns of `materia.csv`. Row 0 remains in the export.
[`derived/materia_book.csv`](../derived/materia_book.csv) independently
preserves all 52 rows and all five text columns of `materiaBook.csv`.

The source sheet IDs are `materia` `0x01030582` and `materiaBook` `0x03A21DA8`
in [`sheet_inventory.csv`](../manifests/sheet_inventory.csv). Exact source and
output identities for extraction `2012.09.19.0001` are recorded in
[`manifests/retail_sheet_exports.json`](../manifests/retail_sheet_exports.json).

## Materia columns

`materia_id` and `source_row` preserve the source row ID. Named output columns
preserve the cells read by the client getters below. Columns are zero-based
source positions after the CSV row ID. No typed source column is omitted.

| Output | Source columns | Type |
|---|---|---|
| `catalog_id_quality_group_0` to `catalog_id_quality_group_3` | 0 to 3 | `s32` |
| `parameter_1` | 4 | `s32` |
| `value_1_quality_0` to `value_1_quality_15` | 5 to 20 | `s16` |
| `parameter_2` | 21 | `s32` |
| `value_2_quality_0` to `value_2_quality_15` | 22 to 37 | `s16` |
| `icon_quality_group_0` to `icon_quality_group_3` | 38 to 41 | `s32` |
| `materia_col_42` to `materia_col_79` | 42 to 79 | `bool` |

For example, row 1 begins with `10100001,10100002,10100003,10100004,15001`.
The client supplies a quality argument `q`. `getMateriaCatalogID(type,q)`
selects column `floor(q/4)`. `getMateriaIcon(type,q)` selects columns 38 to 41
for quality ranges 0 to 3, 4 to 7, 8 to 11 and 12 to 15. Thus a
`quality_group_N` suffix denotes `floor(q/4)` within the documented 0 to 15
domain, not a server grade encoding.

`getMateriaProperty(type,q)` returns the ordered values at columns
`4,5+q,21,22+q`. The two parameter/value pairs feed `getItemParamString` and
materia parameter labels. These mappings establish display-parameter use.
Columns 42 to 79 remain unnamed booleans. No column is labeled a catalyst,
success rate or eligibility rule. The table does not establish a meld formula,
conversion reward, loss rule or transaction result.

The consumer evidence is
`xivl-client-scripts:docs/materia-meld-client-contract.md`, section
`Sheet getters`. It identifies `desktopwidget_materia.lua:208-294` and pins
its decoded payload SHA-256 to
`834e5180a20668add24bafe7d94baa430dce855a13797d3038eab31a26392fb0`.
Property prototype `0.5` reads the four positions at CALL PCs `8,14,20,26`
(`0x798,0x7B0,0x7C8,0x7E0`). Icon prototype `0.6` reads at CALL PC `28`
(`0x8E5`). Catalog prototype `0.7` uses floor CALL PC `3` (`0x9CF`) and
data CALL PC `8` (`0x9E3`). PCs and prototype indices are zero-based in the
decoded Lua 5.1 chunk. The manifest's `typedColumns` records the complete
field-to-source-position mapping.

## Materia book

`text_id` and `source_row` preserve the `materiaBook.csv` row ID. Columns
`text_ja`, `text_en`, `text_de`, `text_fr` and `text_zh` preserve source columns
0 to 4. Text and encoded controls are retained without normalization.

The book is instructional prose. English row 1 identifies a treatise on
materia creation and application, row 2 offers a chapter selection, and rows
3 to 5 name creation, catalyst and melding chapters. These are text keys,
not demonstrated materia-type foreign keys. Overlapping integer row IDs do
not establish a join to `materia.csv`, so the exports remain independent.

This finding covers static sheet content and the named getter projections.
The cited client contract owns the request flow, widget results and remaining
packet boundaries.

## Reproduction

Run `python tools/build_retail_sheet_exports.py --csv-dir <root>` to regenerate
all four sheet products and the shared manifest. Add `--check` to verify
without writing. Run `python tools/test_retail_sheet_exports.py`, with
`XIVL_CSV_DIR` set to enable complete raw-cell and locale fidelity checks.
`tools/validate_corpus.py` validates public hashes, source pins, counts and
locators, then reproduces the exports when the selected corpus is present.
