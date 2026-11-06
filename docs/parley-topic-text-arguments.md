# Parley topic text arguments

The selected English `xtx/_text_ui` row 7103 consists entirely of one `0x28`
named-sheet token. It uses supplied integer argument 1 as a row selector in
`xtx/negotiationItem`, logical field 4, with no trailing argument expressions.
The original resource and the canonical CSV's lossless cell decode to the same
28 bytes. This establishes the reference structure, without resolving the
referenced row, field value or displayed topic.

## Selected original and canonical sources

The source is FINAL FANTASY XIV 1.23b, extraction `2012.09.19.0001`.
The static English selection is adopted from
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, Static English
definition and UISTR-01, revision `4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`.
Master resource `0x01030000`, reference ordinal 32, names `xtx/_text_ui` through
definition `0x0B450082`. Its unique explicit `lang="en"`, `mode="client"`
sheet is ordinal 1. Logical field 1 maps to its sole physical column, ordinal
0, declared `str`. This is the outer row's schema. The token's logical field
4 belongs to the separately named referenced table.

Block ordinal 0 begins at row 0 and declares 13020 slots. Row 7103 is enabled
and occupies exactly `[50959,50991)` in data resource `0x0B4502B5`, a 32-byte
complete scrambled `str` frame. Removing the length, marker and terminator
leaves 28 bytes, SHA-256
`a9c99597505358a90fef10dd2313b309c049b769a1dd52b302a80af007fac246`.

| Input resource | Bytes | SHA-256 |
| --- | ---: | --- |
| Data `0x0B4502B5` | 71588 | `f99e738cf8762e0831f9675f37ddfea7b6072d475b3d4b0c9edeadb67bb013e0` |
| Enable `0x0B4502B6` | 1552 | `3f7c0b8461cfd18a336fb9bb72dbcd5439e65106eea8ea85a6ab731894866183` |
| Row offsets `0x0B4502B7` | 52080 | `c027d8115b2d9f7a67b0d1f1ec2b6623bdf214defd83f255a00dc96922ff2804` |

The master/definition original and decoded digests are owned by the adopted
Static English definition. Both document transforms were authenticated and
independently decoded and exactly re-encoded before selecting this schema.

The canonical counterpart is `csv/xtx__text_ui.csv`, row 7103, physical line
1894, column label `1`, type `str`. It is zero-based CSV field index 2,
including the leading row-ID field. The selected cell is a lossless
`[@sheet:...]` spelling, rather than the raw decoded bytes. Decoding that
spelling reproduced the original 28 bytes, and re-export reproduced the cell
exactly. [tables.json](../manifests/tables.json) pins the complete CSV:
1284564 bytes, SHA-256
`23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece`.
The authenticated containing archive is pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json).

## Argument structure and conditional interpretation

Token offset 0 is measured within the decoded string. Its payload has exactly
three top-level expressions. The row operand is expression ordinal 1,
counting from zero. Its `0xE8` selector starts at payload offset 21 and has
literal index 1. The other two operands specify the literal sheet name
`xtx/negotiationItem` and logical field 4. No literal text run, nested token,
trailing argument expression or `0xEA`/`0xE9`/`0xEB` reference occurs
in this selected English row.

The native interpretation adopts these publications at Decomp revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`:

- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-04:
  `FUN_00CB2D50` reads `0xE8` from the supplied heterogeneous argument vector
  using a one-based index. Its typed accessor requires integer variant tag 0.
  Out-of-range access yields zero; a mismatched tag throws `std::bad_cast`
  on the studied path, without a demonstrated outer exception handler.
- `xivl-decomp:docs/resource/rich-text-sheet-and-case-handlers.md`, RT-03:
  handler `FUN_00CA0E20` decodes sheet, row and logical field in that order.
  Its row decoder is at VA `0x00CA0EB1`. Only expressions after the field
  populate the nested argument container. This row therefore supplies an
  empty container to the nested lookup.
- The same RT-03 and the plain-reference page's Concrete lookup and
  loaded-schema condition own actual table/row lookup, mapped field/type,
  formatting and failure conditions. Logical field 4 does not itself identify
  a physical column, type or value in the referenced table.

The original Lua request is owned by
`xivl-client-scripts:docs/parley-parameter-request.md`, Ordinary request order,
at revision `6d0a026a1e6d8bc2f8f41f187a7dbf18606c2ac8`. It supplies exactly one
format position R1 after key 7103, retaining the first of three opaque
get-data results. The conditional frame/provider projection is owned by
`xivl-client-scripts:docs/parley-topic-text-provider.md`. On its admitted
integer-argument path, this token uses R1 as the referenced row key. A Nil
native format cell terminates serialization, so the supplied vector can be
empty even though Lua forwarded one nil position. Forwarded false or a string
does not establish the required integer tag or a conversion into it.
For non-Nil R1, exactly one serialized outer argument additionally requires
the following native scan cell to be Nil in the actual prepared frame.

No `xtx/negotiationItem` row or field value is resolved here. The namespace and
control names supply no item, actor, display-name or gameplay-domain meaning
for R1. Actual R1, native binding/preparation/frame, part and preprocessing,
default-table preservation, loaded schema/locale, referenced row readiness,
mapped field type, formatter success, applied property and rendering remain
conditions. This single English row establishes no other locale, server rule
or historical outcome.

## Verification

Bounded verifiers authenticated the resources and canonical archive/member,
checked non-reparse input paths, monotonic little-endian row ends, declared
slot count, final data bound and unique selected enable membership. Only the
selected original row body and canonical English cell were interpreted.
Two string decodings agreed; rebuilding the original frame reproduced its
exact bytes. Independent expression parsing/re-encoding reproduced the token
and its selected reference structure, and the canonical text transform agreed
in both directions. No raw row, complete token bytes or AST is retained.

The adopted format contract is `xivl-tools:docs/formats/ssd-sheet.md`, Rows and
columns, The sheet string and its obfuscation, Rich-string control tokens and
Rich-string read and text-export contract, revision
`604210657f4858fb69744a3a92c90f3369040057`. Source checks used that revision's
`src/formats/src/sheet.rs`, `parse_sheet_string` and `encode_sheet_string`, and
`src/formats/src/richstring.rs`, `parse_token`, `parse_expression`,
`RichString::encode`, `from_lossless_text` and `to_lossless_text`.

Rejecting controls covered framing, terminators, payload bounds/closure and
expression exhaustion, changed enable/span/final bounds, wrong canonical token
name/bytes or extra suffix, and changed named-sheet, vector selector, index,
logical field or nested argument count. Strict structural rejection is the
verifier's contract; SQTP-05 retains the native formatter's weaker validation
boundary. No production build, native execution or rendered output is asserted.
