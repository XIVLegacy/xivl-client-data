# Guildleve display names

[`derived/guildleve_names.csv`](../derived/guildleve_names.csv) joins all 624
`guildleve.csv` row IDs to their English and Japanese display-name cells in
`xtx_guildleve.csv`. It preserves duplicate names, placeholders, punctuation,
and decoded locale text without normalization. The stable consumer citation is
`xivl-client-data:derived/guildleve_names.csv`.

The [product manifest](../manifests/guildleve_names.json) pins the complete
source and output byte identities for extraction `2012.09.19.0001`.
The source [table manifest](../manifests/tables.json) and
[sheet inventory](../manifests/sheet_inventory.csv) identify `guildleve` as
sheet `0x010300E5` and `xtx/guildleve` as sheet `0x0B450013`.

## Columns and categories

Positions are zero-based after the source row ID, matching
[`tools/mappings/guildleve.py`](../tools/mappings/guildleve.py).
Both sources have exactly the same 624 row IDs.

| Output column | Source or rule |
| --- | --- |
| `guildleve_id` | `guildleve.csv` row ID |
| `name_en` | `xtx_guildleve.csv` position 10 |
| `name_ja` | `xtx_guildleve.csv` position 9 |
| `placeholder` | `true` only for the exact EN cell `x`, `dummy`, or the Japanese no-translation marker U+7FFB U+8A33 U+4E0D U+8981 |
| `category` | `guildleve.csv` position 1, mapped as below |
| `source_sheet` | `xtx/guildleve` |
| `source_row` | Text-sheet row ID, equal to `guildleve_id` |

The category is a grouping of the mapped `classType` value: 1 becomes
`battlecraft` on 505 rows, 2 becomes `fieldcraft` on 99 rows, and all other
values become `other`. All 20 `other` rows have value 4 and belong to the
Horn and Hand faction block described in
[selected row values](guildleve-selected-row-values.md#faction-guildleve-rows).
There are no `local` rows in this source. Category does not establish runtime
eligibility or the playable subset.

## Placeholder and duplicate names

There are 262 placeholders: 54 `x`, 194 `dummy`, and 14 no-translation cells.
The complete observed ID ranges follow. These are exact EN values, even when
the Japanese name is populated.

| EN cell | Guildleve IDs, inclusive |
| --- | --- |
| No-translation marker | 0, 2-11, 47-49 |
| `x` | 1021-1025, 1120, 1215-1220, 10829-10835, 10849-10855, 10869-10875, 10889-10895, 10941-10944, 10961-10964, 11001-11003, 11021-11023 |
| `dummy` | 10910-10915, 10930-10935, 10945-10948, 10965-10968, 10981-10988, 11005-11008, 11024-11028, 11041-11048, 11441-11455, 11461-11468, 11602, 11629-11635, 11649-11655, 11669-11675, 11689-11695, 11710-11715, 11730-11735, 12229-12235, 12241-12255, 12402, 12429-12435, 12449-12455, 12469-12475, 12489-12495, 12510-12515, 12530-12535, 13029-13035, 13041-13055 |

IDs 10801 and 10802 both have the English name `My Very First Adventure`
and identical Japanese name cells. Both rows remain distinct. A name alone
is not a unique guildleve key.

## Reproduction and limits

Select the [hydrated corpus](corpus-inventory.md) with `XIVL_CSV_DIR` or
`--csv-dir`, then run:

```powershell
python tools/build_guildleve_names.py
python tools/build_guildleve_names.py --check
python tools/test_guildleve_names.py
python tools/validate_corpus.py
```

The builder authenticates both source files against `tables.json`, checks
their layouts and complete row-ID join, and writes the CSV and manifest.
The normal validator checks the public product, schema, counts and hashes.
With a hydrated corpus it also runs the builder's `--check` mode.

The artifact establishes the extracted client display-name cell per ID. It
does not establish server enum identifiers, availability, objective semantics,
or local guildleve names. Local IDs such as 120005 belong to
`passiveGL_craft.csv` and use the separate product below.

The raw `aetheryte.csv` label row is ` ,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14`; no column label names a guardian.

## Local guildleve names

[`derived/local_guildleve_names.csv`](../derived/local_guildleve_names.csv)
preserves the English and Japanese titles for all 169 `passiveGL_craft.csv`
row IDs. The local journal title lookup resolves the same row ID in
`xtx_quest.csv`, taking English from position 2 and Japanese from position 1.
It is independent of `passiveGL_craft` positions 8-11. The client consumer
and title-control evidence is recorded in
`xivl-client-scripts:docs/passivegl-craft-columns.md`.

[`manifests/local_guildleve_names.json`](../manifests/local_guildleve_names.json)
pins the source and output hashes and the exact UI text 4219 controls.
Regenerate with `python tools/build_local_guildleve_names.py`, verify with
`python tools/build_local_guildleve_names.py --check`, and run
`python tools/test_local_guildleve_names.py` for focused checks. Select the
hydrated corpus as above. Test and dummy titles remain verbatim. This product
does not establish availability or server behavior.
