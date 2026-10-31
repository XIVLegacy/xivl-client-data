# Selected message operand rows

These observations describe decoded text expressions in extraction
`2012.09.19.0001`. Formatting arguments are numbered from one. Logical source
columns exclude the CSV row ID. Text lookup positions do not identify the
server producer, its runtime argument type or an observed rendered message.

| Bank and row | Static expression or meaning | Source column |
| --- | --- | --- |
| worldMaster 30604 | Command-removal text looks up `xtx/command` using formatting argument 2. It does not render an action slot. | English 1 |
| worldMaster 50141 | Remaining leve allowances, using formatting argument 1 for the count and singular/plural selection. | English 1, physical line 1877 |
| worldMaster 34102 | Countdown using formatting argument 1 for seconds and argument 2 to select Logging out, Returning or Teleporting. | English 1, physical line 1300 |
| man2u0 176 | A proximity refusal for fixed item 11000081. | English 1 |
| man2u0 177 | Fixed item 11000081 has no effect on the display-name target supplied by formatting argument 1. The item key is embedded in the row. | English 1 |
| man2u0 178 | The fixed item's effect expires. | English 1 |
| worldMaster 51075 | Generic item-use defeat objective: item argument 1, display-name argument 2 and group/singular selector argument 3. | English 1 |
| noc000 66 | Japanese and German text look up `xtx/text_jobName` using formatting argument 1. The English text omits that label. | Selected localized expressions |
| noc000 67 | Level, item, quality and quantity use arguments 1, 2, 3 and 4, respectively. | Selected localized expressions |

Item 11000081 is Niellefresne's Gold Dust in `xtx_itemName.csv` English
column 5. The fixed item in man2u0 177 must not be mistaken for a supplied
first item argument followed by a display name. Likewise, worldMaster 30604
does not independently name its unused first argument as a slot.

The selected job-name keys used by the Task Board text are:

| Key | English job-name label |
| ---: | --- |
| 29 | carpenter |
| 30 | blacksmith |
| 31 | armorer |
| 32 | goldsmith |
| 33 | leatherworker |
| 34 | weaver |
| 35 | alchemist |
| 36 | culinarian |
| 39 | miner |
| 40 | botanist |
| 41 | fisher |


The caller's forwarding positions belong to
`xivl-client-scripts:docs/quest-event-client-contracts.md`, Task Board speech
operands. The text identifies a lookup domain, without a separate guild enum
or a complete server eligibility rule. WorldMaster 51075 is a generic template;
it does not identify a particular duty or prove its objective dispatcher.

The arithmetic `0x20C3DD = 2147293 = 0x200000 + 50141` and
`0x208536 = 2131254 = 0x200000 + 34102` identifies candidate row numbers.
It does not establish a GameMessage bank-selector relationship or observed
runtime parameters. Row 34102 describes logout, return and teleport
countdowns, without identifying a guildleve-start countdown.

Source rows are in `worldMaster.csv`, `man2u0.csv` and `noc000.csv` as listed
above, with names in `xtx_itemName.csv` and `xtx_text_jobName.csv`.
Their complete size/SHA-256 identities are in
[tables.json](../manifests/tables.json).
