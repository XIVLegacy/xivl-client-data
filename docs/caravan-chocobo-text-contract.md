# Caravan chocobo command text

Ten selected English cells in `chocoboCaravanGuard.csv` supply an action
question, calm/feed/recall/decline wording, a feed question and three identical
controlled name expressions. The cells label authored presentation. They do
not prove displayed choices, an identified food item or an applied command.

## Sources and positions

The evidence class is `client_extraction`, extraction `2012.09.19.0001`.
[tables.json](../manifests/tables.json), record
`csv/chocoboCaravanGuard.csv`, pins the 5,723-byte member, SHA-256
`5e5a76d8910f03eceeadd2bb15437d9a692a3dcab3a6d2f861a65e31531e1b33`.
The archive identity is owned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json).

Both headers start with a single-space ID-label field. They declare five
positions after the row ID, labels 0-4, all `str`. English is position 1,
the third physical CSV field. The member has 11 data rows and 13 CSV records.
Only the ten cells below are interpreted. Row IDs are lookup keys, distinct
from physical record numbers, answer positions and returned choices.

| Row ID | One-based CSV record, including headers | Authored English content |
| --- | --- | --- |
| 1 | 3 | A question asks what action to take. |
| 2 | 4 | Calm the chocobo. |
| 3 | 5 | Feed the chocobo. |
| 4 | 6 | Call the chocobo back. |
| 5 | 7 | Do nothing. |
| 6 | 8 | A question asks what to feed. |
| 7 | 9 | A controlled name expression, followed by a period. |
| 8 | 10 | The same complete cell as row 7. |
| 9 | 11 | The same complete cell as row 7. |
| 10 | 12 | Decline the feed selection. |

These are paraphrases. The three identical cells supply no distinct literal
food names. Their equality also does not prove identical rendered names:
actual formatting inputs and per-answer adaptation remain uncharacterized.

## Complete exported controls

Control syntax follows
`xivl-tools:docs/formats/ssd-sheet.md#rich-string-read-and-text-export-contract`.
The export preserves tokens without executing or rendering them. `E8` below
is a syntactic unary expression code with its integer index. `EC` denotes a
placeholder expression, rather than a supplied color or a runtime default.

Rows 1-6 and 10 contain no exported controls. Each of rows 7-9 contains one
`head` token with one string expression. That string contains exactly the
following ordered controls, with no intervening text runs:

| Position inside the `head` string | Complete ordered expressions |
| --- | --- |
| 1: `switch` | A selector string containing `sheet` with operands string `itemData`, E8 index 1 and integer 41. It is followed by six string alternatives, each containing one `color` control. Their integer operands are `4294177779,4290838432,4284532991,4289957119,4294944358,4293254526`, in that order. |
| 2: `edge-color` | Integer 4280690214. |
| 3: `english-noun` | String `xtx/itemName`, integer 1, E8 index 1, integer 1 and integer 1, in that order. |
| 4: `edge-color` | Placeholder EC. |
| 5: `color` | Placeholder EC. |

The period follows the outer `head` token. There is no exported `number`
control or stated food quantity or HP amount in these selected cells.
The strings `itemData` and `xtx/itemName` and integer 41 are literal operands.
Their presence does not establish a successful sheet lookup, an item identity,
the meaning of field 41, a selected switch branch or a color. Neither noun
operand 1 nor E8 index 1 becomes an item quantity through this structure.
The `head` name alone does not prove capitalization or any native operation.

## Conditional caller and text join

The caller is adopted from
`xivl-client-scripts:docs/caravan-chocobo-command-contract.md`, sections
"Fixed frame and ordered requests," "Restricted flags and formatting
boundary" and "Conditional Ask and result composition," revision
`f9384624317586fb242cdb6a9dc7b3d32ed55d7f`. Its 14,282 bytes have SHA-256
`9097bc941f09c69f46061c54d9ce94fb6de800a1d6665e0a857c3796b82f707c`.
That publication owns the method's calls, type boundaries, result widths
and conditional helper bindings.

Its separate initializer requests text bank 7680 and identifier
`chocoboCaravanGuard`. That name matches this member. The following joins
require the actual text provider N to resolve these English cells, and the
dynamic helpers, work storage and native text path to match their published
contracts. The initializer's existence does not establish that it ran for N.

The fixed caller is `chocoboCommand(N,A1,A2,A3,A4,A5,A6,A7)`. It requests
question row 1 with the finite restriction sequence `true,true,A1,true`.
Nominal original slots 1-4 have row keys 2-5, respectively:

| A1 | Conditional answer rows and authored labels | First formatting tail |
| --- | --- | --- |
| Boolean true | 2 calm; 3 feed; 4 call back; 5 nothing. | No values. |
| Boolean false | 2 calm; 3 feed; 5 nothing. | No values. |
| Any non-Boolean, including nil or numeric 0 | 2 calm; 3 feed. | Exactly `A1,true`, preserving explicit nil. |

For either Boolean A1, the original helper's next open prefix probe is
`type()` with no argument. With retained base `select` and standard `type`,
it errors before connector/widget entry. The published LGE override also
distinguishes missing input from explicit nil, with its diagnostic path
separately qualified. The Boolean rows above therefore require normal
prefix-scan completion under the stated interpretation. They are neither
proved rendered choices nor evidence of an observed retail menu failure.
A non-Boolean A1 ends the Boolean prefix and supplies both formatter-tail
values. The final literal true then belongs to that tail.

Only a first result Q equal to numeric 2 requests question row 6 with four
answer rows `7,8,9,10` and formatter tail exactly `A2,A3,A4`. Those rows
conditionally label three controlled name expressions followed by a decline
choice. The caller supplies N as provider for the question and answers.
Neither the extra WorldMaster operand nor a sheet operand replaces N.

For a compact first answer within the normally completed helper's requested
range, the helper returns the original slot number. Compact answer 2 thus
conditionally selects the feed question. False A1 omits row 4, so its compact
answer 3 maps to original slot 4, the nothing row. The caller does not validate
returned choices or provide a general safe result for out-of-range answers.

After normal talk finish it returns exactly `(Q,R)`. R is nil when the second
question was skipped, and otherwise is its first result. The helper
composition's cancellation and failure distinctions remain intact: first
cancellation normally gives `(nil,nil)`, first numeric-zero failure gives
`(0,nil)`, and second cancellation gives `(2,nil)`. A second false result
remains `(2,false)`. These results do not prove that food was selected or used.
Errors can prevent talk finish and a normal return.

The per-answer suffixes are adopted from
`xivl-client-scripts:docs/duty-confirmation-client-contract.md`, "Text and
native property input," revision `26e98d3be5c2d105c8a6ef52c9b504cc9748ca15`.
Its 16,150 bytes have SHA-256
`0e183e7e277c9cfc85c641425d596fe7a584490d1cdb6e0e75f3d77c25cc2c1a`.
With the four-entry answer table unchanged at its separate length read,
retained base `select`, applied work count 4 and normal helper completion,
the original Ask method requests:

| Property | Provider / row | Complete formatting tail |
| --- | --- | --- |
| Question | N / 6 | `A2,A3,A4` |
| Answer 1 | N / 7 | `A2,A3,A4` |
| Answer 2 | N / 8 | `A3,A4` |
| Answer 3 | N / 9 | `A4` |
| Answer 4 | N / 10 | No values. |

Explicit nil, false and numeric zero retain their supplied positions.
The final row has zero formatting values, rather than one nil. The question
call precedes the later work-count read for the loop limit. The earlier
answer-table length is not recomputed then. The publication preserves the
canonical source's fixed captures of 14 vararg slots before counting, seven for the question,
one value before `select` and three after it as discrepancies from the
original open tails. Those captures do not replace the original suffixes.

The three byte-identical name cells thus receive different Lua suffixes
under this composition. They do not identify three food items. In particular,
the structural E8 index 1 cannot be equated with A2, A3 or A4 merely because
one is first in each suffix. The native NPC-provider adaptation into
`_setProperty` formatting remains uncharacterized, including any conversion
or implicit inputs. No rendered noun, item selection or feed effect follows.

## Reproduction and remaining boundary

Authenticate the declared archive and member before parsing in memory.
Assert the exact two headers, all row widths, selected-key uniqueness,
English position and record locators. Check selected UTF-8 cell identities,
the equality of rows 7-9, independent wording assertions and the complete
nested expression structure. Reject changed schema/column/record positions,
removed wrappers or alternatives, reordered colors, changed literal or E8
operands, lost resets and introduced formatter or mechanics assumptions.
No corpus hydration or product regeneration is needed.

The first unresolved edges are actual invocation, provider/schema/locale
binding, native formatting and answer/result delivery. Structural E8 indices
do not identify the caller's formatter positions without the missing native
NPC-provider adaptation. These cells establish no HP restoration amount,
food consumption, inventory debit, actual recall or movement, cargo handling,
reward entitlement or return travel.
