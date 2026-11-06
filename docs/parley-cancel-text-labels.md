# Parley cancel-confirmation text

The selected English `xtx/_text_ui` rows contain these literal strings,
including the question mark and final periods:

| Request role | Row key | Static English wording |
| --- | ---: | --- |
| Question | 7124 | `Abandon the parley?` |
| Answer 1 | 7125 | `Yes.` |
| Answer 2 | 7126 | `No.` |

Under the published conditional CommonAsk initialization frame, the default
answer operand is 2, corresponding to `No.`. Numeric child result 1,
corresponding to the first answer `Yes.`, requests parent base result -1.
This joins static wording to request and callback positions. It establishes
neither an actual default focus, a user choice nor an accepted gameplay quit.

## Conditional request and provider

`xivl-client-scripts:docs/parley-cancel-confirmation-request.md`, Conditional
creation and initialization and Child result and confirmed-cancel continuation,
revision `a111d29100881b03f92c3db67ac5fe9e17561392`, owns the selected
desktop/parent receivers, child-opening projection and exact numeric-result
comparison. Its actual creation, binding, converted-frame and delivery
conditions remain required. Under the matching delivered frame and shared
initializer bindings, CommonAsk receives `(C,nil,7124,2,7125,7126)`.

The following Script publications are adopted at that same revision:

- `xivl-client-scripts:docs/common-ask-text-request.md`, Original initializer
  contract: C requests question key 7124 on `TextBlock_Question`, supplies the
  complete two-answer tail and requests `askDefaultAnswer=2`.
- `xivl-client-scripts:docs/common-ask-answer-list.md`, Selected helper
  contract and Numeric named-context projection: answers 7125 and 7126
  request `Content` on part `TemplateButton_Answer`, in contexts
  `Item_Answers1` and `Item_Answers2`, respectively.
- `xivl-client-scripts:docs/parley-topic-text-provider.md`, Request and wrapper
  projection: the selected `setText` and `setItemText` wrappers route the
  question through the numeric `setTextProperty` path.
- `xivl-client-scripts:docs/confirm-prompt-client-contracts.md`, Answers and
  command submission: numbered CommonAsk answers produce numeric results;
  UI cancel produces 0, with parent-callback and closure requests.

With those actual methods, normal prerequisite completion and the reached
`type(key)` result exactly `"number"`, the three native request candidates
are:

```text
_setTextProperty(C,nil,"TextBlock_Question","Text",7124)
_setTextProperty(C,"Item_Answers1","TemplateButton_Answer","Content",7125)
_setTextProperty(C,"Item_Answers2","TemplateButton_Answer","Content",7126)
```

Each has an empty Lua formatting tail. The numeric wrapper captures the
native method and C after the type call. The question uses the leading-Nil
Text route; the answers use the distinct named-context Content route.

The adopted native Property access and Native frame contracts are
`xivl-client-structs:docs/widget-native-call-contract.md` and
`xivl-client-structs:docs/global-native-contract.md`, revision
`180ab8aaa49b0157fee8996abe4d27e05b588bda`. Actual binding, marshalling and
preparation must produce and preserve the corresponding typed frame and
values. The non-Nil identifier serializer begins `@7124`, `@7125` or
`@7126` and scans integer/string alternatives until its first Nil.
Exactly zero serialized format arguments requires the first actual prepared
scan cell to be Nil. An empty Lua tail alone does not establish that cell
or the actual native argument count.

The native provider composition adopts these publications at Decomp revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`:

- `xivl-decomp:docs/resource/sqwt-anime-property.md`, Route to the setter and
  Setter: the leading name selects a form/request context, with request-ID,
  record, part and receiver/value gates before generic property processing.
  `Text` and `Content` retain their own keys and reference strings.
- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-03:
  successful lookup and visibility, selected TextBlock.Text info, permitted
  owner interception and admitted preprocessing qualify the question route.
- The same page, SQTP-07: the selected Button/Label Content info and callback
  connect the answers to ContentControl preprocessing. This retains the
  published registration/lookup inference and actual target conditions.
- The same page, Default table and named language fields, Concrete lookup
  and loaded-schema condition, and Static English definition: the admitted
  default route retains TextModule and uses `xtx/_text_ui`, unless a pending
  table override replaces it. English logical field 1 maps to physical
  string column 0, native type 10.

Property flags, TLS, interface and table selection, preliminary-helper
effects including aliased-input changes, preprocessing admission, schema
loading and row readiness remain conditions. The selected Lua calls supply
no locale. No raw form or template was decoded for this composition, and no
actual form, context, Button or TextBlock instance is identified here.

## Original and canonical English sources

These are `client_extraction` findings for retail FINAL FANTASY XIV 1.23b,
extraction `2012.09.19.0001`. The adopted Static English definition identifies
`xtx/_text_ui` through master `0x01030000`, reference ordinal 32, and definition
`0x0B450082`. Its unique explicit `lang="en"`, `mode="client"` sheet is
ordinal 1, with sole physical column `str` and logical source index 1.
Block ordinal 0 begins at row 0 and declares 13020 slots. This schema is
adopted without another definition-document decode.

| Resource | Bytes | SHA-256 |
| --- | ---: | --- |
| Data `0x0B4502B5` | 71588 | `f99e738cf8762e0831f9675f37ddfea7b6072d475b3d4b0c9edeadb67bb013e0` |
| Enable `0x0B4502B6` | 1552 | `3f7c0b8461cfd18a336fb9bb72dbcd5439e65106eea8ea85a6ab731894866183` |
| Row offsets `0x0B4502B7` | 52080 | `c027d8115b2d9f7a67b0d1f1ec2b6623bdf214defd83f255a00dc96922ff2804` |

Resource ID bytes `AA BB CC DD` select `data/AA/BB/CC/DD.DAT` under the
supplied install root, with uppercase hexadecimal path components.
Each selected row is enabled and occupies exactly one complete scrambled
string frame. Stored spans include the length, scramble marker and terminator.
Decoded lengths and digests exclude that framing. Offsets and ordinals are
zero-based; span ends are exclusive.

| Row | Original span | Frame bytes | Decoded bytes | Canonical physical line |
| ---: | --- | ---: | ---: | ---: |
| 7124 | `[51360,51383)` | 23 | 19 | 1915 |
| 7125 | `[51383,51391)` | 8 | 4 | 1916 |
| 7126 | `[51391,51398)` | 7 | 3 | 1917 |

| Row | Decoded SHA-256 |
| ---: | --- |
| 7124 | `a1292312c003a4adf51e1c5be87175ed51922fe161e1b6de82b206e8ea4aea55` |
| 7125 | `5f9a2b795615ba6a3d5455fd5624d773fbca5bcd16249c421fd37411dc9837da` |
| 7126 | `38178a20b470cfd18299fb1593dd4ba706f1a83321dac051d01086efd8b7a96f` |

The canonical counterparts are `csv/xtx__text_ui.csv`, column label `1`,
declared `str`, zero-based CSV field index 2 including the leading row-ID
field. This CSV field differs from original physical column 0.
[tables.json](../manifests/tables.json) pins the whole CSV at 1284564 bytes,
SHA-256 `23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece`.
The authenticated containing archive is pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json).
Only the three selected English cells were decoded. Their literal spellings
reproduce the original decoded bytes, and re-export reproduces each cell.

All three bodies are nonempty ASCII/UTF-8 with no embedded NUL, control byte
`0x02` or encoded argument reference. The published Plain and empty output
contract therefore supplies the conditional plain-copy interpretation,
subject to its normal allocation, copy and helper completion conditions.
No token-handler interpretation is needed for these bodies. Their contents
do not establish the actual native argument vector, property application
or rendered wording.

## Verification and result boundary

The caller's accepted committed page and the complete conditional provider
and schema composition were authenticated before any selected row body or
canonical cell was decoded. Checks authenticated non-reparse paths, the
three original resources and canonical archive/member. They required exactly
13020 monotonic little-endian row ends, a final end equal to data length,
unique selected enable membership and the exact spans above.

The adopted format contract is `xivl-tools:docs/formats/ssd-sheet.md`, The
enable file and the row-offset array, Rows and columns, and The sheet string
and its obfuscation, revision `604210657f4858fb69744a3a92c90f3369040057`.
That revision's `src/formats/src/sheet.rs`, `parse_sheet_string` and
`encode_sheet_string`, and `src/formats/src/richstring.rs`, `from_lossless_text`
and `to_lossless_text`, own the framing and canonical literal-text transform.
Each selected little-endian u16 length-prefixed frame consumed its entire
row span. Its body began with `0xFF` and ended with `0x73`. XOR `0x73` between
those body bytes recovered
the text. Independent byte readings, exact frame reconstruction and
canonical decode/re-export agreed in memory.

Synthetic plain and scrambled frames passed. Rejecting controls covered the
accepted-caller gate, wrong provider/schema/locale, question or answer role,
default-answer position, native-count inference, wrong row/span/enable,
length, scramble marker, terminator, truncation, trailing bytes, control
tokens and changed literal/canonical wording. A synthetic multiline CSV
control distinguished a real selected record from a matching row spelling
inside another quoted field. Other locale cells were left undecoded.
These strict checks describe the verifier, without asserting equivalent
native rejection. No build or client/native execution was used.

The published callback contract leaves answer 2 and UI cancel 0 without a
base-result write through this `processAskResult` body. It does not prove an
earlier parent result was zero or exclude another writer. The default request
for `No.` does not demonstrate actual focus or automatically produce that
answer. The `Yes.` wording and requested -1 do not establish accepted
cancellation, expiry, a timeout, authoritative settlement or a historical
Parley outcome. Actual bindings, native frames, parent selection, callback
delivery, storage/readback, locale, formatting, property application and
rendering remain unresolved.
