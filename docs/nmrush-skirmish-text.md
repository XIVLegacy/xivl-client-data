# NMRush guide Skirmish text

The retail `populaceNMRushGuide.csv` bank explicitly names Skirmish. Its
English row IDs match numeric arguments in the published
`PopulaceNMRushGuide` methods, whose initialization loads
`(10608, "populaceNMRushGuide")`. This is a static association through the
loaded bank name and matching keys. Helper/native text resolution, rendered
strings and a live guide actor were not established.

The argument order, talk modes and result arities belong to
`xivl-client-scripts:docs/nmrush-guide-director-contract.md`, Guide arguments
and results. The text below adds authored content identity to those numeric
calls without changing their return contract.

## Selected English rows

| Method with matching numeric key | Row IDs | Authored content |
| --- | --- | --- |
| `processWarpAsk` messages | 19, 20 | The speaker names himself Captain Berkoeya Loetahlsyn, describes training Grand Company soldiers for the Eorzean Alliance, and welcomes them to Skirmish |
| `processWarpAsk` menu argument | 21 | "Participate in Skirmish?" |
| First key in its option list | 22 | "No." |
| `processBattleAsk` messages | 29-31 | Island training against powerful creatures and an instruction to defeat all enemies |
| `processBattleAsk` menu argument | 32 | "What will you do?" |
| First key in its option list | 33 | "Commence Skirmish." |
| `processBattleEnd` message | 44 | Praise after battle and a warning of coming war |
| `processContentEndAsk` message | 46 | A taunt about a blistered thumb |
| First key in its option list | 49 | "Yes." |

Row 19 is an authored self-introduction, without a spawn record identifying
an actual NPC. The selected island dialogue names no site. The menu labels
do not establish the numeric result returned for a choice or the caller's
response to it. The published ask methods retain and return one option
result without interpreting it.

The rows do not bind either `QuestDirectorNMRush01` or
`QuestDirectorNMRush02` to a particular instance. Instructions and battle
praise do not prove admission requirements, encounter composition, waves,
state progression, termination or reward grants. The script finding owns
the separately established Director01 UI-state branches.

## Source and reproduction

The source is extraction `2012.09.19.0001`, `populaceNMRushGuide.csv`,
14,034 bytes, SHA-256
`D0517710E8E6D74325E5E75BEA431FB2BD47D350A309D10AE8B15459ED5B61B4`,
pinned in [tables.json](../manifests/tables.json). English is source column 1
after the row ID in the five-string-column layout documented by the
[text-column convention](materia.md#materia-book).

Read only this member from the exact archive pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json), verify its
size/hash, then parse its label/type headers and the 12 row IDs above with
Python `csv`. Preserve encoded controls and row IDs. Their physical lines
are 6-9, 16-20, 27-28 and 31, including both header rows. Physical line
numbers are not row IDs. This reproduces the static cell/key associations
without an original Lua/native body or a claim about helper execution.
