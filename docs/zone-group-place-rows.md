# Zone-group place-key rows

The pinned `_zoneParam.csv` rows `236` and `269` both carry place-name ID
`1041`; rows `237` and `270` both carry ID `1011`. The corresponding
`zoneGroupParam.csv` rows `112` and `113` list those zone pairs respectively.

| Zone IDs | Zone-group row | Place-name ID |
| --- | ---: | ---: |
| `236`, `269` | `112` | `1041` |
| `237`, `270` | `113` | `1011` |

The same shape holds for the three capital groups. `zoneGroupParam.csv`
rows `101`, `201`, and `301` carry place-name IDs `1051`, `2001`, and
`3051` at position 0 and list five zones each at positions 1-5. Their first
two zones carry that place-name ID in `_zoneParam.csv` position 0:

| Zone IDs | Zone-group row | Place-name ID |
| --- | ---: | ---: |
| `133`, `230` | `101` | `1051` |
| `155`, `206` | `201` | `2001` |
| `175`, `209` | `301` | `3051` |

Their other three listed zones carry different place-name IDs. Zones `184`
through `188` also carry `3051` but are not listed in row `301`. A prior
external lead, `docs/mob_placement_records_2026-09-27.md` at revision
`d5fb880e17f07f31ea7f8380ff813e5d71b6b678`, groups these zone IDs the same
way.

These are static CSV relationships. The shared keys do not identify localized
place names, prove identical scene geometry or transforms, or establish
historical encounter use.

## Gridania and Black Shroud fields

Joining `_zoneParam.csv` column 0 to `xtx_placeName.csv` column 1 supplies
these English labels. `zoneGroupParam.csv` columns 1-5 supply membership.
Columns are zero-based after the row key.

| Zone ID | Zone-group row | Place-name ID | English label |
| ---: | ---: | ---: | --- |
| 150 | 202 | 2007 | Central Shroud |
| 151 | 203 | 2008 | East Shroud |
| 152 | 204 | 2009 | North Shroud |
| 153 | 205 | 2010 | West Shroud |
| 154 | 206 | 2011 | South Shroud |

The capital pair above has English label Gridania at place-name row 2001.

`regionParam.csv` row 2, columns 0-2, contains `104,201,209`.
`_region.csv` row 103, column 1, carries code 104. These selected groups
therefore resolve structurally to region 103. Regional membership does not
select one layout child or establish a per-session instance.

[`zone_internal_names.json`](../manifests/zone_internal_names.json) binds
151 to layout 302 / `fst0Field02` and 153 to layout 304 / `fst0Field04`.
The other selected zones retain its shared-place-key limitation. In
particular, the separate `fst0Town01` / `fst0Town01a` vocabulary and layouts
321 / 331 do not uniquely assign either resource to 155 or 206. Preserve
the two numeric zone IDs separately. These rows do not establish public or
private status, equal geometry, a coordinate transform or NPC placement.

Source identities in `manifests/tables.json`:

| Sheet | SHA-256 |
| --- | --- |
| `xtx_placeName.csv` | `81467ef42e8aeba82fe95f6c4249356550c02e41e6734abf9fdd194051dc1714` |
| `regionParam.csv` | `720ae958fd38d53721b6ddce380b82a5cddecb111157291ca29f9465c56bc147` |
| `_region.csv` | `7dc1f9b9657dc302e8ba341181233455149e57ad12291cc1c2bd6483455f666d` |

The source identities are pinned in `manifests/tables.json`:
`_zoneParam.csv` has SHA-256
`1E75E434217E8D99848AC1D690A9FCD93E43C9A2B00FC983E3BA7FB592D377F9`, and
`zoneGroupParam.csv` has SHA-256
`E521ADB118F8EDC099FCF4171E905299B5B8C83C13C90FC62D46C646E80D8B23`.
