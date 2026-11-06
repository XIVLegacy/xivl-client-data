# NPC repair menu text

Twenty-three selected English cells in `populaceItemRepairer.csv` label
repair menu choices, equipment slots, a paged prompt and confirmation text. The NPC initializer
requests text bank 2204 with schema name `populaceItemRepairer`. These
static facts conditionally label the published menu caller. They do not
identify an inventory item or establish a repair result.

## Sources and positions

The evidence class is `client_extraction`, extraction `2012.09.19.0001`.
[tables.json](../manifests/tables.json), record
`csv/populaceItemRepairer.csv`, pins the 52,329-byte member, SHA-256
`a9f5536635295c844a3b07bb55f4410ec4848412bf6a31d4938025e235b86ff5`.
[private_csv_corpus.json](../manifests/private_csv_corpus.json) pins the
source archive. The member has 102 data rows and 104 CSV records. Both
headers declare five positions after the row key, labels 0-4, all `str`.
English is position 1, the third physical CSV field.

| Selected row keys | One-based CSV records, including both headers |
| --- | --- |
| 6, 7, 8 | 8, 9, 10 |
| 13, 14, 15, 16, 18 | 15, 16, 17, 18, 20 |
| 20, 21, 23, 25, 26 | 22, 23, 25, 27, 28 |
| 33, 34, 35, 36 | 35, 36, 37, 38 |
| 88, 89, 90, 92, 94, 95 | 90, 91, 92, 94, 96, 97 |

Row keys, physical record numbers, menu positions and caller return values
remain separate domains.

The caller is adopted from
`xivl-client-scripts:docs/repair-request-client-contract.md`, section
"NPC item-selection menu," 19,525 bytes, SHA-256
`eb7674cebc45e7453e8d43dfbaea23d4c9d988993fe7a7d628794b01e6eda09e`.
That publication owns its exact argument frames, Boolean comparisons,
local arithmetic, errors and result widths. Its helper contracts are
conditional bindings, not evidence of a historical menu invocation.

## Authored English labels

The content below paraphrases the selected English cells. Slot names are
authored labels, without a demonstrated inventory or package/slot binding.

| Row keys | Authored content |
| --- | --- |
| 13 | Cancel repairs. |
| 14 | Repair all currently equipped items. |
| 33 | Quit. |
| 34 | All equipped gear. |
| 15, 35 | Main Hand, followed by an Empty/Condition control. |
| 16, 36 | Off Hand, followed by an Empty/Condition control. |
| 18 | Head, followed by the same kind of control. |
| 20, 21, 23, 25, 26 | Body, Hands, Waist, Legs and Feet, respectively, with that control. |
| 89, 90, 92, 94, 95 | Neck, Ears, Wrists, Right Finger and Left Finger, respectively, with that control. |
| 88 | Select an item slot for repairs, followed by two formatted numbers separated by "of". |

"All" in rows 14/34 labels a local choice. It does not prove a bulk repair
service, enabled choices, accepted repair request or successful repair.

## Controls and conditional caller joins

Control syntax is adopted from
`xivl-tools:docs/formats/ssd-sheet.md#rich-string-read-and-text-export-contract`.
The export preserves tokens without evaluating them. `E8` below is a
syntactic unary expression code, with its integer index. `E3` is a binary
expression code. These structural names do not supply runtime semantics.

| Selected cells | Preserved control positions |
| --- | --- |
| 15, 16, 18, 20, 21, 23, 25, 26, 35, 36, 89, 90, 92, 94, 95 | Each slot suffix contains one `if`. Its first expression is E3 with operands E8 index 1 and integer 0. The following string alternatives contain Empty, and Condition with a nested `number` using E8 index 1. |
| 15, 16, 18, 20, 21, 23, 25, 26, 89, 90, 92, 94, 95 | The Condition alternative ends with ASCII percent U+0025. |
| 35, 36 | The Condition alternative instead ends with fullwidth percent U+FF05. |
| 88 | Two `number` controls use E8 indices 1 and 2, in that order. |

Rows 13, 14, 33 and 34 contain no exported controls. No selected cell is
flattened or rendered here. In particular, the expression grammar alone
does not establish an equality operation, branch choice, actual condition
percentage or the source of either formatted prompt number.

Use the caller's symbols A2 and A9. The following ordered joins apply only
if its text-provider lookup resolves these English cells:

| Caller branch | Row keys at answer positions 1-5 | Conditional labels in that order |
| --- | --- | --- |
| A2 equals numeric 1, A9 exactly Boolean false | `33,34,35,36,18` | Quit; all equipped gear; Main Hand; Off Hand; Head. |
| A2 equals numeric 1, every other A9 | `13,14,15,16,18` | Cancel repairs; repair all equipped items; Main Hand; Off Hand; Head. |
| A2 equals numeric 2 | `20,21,23,25,26` | Body; Hands; Waist; Legs; Feet. |
| Every other A2 | `89,90,92,94,95` | Neck; Ears; Wrists; Right Finger; Left Finger. |

The caller supplies literal prompt key 88 and formatter tail A4-A8. Those
five values retain their positions, including nil, without an established
item, condition or other domain. This does not bind A4 to E8 index 1, assign
the two prompt indices to page counters, or establish per-choice formatter
selection. Native answer-to-result mapping and the delivered UI remain
separate from these authored labels. The caller's arithmetic choice value
does not become an item ID through this table.

## Initializer declaration

`PopulaceItemRepairer.initForEvent(self)` has one fixed parameter and no
varargs, upvalues or child prototypes. It makes these ordered member calls
on the supplied receiver:

| Order | Requested call arguments, including receiver | Original CALL PC | B,C |
| --- | --- | --- | --- |
| 1 | `initWork(self,freshEmptyTable1,freshEmptyTable2)` | 5 | 4,1 |
| 2 | `_loadTextDataPermanently(self,2204,"populaceItemRepairer")` | 9 | 4,1 |
| 3 | `_setGroundOn(self,false)` | 12 | 3,1 |

The two empty tables are distinct and newly created on every invocation.
The bank argument is a number, the schema argument a string and the final
argument Boolean false. Each member is looked up when its call is reached.
Every call discards all results. There is no result guard or catch, so a
lookup or call error prevents later requests. Normal completion returns
zero values at PC 13, RETURN B=1. B includes the function slot for CALL;
C=1 requests zero call results.

This declares a matching schema name and requests bank 2204. It does not
prove successful loading, actual provider/schema/locale binding, native
meaning of the calls, execution of this initializer or ground behavior.
`initWork` and the two underscore-prefixed members remain uninspected.

Source: `xivl-client-scripts:lua/scripts/chara/npc/populace/populaceitemrepairer.lua:11-31`,
original Lua 5.1 `root/proto0`, decoded code offset 420, 14 instructions.
Root PCs 8/9 create and bind `initForEvent`; the header declares
`PopulaceItemRepairer` with `NpcBaseClass` and requires
`/Chara/Npc/NpcBaseClass`, without inspecting those dependencies.
`xivl-client-scripts:manifests/scripts.json` pins the 15,881-byte,
742-line canonical source with SHA-256
`027ac93ef6e805ee4c2197d5fa7353a0ebdff125f6d52f0d6c08bedfb5218ea3`.
`xivl-client-scripts:manifests/retail_lua_coverage.json`, the matching
`decodedScriptPath` record, pins original resource
`729s9/wu7/uvupy975/uvupy9751q5xs5u91s5s.le.lpb`, 4,762 bytes, SHA-256
`3d2148a689cbf940bbfc80260fd3d5a540e75d4992cdbd296a36a1e0cf3e1e7d`,
and its 4,749-byte decoded payload, SHA-256
`90d9858f42360f5078a0f567d17c3f1651832127f81bd146d293e33ee01889e7`.
The canonical archive identity is owned by
`xivl-client-scripts:manifests/private_lua_corpus.json`.

## Confirmation text and conditional caller joins

The three additional English cells supply the confirmation prompt and its
ordered answer labels:

| Row key | Authored content |
| --- | --- |
| 6 | Repair costs for a formatted item name and suffix, followed by a gil amount and a second gil amount labeled as in the player's possession. |
| 7 | Proceed with repairs. |
| 8 | Never mind the repairs. |

Rows 7/8 contain no exported controls. Row 6 preserves the following
positions. Token names and E8 nodes follow the published rich-string
syntax cited above; they do not establish evaluation or a rendered quote.

| Position in row 6 | Preserved control operands |
| --- | --- |
| First `switch` | Its selector is a string containing `sheet` operands string `itemData`, E8 index 1 and integer 41. Six string alternatives each contain a `color` control, with integer operands `4294177779,4290838432,4284532991,4289957119,4294944358,4293254526` in order. |
| Following `edge-color` | Integer 4280690214. |
| `english-noun` | String `xtx/itemName`, integer 2, E8 index 1, integer 1, integer 1, in order. |
| Second `switch` | E8 index 2 followed by four string alternatives: empty, a space followed by +1, a space followed by +2 and a space followed by +3. |
| Following `edge-color`, then `color` | Each has placeholder EC. |
| First `kilo` | E8 index 3 followed by string comma. The following authored text labels the amount in gil. |
| Second `kilo` | E8 index 4 followed by string comma. The following authored text labels the amount as gil in the player's possession. |

The `sheet` operands and `xtx/itemName` string do not themselves establish
an item lookup result, selected inventory object, switch branch, color or
formatted amount. A structural E8 index remains distinct from a caller's
formatter argument position.

The caller contract is adopted from
`xivl-client-scripts:docs/repair-request-client-contract.md`, sections
"NPC repair confirmation" and "Conditional wallet-helper binding",
at revision `1750b735bf9069323f773c141e0500335ea2af97`, 28,166 bytes,
SHA-256 `fe34a9346ba4f43b318ccb7689537c1190432d318a6442fa95cfafb88a40f6bc`.
Its original `confirmRepairItem` frame, including the ask receiver, is
`(N,N,6,2,1,1,A3,A4,A2,...G)`, where G is the complete result sequence of
the supplied A1 receiver's `getMoneyOnHand` call. This preserves every
result and its position, including trailing nils. The inherited helper
contract in
`xivl-client-scripts:docs/request-warden-event-contract.md#widget-result-production`
conditionally requests prompt 6, consecutive answer rows 7/8, default index
1, paging false and cancellation true. Its open formatter tail is owned by
`xivl-client-scripts:docs/open-world-key-coffer-contract.md#confirmation-and-event-contract`.

If the dynamic helper and provider resolve these English cells, row 7
labels answer position 1 and row 8 labels answer position 2. The original
caller retains one ask result and returns one Boolean, true only when that
result equals numeric 1. This does not authenticate a native UI event's
label-to-result association or prove that repairs proceed.

The original formatter tail begins with A3,A4,A2, followed by all of G.
Under the exact published wallet-helper binding, that helper returns one
M on every normal path, giving tail `(A3,A4,A2,M)`. The canonical
confirmation instead appends two getter-result slots and gives
`(A3,A4,A2,M,nil)` under that binding. The original open width and canonical
fixed width remain distinct. Neither frame establishes an E8-index-to-tail
binding, actual formatter values or a delivered quote. The initializer's
bank 2204/schema declaration remains conditional on the actual provider,
schema and locale binding.

The first uninspected edges are those actual bindings, formatter evaluation
and native answer/result association. These text and caller facts do not
identify an inventory item or establish a global NPC fee, bulk service,
payment, condition restoration, material use or settlement.

## Verification and boundary

The selected member, headers, row locators, English labels and control
positions were checked against the pinned source. Original initializer
calls and widths were checked independently of the canonical method using
authored fixtures for fresh tables, lookup/call ordering, discarded results
and errors. These are source and fixture checks, without retail execution.
The confirmation cells and conditional caller joins were checked against
their pinned sources with literal control, argument-position and rejecting
checks. Reproduction needs the selected cells and published contracts,
without another raw repair method or adjacent text row.

Actual provider/schema/locale and formatter binding are the first unresolved
edges. Supplied argument meanings, historical NPC binding and invocation,
native answer mapping, selected-item identity, gil or material debit and
durability outcomes require their own evidence.
