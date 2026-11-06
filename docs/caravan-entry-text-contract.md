# Caravan entry and question text

Sixteen selected English cells in `populaceCaravanManager.csv` describe
escort offers, an escort-count limit, possible early departure, a reduced-seal
participation question, and fighter-count and level wording. Their numeric
keys match arguments in the published CaravanManager entry and Question
methods. This conditionally labels authored presentation, without proving
actual input roles, eligibility, registration, travel or rewards.

## Sources and positions

The evidence class is `client_extraction`, extraction `2012.09.19.0001`.
[tables.json](../manifests/tables.json), record
`csv/populaceCaravanManager.csv`, pins the 70,472-byte member, SHA-256
`cb8798f4f8fdb40932a96bdabd5d37e1248859554c5ba523ac6aa776fbc769da`.
The archive is pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json).

Both header rows declare five positions after the row ID, labels 0 through
4, all `str`. English is position 1, the third physical CSV field. The
selected cells contain English questions and prose independently of their
matching caller keys. The member has 64 data rows and 66 CSV records.

| Selected row IDs | One-based CSV records, including both headers |
| --- | --- |
| 4, 11, 15, 16, 23, 32 | 5, 12, 16, 17, 24, 33 |
| 37, 43, 44, 47, 48, 49, 50, 63, 64, 65 | Same numbers as their row IDs |

Row IDs are lookup keys. In particular, row 16 is record 17, while row 37
is record 37. Neither a physical record number nor an adjacent answer row
may replace a selected key.

The caller source is
`xivl-client-scripts:docs/caravan-entry-client-contract.md`, "Incoming
values," "Entry ordering and result," "Question ordering and repeat
behavior" and "Shared rank gate," revision
`7097e83e43c26ce0e08af063e392cccc1d53030a`. Its 14,169 bytes have SHA-256
`86f25a31cdf565f55d5703503698cea5dd434ea042a4d82beb27a21530d24c1c`.
That publication owns the actual argument frames, strict Boolean tests,
fresh helper calls and returns. The declared manager text bank 7520 is
adopted from
`xivl-client-scripts:docs/content-director-ui-contracts.md#caravan-escort-director`,
revision `b407618eab0655b6d769580c6d9fae550366a46a`, paragraph naming
`PopulaceCaravanManager` and bank 7520.
Neither publication establishes the actual provider, schema, locale or
format-argument binding for these cells.

## Authored English content

These are paraphrases of the selected cells, including wording carried
inside their controls. They describe the authored offer rather than a
historical event or an applied game rule.

| Row IDs | Authored content |
| --- | --- |
| 4 | A question asks what the reader wants to ask. |
| 11, 32 | The speaker handles enlistment and limits escorts per caravan to a formatted count, to avoid drawing unwanted attention. |
| 15, 37 | An organization and a caravan destination are selected within the text, followed by an offer of service as an escort. |
| 16 | A question asks about escorting the caravan associated with a selected camp. |
| 23 | A question asks about participating despite not receiving the full amount of seals. |
| 43, 44 | Departure times are generally established, but an early departure is possible if the formatted number of escorts is found with time to spare. |
| 47, 48 | The reader is addressed as an able adventurer and directed toward a caravan associated with another selected camp. |
| 49, 50 | The other road is described as more perilous, with greater rewards, followed by a question about remaining here. |
| 63, 64 | An organization seeks brave people regardless of allegiance to help with important matters. |
| 65 | The task is described as requiring at least a formatted count of skilled fighters at a formatted level or higher. |

The complete selected English cells are byte-identical for pairs 11/32,
15/37, 43/44, 49/50 and 63/64. Those pairs cannot distinguish named rank
states. Rows 47 and 48 differ in wording, while retaining the same selected
camp alternatives and address alternatives. Neither difference assigns a
military rank title or an authoritative eligibility rule.

## Conditional caller joins

Use the caller publication's symbols: `M` is supplied self, `W` is
`worldMaster`, and `H` is one fresh helper result exactly equal to Boolean
true. For entry, `S = A1+A3` and `G = (40 <= A4 and A3 == 0)`.
The rows below match numeric keys only if the actual text lookup resolves
the selected English cells. The formatting tails are supplied operands,
not independently established runtime meanings.

| Published request | Matching rows and selected operands |
| --- | --- |
| Entry, A1 differs from A5 | H selects 63, otherwise 64; M's say tail is A1. |
| Entry, G false | H selects 15, otherwise 37; M's say tail is A1, S. |
| Entry, G true | H selects 47 then 49, otherwise 48 then 50. Only 47/48 receive the tail A1. |
| Entry's first ask | Row 16 receives the published arguments `2,1,1,S` after its row key. |
| Entry, first result 1 and A2 exactly false | After the separately documented dialogue, row 23 receives `2,1,2` after its row key. |
| Entry's W-say | The exact call is `W.say(W,M,65,D,A7,A6)`, with D=A1 when A3 equals 0, otherwise S. |
| Question's repeated menu | Row 4 receives `3,1,3` after its row key. |
| Question, menu result 2 | H selects 11 then 43, otherwise 32 then 44; each selected say receives A3. |

M's selected say layout includes a zero before its formatting tail. W's
row-65 call has a different receiver and no inserted zero after the row key.
Its presence here does not replace the provider with `worldMaster.csv` or
prove how D, A7 and A6 bind to text placeholders.

The caller's strict helper result selects presentation. Under the published
helper binding, it compares a freshly obtained, normalized value numerically
at most 25, including the documented 127-to-0 normalization. Authored
organization, camp and level wording does not rename A1, A4 or A5 as proved
external company, level or rank fields. In particular, the `40 <= A4`
comparison is not established as a character-level rule by row 65's wording.

## Controls and formatting limits

The lossless export keeps control tokens embedded in the cells. Their
syntax follows
`xivl-tools:docs/formats/ssd-sheet.md#rich-string-read-and-text-export-contract`.
The parser's structural names do not execute a formatter. `E8` and `E9`
below denote syntactic unary expression codes, with the following integer
as their index.

| Selected cells | Preserved control structure relevant to the wording |
| --- | --- |
| 15, 37 | `switch` controls use E8 index 1 for organization alternatives and E8 index 2 for destination alternatives. |
| 16 | A `switch` uses E8 index 1 for camp alternatives. This alone does not bind the ask's S operand to that index. |
| 11, 32, 43, 44 | The count contains nested `if`, `switch` and `number` controls using E8 index 1. Its alternatives include number words and numeric formatting. |
| 47, 48 | A camp `switch` uses E8 index 1. An `if` uses E9 index 4 with woman/man address alternatives. |
| 63, 64 | An organization `switch` uses E8 index 1 and includes grammar within its alternatives. |
| 65 | The minimum-fighter count uses nested controls with E8 index 3. The level position has a `number` control with E8 index 2. |

Rows 4, 23, 49 and 50 contain no exported control token. No selected cell
is normalized, flattened or rendered here. Actual selector conventions,
fallback behavior, argument types, number formatting and implicit formatter
inputs remain uninspected. The selected syntax does not prove an actual
displayed number, organization, destination, camp or address.

Questions 4, 16 and 23 identify authored prompts. They do not identify the
adjacent answer strings, native result-to-answer mapping, enabled choices,
default selection or cancellation delivery. The caller publication's numeric
result handling remains unchanged. Neither a question about reduced seals
nor a promise of greater rewards establishes entitlement or settlement.

## Reproduction boundary

Authenticate the declared archive and selected member before parsing it in
memory. Check both header rows, all row widths, selected-key uniqueness and
the listed record locators. Select only English position 1 at the sixteen
keys above. Compare the selected cells' hashes when testing another locale
position, without interpreting that other text. Reject a shifted position,
changed schema, missing selected row, wrong member/provider or stale source
pin before accepting the association.

Compare each paraphrase and control position directly with its selected
cell and each caller join with the pinned publication. Keep encoded controls,
duplicates and raw blank/zero distinctions intact. This needs no corpus
hydration or regeneration. The first unresolved edge is actual
provider/schema/locale and helper-format binding. Native answer mapping,
actual supplied operands, admission, signup, travel and reward grants require
their own evidence.
