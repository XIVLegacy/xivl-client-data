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

Rows 5, 6, 144, 146 and 148 retain encoded minute/shortly alternatives.
The script passes `floor(A1/60+0.5)` with the corresponding text keys. The
matching authored time expressions do not establish native formatting or the
unit or producer of A1. The preceding `1+s` keys match greetings at rows 1-4 with
territorial-force alternatives. The text does not establish the live values
or producers of `speechType` and `townType`.

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
pinned in [tables.json](../manifests/tables.json). English is source column 1
after the row ID in the five-string-column layout, as in the
[text-column convention](materia.md#materia-book).

The exact local input archive is pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json). Read only its
named member, verify the member size/hash, and parse its label/type headers
and the 18 row IDs listed above with Python `csv`. Preserve encoded controls
and row IDs. The rows occupy physical lines 3-8, 59, 90, 106, 110, 114, 126
and 134-139. Physical line numbers include both header rows and must not be
substituted for row IDs. No original Lua or native body is needed to reproduce
these static text observations.
