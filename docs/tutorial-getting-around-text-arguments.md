# Getting Around text arguments

The selected English `xtx/_text_ui` rows 9008 and 9009 each encode one
reference to supplied integer argument 1. It is the row selector of a
`0x28` named-sheet lookup targeting `xtx/displayName`, logical field 1.
Neither row encodes a reference to supplied argument 2 or 3. Each lookup
has no trailing argument expressions, so the published handler constructs
an empty argument container for the nested lookup.

This qualifies the first operand's use as a row key in that namespace.
It does not identify the selected row's subject, resolve its contents or
assign a town, NPC, gender or count meaning to the tutorial operands.

## Selected source and references

The retail build is FINAL FANTASY XIV 1.23b, `2012.09.19.0001`. The
English schema selection is adopted from
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, Static English
definition and UISTR-01, at revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`. It selects the `lang="en"`,
`mode="client"` definition at zero-based sheet ordinal 1, physical `str`
column 0. Logical field 1 maps to that column. Its block ordinal 0 begins
at row 0 and declares 13020 slots.

The following offsets locate only the two selected row windows in data
resource `0x0B4502B5`. Token offsets are zero-based within the decoded
string, after removing the sheet marker and terminator.

| Row | Stored byte span | Decoded bytes | Token counts | `0x28` token offset |
| --- | --- | ---: | --- | ---: |
| 9008, Pad request | `[52844,52887)` | 39 | `0x28`: 1 | 14 |
| 9009, Keyboard request | `[52887,53055)` | 164 | `0x28`: 1; `0x19`: 8 | 8 |

Both `0x28` payloads contain exactly three top-level expressions. In each,
the row operand is expression ordinal 1, counting from zero. Its `0xE8`
selector begins at payload byte offset 17 and has literal index 1.
The selected reference metadata agrees on `xtx/displayName` and logical
field 1. There are no `0xEA`, `0xE9` or `0xEB` references in either row.
The count of `0x19` tokens establishes no downstream rendering behavior.

| Input resource | Bytes | SHA-256 |
| --- | ---: | --- |
| Data `0x0B4502B5` | 71588 | `f99e738cf8762e0831f9675f37ddfea7b6072d475b3d4b0c9edeadb67bb013e0` |
| Enable `0x0B4502B6` | 1552 | `3f7c0b8461cfd18a336fb9bb72dbcd5439e65106eea8ea85a6ab731894866183` |
| Row offsets `0x0B4502B7` | 52080 | `c027d8115b2d9f7a67b0d1f1ec2b6623bdf214defd83f255a00dc96922ff2804` |

The complete decoded string digests, including control tokens but excluding
sheet framing, are:

| Row | SHA-256 |
| --- | --- |
| 9008 | `ceb0dd3e3c91728cb9c301a4a66c8c9b4f99356b03d599432da3c23cdbf61b23` |
| 9009 | `4915ce58d4dee2ce370153fd9af880d583f70b4ab7084ffc5feff374068f305d` |

## Native interpretation and limits

The selected Lua request is owned by
`xivl-client-scripts:docs/normal-tutorial-panel-completion.md`, Getting Around
format operands and Selected text-property request. It forwards three helper
results as R1, R2 and R3 after text key 9008 for Pad or 9009 for Keyboard.
The first-Nil native scan and integer/string serialization remain conditional
on the actual typed native frame. The conditional provider candidate is owned
by `xivl-client-scripts:docs/tutorial-text-reference-provider.md`. Both are
adopted at revision `b4d0e96b02a9bac3b0a62941c0e18493f2b2713f`.

The native composition comes from these publications at decomp revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`:

- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-04:
  `0xE8` reaches the supplied vector through the integer decoder
  `FUN_00CB2D50`, using one-based indexing and requiring variant tag 0.
  `0xE9` and `0xEB` use the decoder's own vector instead.
- `xivl-decomp:docs/resource/rich-text-sheet-and-case-handlers.md`, RT-03:
  handler `FUN_00CA0E20` decodes its row through `FUN_00CB2D50` at
  VA `0x00CA0EB1`, then calls TextModule lookup `FUN_00CA0930`. It builds
  the nested argument container only from expressions after the field.
- The same RT-03 and the plain-reference page's Concrete lookup and
  loaded-schema condition own table/row readiness, logical-field mapping,
  type selection, lookup failure and nested formatting conditions.

Under those published paths, the selected rows use R1 as an integer row
selector and do not forward R2 or R3 through these `0x28` lookups. The absence
of their encoded references is limited to these two English row bodies.
It does not establish that other languages, rows, handlers or downstream
consumers ignore those operands.

The actual native binding and frame, selected receiver and part, preprocessing
state, default-table preservation, loaded locale/schema, ready referenced row,
mapped field type, formatter success, applied property and rendered lesson
remain conditions. No referenced `xtx/displayName` row was decoded here.

## Verification

A bounded Python verifier authenticated the three resources and required
monotonic little-endian row ends, the declared slot count, final data bound
and exactly one matching enable range for each selected row. Each selected
span consumed exactly one complete little-endian length-prefixed `str`
frame. Both were scrambled strings with valid terminators. Independent XOR
readings agreed, and rebuilding the original encoding reproduced both
selected frames exactly in memory.

The verifier checked UTF-8 outside tokens, every declared token length and
closing byte, complete prefix-expression consumption and exact rich-string
reconstruction. Its contract was checked against
`xivl-tools:docs/formats/ssd-sheet.md`, The enable file and the row-offset array,
Rows and columns, The sheet string and its obfuscation, Rich-string control
tokens, and Rich-string read and text-export contract, at revision
`604210657f4858fb69744a3a92c90f3369040057`. Source inspection independently
checked `src/formats/src/sheet.rs`, `parse_sheet_string` and
`encode_sheet_string`, and `src/formats/src/richstring.rs`, `parse_token`,
`parse_expression`, `decode_integer` and `RichString::encode`, in that repository.
No production build or formatter execution is asserted.

Synthetic controls checked supplied versus decoder-owned selectors, literal
indices, the named-sheet row-operand position and packed integers. Rejecting
controls covered changed row spans, enable membership, decreasing or incorrect
final offsets, incomplete string frames, invalid terminators, truncated
payloads, missing closing bytes, missing expression operands, trailing invalid
expression bytes, selected zero integer bytes and invalid text UTF-8.
These strict checks establish the verifier's bounded interpretation. SQTP-05
explicitly distinguishes such span, exhaustion and closing-byte requirements
from the native formatter's weaker validation. Raw strings, complete operand
vectors and token bytes are not retained by this finding.
