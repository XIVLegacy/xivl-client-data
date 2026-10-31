# Selected creation equipment rows

The decoded `boot_skillequip.csv` sheet has 22 `s32` columns after its row ID.
Extraction `2012.09.19.0001` contains these selected cells. Column positions
are zero-based after the row ID.

| Row | Column | Value |
| ---: | ---: | ---: |
| 102 | 0 | 60818432 |
| 102 | 1 | 61867008 |
| 104 | 8 | 1184 |
| 129 | 8 | 1184 |
| 130 | 8 | 1184 |
| 139 | 8 | 1184 |
| 141 | 8 | 1184 |

Row 102's first two cells are distinct. The five selected column-8 cells all
store 1184. These source values do not establish a per-tribe replacement,
an equipment-slot interpretation or a historical character-creation result.

The complete member SHA-256 is
`72E1861DBC07A3025FC056CBB8784E943129F40DF69C959D11C961C025486CB5`,
recorded in [tables.json](../manifests/tables.json).
