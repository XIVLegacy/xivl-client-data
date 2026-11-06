# Craft HQ display text and arguments

The selected English `xtx/_text_ui` row 3006 formats the crafting display
argument inside text containing `Chance of HQ` and a percent sign. It is a
conditional rich string. Its second supplied integer argument selects
between two alternatives; both format supplied integer argument 1.

The published crafting caller supplies its display value and literal zero.
If the actual native argument vector preserves those as two integers,
the zero selects the alternative with the `Chance of HQ` wording and no
named-sheet lookup. This is a conditional display contract. The wording
does not authenticate a probability, successful craft, quality formula,
item debit, reward or authoritative outcome.

## Published caller and conditional provider

The complete caller contract is
`xivl-client-scripts:docs/craft-progress-flow-contract.md`, Initialization
and refresh, revision `bc672622794150bfcaecda2c0b48bd36f17ceb89`.
That publication is 11375 bytes, SHA-256
`2349150922e18431e82db51c95cf0f7f06507c542398761cfc5b1bc4815b12f0`.
Its accepted update requests `setText(W,"TextBlock_HQRate",3006,D,0)`.
D is `param2`, with numeric zero substituted only for this display call
when `param2` is nil. False and numeric zero are preserved. Opening uses
the initializer's separate HQ display value; refresh supplies Judge
position 9. The caller owns its earlier bounds tests, method bindings,
normal continuation and distinction between display fallback and work state.

The full-tail Text wrappers and numeric projection are adopted from
`xivl-client-scripts:docs/parley-topic-text-provider.md`, Request and wrapper
projection, and `xivl-client-scripts:docs/common-ask-answer-list.md`, Numeric
named-context projection, revision
`1c427f636f2e68eac4ca3c3f47d84c9daf37f4ec`. With the selected dynamic methods,
normal prerequisite completion and reached `type(3006)` result exactly
`"number"`, they request
`_setTextProperty(W,nil,"TextBlock_HQRate","Text",3006,D,0)`.
The native method and W are captured after the type call. Both Lua format
positions remain supplied, including false or zero D. The wrappers discard
all results.

The adopted native and schema sources are:

- `xivl-client-structs:docs/widget-native-call-contract.md`, Property access,
  and `xivl-client-structs:docs/global-native-contract.md`, Native frame,
  revision `180ab8aaa49b0157fee8996abe4d27e05b588bda`.
- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`,
  SQTP-01..06, Default table and named language fields, Concrete lookup and
  loaded-schema condition, and Static English definition, revision
  `4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`.
- `xivl-decomp:docs/resource/sqwt-anime-property.md`, Route to the setter
  and Setter, at that Decomp revision.

Actual binding, marshalling and preparation must preserve the matching
typed native frame, including the leading Nil name and non-Nil identifier.
On the admitted path the serializer begins `@3006` and scans supported
integer/string alternatives until its first Nil. Two Lua positions alone
do not prove two serialized native values. The two-integer interpretation
below requires the first two actual prepared scan cells to contain integer
D and integer zero, with the third Nil. A first Nil yields no serialized
arguments; a Nil in the second cell terminates after the first. Forwarded
false does not establish an integer type or conversion.

Application also requires the intended form and record, successful part
lookup and visibility/receiver gates, selected TextBlock.Text info and
callback, and permitted owner interception. Property flags, TLS, selected
interface/tables, preliminary-helper effects including aliased-input
changes, reference admission and normal completion remain conditions.

On that reference path the published constructor retains TextModule and
defaults to `xtx/_text_ui`, unless a pending table override replaces it.
Language input selects the logical field. This Lua request supplies no
language selector. The static English definition maps logical field 1 to
physical `str` column 0. Actual loaded schema, ready row, mapped native type
10, argument copying, formatting, allocation and property application
remain required.

## Selected form declaration

These are `client_extraction` findings for retail 1.23b, extraction
`2012.09.19.0001`. The supplied `game.ver` marker agrees with that version.
The selected input is `client/sqwt/widget/CraftProgressWidget.form`:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Form input | 9565 | `ccd83bd31bf0885fa8b480bad84b454624f70598a1e5ad417c812ff56fb8fb42` |
| Decoded strict UTF-8 XML | 9557 | `9db3d980959e3caa259d41270734e59bf5b2cf50abf9d131dd570ef7ba905197` |

Exactly one element has raw `Name="TextBlock_HQRate"`. Its expanded type
is `{http://namespace.square-enix.com/sqwt}TextBlock`, starting at decoded
byte 9251, line 116. Its ancestor types from the root are
Window / Grid / Grid / Grid / Grid, all in the same Sqwt namespace.
Their raw Names in that order are `Window_CraftProgressWidget`,
`Grid_Current`, absent, `Grid_Right` and `Grid_Bottom`.
Only the selected Name/type/namespace and necessary ancestor context were
interpreted. This declaration qualifies a static TextBlock.Text candidate
without proving the selected form, native part or applied property.

The complete eight-byte SQEX signature `5351455800000000`, basename-key
Blowfish transform, strict UTF-8/XML parsing and exact re-encryption were
checked using the pinned decoder in the
[Ask reproduction recipe](sqwt-ask-structure.md#reproduction-recipe), with
basename `CraftProgressWidget.form`. Tree and streaming XML locators agreed.
The input and decoded XML are not distributed here.

## Selected English row structure

The [topic-text source contract](parley-topic-text-arguments.md#selected-original-and-canonical-sources)
owns the original master, definition, backing-resource and canonical CSV
identities. Master `0x01030000`, reference ordinal 32, names `xtx/_text_ui`
through definition `0x0B450082`. Its unique explicit `lang="en"`,
`mode="client"` sheet is ordinal 1. The master and definition were
authenticated, independently decoded and exactly re-encoded before
selecting that schema.

Row 3006 is enabled in block ordinal 0, beginning at row 0 with 13020 slots.
Its data is resource `0x0B4502B5`, with enable `0x0B4502B6` and offsets
`0x0B4502B7`. Physical column 0 occupies `[24652,24730)`, with an exclusive
end: one complete 78-byte scrambled `str` frame. Its 74 decoded bytes have
SHA-256 `aedf26015a2045ec26e4395a153fe2d2504ac8a0b587f9e266fdff761877aa25`.

The canonical counterpart is `csv/xtx__text_ui.csv`, row 3006, physical line
976, column label `1`, declared `str`, zero-based CSV field index 2 including
the leading row-ID field. This CSV position differs from original physical
column 0 and logical field 1. Its 154-byte lossless cell has SHA-256
`d9cc0bf9c36d4ad6cc380832e6d5e8e2dd3a178f0ee52839511ba817fd79a55d`.
Decoding that spelling reproduced the original bytes, and re-export
reproduced the cell exactly.

The complete row consists of one outer `0x08` token at decoded offset 0.
It has three top-level expressions: one condition and two `0xFF` string
alternatives. The condition is `0xE1`, supplied integer argument 2 on the
left and literal integer zero on the right. The alternatives contain:

| Outer expression ordinal | Selected structure |
| ---: | --- |
| 1 | A `0x28` named-sheet request to `xtx/command`, row selected by supplied integer argument 2, logical field 2, no trailing arguments. It also contains one `0x20` numeric request for supplied integer argument 1 and a literal percent sign. |
| 2 | Literal wording containing `Chance of HQ`, followed by one `0x20` numeric request for supplied integer argument 1 and a literal suffix containing the percent sign. No named-sheet token occurs in this alternative. |

Offsets inside each alternative's decoded string begin at zero. The first
alternative's sheet token begins at offset 10 and its numeric token at 32.
The second alternative's numeric token begins at offset 15. These are
relative string offsets, not offsets into the original resource or outer
row. No referenced `xtx/command` row or field value was decoded.

## Conditional formatter interpretation

These existing publications at Decomp revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce` supply the interpretation:

- `xivl-decomp:docs/resource/rich-text-sheet-and-case-handlers.md`, RT-02:
  `0xE1` compares the two admitted integer operands as signed values,
  first greater than second. An `0xE8` literal-index reference is a
  supported operand. RT-03 owns the conditional `0x28` named-sheet request.
- `xivl-decomp:docs/resource/rich-string-entry-counts.md`, selected `08`
  handler `FUN_00C9F000` and `FF` string-expression path: a nonzero condition
  formats the first alternative and skips the second; zero skips the first
  and formats the second. The selected `FF` path recursively formats its
  string and requires writable source and normal completion. The handler
  also requires its accumulated width to equal the declared payload length.
- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, SQTP-04/06:
  `0xE8` selects the one-based supplied integer variant; handler `0x20`
  passes its dword through the selected signed decimal conversion and
  appends the result. Type mismatch and out-of-range conditions remain
  those of SQTP-04, without an established outer exception handler.

With the matching two-integer vector `(D,0)`, signed `0 > 0` is false.
The outer handler therefore formats expression 2 and skips expression 1.
The selected path places the signed decimal interpretation of D within
the `Chance of HQ` text and percentage suffix. It performs no named-sheet
lookup from this row. This join requires the published constructor-selected
handlers, runtime table preservation, admitted typed arguments, complete
writable source, allocation/copy and formatter/helper completion.

The row also contains the alternative dynamic `xtx/command` reference.
Its row argument is not a static row identity. Its logical field does not
identify a physical column, type or value without the referenced loaded
schema. No value or gameplay meaning is inferred from the table name.
The Lua numeric zero only selects the second alternative when its actual
native type, position and value survive preparation and serialization.

## Verification and limits

The published caller, wrapper, declaration and conditional provider/schema
were qualified before row decoding. Checks authenticated non-reparse input
paths, original resources and canonical archive/member. They checked the
form transform, exact selected Name/type/namespace/count/ancestry, selected
enable membership, monotonic little-endian row ends, slot count, final data
bound and exact row span. Independent string and expression parsers
reproduced the original frame and lossless canonical cell in both directions.

The format contract is `xivl-tools:docs/formats/ssd-sheet.md`, Rows and
columns, The sheet string and its obfuscation, Rich-string control tokens
and Rich-string read and text-export contract, revision
`604210657f4858fb69744a3a92c90f3369040057`. That revision's
`src/formats/src/sheet.rs`, `parse_sheet_string` and `encode_sheet_string`,
and `src/formats/src/richstring.rs`, `parse_token`, `parse_expression`,
`RichString::encode`, `from_lossless_text` and `to_lossless_text` own the
structural parsing and export contract. Token annotation names alone were
not used as native semantics.

Rejecting controls changed the source signature/basename, declaration name,
type, namespace, count and ancestor context; caller, provider, selected row,
schema and asserted native count; enable/span/final bounds, framing and
canonical spelling; outer handler, comparison/arguments/literal, number
argument/count, selected label/percent and named-sheet name/field/tail.
Existing controls covered token length, closing byte and expression
exhaustion. Strict structural refusal is the verifier's contract, rather
than a general native malformed-input rejection claim.

Only this declaration and English row were interpreted. Other form
attributes/nodes, templates/styles, rows/locales, Lua/native bodies and
runtime cases remain outside this finding. Complete XML, row bodies,
ASTs, tokens and vectors are not retained. Actual selected part, prepared
frame, provider/schema/locale, formatting, applied storage/readback and
rendering remain unresolved. No craft formula, probability, success,
quality debit, result policy or historical outcome is established.
