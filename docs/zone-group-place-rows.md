# Zone-group place-key rows

The pinned `_zoneParam.csv` rows `236` and `269` both carry place-name ID
`1041`; rows `237` and `270` both carry ID `1011`. The corresponding
`zoneGroupParam.csv` rows `112` and `113` list those zone pairs respectively.

| Zone IDs | Zone-group row | Place-name ID |
| --- | ---: | ---: |
| `236`, `269` | `112` | `1041` |
| `237`, `270` | `113` | `1011` |

These are static CSV relationships. The shared keys do not identify localized
place names, prove identical scene geometry or transforms, or establish
historical encounter use.

The source identities are pinned in `manifests/tables.json`:
`_zoneParam.csv` has SHA-256
`1E75E434217E8D99848AC1D690A9FCD93E43C9A2B00FC983E3BA7FB592D377F9`, and
`zoneGroupParam.csv` has SHA-256
`E521ADB118F8EDC099FCF4171E905299B5B8C83C13C90FC62D46C646E80D8B23`.
