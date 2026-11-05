# Getting Around display-name labels

The three published nondefault Getting Around R1 values select these English
logical-field-1 labels in `xtx/displayName`:

| Local numeric selector | R1 row key | Static English label |
| --- | ---: | --- |
| 1 | 1600150 | `Rostnsthal` |
| 2 | 2300120 | `Yda` |
| 3 | 1100003 | `Ascilia` |

These are decoded sheet labels. They establish neither city names for the
numeric selectors nor the identity of a spawned actor or historical NPC.

## Composition with the tutorial request

The [English text-argument finding](tutorial-getting-around-text-arguments.md)
owns the selected `xtx/_text_ui` rows 9008 and 9009. Each contains a `0x28`
lookup of `xtx/displayName`, using supplied integer argument 1 as its row
selector and literal logical field 1. Each has an empty nested argument
container. That finding is adopted at Data revision
`1b4bcb81f9522d72febf5041b6d164dbd149c714`.

`xivl-client-scripts:docs/normal-tutorial-panel-completion.md`, Getting Around
format operands and Selected text-property request, at revision
`297a21a9bfa87f71bd033294fc92b087fd553e40`, owns the exact local selector
comparisons and R1 values above. Under its selected bindings and normal call
completion, the corresponding R1 can therefore request the label in this
table through either selected English tutorial row.

The outer conditional provider remains owned by
`xivl-client-scripts:docs/tutorial-text-reference-provider.md`, Default table,
fields and remaining values, at revision
`b4d0e96b02a9bac3b0a62941c0e18493f2b2713f`. The native named-sheet lookup,
logical-field mapping and nested formatting conditions remain owned by these
publications at Decomp revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`:

- `xivl-decomp:docs/resource/rich-text-sheet-and-case-handlers.md`, RT-03:
  handler `FUN_00CA0E20` passes the name, row, logical field and its own
  trailing-expression container to `FUN_00CA0930`.
- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, Concrete
  lookup and loaded-schema condition: ready table/row lookup and the loaded
  index/type arrays select a physical field. Schema `str` maps to native
  type 10 and reaches the string formatter.
- The same plain-reference page, Plain and empty output: a NUL-terminated
  string without `0x02` takes the plain copying path, conditional on normal
  helper and allocation completion.

All three selected labels are nonempty UTF-8 without control bytes, including
`0x02`. Thus their own selected strings require no nested control-token
interpretation under that published plain-string path. This does not establish
success of the containing tutorial row's formatter or its other tokens.

Actual getter values and their domain, method/native binding, typed frame,
selected receiver and part, preprocessing state, default-provider preservation,
loaded locale/schema, ready rows, formatter success, applied property,
rendered lesson and historical acceptance remain conditions.

## Original resource and schema identity

The source is retail FINAL FANTASY XIV 1.23b, `2012.09.19.0001`.
Master resource `0x01030000` has one reference named `xtx/displayName`, at
zero-based reference ordinal 12, naming definition `0x0B450000`. That
definition has one `lang="en"`, `mode="client"` sheet at zero-based ordinal 1.
Its five physical types, in order, are `str,str,s8,s8,s8`, and its source
logical-index sequence is `1,2,3,4,5`. The published native index-construction
contract therefore maps logical field 1 to physical string column 0.
This static selection does not establish a running locale or loaded provider.

A resource ID written as big-endian bytes `AA BB CC DD` resolves to
`data/AA/BB/CC/DD.DAT` under the supplied retail install root. The definition
explicitly names every backing resource below.

| Resource | Bytes | SHA-256 |
| --- | ---: | --- |
| Master `0x01030000` | 7044 | `860023878f9ad1e98fd1baa3e3380f971f86bf1f7747043cf0c3c7459cee2eb4` |
| Definition `0x0B450000` | 16987 | `7c9b77f9e5989c1c85bbd8152162160cc423f1a6ca17b730f51b5ddc5e4ff866` |
| Data `0x0B4505A0` | 8617 | `945dcef1b5fca12b13f4a3378f600a47796cfb5f8db979c7d6dbd30f13d94e0e` |
| Enable `0x0B4505A1` | 48 | `4f3c654a141ba723d056ecc401fc7a3f15b8b13266967f0631aabc5dc6e73d7d` |
| Offsets `0x0B4505A2` | 2244 | `289748b06036fb212809a7c642fa71f9a335bc197a8c13dad4e732302a5ba7ff` |
| Data `0x0B4505AF` | 2514 | `6f8620690ae3cc12d330216cca1609e66b6f2cd62217faca1eecacacdb82cd3c` |
| Enable `0x0B4505B0` | 40 | `ec8c7c658064fb861217ae189a256e07a3c0796be0850a632132f6998c7975d2` |
| Offsets `0x0B4505B1` | 604 | `c583381ecd6e2123499959aa5dd9c663c9de566116b77d7568e0d0ccd2a3e2d1` |
| Data `0x0B450594` | 10002 | `9f129150d64bbfa4cd393bd6c13b7b27c0ced81a1738cbfc77130463074a6206` |
| Enable `0x0B450595` | 96 | `ee1b63bf14d7cc66b81214647a2dcdb9b7271cc1cbba9b0473aa129ab6098bbe` |
| Offsets `0x0B450596` | 2404 | `a9060aead5fab5248b9efa4952b2e70924ddb6c5296fa4d824cf4416e4fd8dd9` |

The decoded master is 7043 bytes, SHA-256
`508ae64ce9d60c18241dba3200ba317157f086e201fe0b0fce3aeb807c9ec113`.
The decoded definition is 16986 bytes, SHA-256
`b11c4640b3133419a15ffecb3c99a1414f75a3f40a689abb456d74383ab42498`.

| Row | Block ordinal | Block begin / slots | Data / enable / offsets | Complete stored row span | Selected column-0 frame span |
| --- | ---: | --- | --- | --- | --- |
| 1600150 | 7 | 1600000 / 561 | `0x0B4505A0` / `0x0B4505A1` / `0x0B4505A2` | `[3677,3702)`, 25 bytes | `[3677,3691)`, 14 bytes |
| 2300120 | 13 | 2300000 / 151 | `0x0B4505AF` / `0x0B4505B0` / `0x0B4505B1` | `[2496,2514)`, 18 bytes | `[2496,2503)`, 7 bytes |
| 1100003 | 2 | 1100000 / 601 | `0x0B450594` / `0x0B450595` / `0x0B450596` | `[41,63)`, 22 bytes | `[41,52)`, 11 bytes |

All ordinals and offsets are zero-based. Stored spans include sheet framing.
Decoded-label hashes exclude the length, scramble marker and terminator:

| Row | Decoded label bytes | SHA-256 |
| --- | ---: | --- |
| 1600150 | 10 | `8119e3994321daa70bafb5f406e47724a423f0aad1d45f967ea142b3f975060d` |
| 2300120 | 3 | `adb3e4ca807360b2773019a509ca5bc2094f8d8293b300f9e8ecf93048e013d6` |
| 1100003 | 7 | `9196f43f3e1abc0d1e6520e90ed74eac9adec2b66e7c7bba08f9cfd23417b1fb` |

## Bounded reproduction

Authenticate only the master, definition and three declared triples above.
Decode the documents in memory with the transform in
`xivl-tools:tools/research/census_sheet_stack.py`, `decode_document`, at revision
`604210657f4858fb69744a3a92c90f3369040057`. Independently decoding and
re-encoding the two documents reproduced their exact stored bytes. Select the
named reference and English schema by the ordinals and attributes above.

At the same Tools revision, `docs/formats/ssd-sheet.md`, The enable file and
the row-offset array, Rows and columns, and The sheet string and its
obfuscation, owns the framing contract. `src/formats/src/sheet.rs`,
`parse_enable_file`, `parse_row_offsets`, `parse_sheet_string`,
`encode_sheet_string` and `parse_column`, supplies the inspected reader/writer
and one-byte `s8` width. No production build or formatter execution is asserted.

Require exactly the declared number of little-endian 32-bit row-end offsets,
monotonic ends and a final end equal to the data length. Each selected row
must have exactly one enable-range membership and its exact nonempty span
above. Read no adjacent row. Within each selected span, structurally consume
two length-prefixed strings followed by three one-byte fields, exhausting the
row exactly. Interpret only the first string. Keep the second stored body and
the fixed tail opaque during structural reassembly.

Each selected first-string body starts with `0xFF`, ends with `0x73`, and
decodes by XOR `0x73` between those bytes. Its declared body length is 12, 5
or 9 bytes respectively. Independent readings agreed. Strict UTF-8 decoding,
absence of control bytes and re-encoding reproduced every selected frame.
Structural row reassembly reproduced each complete selected span while leaving
other-column values uninterpreted.

Synthetic checks accepted plain and scrambled selected strings and rejected
wrong row, logical field and locale selections, zero or overlong lengths,
invalid terminators in either string, truncated fixed tails, trailing row
bytes, selected control-token leads, invalid UTF-8 and embedded NUL.
These checks establish this bounded verifier's requirements. They do not
establish the native formatter's validation behavior. Only the selected
labels and identity metadata are retained; other column values, complete
rows and original XML are not published.
