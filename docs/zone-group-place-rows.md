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

The source identities are pinned in `manifests/tables.json`:
`_zoneParam.csv` has SHA-256
`1E75E434217E8D99848AC1D690A9FCD93E43C9A2B00FC983E3BA7FB592D377F9`, and
`zoneGroupParam.csv` has SHA-256
`E521ADB118F8EDC099FCF4171E905299B5B8C83C13C90FC62D46C646E80D8B23`.
