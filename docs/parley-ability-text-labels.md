# Parley ability-list text labels

The selected English `xtx/_text_ui` rows supply the short labels `Ability`
and `Close`, plus four help descriptions about tile order, values,
positions and a board reset. All six selected bodies are plain ASCII text,
without control tokens or encoded argument references. Original resource
frames and the canonical English CSV cells agree exactly.

The supplied ability-list form declares the title/help TextBlocks and close
Button needed for their conditional provider routes. None of its five raw
ability buttons contains a descendant named `TextBlock_Ability`. This
leaves the four numbered button-label requests and the omitted fifth label
unresolved at that declaration boundary. No numbered label row or fifth
label source is inferred from a control name or template default.

The [button-text finding](parley-ability-button-text.md) owns the selected
explicit template reference, named TextBlock candidate and four numbered
English labels. Actual template/part selection and the fifth label source
remain unproved.

## Caller and conditional provider

The caller is
`xivl-client-scripts:docs/parley-ability-list-initialization.md`, Ordered
initializer requests and Selected help request, revision
`e81ad360db72c58df104e6682e0eac642af2eb4e`. Its selected requests are:

| Request | Numeric key | Matching raw declaration |
| --- | ---: | --- |
| `setText(W,"TextBlock_AbilityTitle",7108)` | 7108 | TextBlock. |
| `setContent(W,"Button_CloseWindow",7109)` | 7109 | Button. |
| `setText(W,"TextBlock_AbilityHelp",key)` for helper indices 1-4 | 7114-7117 respectively | TextBlock. |

These requests supply no Lua formatting operand after the numeric key.
The caller owns their actual ordering, first-truthy help selection, missing
values and binding/delivery conditions. Neither the row labels nor their
help wording authenticates supplied ability flags or selects an ability.

The Text wrappers and numeric projection are adopted from
`xivl-client-scripts:docs/parley-topic-text-provider.md`, Request and wrapper
projection, and `xivl-client-scripts:docs/common-ask-answer-list.md`, Numeric
named-context projection, revision
`1c427f636f2e68eac4ca3c3f47d84c9daf37f4ec`. The Content adapter is owned
by `xivl-client-scripts:docs/parley-content-property-request.md`. Under
matching methods, normal prerequisite completion and the reached type
result exactly `"number"`, these project to
`_setTextProperty(W,nil,partName,"Text",key)` or
`_setTextProperty(W,nil,"Button_CloseWindow","Content",7109)`.
The numeric wrapper captures the native method and W after its type call.

The adopted native sources are:

- `xivl-client-structs:docs/widget-native-call-contract.md`, Property access,
  and `xivl-client-structs:docs/global-native-contract.md`, Native frame,
  revision `180ab8aaa49b0157fee8996abe4d27e05b588bda`.
- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`,
  SQTP-01..03, SQTP-07, Default table and named language fields, Concrete
  lookup and loaded-schema condition, and Static English definition,
  revision `4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`.
- `xivl-decomp:docs/resource/sqwt-anime-property.md`, Route to the setter
  and Setter, at that Decomp revision.

Actual binding, marshalling and preparation must produce and preserve the
matching typed native frame. On the admitted non-Nil identifier path, the
serializer begins `@key` and scans integer/string alternatives until its
first Nil. The empty Lua tail alone proves no native argument count. A
plain `@key` projection requires the first actual prepared format scan cell
to be Nil. Supported argument types/values, preparation and aliased-input
preservation retain their published conditions.

The leading-Nil route must obtain the intended form record and part, pass
its visibility gate and find the selected TextBlock.Text info, or the
SQTP-07 Button.Content/ContentControl info and callback. The Button/Label
Content connection is the published registration/lookup inference, not
proof of an actual runtime receiver. Permitted owner interception, property
flags, TLS, interface/table selection, preliminary-helper effects and
preprocessing admission remain required.

On that reference path the published constructor retains TextModule and
defaults to `xtx/_text_ui`, unless a pending table override replaces it.
Language input chooses the outer logical field. These Lua calls supply no
language selector. The static English schema maps logical field 1 to
physical string column 0. Actual loaded schema, ready row, mapped type 10,
formatting/copy/allocation success and property application remain
conditions. A raw declaration does not establish native part selection.

## Selected raw form declarations

The source is retail 1.23b `client/sqwt/widget/NegotiationAbilityListWidget.form`.
The supplied `game.ver` marker was `2012.09.19.0001`. The form is 3845 bytes,
SHA-256 `624c8a8a183d6f29964bc44163127821ba527477a8aa57eca9c1e5b98d97ce38`.
Decoded strict UTF-8 XML is 3837 bytes, SHA-256
`5ef282db5f27f1afb91ed4127a4a30373c86062cccc55a26b75c939cd323eba0`.
The full SQEX signature, basename-key Blowfish transform, strict XML parsing
and exact re-encryption were checked using the pinned decoder in the
[Ask reproduction recipe](sqwt-ask-structure.md#reproduction-recipe).
Inputs and decoded XML are not distributed here.

All selected elements below occur once by exact raw Name. Their expanded
types use namespace `http://namespace.square-enix.com/sqwt`.

| Raw Name | Local type | Decoded line | Decoded start byte |
| --- | --- | ---: | ---: |
| `TextBlock_AbilityTitle` | TextBlock | 26 | 1484 |
| `TextBlock_AbilityHelp` | TextBlock | 31 | 1940 |
| `Button_AbilityCommand_1` | Button | 37 | 2416 |
| `Button_AbilityCommand_2` | Button | 38 | 2615 |
| `Button_AbilityCommand_3` | Button | 39 | 2814 |
| `Button_AbilityCommand_4` | Button | 40 | 3013 |
| `Button_AbilityCommand_5` | Button | 41 | 3212 |
| `Button_CloseWindow` | Button | 46 | 3577 |

The named Window ancestor is `Window_NegotiationAbilityListWidget`.
The title's ancestor types are Window / Grid / Grid, with final Grid
named `Grid_Title`. The close Button has the same ancestor types, with
final Grid named `Grid_CloseWindow`. The help TextBlock's ancestor types
are Window / Grid / Label / Grid. Each numbered Button has ancestors
Window / Grid / Label / Grid / StackPanel. All those types use the same
Sqwt namespace; the remaining ancestors have no raw Name.

Within each selected numbered Button's raw subtree, no descendant has
exact Name `TextBlock_Ability`. This is a scoped absence in this form,
without a template, style, resource or runtime-part conclusion. The
initializer requests `Button_AbilityCommand_1:TextBlock_Ability` through
`Button_AbilityCommand_4:TextBlock_Ability` with keys 7110-7113. Their final
named part cannot be qualified from these admitted declarations. Those
row bodies remain uninterpreted here.

The caller supplies no fifth button text request. The fifth Button likewise
has no matching raw `TextBlock_Ability` descendant, so there is no admitted
matching label node on which to inspect a raw Text attribute. This supplies
no fifth label, direct fifth row reference or proof that a runtime label is
absent. Only selected Name/type/namespace and ancestor Names were
interpreted. Other attributes, styles and templates were not inspected.

## Selected English labels and help wording

These are `client_extraction` findings for extraction `2012.09.19.0001`.
The [topic-text source contract](parley-topic-text-arguments.md#selected-original-and-canonical-sources)
owns the adopted master/definition identity. Master resource `0x01030000`,
reference ordinal 32, names `xtx/_text_ui` through definition `0x0B450082`.
Its unique explicit `lang="en"`, `mode="client"` sheet is ordinal 1.
Both document transforms were independently decoded and exactly re-encoded
before selecting this schema.

The six selected rows are enabled in block ordinal 0, beginning at row 0
with 13020 slots. Each is one complete scrambled `str` frame in physical
column 0. Original data spans have exclusive ends.

| Row | Original span | Frame bytes | Decoded bytes | Canonical physical line | Selected wording |
| ---: | --- | ---: | ---: | ---: | --- |
| 7108 | `[51054,51065)` | 11 | 7 | 1899 | Literal short label `Ability`. |
| 7109 | `[51065,51074)` | 9 | 5 | 1900 | Literal short label `Close`. |
| 7114 | `[51120,51166)` | 46 | 42 | 1905 | Help describes reversing tile advancement order. |
| 7115 | `[51166,51197)` | 31 | 27 | 1906 | Help describes tile values becoming twice as large. |
| 7116 | `[51197,51234)` | 37 | 33 | 1907 | Help describes randomizing tile positions. |
| 7117 | `[51234,51270)` | 36 | 32 | 1908 | Help describes a board reset using fresh tiles. |

Help descriptions above are paraphrases of text. They establish no
implemented ability effect, accepted input, probability, legal move,
server rule, score change or historical Parley behavior. In particular,
the four help indices are not authenticated ability identities or the
unresolved numbered button labels.

Each selected body is plain ASCII text with no embedded NUL, `0x02`
control token or argument-reference expression. No supplied format
argument is encoded by these rows. This absence is local to the six bodies
and does not prove an empty actual native argument vector. The adopted
Decomp Plain and empty output section supplies the conditional native
plain-copy interpretation, subject to its normal allocation/copy conditions.

| Input resource | Bytes | SHA-256 |
| --- | ---: | --- |
| Data `0x0B4502B5` | 71588 | `f99e738cf8762e0831f9675f37ddfea7b6072d475b3d4b0c9edeadb67bb013e0` |
| Enable `0x0B4502B6` | 1552 | `3f7c0b8461cfd18a336fb9bb72dbcd5439e65106eea8ea85a6ab731894866183` |
| Row offsets `0x0B4502B7` | 52080 | `c027d8115b2d9f7a67b0d1f1ec2b6623bdf214defd83f255a00dc96922ff2804` |

| Row | Decoded SHA-256 |
| ---: | --- |
| 7108 | `9c40ae32bd6bd868d855635f6d295120e965580a1182c2930a44c845569d1851` |
| 7109 | `7d9eb7acb13e24625c404401d8e88b2350e32162455885f18276cf802f7701ed` |
| 7114 | `0ce34dff5b2bf50375eaaedd93dc3cda1d8b168600be0e42cc78057800e6fdd2` |
| 7115 | `349147b0b9741d0e7668d175dac27317873e3931a01ebc81b96d3a69efda6e60` |
| 7116 | `664017a9cc8f6bb9558021b869440e46e430e28a8a7321cf1b1cf603f37b35b9` |
| 7117 | `6013723cf3e1fdd9e1b788fe589f891e793dbc63d94f2e81adaf7f0e6ed556a2` |

The exact canonical counterparts are `csv/xtx__text_ui.csv`, column label
`1`, declared `str`, zero-based CSV field index 2 including the leading
row-ID field. This CSV position is distinct from original physical column
0 and its logical field 1. Each selected cell is direct literal text.
Decoding and re-export reproduced the canonical cell exactly.
[tables.json](../manifests/tables.json) pins the whole CSV at 1284564 bytes,
SHA-256 `23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece`.
The authenticated archive is pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json).

## Verification and limits

Caller and per-request wrapper/declaration/provider qualification preceded
row decoding. Checks authenticated non-reparse paths, all selected inputs,
canonical archive/member and adopted publications. They checked the form's
strict transform and exact roundtrip, selected declarations and scoped
absences, English schema/field identity, slot count, monotonic little-endian
row ends, final data bound, unique enable membership and exact selected
spans. Independent string decodings and parsers reproduced all six complete
original frames and canonical cells in both directions.

The adopted format source is `xivl-tools:docs/formats/ssd-sheet.md`, Rows and
columns, The sheet string and its obfuscation, Rich-string control tokens
and Rich-string read and text-export contract, revision
`604210657f4858fb69744a3a92c90f3369040057`. Source checks used that revision's
`src/formats/src/sheet.rs`, `parse_sheet_string` and `encode_sheet_string`,
and `src/formats/src/richstring.rs`, `parse_token`, `parse_expression`,
`RichString::encode`, `from_lossless_text` and `to_lossless_text`.

Rejecting controls changed declaration name/type/namespace/count, root
context and each scoped descendant absence. Row controls changed spans,
enable/final bounds, frame extents, canonical text, schema field/type/count
and help action words, and introduced an encoded argument into a claimed
literal body. Existing framing/expression controls checked invalid lengths,
terminators and token closure. Strict structural rejection is the verifier's
contract, rather than a general native rejection claim.

Only the six qualified English bodies and counterparts were interpreted.
No numbered label row, fifth label, other locale, template/style, new native
body or runtime case was studied. Complete raw help bodies, XML, row bytes,
ASTs and token vectors are not retained. Actual selected form/part, input
flags, native frame, provider override, schema/locale, property application
and rendered output remain unresolved.
