# Actor appearance packed-word crosswalk

## Verdict

Client column positions `0x19..0x1F` map to the canonical
`actorclass_graphic` fields `mainHand`, `offHand`, `spMainHand`, `spOffHand`,
`throwing`, `pack`, and `pouch`. All seven source columns are `s32`. The native
client copies those positions without transformation into the seven appearance
words later decoded as `2/10/10/10` bits.

The four bounded rows `0x5A0700..0x5A0703` are all present as decimal IDs
5900032 through 5900035. Every one of their seven words is zero, so every
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

## Reproduction

With the local corpus present, run:

```powershell
python tools\verify_actor_appearance_crosswalk.py
```

The verifier fails if the mapping names, positions, header types, bounded row
presence, values, or zero-word unpack result changes.
