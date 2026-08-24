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
