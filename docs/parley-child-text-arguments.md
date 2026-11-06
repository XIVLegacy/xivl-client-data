# Parley child title and turn-label arguments

The selected English `xtx/_text_ui` row 7122 is the literal label `Turn`.
Row 7123 consists entirely of one `0x28` named-sheet token. It uses supplied
integer argument 1 as a row selector in `xtx/negotiationTable`, logical field
48, with no trailing argument expressions. Original resource decoding and
the canonical English CSV cells agree exactly. These are static reference
and label findings, without an actual B1 value, selected title or rendered
output.

## Conditional child requests and provider

`xivl-client-scripts:docs/parley-child-initialization-request.md`, Conditional
unprefixed initializer, revision
`8d159b9290c871b72ff61fab529a4ec5c17a59ca`, owns these ordered requests on
the child receiver C:

| Request | Lua formatting tail after the numeric key |
| --- | --- |
| `setText(C,"TextBlock_NegotiationTitle",7123,B1)` | Exactly one position B1, including nil, false or zero. |
| `setText(C,"TextBlock_TurnText",7122)` | Empty. |

Other initializer calls occur between these two requests. The literal
string `"1"` and conversion-result T retain their separate caller contracts;
neither supplies another selected literal numeric key here. Actual child
selection, initialization delivery and B1 remain conditions of that caller.

Adopt the wrapper and provider composition from
`xivl-client-scripts:docs/parley-topic-text-provider.md`, Request and wrapper
projection and Conditional native provider, revision
`1c427f636f2e68eac4ca3c3f47d84c9daf37f4ec`.
With the selected `setText`, `setItemText` and `setTextProperty` bindings,
normal prerequisite completion and the reached `type(key)` result exactly
`"number"`, each request projects to
`_setTextProperty(C,nil,controlName,"Text",key,...)`. The wrappers preserve
the complete format tail and discard their call results. They supply no
conversion or type validation for B1. The native method and C receiver are
captured after the `type` call.

The adopted Property access and Native frame contracts are
`xivl-client-structs:docs/widget-native-call-contract.md`, Property access,
and `xivl-client-structs:docs/global-native-contract.md`, Native frame,
revision `180ab8aaa49b0157fee8996abe4d27e05b588bda`. Their application
requires the actual native binding, marshalling and preparation to preserve
the matching typed frame and values. The declared reader has three string
names, an integer identifier and eight integer/string alternatives.

On that admitted path the serializer begins `@7123` or `@7122`. Its first
Nil format scan cell terminates serialization. An admitted integer appends
`/i` and its value, including `/i0` for integer zero. An admitted string
appends `/s` and its value. Exactly zero serialized arguments requires the
first actual prepared scan cell to be Nil. Exactly one requires a supported
non-Nil first cell and a Nil second scan cell. The empty turn-label Lua tail
and one-position title Lua tail alone prove neither native count. A Lua nil
B1 position can terminate the scan immediately, while false supplies no
established integer tag or conversion.

The adopted SQTP-01..04 contract is
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`. Its restricted descriptor subset
admits canonical signed 32-bit integer payloads and printable ASCII strings
excluding `/`. Other strings and conversions retain their own boundaries.
The leading-Nil Text route reaches TextBlock.Text only under successful part
lookup and its visibility gate, selected property info, permitted owner
interception and admitted preprocessing. Property flags, TLS, interface and
table selection, and preliminary-helper effects including aliased-input
changes remain conditions.

On that reference path the published constructor retains TextModule and
defaults to `xtx/_text_ui`, unless a pending table override replaces it.
Language input selects the outer logical field. These Lua requests supply
no language selector. The static English definition maps logical field 1
to physical `str` column 0. Actual loaded schema, ready row, mapped native
type 10 and successful argument copying/allocation/iteration remain required.

## Selected child declarations

The supplied `client/sqwt/widget/NegotiationMessageWidget.form` contains
exactly one element with each selected raw Name below. Both have expanded
type `{http://namespace.square-enix.com/sqwt}TextBlock`.

| Raw Name | Decoded line | Decoded start byte |
| --- | ---: | ---: |
| `TextBlock_NegotiationTitle` | 37 | 1907 |
| `TextBlock_TurnText` | 44 | 2391 |

Each has ancestor types Window / Grid / Grid in that namespace. The Window
is named `Window_NegotiationMessageWidget`; neither ancestor Grid has a Name.
Only Name/type/namespace and this ancestor context were interpreted.

The original form is 3383 bytes, SHA-256
`edce5467cb7b8008fbb0febec9418a22a719dc94fa2ae0b2ba38440e8a59ecd3`.
Decoded strict UTF-8 XML is 3375 bytes, SHA-256
`549a281a5d98299a228bbc80dc61a8e54be8d3c192a06a3a95e549f2e587153e`.
The full SQEX signature, ASCII basename-key Blowfish transform, strict XML
parsing and exact re-encryption were checked using the pinned decoder in
the [Ask reproduction recipe](sqwt-ask-structure.md#reproduction-recipe).
The [root declaration finding](parley-message-widget-declarations.md)
owns the form's existing selection boundary. Matching control declarations
do not identify an actual selected form or native part. Other attributes,
styles and templates are outside this finding.

## Original and canonical English rows

These are `client_extraction` findings for retail 1.23b, extraction
`2012.09.19.0001`. The [topic-text finding](parley-topic-text-arguments.md#selected-original-and-canonical-sources)
owns the adopted master/definition identity and schema. Master resource
`0x01030000`, reference ordinal 32, names `xtx/_text_ui` through definition
`0x0B450082`. The unique explicit `lang="en"`, `mode="client"` sheet is
ordinal 1. Both document transforms were independently decoded and exactly
re-encoded before selecting this schema.

The selected rows are enabled in block ordinal 0, beginning at row 0 with
13020 slots. Each occupies one complete scrambled `str` frame in physical
column 0. Offsets below are within the data resource, with exclusive ends.

| Row | Original span | Frame bytes | Decoded bytes | Canonical physical line |
| ---: | --- | ---: | ---: | ---: |
| 7122 | `[51319,51327)` | 8 | 4 | 1913 |
| 7123 | `[51327,51360)` | 33 | 29 | 1914 |

| Input resource | Bytes | SHA-256 |
| --- | ---: | --- |
| Data `0x0B4502B5` | 71588 | `f99e738cf8762e0831f9675f37ddfea7b6072d475b3d4b0c9edeadb67bb013e0` |
| Enable `0x0B4502B6` | 1552 | `3f7c0b8461cfd18a336fb9bb72dbcd5439e65106eea8ea85a6ab731894866183` |
| Row offsets `0x0B4502B7` | 52080 | `c027d8115b2d9f7a67b0d1f1ec2b6623bdf214defd83f255a00dc96922ff2804` |

| Row | Decoded SHA-256 |
| ---: | --- |
| 7122 | `b823d5f9d1ce690c00935e097200405bcf903b6bbd61e4866c3c1fda7fb3238c` |
| 7123 | `c478635f3afb154a6e93336d54550cc6b3cc417ca9bc81dd9abaa3ce46584e10` |

The canonical counterparts are in `csv/xtx__text_ui.csv`, column label
`1`, declared `str`, zero-based CSV field index 2 including the leading
row-ID field. This CSV position is distinct from original physical column
0 and the title token's referenced logical field 48.
[tables.json](../manifests/tables.json) pins the whole CSV at 1284564 bytes,
SHA-256 `23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece`.
The authenticated containing archive is pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json).

Row 7122's cell is directly `Turn`, with no token or encoded argument
reference. Row 7123's cell is a lossless `[@sheet:...]` spelling. Decoding
it reproduced the original 29 bytes, and re-export reproduced the exact
canonical cell.

## Title reference and remaining values

Row 7123 has one token at decoded offset 0 and exactly three top-level
expressions: literal sheet name `xtx/negotiationTable`, supplied integer
argument 1 as the row expression, and literal logical field 48. The row
expression is ordinal 1 counting from zero. Its `0xE8` selector starts at
payload offset 22. No literal text run, nested token, trailing argument
expression or `0xEA`/`0xE9`/`0xEB` reference occurs in this selected body.

SQTP-04's `FUN_00CB2D50` reads `0xE8` using a one-based index into the
supplied heterogeneous argument vector. Its typed accessor requires integer
variant tag 0. Out-of-range access yields zero. A mismatched tag throws
`std::bad_cast` on the published path, without a demonstrated outer handler.
Only under the native frame and argument-preservation premises above does
this request's admitted integer argument 1 carry B1's row-selector value.
The body does not encode an item value, turn count or direct title string.

The same Decomp revision's
`xivl-decomp:docs/resource/rich-text-sheet-and-case-handlers.md`, RT-03,
owns handler `FUN_00CA0E20`. It decodes sheet, row and logical field in that
order. Only expressions after the field populate its nested argument
container. This selected token supplies an empty nested container; the
referenced cell does not inherit the outer B1 argument vector. Actual named
table/row readiness, logical-to-physical mapping, field type and formatting
remain conditions of that lookup.

The [Parley title-row finding](parley-title-rows.md) owns static English
titles in canonical `xtx_negotiationTable.csv` column 48 and their name
matches. The token's named namespace and field number agree with that
static title source. This does not establish its active schema mapping,
B1's value or domain, a selected referenced row, quest/actor identity or an
actual title. No referenced row was decoded here.

Outer locale selection and the token's explicit logical field 48 are
separate. Neither the static English body nor the initializer establishes
an active locale, rendered title/label, applied property, successful Parley
initialization, gameplay rule or historical invocation.

## Verification

The conditional provider was qualified from pinned publications and the
selected form declarations before decoding either row body. Bounded checks
authenticated non-reparse paths, original resources, master/definition
documents and canonical archive/member. They checked schema/field identity,
slot count, monotonic row ends, final data bound, unique enable membership
and exact selected spans. Two string decodings agreed. Complete framing,
strict text/token/expression parsing and independent reconstruction reproduced
both original frames and the canonical cells in both directions.

The adopted format contract is `xivl-tools:docs/formats/ssd-sheet.md`, Rows
and columns, The sheet string and its obfuscation, Rich-string control tokens
and Rich-string read and text-export contract, revision
`604210657f4858fb69744a3a92c90f3369040057`. Source checks used that revision's
`src/formats/src/sheet.rs`, `parse_sheet_string` and `encode_sheet_string`,
and `src/formats/src/richstring.rs`, `parse_token`, `parse_expression`,
`RichString::encode`, `from_lossless_text` and `to_lossless_text`.

Rejecting controls changed selected declaration name/type/namespace/count,
row span/enable/slot/final bounds, schema field/type/column count, complete
framing and canonical text. Structural controls changed the title handler,
sheet, reference vector/index/kind, literal row, field, nested/trailing
arguments and literal prefix/suffix. Existing framing/expression controls
also rejected invalid lengths, terminators, token closure and exhausted
operands. Strict structural rejection is the verifier's contract; SQTP-05
retains the native formatter's weaker validation boundary. No raw body,
complete token encoding or AST is retained. No build, new native body or
runtime execution was used.
