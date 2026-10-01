# Item compatibility inspection

`tools/inspect_item_compatibility.py` reads one item catalog ID and class/job
skill ID and prints the source row chain, selected sheet column, stored signed
integer, and client factor. It writes no files.

```powershell
python tools/inspect_item_compatibility.py <catalog-id> <skill-id> --csv-dir <csv-root>
```

Both IDs are decimal integers. The catalog ID is a `u32`; supported skill IDs
are 1 through 44, matching the compatibility projection in
[command battle parameters](command-battle-params.md#1-compatibility-projection).
CSV-root selection and filesystem restrictions follow
[the tooling contract](../tools/README.md): `--csv-dir`, then `XIVL_CSV_DIR`,
then the ignored repository-local `csv/` cache.

## Source join and value contract

The inspector follows the existing [item mapping](../tools/mappings/items.py):
`_item.csv` supplies the catalog row, and `itemData.csv` joins on that same row
ID. No catalog cell is used as an alternate item-data key. `itemData.csv`
column 48 is an `s32` compatibility key; that key selects the row of
`compatibility.csv`. Skill `N` selects sheet column `8 + (N - 1)`.
Sheet columns count from zero after the CSV row-ID field, as implemented by
[`CsvRow.values`](../tools/_csv_reader.py).

The selected compatibility cell must declare `s8` and contain an integer in
`[-128, 127]`. The client factor is the stored integer divided by 100, without
clamping or unsigned reinterpretation. A stored `-1` therefore reports
`-0.01`; a stored `0` reports `0.00`.

Missing files or rows, missing columns, blank cells, wrong declared types,
malformed integers, and out-of-range integers fail with a source-specific
error and nonzero exit status. They produce no numeric report. A compatibility
key of zero remains an ordinary row lookup; it does not imply a stored zero.
The shared typed coercion is used only after checking for a blank cell, so its
seed-export blank-to-zero convention does not apply to this inspection.

## Equipment eligibility and evidence limits

The promoted client helper contract is
`xivl-client-scripts:docs/item-equipment-compatibility.md`, under "Recovered
helper contract". For extraction `2012.09.19.0001`, `getItemCompatibilityKey`
reads item-data field 48 and `getItemCompatibilityData` reads the selected
compatibility cell and divides it by 100. `getItemCompatibility` supplies the
actor's `getMainClassOrJob` value. `canEquipSimple` rejects an exact zero
compatibility result before applying tribe and required-level checks.

A zero report matches that observed rejection. A nonzero report only avoids
that particular rejection; it does not establish complete equipment
eligibility. The inspector accepts a supplied skill ID and does not recover an
actor's active class/job or evaluate tribe, required level, unlocks, soul rules,
or server policy. Compatibility-based combat scaling and the item catalog ID
to appearance mapping remain unresolved by this lookup. The latter boundary
is retained in [item/equipment columns](item-equipment-columns.md).

Synthetic tests exercise the joins and error distinctions:

```powershell
python tools/test_item_compatibility.py
```

Synthetic results are not retail validation. For retained retail inputs, first
establish their declared identities against [tables.json](../manifests/tables.json)
using the hydrated-corpus validation procedure in
[retail input validation](ai_agents/retail-input-validation.md#local-verification).
The public-tree absence check validates metadata and public products, not CSV
bytes.

## Retained retail row checks

The retained input was extraction `2012.09.19.0001`, input ID
`decoded-csv-corpus-1.23b`. Its archive size, SHA-256, private source revision,
and expanded tree identity are pinned in
[`private_csv_corpus.json`](../manifests/private_csv_corpus.json).
`tools/verify_retail_csv_corpus.py --archive <archive>` verified the archive
and every member; `tools/private_csv_corpus.py hydrate <archive> <csv-root>`
hydrated a separate plain directory. `tools/validate_corpus.py` passed against
that directory with `XIVL_CORPUS_ABSENT` unset.

The producing inspector, verifier, hydration tool, and identity manifests were
at revision `1326bc2d7d31559b8000dff8de3f510429301125`.
The source identities are the `_item.csv`, `itemData.csv`, and
`compatibility.csv` entries in [`tables.json`](../manifests/tables.json) at
that revision. Their sizes and SHA-256 digests matched the retained files.

A separate standard-library CSV reader used no inspector or lookup helpers.
It joined `_item.csv` and `itemData.csv` by the same row ID, read the `s32` key
at item-data column 48, and read the declared `s8` compatibility cell at
column `8 + (N - 1)`. Columns below count from zero after the row-ID field.
All 44 skills for each documented gear anchor matched the inspector CLI's
row IDs, key, column, stored integer, and factor. One additional retained
fractional result also matched, for 133 comparisons in total.

| _item / itemData row ID | itemData column 48 / compatibility row ID | Skill N | Compatibility column | Stored s8 | Factor |
|---|---|---:|---:|---:|---:|
| `8030423` | `1001` | 1 | 8 | 100 | 1.00 |
| `8030423` | `1001` | 44 | 51 | 100 | 1.00 |
| `8011608` | `2004` | 1 | 8 | 100 | 1.00 |
| `8011608` | `2004` | 29 | 36 | 0 | 0.00 |
| `4030013` | `2131` | 44 | 51 | 0 | 0.00 |
| `4050001` | `2001` | 1 | 8 | 1 | 0.01 |

These are selected row observations, not an exhaustive item/skill validation.
No negative value occurred in columns 8-51 across the 219 retained
compatibility rows (9636 cells); negative-value and malformed-input behavior
remain covered by the synthetic tests. No inspector defect was demonstrated.
The local corpus check does not establish hosted retail-CI reproduction.
Nonzero compatibility retains the equipment-eligibility and appearance limits
above. CSV bytes and full row reports are not public products.
