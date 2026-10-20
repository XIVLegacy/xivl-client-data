# Request-warden operation text

The retail `populaceRequestWarden.csv` bank contains timed-cull recruitment,
participation and withdrawal text matching numeric keys in the selected
request-warden methods. This static association follows the loaded bank name
and matching row IDs. Helper/native row resolution and rendered strings were
not established. The rows do not identify an actual NPC, content instance or
the normal/company Behest variant. The
`xivl-client-scripts:docs/request-warden-event-contract.md` finding owns the
event argument, retry and return contracts used for the joins below.

## Conditional recruitment rows

Let `s` be the externally supplied `speechType`. The published Join method
passes text key `5+s` when A5 equals numeric zero. Otherwise it passes keys
`143+2*s` and `144+2*s`. The matching bank rows below cover only the listed
values of s:

| A5 branch | s | English row IDs | Authored content |
| --- | ---: | --- | --- |
| Equals numeric zero | 0 | 5 | Adventurers' Guild culls and an invitation to the next operation |
| Equals numeric zero | 1 | 6 | A cull invitation describing beasts threatening the city |
| Otherwise | 0 | 143, 144 | Enlarged creatures and colorless crystals, then a timed cull invitation |
| Otherwise | 1 | 145, 146 | Colorless-crystal rumors, then an organized cull invitation |
| Otherwise | 2 | 147, 148 | Crystals losing their aspects and creatures growing, then an operation invitation |
| Equals numeric zero | 3 | 8 | Creatures must be purged; the operation begins in less than the supplied minute count, or soon |
| Otherwise | 3 | 149, 150 | Threatening creatures, ominous foreign travelers and hostile skies, then an invitation to depart in approximately the supplied minute count, or shortly |

The timing rows retain encoded minute/soon/shortly alternatives.
The script passes `floor(A1/60+0.5)` with the corresponding text keys. The
matching authored time expressions do not establish native formatting or the
unit or producer of A1. The preceding `1+s` keys match greetings at rows 1-4 with
territorial-force alternatives. The text does not establish the live values
or producers of `speechType` and `townType`.

## Retained speechType 3

The conditional initializer binding in
`xivl-client-scripts:docs/request-warden-event-contract.md`, "Retained Warden
initializer", supplies `speechType=3` and `townType=2` for retained actor
`0x44D04940`. It does not supply Join's A5. Both A5 branches use greeting
row 4; only the following recruitment rows differ: row 8 for numeric zero,
or rows 149 and 150 otherwise.

Row 4 contains an encoded switch with the names Knights of the Barracuda,
Holtwatch and Brass Blades. Its native selection/formatting contract was not
established, so townType 2 is not assigned to one alternative here. Row 8
calls for a purge of evil creatures. Row 149 adds ominous travelers,
threatening creatures and hostile skies; row 150 asks adventurers to stand
together and join a departing party. The latter pair changes the authored
recruitment presentation, without naming normal or company Behest.

None of these four English cells labels the operation as normal Behest,
company Behest or a Grand Company mission. The common greeting cannot
distinguish the branches. Neither the text nor the captured speechType
identifies A5's producer or makes A5 a normal/company selector. A retained
event argument or another explicit content binding is still required.

## Menu and retry text

| Method with matching numeric key | English row ID | Text or authored instruction |
| --- | ---: | --- |
| Join widget | 111 | "Participate in the operation?" |
| Cancel widget | 131 | "Withdraw from the operation?" |
| Give-up widget | 63 | "Withdraw from the operation?" |
| End widget | 94 | "Accept the offer?" |
| Join/Cancel retry, s=0 | 115 | Slay all targets in the map-designated area before they escape |
| Join/Cancel retry, s=0 | 119 | A statement that success will be rewarded |

These are authored prompts and instructions, without encounter-state or
reward-grant evidence. Row 157 in the separate `worldMaster:say` call is not
a row join to this bank. The selected operation text supplies no binding for
the Director's externally supplied `requestId` or Guildleve row 1.

## Source and reproduction

The source is extraction `2012.09.19.0001`, `populaceRequestWarden.csv`,
107,647 bytes, SHA-256
`C8D877CA851254DA8247D33F75250C03647E45D00CB30584749266C40374B5C5`,
pinned in [tables.json](../manifests/tables.json). English is the column labeled
`1`, physical CSV field index 2 when the row ID is included, in the
five-string-column layout described by the
[text-column convention](materia.md#materia-book).

The exact local input archive is pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json). Read only its
named member, verify the member size/hash, and parse its label/type headers
and the 21 row IDs listed above with Python `csv`. Preserve encoded controls
and row IDs. The rows occupy physical lines 3-8, 10, 59, 90, 106, 110, 114,
126 and 134-141. Rows 4, 8, 149 and 150 occupy lines 6, 10, 140 and 141.
Physical line numbers include both header rows and must not be
substituted for row IDs. No original Lua or native body is needed to reproduce
these static text observations.
