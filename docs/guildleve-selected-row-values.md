# Guildleve selected row values

This note records selected values from the retail `passiveGL_craft.csv` and
`guildleve.csv` tables using the column positions named by the existing
mappings. The mapping names are not proof of how a client or server uses these
values. No eligibility, objective-completion, reward, or runtime rule is
inferred here.

CSV positions below are zero-based after the row ID, matching the index
convention in `tools/mappings/passivegl_craft.py` and
`tools/mappings/guildleve.py`.

## Passive crafting guildleve

The retail `passiveGL_craft.csv` row `120214` stores these values in the four
mapped `recommendedLevel` fields:

| Row ID | Fields | CSV positions | Stored values |
| ---: | --- | --- | --- |
| 120214 | `recommendedLevel1` through `recommendedLevel4` | 16, 24, 32, 40 | 5, 15, 25, 40 |

## Guildleve rows

The `guildleve.csv` mapping names positions 39-42 `aimNum1` through `aimNum4`.
The selected rows contain these raw tuples:

| Row ID | Fields | Stored values |
| ---: | --- | --- |
| 12487 | `aimNum1` through `aimNum4` | 3, 3, 0, 0 |
| 11704 | `aimNum1` through `aimNum4` | 3, 4, 0, 0 |
| 13028 | `aimNum1` through `aimNum4` | 4, 0, 0, 0 |

The field labels above come from the existing mapping code. These tuples do not
by themselves define target counts, client display, objective completion, or
server policy.

## Source identity

Both files are pinned in `manifests/tables.json` for extraction
`2012.09.19.0001`. The selected row bytes were read from copies whose complete
file hashes match those pins:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `passiveGL_craft.csv` | 26972 | `2e2b68515f43ba2898bc3c4bf642332bd924687a4d771ba8d8d9733c539cd0ba` |
| `guildleve.csv` | 80881 | `74ee8061449bf538d504443017c776f994c06fd1bcd2fd008bbee18284d93b2d` |

The hashes identify the complete source tables; the mapping code identifies
the stored column positions. Neither supplies a runtime consumer interpretation
for the `aimNum` tuple.
