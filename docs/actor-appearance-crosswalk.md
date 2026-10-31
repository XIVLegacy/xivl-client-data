# Actor appearance packed-word census

## Verdict

Client column positions `0x19..0x1F` map to the canonical
`actorclass_graphic` fields `mainHand`, `offHand`, `spMainHand`, `spOffHand`,
`throwing`, `pack`, and `pouch`. All seven source columns are `s32`. The native
client copies those positions without transformation into the seven appearance
words later decoded as `2/10/10/10` bits.

The complete sheet contains 7,831 rows. Of these, 2,501 have at least one
nonzero word in the seven positions, with 3,651 nonzero word occurrences. The
generated census lists all 2,501 rows and decodes every word. The generated
value-count table gives the exact distribution of every distinct packed value,
including zero, in each field.

The four native-anchored rows `0x5A0700..0x5A0703` are all present as decimal
IDs 5900032 through 5900035. Every one of their seven words is zero, so every
decoded lane is also zero. These rows prove the positional crosswalk but do not
provide a nonzero example from which to infer lane semantics.

## Exact crosswalk

| Client column | Canonical field | CSV type | `0x5A0700` | `0x5A0701` | `0x5A0702` | `0x5A0703` |
|---:|---|---|---:|---:|---:|---:|
| `0x19` | `mainHand` | `s32` | 0 | 0 | 0 | 0 |
| `0x1A` | `offHand` | `s32` | 0 | 0 | 0 | 0 |
| `0x1B` | `spMainHand` | `s32` | 0 | 0 | 0 | 0 |
| `0x1C` | `spOffHand` | `s32` | 0 | 0 | 0 | 0 |
| `0x1D` | `throwing` | `s32` | 0 | 0 | 0 | 0 |
| `0x1E` | `pack` | `s32` | 0 | 0 | 0 | 0 |
| `0x1F` | `pouch` | `s32` | 0 | 0 | 0 | 0 |

## Raw row correlations

All 7,831 `actorclass_graphic.csv` row IDs have an equal row ID in
`actorclass.csv`, and all of those actor-class rows carry a display-name
reference present in `xtx_displayName.csv`. The census keeps these facts in
separate columns: the raw graphic row ID, the correlated actor-class row ID,
the display-name ID, and the English display text. `actorclass.csv` has 153
additional rows with no graphic row; they are not part of this census.

These are row-identity and display-name correlations only. They do not turn a
display-name ID into an appearance ID and do not establish an item-catalog
mapping.

## Selected actor-class row

`csv/actorclass.csv` row `2303401` references display-name ID `3203405`. The
matching `csv/actorclass_graphic.csv` row has base `10049`, size `2`, head `0`,
and body `1024`. These are static row values, not a resolved display name,
client resource pathname, Lua class path, or runtime appearance selection.

The source identities are pinned in `manifests/tables.json`: `actorclass.csv`
has SHA-256
`3AC9F8D1812D49101F367E2A41356BE96B5D64B1FC5CA29949195F50EBE1D984` and
`actorclass_graphic.csv` has SHA-256
`7DA8241400530885E0A28DED04A03ACF2771B0580A79C1F49F46EE0861010611`.

## Exact field summary

The full per-value counts are in
`derived/actor_appearance_value_counts.csv`. This summary reports counts over
all 7,831 rows. Distinct-value counts include zero.

| Field | Column | Nonzero rows | Distinct packed values | Distinct `31:30` | Distinct `29:20` | Distinct `19:10` | Distinct `9:0` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `mainHand` | `0x19` | 2,474 | 399 | 1 | 51 | 27 | 39 |
| `offHand` | `0x1A` | 943 | 104 | 1 | 23 | 14 | 19 |
| `spMainHand` | `0x1B` | 1 | 2 | 1 | 2 | 2 | 1 |
| `spOffHand` | `0x1C` | 0 | 1 | 1 | 1 | 1 | 1 |
| `throwing` | `0x1D` | 3 | 4 | 1 | 4 | 4 | 1 |
| `pack` | `0x1E` | 230 | 13 | 1 | 2 | 3 | 12 |
| `pouch` | `0x1F` | 0 | 1 | 1 | 1 | 1 | 1 |

Bits `31:30` are zero in every field and row. `spOffHand` and `pouch` are zero
throughout the corpus. The remaining lane counts show variation without
assigning meaning to any internal lane.

The four rows carrying the rare `spMainHand` or `throwing` values are:

| Graphic row ID | Display name ID | English display name | Nonzero rare field | Packed value | Decode `31:30/29:20/19:10/9:0` |
|---:|---:|---|---|---:|---|
| 1000063 | 2200116 | Gerulf | `spMainHand` | 955253760 | `0/911/1/0` |
| 1000642 | 1600130 | Oefyrblaet | `throwing` | 950010880 | `0/906/1/0` |
| 1000652 | 1500007 | Mamaza | `throwing` | 953160704 | `0/909/5/0` |
| 1000666 | 1500084 | Ococo | `throwing` | 944769024 | `0/901/2/0` |

The names and positions come from
`tools/mappings/actor_appearance.py`, re-derived against the numeric label and
type header in `csv/actorclass_graphic.csv`. The catalog is extraction
`2012.09.19.0001`; `manifests/tables.json` pins its SHA-256 as
`7DA8241400530885E0A28DED04A03ACF2771B0580A79C1F49F46EE0861010611`.
The native copy and bit widths are independently recorded in
`xivl-decomp:docs/actor/item-appearance-boundary.md` at the catalog-resolution
result and native locations `0x0055D2B0` and `0x006306F0`.

These canonical field names label sheet positions. The native evidence proves
the seven positions and packed widths, not semantic names for the four bit
lanes inside each word. It also does not establish an item catalog
ID-to-appearance mapping.

The known native consumers remain bounded to the direct chain already cited:
`0x0055D2B0` resolves the graphic row and copies the seven words,
`0x00665E40` sends them to weapon-controller entries, `0x006306F0` performs
the `2/10/10/10` split, and `0x006B5770` consumes the decoded components for
resource-tag arrays. This census adds value coverage and row correlations. It
does not name the four internal components, and the typed Item sheets provide
no catalog-ID-to-appearance mapping.

## Generated products

- `derived/actor_appearance_census.csv` contains every row with at least one
  nonzero packed word. It keeps correlations first, followed by the seven raw
  signed values, their unsigned hexadecimal forms, and neutral bit-range
  decodes.
- `derived/actor_appearance_value_counts.csv` contains every distinct packed
  value per canonical field, its neutral decode, and its exact row count.

## Reproduction

With the local corpus present, run:

```powershell
python tools\build_actor_appearance_census.py --check
python tools\test_actor_appearance_census.py
```

The builder fails on mapping, header, row-identity, or display-name correlation
drift. Its check mode regenerates both products in memory and compares exact
bytes. The mutation tests cover changed packed values, signed `s32` decoding,
column-type drift, missing actor-class joins, deterministic output, and LF line
endings. `tools/verify_actor_appearance_crosswalk.py` remains the bounded check
for the four native-anchored zero rows.

## Selected generator, transmitter and Vanguard rows

The authenticated actor-class, graphic and display-name tables retain these
static associations. Numeric IDs are source row keys; repeated English text
does not merge the rows or establish an encounter variant.

| Actor/graphic row IDs | Display-name ID | English text | Base | Size ordinal | Head | Body |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| 1002064, 2210802 | 3210802 | ceruleum generator | 10525 | 2 | 2048 | 2048 |
| 1002063, 2210801 | 3210801 | magitek transmitter | 10525 | 2 | 1024 | 1024 |
| 2109001, 2109003 | 3109001 | magitek vanguard | 10052 | 2 | 0 | 1025 |
| 2209001 | 3209001 | magitek vanguard | 10052 | 1 | 0 | 1025 |
| 2209003 | 3109003 | magitek vanguard | 10052 | 1 | 0 | 1025 |

All eight rows have `hairColor`, `skinColor` and `eyeColor` equal to 1.
Every other mapped appearance field, apart from base, size, head and body in
the table, is zero. This includes the seven packed appearance words at
columns 25-31. Raw graphic columns 0-5 are blank, and trailing columns 45-46
are zero. Raw actor-class columns 0-4 are blank; column 5 holds the listed
display-name ID. These blank cells are not rewritten as numeric zero.

Across all 7,831 graphic rows, the exact `(display-name ID, base)` pairs in
the table match only the row IDs listed in their respective rows. Their
cardinalities are 2, 2, 2, 1 and 1. Comparing English text instead of display
ID, `("magitek vanguard", 10052)` matches all four Vanguard IDs listed here;
the generator/base and transmitter/base pairs each match their two listed
IDs. These are full-table counts, not uniqueness claims from the selected
subset. None of the three Vanguard display IDs contains an F-1 or H-1 suffix
in its English text.

Sources are `csv/actorclass.csv`, `csv/actorclass_graphic.csv` at the listed
IDs, and `csv/xtx_displayName.csv` at the listed display IDs, extraction
`2012.09.19.0001`. The column positions come from
`tools/mappings/actor_class.py` and `tools/mappings/actor_appearance.py`,
checked against the label/type headers. SHA-256 pins in
[`manifests/tables.json`](../manifests/tables.json) are, respectively,
`3ac9f8d1812d49101f367e2a41356be96b5d64b1fc5ca29949195f50ebe1d984`,
`7da8241400530885e0a28ded04a03acf2771b0580a79c1f49f46ee0861010611`, and
`36c5dfba312695d9f4ee090dba123dfd7792feba55d88b0062c070d98abc0505`.

The numeric bases are not resource paths. The separately documented
`xivl-decomp:docs/actor/appearance-path-decoder.md`, sections Base-model split
and Directory prefix, maps appearance-record word 0 values 10525 and 10052
to category 1, model numbers 525 and 52, and prefixes
`/client/chara/mon/m525/` and `/client/chara/mon/m052/`. Applying that rule to
these table bases is conditional on their use as appearance-record word 0.
It does not prove file existence, a selected runtime appearance, a Lua class
binding, F-1/H-1 identity, content 13 ownership or a historical spawn.

## Companion-preset row range

All 116 `actorclass_graphic.csv` rows 1070001-1070116 are present.
`mainHand` at logical column 25, excluding the row ID, has type `s32`.
There are 107 nonzero words and nine zero words. The neutral bits 29:20
component has these counts among the nonzero words:

| Component | Rows |
| ---: | ---: |
| 56 | 9 |
| 76 | 25 |
| 161 | 25 |
| 201 | 16 |
| 281 | 16 |
| 316 | 16 |

Bits 31:30 are zero in all 116 rows. The zero-word row IDs are
1070108-1070116. A zero source word remains an explicit case. These
component values do not establish weapon-family names, item `mainSkill`,
a caster category or an item-catalog-to-appearance foreign key.

Source: `csv/actorclass_graphic.csv`, rows 1070001-1070116, logical column
25, with the complete member identity pinned above and in
[tables.json](../manifests/tables.json). The existing packed-word census and
native boundary own the `2/10/10/10` representation.
