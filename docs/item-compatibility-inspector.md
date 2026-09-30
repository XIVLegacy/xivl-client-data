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
bytes. Without identity-verified retained inputs, retail validation is
unperformed.
