# NPC repair manual text

Thirty-three selected English cells in `populaceItemRepairer.csv` provide
repair instructions, topic choices and dialogue. They describe equipment
wear, repair services, self repair and repairing for others. These are
instructions authored for the 1.23b client, not observed repair enforcement.

## Sources and positions

The evidence class is `client_extraction`, extraction `2012.09.19.0001`.
[tables.json](../manifests/tables.json), record
`csv/populaceItemRepairer.csv`, pins the 52,329-byte member, SHA-256
`a9f5536635295c844a3b07bb55f4410ec4848412bf6a31d4938025e235b86ff5`.
[private_csv_corpus.json](../manifests/private_csv_corpus.json) pins the
source archive. Both headers declare five string positions after the row
key. English is position 1, the third physical CSV field.

Only English rows 58-86 and 98-101 are interpreted here. Their one-based
CSV record numbers, including both headers, are respectively 60-88 and
100-103. Row keys, record numbers, answer indices and returned values
remain separate domains.

The caller is adopted from
`xivl-client-scripts:docs/npc-repair-manual-client-contract.md`, sections
"Arguments and ordered requests" and "Conditional helpers and text metadata,"
at revision `f60f205e750fdbe626fa8ac24e612f531c015b7e`, 8,455 bytes,
SHA-256 `6ad81d899d5d275d65c9d5e53df5269937831b08290d1e7b7f2b38a338f8cbf3`.
That publication owns the original instruction frames, strict comparisons,
loop, fresh lookups, result widths and stopping errors.
The [repair menu contract](repair-menu-text-contract.md#initializer-declaration)
owns the initializer's request for bank 2204/schema `populaceItemRepairer`.
Actual provider/schema/locale binding and historical invocation remain
conditional.

## Authored English meanings

The following paraphrases preserve instruction intent without reproducing
the retail dialogue. Advice about prices, skill or materials remains advice
in these cells.

| Row key | Authored meaning |
| --- | --- |
| 58 | Offer to read about repairs. |
| 59 | Accept that offer. |
| 60 | Decline that offer. |
| 61 | Choose a subject to read about. |
| 62 | Why repairs are necessary. |
| 63 | Having repairs done. |
| 64 | The player's own role in repairs. |
| 65 | Making repairs for others. |
| 66 | Stop reading. |
| 67 | Weapons and tools wear through use and can become useless. |
| 68 | Armor likewise becomes worn and damaged. |
| 69 | Damaged items lose benefits, making repairs necessary. |
| 70 | Introduce two ways of obtaining repairs. |
| 71 | Use specialist repair services as one method. |
| 72 | Specialist repairs have a high price and limited restoration. |
| 73 | Another method uses an adventurer in a crafting discipline. |
| 74 | Identify the item that is to be mended. |
| 75 | Request repairs for that item with a fee. |
| 76 | Discuss finding a crafter trained in the proper skill, how much to pay and repair offers. |
| 77 | A crafter can perform repairs personally. |
| 78 | Present self repair as easy relative to relying on others. |
| 79 | Identify the item intended for personal repair. |
| 80 | The proper dark matter is required for repairs. |
| 81 | A crafter's repair skill depends on profession. |
| 82 | Disciples of the Hand may repair for others. |
| 83 | Bazaars also provide a way to seek repair opportunities. |
| 84 | Finding someone in need of repairs presents an opportunity for rewards. |
| 85 | Offer repair services through the item in a bazaar. |
| 86 | The repairer must possess the dark matter needed for repairs. |
| 98 | Repair requests also apply to equipped items. |
| 99 | Choose Inventory through the main menu. |
| 100 | Choose the repair-request option. |
| 101 | Another Disciple of the Hand can select the request, with class and level requirements related to the gear. |

These cells give no numeric skill threshold or resulting condition
percentage. The wording does not establish an actual class/level test,
material grade selection, material supplier at a transaction, consumption,
price computation, gil debit or reward settlement.

## Preserved controls

Control syntax follows
`xivl-tools:docs/formats/ssd-sheet.md#rich-string-read-and-text-export-contract`.
The CSV export preserves tokens without evaluating them.

| Selected cell | Ordered control expressions |
| --- | --- |
| 77 | Two `italic` controls, with integer operands 1 then 0. |
| 99 | `color` integer 4278242338; `edge-color` integer 4280690214; `color` placeholder EC; `edge-color` placeholder EC. |

The other 31 selected cells contain no exported control tokens. These
controls supply styling declarations, not runtime skill, material, price
or condition values. No selected control has a number formatter, switch,
conditional branch, sheet lookup or parameter-index expression. No token
is flattened or rendered here.

## Conditional topic and provider composition

Write N for the manual method's receiver. Only if the actual ask member
resolves the published inherited helper and N's text lookup resolves these
English cells does the following labeling apply:

| Request | Prompt and answer rows | Conditional authored labels |
| --- | --- | --- |
| Initial question | Prompt 58; answer indices 1/2 use 59/60. | Read about repairs; accept or decline. |
| Repeated topic menu | Prompt 61; indices 1-5 use 62/63/64/65/66. | Necessity; obtaining repairs; personal repairs; repairs for others; stop. |

The initial frame is `(N,N,58,2,1,1)` and the repeating frame is
`(N,N,61,5,1,1)`, each retaining one result. Under that helper binding,
N occupies owner, speaker and text-provider positions, default index is 1,
paging is false and cancellation is true. Both formatter tails are empty.
Only numeric initial result 1 enters the loop. Other initial results
return one Boolean false.

| Numeric topic result | Ordered dialogue keys and instruction subject |
| --- | --- |
| 1 | 67,68,69: equipment wear and the need for repairs. |
| 2 | 70,71,72,73,74,75,76,98,99,100,101: repair services, fees and equipped repair requests. |
| 3 | 77,78,79,80,81: personal repairs, dark matter and profession. |
| 4 | 82,83,84,85,86: repairing for others through bazaars and possessing dark matter. |

Supported topics repeat the menu. Every other topic result exits with one
Boolean true, including numeric 5, cancellation -3, zero, nil, false and
string `"1"`. The last answer label therefore does not establish that
only a particular returned value can end the manual. A Boolean return
reports the local manual path, not completion of a repair.

For each dialogue key K, the method freshly obtains global `worldMaster`
as W and requests `W.say(W,N,K)`, discarding all results. Under the
published speech-helper binding, this requests
`showMessage(D,W,40,N,K)` and then `_appendMessagePool(D,W,40,N,K)`,
without formatter arguments. W is the speech receiver; N is the source
object supplied for text lookup. These conditional helper positions do
not establish an actual NPC instance, delivery or rendering.

## Verification and remaining boundary

The selected source identity, headers, English positions, all row locators,
semantic predicates and six controls were checked in memory. Authored
fixtures checked the conditional answer construction, strict numeric
entry/topic handling, dialogue order and provider distinction. Rejecting
controls covered wrong keys, providers, topic order, extra formatter values
and an invented numeric rule. These are source and fixture checks, not
retail execution.

The first unresolved edges are actual ask/speech binding and invocation,
then provider/schema/locale selection, text evaluation and delivered
answer/result association. Instruction wording supplies no repair licence,
eligibility evaluator, material transaction, durability update, payment or
settlement implementation.

Existing historical and runtime limits remain owned by
`xivl-captures:docs/repair-announcements.md`, section "Comparison and adoption
limits," and
`xivl-captures:studies/retail-repair-contract/derived/verdicts.md`, sections
"First-party intent, not runtime proof" and "Exact gates."
The patch 1.18 announcement, official manual summary and captured NPC
transactions retain their distinct evidence tiers. This text does not
resolve their result-condition, self-repair execution or settlement gaps.
