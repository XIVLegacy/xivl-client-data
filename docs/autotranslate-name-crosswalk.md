# Localized name and key crosswalk

`derived/autotranslate_name_crosswalk.json` is the reproducible localized-name
crosswalk for the authenticated FFXIV 1.23b extraction
`2012.09.19.0001`. It records fixed-phrase, item-name, place-name, and zone
associations while preserving every duplicate name and every candidate join.
The generator is `tools/build_autotranslate_name_crosswalk.py`.

The producing method verifies byte count and SHA-256 for eight authenticated
source sheets, reads their row keys and localized cells, joins items by equal
row keys, joins zones through `_zoneParam` field 0 and place-name row keys,
retains every zone-group membership column, and attaches existing zone names
only as source-product candidates. Confidence is high for source-cell/key
equality. It does not extend to UI selection, wire tokens, token framing, or
runtime zone/item selection.

## Reproduction

Hydrate the approved decoded CSV archive into an external directory, verify
the archive with `tools/private_csv_corpus.py`, and run:

```
python tools/build_autotranslate_name_crosswalk.py --csv-dir <csv-root>
python tools/build_autotranslate_name_crosswalk.py --csv-dir <csv-root> --check
python tools/test_autotranslate_name_crosswalk.py
```

The generator checks every input byte count and SHA-256 against
`manifests/tables.json`. The JSON source block records the corpus input id,
archive digest, expanded tree digest, and the hashes of all eight source
sheets. It also records the hash of the existing
`manifests/zone_internal_names.json` product used for internal-name candidates.
The output is ASCII JSON with escaped localized cells and stable numeric
ordering. Source locators use exact CSV row ids and zero-based columns; they do
not claim physical line numbers.

## Records and source fields

Each record has a stable id, numeric key, localized field values, and source
sheet row and column locators. Empty locale cells are represented by `null`.
The `localeColumns` object gives the raw zero-based fields retained for each
language:

- `xtx__fixedPhrase.csv`: Japanese 2-3, English 4-5, German 6-7, French 8-9.
- `xtx_itemName.csv`: Japanese 4, English 5-7, German 11-12 and 14, French
  19-21.
- `xtx_placeName.csv`: Japanese 0, English 1-2, German 4-5, French 6-7.

The adjacent fields remain separate so grammatical, fallback, and encoded
forms cannot collapse into one name. `ambiguityGroups` indexes repeated values
by locale and raw column and lists every stable record id and numeric key.
The JSON also retains unsupported or unindexed localized fields: fixed-phrase
columns 10-11, item-name columns 25-32 and 131-134, and place-name column 8.
Their raw values and nulls are explicit under `unsupportedLocaleFields`.

Item records prove the row-id join across `_item.csv`, `itemData.csv`, and
`xtx_itemName.csv`. The `_item.csv` field 0 value is retained as a raw join
field and is not relabeled as a server type. No dated/current interpretation
is assigned to any item row.

Literal anchors include fixed-phrase row 974, field 0 = `9`, field 1 empty,
and English column 4 = `Map`; fixed-phrase row 100, field 1 = `@`, remains an
uninterpreted table cell. Item row 1000001 has `xtx_itemName.csv` column 5 =
`Gil` and `_item.csv` field 0 = `Money/MoneyStandard`. English column 5 =
`Bat Wing` occurs on item rows 10009506 and 12000016, while their `_item.csv`
field 0 values are respectively `Normal/StandardItem` and
`Normal/DummyItem`; both keys remain in the crosswalk.

Zone records join `_zoneParam.csv` field 0 to `xtx_placeName.csv` row ids and
retain all matching `_layout.csv` rows and `zoneGroupParam.csv` candidates.
Zone-group memberships retain the source row and membership column for every
candidate; no last-membership-wins projection is applied. For Limsa, the raw
rows are `_zoneParam` 133/230 field 0 = 1051, `zoneGroupParam` row 101 fields
0-5 = `1051,133,230,134,232,140`, and `_layout` rows 121/131/171 fields
1/2/3 = `2,800,1051`, `2,900,1051`, and `4,1,1051` respectively.
The existing zone-name product is shown only when it has an already promoted
candidate. Place-name 1051 (`Limsa Lominsa` in the English field) has zone ids
133 and 230, layout rows 121, 131, and 171, and no selected internal name.
The literal `Limsa Lominsa` occurs four times in place-name row 1051's English,
German, and French display fields, and zero times in `xtx__fixedPhrase.csv`.
That textual equality check does not establish a selection or token join.
Those records remain separate in the JSON.

## Selection boundary

The crosswalk is a client-extraction name/key index. The native wire-format
study in `xivl-client-structs:manifests/autotranslate_wire_format_study.json`
found no proven edge from a fixed-phrase lookup to a chat encoder or decoder.
Consequently the product does not assign a phrase row key or field 0 value to
wire bytes, infer token framing, or choose one zone/layout from a duplicate
place name. The `selectionBoundary` object carries these unresolved claims
explicitly.
