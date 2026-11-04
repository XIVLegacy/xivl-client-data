# Selected var_wep visual column types

The retail `var_wep` definition and authenticated CSV headers agree on two
selected column ranges:

| Logical column, zero-based | Decimal position | Declared type | Raw CSV field, zero-based |
| --- | --- | --- | --- |
| `0xAB..0xBA` | 171..186 | `bool` | 172..187 |
| `0xBB..0xCA` | 187..202 | `f16` | 188..203 |

These are declaration and header facts from client extraction
`2012.09.19.0001`. They do not establish a selected weapon/model or runtime
row identity. The bounded stored-row check below covers source encodings only.

## Source definition

The `var_wep` row of [sheet_inventory.csv](../manifests/sheet_inventory.csv)
binds the sheet to resource `61276937` (`0x03A70309`), source `var_schema`.
The selected installed resource `data/03/A7/03/09.DAT` is 20743 bytes with
SHA-256
`5e0cf00b5a5f546f871879a660155ad32b1d09fd7df7533186ca09a578e33428`.
Its scrambled SSD version 0.1 document decodes through
[compare_sheet_inventory.py](../tools/compare_sheet_inventory.py),
`decode_document`/`unscramble`, including the encoded `F1` trailer convention.

The document contains one sheet named `var_wep`, mode `client`,
`column_max=204`, `column_count=204`, `cache=-1` and `type=none`, without a
language attribute. Its inline type and index lists contain 204 entries.
The index list is exactly `0..203`, so each selected logical index is also
its position in the type list. The two selected ranges have the declarations
shown above. This is a sheet definition, rather than a master reference to
another definition resource.

## CSV header association

The `var_wep.csv` entry of [tables.json](../manifests/tables.json) pins
2072972 bytes and SHA-256
`f04b923a94592d539ad12618673a076868c65e644e18f4186135a2a6a6b6d4b1`.
The selected retained archive matched
[private_csv_corpus.json](../manifests/private_csv_corpus.json). Its unique
exact `var_wep.csv` member matched the table's complete size and SHA-256,
and its ZIP CRC passed before header interpretation.

Only the first two CSV records were parsed. Both contain 205 fields: a
separate key field followed by 204 column fields. The first record labels
those fields `0..203`. The second has `bool` at logical positions 171..186
and `f16` at 187..202, agreeing with every selected definition entry.

[The CSV reader](../tools/_csv_reader.py), `read_csv` header and row parsing,
separates raw field 0 from the value fields. Thus logical column `j` occurs
at raw CSV field `j+1`. This is CSV serialization arithmetic. It does not
add one to the native sheet index or identify a row key, enabled ordinal or
runtime variant. No data row was parsed, displayed or retained, and no
archive member was extracted to a hydrated corpus.

## Selected stored-row encodings

The same authenticated definition's first one-slot file entry, ordinal 1
with zero-based ordinals, declares `begin=1001035000,count=1` and explicitly
names this resource triple. This selection minimizes declared row slots,
using definition order as a tie-break; it is not a row selected by an observed
WeaponVisual invocation.

| Role and installed path | Bytes | SHA-256 |
| --- | ---: | --- |
| Data `data/03/A7/06/82.DAT` | 394 | `21fff3b5efe486ec51903aa3f2ed35524a297e3f608500db2607bbb909953b83` |
| Enable `data/03/A7/06/83.DAT` | 8 | `df40a68c5a089ef6477eb63d574ee652d7dd120604b3e89b6e99a1f66eefe87e` |
| Offsets `data/03/A7/06/84.DAT` | 4 | `8d2f50703af28decdd8e9f407c074d71c12c059f9259a780a1697ca64e526b4b` |

Regular-file and ancestor checks excluded reparse points; whole-file size,
SHA-256 and repeat-read stability passed. The enable/offset framing from
[build_fixed_phrase_backing_rows.py](../tools/build_fixed_phrase_backing_rows.py),
`read_ranges`/`row_spans`, established the sole enabled/stored key 1001035000
and complete data span `[0,394)`. Both key sets agreed, and the final row end
consumed the whole data file.

The definition's fixed-width order is f16 at 0..170, bool at 171..186,
f16 at 187..202 and s32 at 203. Therefore each of the sixteen selected
f16 source words is at row-relative byte `358+2*i`, i=0..15, within
`[358,390)`. Only these words were classified, after the complete 394-byte
row span passed. All sixteen were positive-zero encodings. Counts for
negative zero, exponent-zero nonzero fractions, normal exponents 1..30 and
exponent 31 were zero. No other field was interpreted.

`xivl-decomp:docs/resource/excel-row-field-decoder.md`, "Type-8 conversion",
owns the native helper's special-case limits. This selected row contained
zero encodings where that native conversion differs from IEEE binary16.
The result covers one declared source row and sixteen columns. It excludes
neither exceptional encodings elsewhere nor a different runtime row, and
it does not demonstrate an extractor conversion defect.

## Native consumer boundary

`xivl-decomp:docs/actor/appearance-path-decoder.md`, "Request and delivery", owns the
native address formula `[row+8] + 4*map[column]`, with the map obtained through
the row's parent sheet. The native consumer's four-byte cell is a distinct
representation from the source declaration `f16`. These selected headers
alone do not establish that cell's conversion, the actual runtime sheet
metadata, a delivered row or the consumer's current object. The local source
types remain `bool` and `f16` regardless of a later consumer's load width.
