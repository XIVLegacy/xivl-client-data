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

The following consecutive rows supply the authored choices. Their order is
not, by itself, a native widget result-code contract.

| Prompt | Consecutive choice row IDs | English choices in row order |
| --- | --- | --- |
| 111 | 112, 113, 114 | Yes; No; Learn operation objectives |
| 131 | 132, 133, 134 | No; Yes; Review operation objectives |
| 63 | 64, 65 | Yes; No |
| 94 | 95, 96, 97 | Yes; Remain here; Cancel |

Rows 90-93 offer transportation. Each contains an encoded `aetheryte` sheet
reference nested inside an `xtx/placeName` noun control and a conditional
"'s aetherial gate" suffix. The matching End method supplies two formatting
arguments. These rows do not describe cancellation, completion or withdrawal
state codes. Their exact native parameter evaluation remains unbound.

Row 157 says that the behest for the supplied place is recommended for the
supplied adventurer level. Its controls contain `xtx/placeName` and a number.
The Join call `worldMaster:say(self,157,A3,A4)` passes the Warden object
explicitly. The helper receiver name does not select a text bank: the Lua
helpers forward the explicit owner and message arguments to the native
message pool. Row 157 exists in this Warden bank and is absent from
`worldMaster.csv`. This is a static text association, without a retained
rendered message or a proven native formatting range.

## Request article text

`worldMaster.csv` row 50090, physical line 1826, contains the exact control:

```text
[@head-all:022d2cff2a022826ff107874782f646973706c61794e616d65ff1202280eff0872657175657374e802e80303020303]
```

Its nested sheet controls name `xtx/displayName` and `request`; the latter
retains the two operand expressions `E8 02` and `E8 03`. The expression
grammar is recorded in `xivl-tools:docs/formats/ssd-sheet.md`, "Rich-string
read and text-export contract". That grammar preserves expressions without
executing their runtime meaning. The scripts contract traces `requestId`
and the objective selector into this article's formatting arguments. The
encoded reference does not establish an encounter instance, a server token
allocation rule or a native row lookup on its own.

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
and the row IDs listed above with Python `csv`. Preserve encoded controls
and row IDs. The recruitment/retry selection occupies physical
lines 3-8, 10, 59, 90, 106, 110, 114, 126 and 134-141. The menu and
transport selection occupies lines 59-61, 86-93, 106-109, 126-129 and 148.
Rows 4, 8, 149 and 150 occupy lines 6, 10, 140 and 141.
Physical line numbers include both header rows and must not be
substituted for row IDs. `worldMaster.csv` contains 1,851,138 bytes with
SHA-256 `2E2E2DD5CD9651388F6FA575B4229081AD0452165E78B725DF0A5B5B7CF7C643`,
also pinned in `tables.json`. The same archive/member check and Python CSV
query reproduce its row 50090 and the absence of row 157. No original Lua
or native body is needed to reproduce these static text observations.
