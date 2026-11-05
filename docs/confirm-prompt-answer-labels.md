# ConfirmWarp and ConfirmRaise answer labels

The selected English `xtx/_text_ui` rows contain these short answer labels,
including their final periods:

| Prompt | Answer position | Row key | Static English label |
| --- | ---: | ---: | --- |
| ConfirmWarp | 1 | 1131 | `Accept.` |
| ConfirmWarp | 2 | 1132 | `Refuse.` |
| ConfirmWarp | 3 | 1136 | `Close.` |
| ConfirmRaise | 1 | 1128 | `Yes.` |
| ConfirmRaise | 2 | 1129 | `No.` |
| ConfirmRaise | 3 | 1136 | `Close.` |

These are static client labels. In particular, `Close.` does not establish
expiry or a timeout, and `Accept.`, `Refuse.`, `Yes.` and `No.` do not prove
authoritative acceptance/refusal, renewal or server policy.

## Conditional request and provider

`xivl-client-scripts:docs/confirm-prompt-client-contracts.md`, Pending work
and prompt presentation, at revision
`64278f28975f345303914f30ee60807c6fe42d0a`, owns the two ordered answer-key
triples and default answer 1. Its Answers and command submission section
owns button results 1/2/3 and cancel result 0. MainMenuWidget omits result 3
from submission, while the matching tray route forwards it. Label wording
does not erase that caller distinction.

The [CommonAsk answer-list contract](https://github.com/XIVLegacy/xivl-client-scripts/blob/main/docs/common-ask-answer-list.md)
owns the original answer-to-item adaptation and conditional native provider
composition. Under its selected bindings and normal prerequisite completion,
the three keys request `Content` on part `TemplateButton_Answer`, in contexts
`Item_Answers1`, `Item_Answers2` and `Item_Answers3`. Its named-context route
adopts the existing native form/request-ID/record/part path into the generic
property setter, then Button/Label Content preprocessing. A successful call
to the item-creation helper alone proves neither created items nor those
actual native targets.

The native publications at Decomp revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce` own the route and provider:

- `xivl-decomp:docs/resource/sqwt-anime-property.md`, Route to the setter and
  Setter: the nonempty leading name selects a request/context ID, while the
  retained part and property names reach `FUN_00537DE0` conditionally.
  `Content` does not take the Anime key/value rewrite.
- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-07:
  selected Button/Label Content info and callback reach preprocessing under
  its property, lookup and owner conditions.
- The same plain-reference page, Default table and named language fields,
  Concrete lookup and loaded-schema condition, and Static English definition:
  the admitted default route uses TextModule and `xtx/_text_ui`, with English
  logical field 1 mapping to physical string column 0.
- The same page, Plain and empty output: a NUL-terminated nonempty string
  without byte `0x02` takes the plain copying path on normal completion.

All five selected labels are nonempty ASCII/UTF-8 without control bytes or
rich-string tokens. Their own contents therefore require no token-handler
interpretation on that published plain path. Actual native frame preparation,
marshalling, bindings, item creation, form/context/record/part lookup,
property admission, preprocessing, default-table preservation, loaded schema,
English selection, ready row, formatter completion, applied property and
rendered text remain conditions. The selected Lua calls supply no locale.

## Original resource identity

The source is retail FINAL FANTASY XIV 1.23b, `2012.09.19.0001`.
The published Static English definition above identifies `xtx/_text_ui`
through master `0x01030000` and definition `0x0B450082`. Its `lang="en"`,
`mode="client"` sheet is ordinal 1, with sole physical column `str` and
logical source index 1. Block ordinal 0 begins at row 0 and declares 13020
slots. This schema is adopted; no definition document was decoded again.

| Resource | Bytes | SHA-256 |
| --- | ---: | --- |
| Data `0x0B4502B5` | 71588 | `f99e738cf8762e0831f9675f37ddfea7b6072d475b3d4b0c9edeadb67bb013e0` |
| Enable `0x0B4502B6` | 1552 | `3f7c0b8461cfd18a336fb9bb72dbcd5439e65106eea8ea85a6ab731894866183` |
| Row offsets `0x0B4502B7` | 52080 | `c027d8115b2d9f7a67b0d1f1ec2b6623bdf214defd83f255a00dc96922ff2804` |

Resource ID bytes `AA BB CC DD` select `data/AA/BB/CC/DD.DAT` under the
supplied install root, with uppercase hexadecimal path components.
Each selected row below is enabled and contains exactly one string frame.
Stored spans include the length, scramble marker and terminator. The decoded
digests exclude that framing. All offsets and ordinals are zero-based.

| Row | Stored span | Stored bytes | Decoded bytes | Decoded SHA-256 |
| --- | --- | ---: | ---: | --- |
| 1128 | `[2414,2422)` | 8 | 4 | `5f9a2b795615ba6a3d5455fd5624d773fbca5bcd16249c421fd37411dc9837da` |
| 1129 | `[2422,2429)` | 7 | 3 | `38178a20b470cfd18299fb1593dd4ba706f1a83321dac051d01086efd8b7a96f` |
| 1131 | `[2493,2504)` | 11 | 7 | `f02ae116e4c5a651e903479246e04215856a31a4e7f43d7f657140fc15cc49a3` |
| 1132 | `[2504,2515)` | 11 | 7 | `f78d9bb769de02f1c309398d6ed3b061d7859760f168244c7a9b9e0d19d82e0b` |
| 1136 | `[2565,2575)` | 10 | 6 | `ff2b71bdbe08a0bdcc205331d2f814f6238f41b2d1487c7e148dfec906dac602` |

## Bounded reproduction

Authenticate only the three resources above, including their non-reparse
paths. Require exactly 13020 little-endian 32-bit row ends, monotonic ends
and a final end equal to the data length. Each selected row must belong to
exactly one enable range and have the exact nonempty span above. Decode no
adjacent row or question row.

`xivl-tools:docs/formats/ssd-sheet.md`, The enable file and the row-offset
array, Rows and columns, and The sheet string and its obfuscation, at revision
`604210657f4858fb69744a3a92c90f3369040057`, owns the adopted framing.
The inspected `src/formats/src/sheet.rs`, `parse_sheet_string` and
`encode_sheet_string`, supplies the matching reader/writer contract.
No production build or native formatter execution is asserted.

Each selected span consumed exactly one complete little-endian `u16`
length-prefixed string. Each body began with `0xFF` and ended with `0x73`.
XOR `0x73` between those bytes recovered the label. Independent byte readings
agreed, strict UTF-8 decoding succeeded and rebuilding the framing reproduced
every selected stored span exactly in memory. No decoded control byte,
including `0x02` or NUL, occurred.

Synthetic plain and scrambled strings passed. Rejecting checks covered wrong
row, field, physical column, locale, namespace, enable membership and selected
span boundaries, zero or inconsistent lengths, truncated frames, wrong
terminators, invalid UTF-8, embedded NUL/control-token leads and trailing
bytes. These strict checks describe this bounded verifier, without assigning
the same validation rules to the native formatter. Only the five short labels
and identity metadata are retained; no raw row frame, other row or CSV was
retained or decoded.
