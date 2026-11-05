# Localized Getting Around text arguments

The selected Japanese, German and French `xtx/_text_ui` rows 9008 and 9009
each encode exactly one `0xE8` reference with literal index 1. None encodes
a reference to supplied argument 2 or 3, or an `0xEA`, `0xE9` or `0xEB`
reference. No control token is nested inside a string expression in these
six bodies. This extends the
[English finding](tutorial-getting-around-text-arguments.md) only to these
explicit locale selections and rows.

The Japanese reference occupies the row operand of a `0x28` lookup of
`xtx/displayName`, logical field 0, with an empty nested argument container
under the published handler. German and French instead contain `0x32` and
`0x33` tokens. Their operand syntax is established below, but their native
operand meanings remain unresolved.

## Selected resources and schema

The retail build is FINAL FANTASY XIV 1.23b, `2012.09.19.0001`. The master
resource `0x01030000` identifies `xtx/_text_ui` uniquely at zero-based
reference ordinal 32, pointing to definition resource `0x0B450082`.
Only the following `mode="client"` definitions are selected. Each has one
physical `str` column, ordinal 0, and block ordinal 0 begins at row 0 with
13020 slots.

| Language | Definition ordinal | Logical field | Data / enable / row-offset resources |
| --- | ---: | ---: | --- |
| `ja` | 0 | 0 | `0x0B4502C1` / `0x0B4502C2` / `0x0B4502C3` |
| `de` | 2 | 2 | `0x0B45029A` / `0x0B45029B` / `0x0B45029C` |
| `fr` | 3 | 3 | `0x0B4502A6` / `0x0B4502A7` / `0x0B4502A8` |

The explicit language-to-reference-field mapping agrees with
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, Default
table and named language fields, at revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`. This schema evidence selects no
running locale or loaded provider.

Each selected row has exactly one matching enable range. Stored spans
below are half-open byte offsets in the selected data resource. Decoded
bytes exclude the sheet marker and terminator, retaining all control tokens.

| Language | Row | Stored span | Stored bytes | Decoded bytes |
| --- | ---: | --- | ---: | ---: |
| `ja` | 9008 | `[67143,67293)` | 150 | 146 |
| `ja` | 9009 | `[67293,67802)` | 509 | 505 |
| `de` | 9008 | `[62795,62868)` | 73 | 69 |
| `de` | 9009 | `[62868,63075)` | 207 | 203 |
| `fr` | 9008 | `[61429,61487)` | 58 | 54 |
| `fr` | 9009 | `[61487,61745)` | 258 | 254 |

Exact input identities are:

| Resource | Bytes | SHA-256 |
| --- | ---: | --- |
| `0x01030000` | 7044 | `860023878f9ad1e98fd1baa3e3380f971f86bf1f7747043cf0c3c7459cee2eb4` |
| `0x0B450082` | 3099 | `27e50caf3d258e8eed2d9e70bc8355e2ab67f54f2dc8bf54e6cfcdf604e5e492` |
| `0x0B4502C1` | 98509 | `8cbf3beef76acec4fd8df31250b8c5e44ea5b1175b77798f887773aabc9b46f6` |
| `0x0B4502C2` | 1544 | `f99e1a16572b6c0b5d20ebefa6b3e00c2ed3928d10ea37b542b362fef50e5e74` |
| `0x0B4502C3` | 52080 | `bc4b1003d6c76cfa376324beb401acf0d541a5f470f50dab732998a4462d7bf4` |
| `0x0B45029A` | 85839 | `b234f9a63f12a22a15d3fdb5879c1d19bf5879ad02eaddcc5d99f6fbe72dd577` |
| `0x0B45029B` | 1544 | `f99e1a16572b6c0b5d20ebefa6b3e00c2ed3928d10ea37b542b362fef50e5e74` |
| `0x0B45029C` | 52080 | `e8b91822b85117a5160971d9cc20c0bdcc14f7831880a3b6776564f32937713b` |
| `0x0B4502A6` | 83641 | `ef0931c6e21955d740e6c609e23360013156603b5c060177e9de32d2f2ceb3cc` |
| `0x0B4502A7` | 1544 | `f99e1a16572b6c0b5d20ebefa6b3e00c2ed3928d10ea37b542b362fef50e5e74` |
| `0x0B4502A8` | 52080 | `ff0b327b89d63f7e00b21aa7ebba8b4c3f21ee7a6742d235a808ae5e4d13b1c1` |

The independently decoded master is 7043 bytes, SHA-256
`508ae64ce9d60c18241dba3200ba317157f086e201fe0b0fce3aeb807c9ec113`.
The decoded definition is 3098 bytes, SHA-256
`2763f4ae79453b368b74f844f9a53647c6788e1c37a327258fd297327f799bac`.
The complete decoded row identities are:

| Language | Row | Decoded SHA-256 |
| --- | ---: | --- |
| `ja` | 9008 | `4f759faac871de23b0f8ad31fbbdc8d29e2c1873f8385c107c1484a49f4da07d` |
| `ja` | 9009 | `895479385977d1665e3f69b1619fd8f60b4c95536284eca8470c50d13831433a` |
| `de` | 9008 | `85f9e4bd00b99351acd8c1346350a7f6ce985dd66280111b644e86ea688ffc74` |
| `de` | 9009 | `eaaf228930c7cae0f27b70156f307a5693c99da89859abc0f60c74ad7f9d447b` |
| `fr` | 9008 | `45237736b73772d3de04f283753a3a842e9a1b75cb2a8c1e37dcf0014e370f25` |
| `fr` | 9009 | `08a90fb312854382862d2b90984ac3d245b9531b541a9c2e517072b85c2c8d34` |

## Exact relevant reference structure

All offsets and expression ordinals below count from zero. Token offsets
are in the decoded row string. Reference offsets are in that token's payload.
Within each language, both selected rows have the same relevant structure.

| Language | Token offset | Code | Top-level expressions | `0xE8` expression ordinal | `0xE8` payload offset | Literal index |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| `ja` | 66 | `0x28` | 3 | 1 | 17 | 1 |
| `de` | 41 | `0x32` | 6 | 2 | 18 | 1 |
| `fr` | 27 | `0x33` | 5 | 2 | 18 | 1 |

The Japanese `0x28` has literal string `xtx/displayName` at expression 0,
the direct `0xE8` reference at expression 1 and literal field 0 at expression
2. There are no expressions after the field. The German and French tokens
also have literal string `xtx/displayName` at expression 0 and a direct
`0xE8` reference, without a surrounding comparison or nested string, at
expression 2. The string literal alone does not establish that these codes
use the same lookup operands or nested argument construction as `0x28`.
Other literals are not assigned grammatical, quantity or identity meanings.

## Published native composition and limits

`xivl-client-scripts:docs/normal-tutorial-panel-completion.md`, Getting Around
format operands and Selected text-property request, owns the selected Lua
request. It forwards R1, R2 and R3 after key 9008 for Pad or 9009 for Keyboard.
The conditional integer/string serialization, first-Nil termination and
actual typed-frame requirement remain in that contract. The conditional
default `xtx/_text_ui` provider is owned by
`xivl-client-scripts:docs/tutorial-text-reference-provider.md`, Selected
request and native property route and Default table, fields and remaining
values. Both publications are adopted at revision
`297a21a9bfa87f71bd033294fc92b087fd553e40`.

The following decomp publications are adopted at revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`:

- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-04:
  the integer decoder `FUN_00CB2D50` interprets `0xE8` through the supplied
  vector using a one-based index and variant tag 0. `0xE9` and `0xEB` use
  the decoder-owned vector instead. These are decoder semantics, not a proof
  that every handler passes an operand to that decoder.
- `xivl-decomp:docs/resource/rich-text-sheet-and-case-handlers.md`, RT-03:
  `0x28` handler `FUN_00CA0E20` decodes its row through that integer decoder
  at VA `0x00CA0EB1`. It constructs the nested argument container only from
  expressions following the field. Applied to the selected Japanese tokens,
  R1 is therefore an integer row selector for `xtx/displayName`, field 0,
  and the nested lookup receives an empty container.
- The same page, RT-01, identifies constructor-selected handlers `0x32` and
  `0x33` through thunks `0x00CA15F0` and `0x00CA1610`, virtual offsets
  `+0x94` and `+0x98`, as `0x00CA13A0` and `0x00CA13D0`. Their operand
  processing is outside the admitted published contracts. Native interpretation
  stops at those handlers. In particular, neither the modern parser names nor
  the `xtx/displayName` literals prove their field, row, grammar or argument
  forwarding semantics.

Thus these six bodies contain no encoded R2/R3 reference. That syntactic
absence does not prove that every handler or downstream consumer ignores
R2/R3. Only the Japanese `0x28` tokens support the matching published row-key
and empty-container interpretation. No referenced display-name row is read.

Actual native binding and typed frame, receiver and selected part,
preprocessing and default-table preservation, provider and loaded locale/schema,
ready rows, mapped field/type, successful formatting, storage and rendering
remain conditions. No translation, subject identity, historical town or NPC
identity, or gender/count meaning follows from these rows or helper values.

## Verification

A bounded Python verifier authenticated the eleven exact resources and their
non-reparse ancestors. It decoded only the two declared documents and six
selected row windows. Independent document decoding agreed with
`xivl-tools:tools/research/census_sheet_stack.py`, `decode_document`, and
re-encoding reproduced both original document containers in memory.

The verifier required unique master/locale/block selection, exact field/type
maps, monotonic little-endian row ends, the declared slot count and final data
bound, and unique selected enable membership. Each row consumed exactly one
complete length-prefixed string frame. Independent XOR readings agreed.
UTF-8 text runs, complete token frames, prefix-expression operands and nested
string bodies were checked, then reconstructed expressions, rich strings and
sheet frames reproduced all six original row encodings exactly in memory.

The parsing contract was checked against
`xivl-tools:docs/formats/ssd-sheet.md`, The enable file and the row-offset
array, Rows and columns, The sheet string and its obfuscation, and Rich-string
read and text-export contract, and against `src/formats/src/sheet.rs`,
`parse_sheet_string` / `encode_sheet_string`, and
`src/formats/src/richstring.rs`, `parse_expression` / `decode_integer` /
`RichString::encode`, at revision `604210657f4858fb69744a3a92c90f3369040057`.
No production build or native formatter invocation is asserted.

Controls distinguished supplied versus decoder-owned selectors, indices
1/2/3, operand positions and packed integers. Rejecting controls changed
selected reference ownership/index/position, locale/field, row span,
enable membership, offset ordering/final bound, frame length/terminator,
token span/closing byte, expression completeness, packed selected zero bytes
and text UTF-8. These strict checks prove the verifier's bounded reading.
SQTP-05 explicitly preserves the native formatter's weaker validation:
strict parser rejection does not prove native rejection. Raw row strings,
token bytes, complete ASTs and operand vectors are not retained.
