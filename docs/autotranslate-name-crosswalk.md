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

## Backing-row identities

`manifests/fixed_phrase_backing_rows.json` compares the named backing resources
with the authenticated merged CSV. The game master resource `0x01030000`
names `xtx/_fixedPhrase` at definition resource `0x0B4508E6`. The report pins
their hashes and each locale's data, enable and offset resources. It retains
selected row spans and metadata rather than reproducing a complete schema.

Reproduce with an explicit preserved 1.23b client install and the authenticated
CSV root:

```
python tools/build_fixed_phrase_backing_rows.py --client-root <install> --csv-dir <csv-root>
python tools/build_fixed_phrase_backing_rows.py --client-root <install> --csv-dir <csv-root> --check
python tools/test_fixed_phrase_backing_rows.py
```

The enable resources name ordered `(base,count)` ranges. Their expanded keys
equal the nonempty row spans independently recovered from the offset files.
Every backing row's field 0 agrees with the same keyed CSV row. These checks
establish backing-to-extraction identities, not loaded native cache contents.

| Definition locale | Enabled rows | Name columns in merged CSV | Offset entries |
|---|---:|---|---:|
| ja | 756 | 2-3 | 2926 |
| en | 756 | 4-5 | 2926 |
| de | 756 | 6-7 | 2926 |
| fr | 756 | 8-9 | 2926 |
| chs | 600 | 10-11 | 2036 |

All five definitions declare 2926 slots beginning at key 100. The chs offset
file omits trailing empty slots. Its enabled keys still agree with its
nonempty spans. The union across locales equals the 758 merged CSV keys.
Rows 2115 and 2133 occur only in chs. The other four locales have identical
enable resources and key sequences. The chs tag identifies a shipped
definition, not an observed runtime language choice.

Sparse anchors distinguish a backing-file ordinal, a row key and field 0.
For ja/en/de/fr, row 974 has enabled ordinal 278 and field 0 = 9. Row 1255
has ordinal 436 and field 0 = 10. Row 3025 has ordinal 755, while its merged
CSV iteration index is 757. The chs ordinal of row 974 is 247. None of those
ordinals is an observed Completion index or selected control argument.

Field 1 is also not a direct copy of one locale's bytes. The extraction view
escapes literal brackets and preserves differing locale values with duplicate
annotations. The report retains the backing metadata separately for rows
where that merged cell differs. In row 2118, the four main locales carry
`xtx/command[22113-22114,29861-29861,tail-IVX]`, while chs carries
`xtx/command[22114-22114,29861-29861,29865-29872,tail-IVX]`.
The merged cell must not be passed to the native descriptor consumer as its
original input. Literal escaping is specified by
`xivl-tools:docs/formats/ssd-sheet.md`, Rich-string read and text-export contract.
Duplicate annotation is implemented by `xivl-tools:src/formats/src/csv.rs`,
`CsvTable::insert_row`.

Backing row 2104's field 1 names `xtx/placeName`, including key 1051, and row
2106 names `xtx/itemName`. The raw locale-specific strings and source spans
are retained in the report. These are descriptor cells. They do not identify
an item/place selection producer or prove how a selected record encodes a
target row. The existing crosswalk owns those target sheets' names and joins.

## Selection boundary

The native study at revision
`6b53147c8afca1a13bd9c753b39662aaa964da3b`,
`xivl-client-structs:manifests/autotranslate_wire_format_study.json`,
AT-COMP-010/011, recovers selected-record production and separate category and
mapped native-key inputs. AT-CHAT-001/002 recovers the conditional native send
path and byte preservation for a complete admitted control in the copied
prefix. AT-CHAT-003 qualifies earlier pronoun replacement. Generic Lua
argument packing and actual execution remain qualified.

The backing-row report supplies static source identities and sparse rows.
It does not join a locale's enable resource to the native CacheAll range
vector at backend+0x14/+0x18, its row storage/order at backend+0x8, or an actual
selected instance. That loader/population join and selected locale are the
first missing evidence for native-key-to-CSV identity. Numeric agreement or
the same range shape alone cannot close it. Item/place producers and the
matching receive/render lookup remain separate missing joins.

The crosswalk therefore assigns no CSV row key or field 0 value to selected
wire bytes and chooses no zone/layout from a duplicate place name. Its
`selectionBoundary` describes unresolved CSV-to-token semantics, not an
absence of the recovered conditional native path. No complete token decoder
or runtime phrase-rendering claim follows from these products.
