# Hamlet supply item rows

The pinned `itemHamletSupply.csv` assigns the following item IDs and
quantities to the supply-list keys read by the client. `PopulaceHamletSupply`
uses the craft and gather key ranges documented in
`xivl-client-scripts:docs/hamlet-supply-ui-contract.md`; the client returns
data columns 0 and 2 as the item and quantity. These rows establish catalog
values, not historical delivery, actor spawns, or reward policy.

| Supply keys | Item IDs by ascending key | Quantity |
| --- | --- | ---: |
| `11001..11008`, `12001..12008`, `13001..13008` | `10011200..10011207` in matching order | 1 |
| `11009..11011`, `12009..12011`, `13009..13011` | `10011197..10011199` in matching order | 10 |

Source: `xivl-client-data:csv/itemHamletSupply.csv`, extraction
`2012.09.19.0001`, SHA-256
`cc32f89d9b20f140a1fcf316491fe73f0dfeb81d894e943de81c34565c896b78`
(`manifests/tables.json`). The row keys, item IDs, and quantities were read
from the pinned CSV bytes. Localized item names are not included here.
