# Parley ability-button text

The selected ability-button template declares `TextBlock_Ability`, matching
the final part name in four numbered text requests. Under the published
TextBlock.Text provider conditions, their English `xtx/_text_ui` labels are
`Reversal`, `Double Down`, `Shuffle` and `Wipe`, in button order 1-4.
The original string frames and canonical English CSV cells agree exactly.
This qualifies static label candidates without proving actual template or
part selection, applied text, ability availability or gameplay effects.

## Explicit form selectors and selected template

These are `client_extraction` findings for retail 1.23b, extraction
`2012.09.19.0001`. The exact
`client/sqwt/widget/NegotiationAbilityListWidget.form` identity and raw
control locators are owned by the
[ability-list form contract](parley-ability-text-labels.md#selected-raw-form-declarations).
Each of its five exact `Button_AbilityCommand_1` through
`Button_AbilityCommand_5` elements is a Sqwt Button and declares both:

| Attribute | Exact raw value |
| --- | --- |
| `Template` | `{StaticResource ControlTemplate_Button_AbilityCommand}` |
| `SqwtStyle` | `BTN_basis_listboxSelect` |

The form's only `ResourceDictionary/@Source` is
`widget/NegotiationAbilityListWidget.tpl`. Its root `SqwtStyleFile` is
`common/default.style`. The
[Ask style contract](sqwt-ask-structure.md#references-and-commands)
owns the matching `BTN_basis_listboxSelect` declaration within
`Widget/@Type="Button"` and that style input's identity. That published
declaration is adopted without inspecting another style body or dependency.
String equality establishes no successful style or resource resolution.

Two local form queries found no declaration header for the selected key:
one required exact namespace-qualified `x:Key`, and the other required an
exact attribute-value match. These results cover only headers in this form.
Separately, none of the five raw Button subtrees contains a descendant
named `TextBlock_Ability`, as recorded by the ability-list form contract.
Neither observation establishes absence from a template or runtime part tree.

The directly named resource is
`client/sqwt/widget/NegotiationAbilityListWidget.tpl`:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Template input | 6593 | `4696f1fe99dc74d741fe704fd1d288f929c2c5c3f78a97b2d2125dd5a5160aeb` |
| Decoded strict UTF-8 XML | 6585 | `93702a8223c94725852955c7804308a8781b0ac7034f94ac33616be7bebb31b7` |
| Selected template declaration | 1683 | `0809ab1589141aed5926a448f5366235d35d33c72288510f6c29e03f07227110` |

Its root is Sqwt `ResourceDictionary`. One direct `ControlTemplate` has
exact `x:Key="ControlTemplate_Button_AbilityCommand"`, matching the selected
form selectors, and raw `TargetType="Button"`. The declaration occupies
decoded lines 68-98 and byte span `[4077,5760)`, with an exclusive end.
Here Sqwt is namespace `http://namespace.square-enix.com/sqwt`, and `x`
is `http://namespace.square-enix.com/sqwt/x`.

Within that selected template, exactly one element has raw
`Name="TextBlock_Ability"`. Its expanded type is Sqwt `TextBlock`, at
decoded byte 4180, line 70. Its ancestor types from the resource root are
ResourceDictionary / ControlTemplate / Grid, all in the Sqwt namespace.
Those ancestors have no raw `Name`. The TextBlock has no raw `Text`
attribute. No computed default, binding or runtime property value follows
from that attribute absence.

This is a matching declaration in an explicitly referenced template. It
does not establish how the full colon-separated request name is resolved
or prove a selected native TextBlock instance. The caller has no fifth
button text request. The shared template declaration supplies no fifth
label or additional row source.

## Conditional Text request and provider

The caller is
`xivl-client-scripts:docs/parley-ability-list-initialization.md`, Ordered
initializer requests, revision
`e81ad360db72c58df104e6682e0eac642af2eb4e`. It requests these names in order:

| Full part-name operand | Key | English label |
| --- | ---: | --- |
| `Button_AbilityCommand_1:TextBlock_Ability` | 7110 | `Reversal` |
| `Button_AbilityCommand_2:TextBlock_Ability` | 7111 | `Double Down` |
| `Button_AbilityCommand_3:TextBlock_Ability` | 7112 | `Shuffle` |
| `Button_AbilityCommand_4:TextBlock_Ability` | 7113 | `Wipe` |

For each full name N and numeric key K, the caller supplies
`setText(W,N,K)` with an empty Lua format tail. The Text wrappers and numeric
projection are adopted from
`xivl-client-scripts:docs/parley-topic-text-provider.md`, Request and wrapper
projection, and `xivl-client-scripts:docs/common-ask-answer-list.md`, Numeric
named-context projection, revision
`1c427f636f2e68eac4ca3c3f47d84c9daf37f4ec`. With matching dynamic methods,
normal preceding completion and the reached `type(K)` result exactly
`"number"`, they project to `_setTextProperty(W,nil,N,"Text",K)`.
N remains the complete colon-separated string. The numeric wrapper captures
the native method and W after its type call. Wrapper results are discarded.

The adopted native contracts are:

- `xivl-client-structs:docs/widget-native-call-contract.md`, Property access,
  and `xivl-client-structs:docs/global-native-contract.md`, Native frame,
  revision `180ab8aaa49b0157fee8996abe4d27e05b588bda`.
- `xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`,
  SQTP-01..03, Default table and named language fields, Concrete lookup and
  loaded-schema condition, Plain and empty output, and Static English
  definition, revision `4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`.
- `xivl-decomp:docs/resource/sqwt-anime-property.md`, Route to the setter
  and Setter, at that Decomp revision.

Actual binding, marshalling and preparation must supply and preserve the
matching typed native frame, including admission of the leading Nil name
and a non-Nil numeric identifier. The serializer begins `@K` and scans
supported integer/string alternatives until the first Nil. An empty Lua
tail alone proves no native argument count. Plain `@7110` through `@7113`
require the first actual prepared format scan cell to be Nil.

The leading-Nil route must select the intended form and record, resolve N
to the intended TextBlock, pass its visibility and receiver/value gates,
and find the Text info and callback with permitted owner interception.
Property flags, TLS, selected interface/tables, preliminary-helper effects
including aliased-input changes, reference admission and normal helper
completion remain conditions. The static template does not prove these
lookups or their result.

On the admitted reference path the published constructor retains TextModule
and defaults to `xtx/_text_ui`, unless a pending table override replaces it.
Language input selects the outer logical field. These Lua calls supply no
language selector. The static English schema maps logical field 1 to
physical `str` column 0. Actual loaded schema, ready row, mapped native type
10, supported argument preservation, formatting/allocation/copy success,
property application and rendering remain required.

## Four selected English rows

The [topic-text source contract](parley-topic-text-arguments.md#selected-original-and-canonical-sources)
owns the master, definition, backing-resource and canonical CSV identities.
Master resource `0x01030000`, reference ordinal 32, names `xtx/_text_ui`
through definition `0x0B450082`. Its unique explicit `lang="en"`,
`mode="client"` sheet is ordinal 1. Both original document transforms were
authenticated, independently decoded and exactly re-encoded before selecting
this schema.

Each selected row is enabled in block ordinal 0, beginning at row 0 with
13020 slots, and occupies one complete scrambled `str` frame in data
`0x0B4502B5`, physical column 0. Enable and row-offset resources are
`0x0B4502B6` and `0x0B4502B7`. Span ends below are exclusive.

| Row | Original span | Frame bytes | Decoded bytes | Canonical physical line |
| ---: | --- | ---: | ---: | ---: |
| 7110 | `[51074,51086)` | 12 | 8 | 1901 |
| 7111 | `[51086,51101)` | 15 | 11 | 1902 |
| 7112 | `[51101,51112)` | 11 | 7 | 1903 |
| 7113 | `[51112,51120)` | 8 | 4 | 1904 |

| Row | Decoded SHA-256 |
| ---: | --- |
| 7110 | `7fee49df06f9b47cf153fcc083101d573ef1198fde89347731931190227ed669` |
| 7111 | `c02b010671a26ede20938f9427afdf2d810795d6ad0bf26bfdc12d13fb363f4a` |
| 7112 | `317cb3a7efadd989cf93430f492995c8a33f10a31ea74699f2c0152bb6c3b9fb` |
| 7113 | `3404644e01177ee996b69247aa3967e7a3f66702c5ff0f7270591e8d9622183b` |

Each complete body is printable ASCII without embedded NUL, `0x02` control
tokens or encoded argument references. Their canonical counterparts are
direct literal cells in `csv/xtx__text_ui.csv`, column label `1`, declared
`str`, zero-based CSV field index 2 including the leading row-ID field.
This CSV position is distinct from original physical column 0 and logical
field 1. Decoding and re-export reproduced each cell exactly. The adopted
Plain and empty output contract supplies the conditional plain-copy
interpretation. The labels establish no implemented effect, eligibility,
score, accepted move, server rule or historical Parley outcome.

## Reproduction and limits

Use the pinned decoder and basename-key SQEX transform in the
[Ask reproduction recipe](sqwt-ask-structure.md#reproduction-recipe), with
basenames `NegotiationAbilityListWidget.form` and
`NegotiationAbilityListWidget.tpl`. Require the complete eight-byte signature
`5351455800000000`, original and decoded identities, strict UTF-8/XML parsing
and exact re-encryption. Select only the exact form names, selector/reference
strings and template key above. Check the named label's expanded type,
ancestry, raw Text presence and lexical position within the selected span.
Independent XML-tree and streaming locators agreed.

Caller, wrapper, selected declaration and conditional provider qualification
preceded the four row decodes. Rejecting controls refused a missing label,
wrong name/type/namespace/count/ancestor/default, changed selector or key,
unqualified caller/part, changed provider/schema and an extra row. The four
original frames had monotonic little-endian row ends, the declared slot
count, final data bound, unique enable membership and exact selected spans.
Independent string decoding and parsing reproduced their frames and
canonical cells in both directions.

The adopted format source is `xivl-tools:docs/formats/ssd-sheet.md`, Rows and
columns, The sheet string and its obfuscation, Rich-string control tokens
and Rich-string read and text-export contract, revision
`604210657f4858fb69744a3a92c90f3369040057`. That revision's
`src/formats/src/sheet.rs`, `parse_sheet_string` and `encode_sheet_string`,
and `src/formats/src/richstring.rs` own the framing and rich-string contract.
Controls rejected changed spans, enable/final bounds, truncated or suffixed
frames, changed canonical text, wrong field/type/count and an encoded argument
in a claimed literal body. Strict structural rejection is the verifier's
contract, without a general native rejection claim.

Only the selected template label declaration and four English row bodies
were interpreted. Other template/style subtrees, transitive resources,
other rows/locales, native bodies and runtime cases remain outside this
finding. Raw XML, row bytes, ASTs and complete vectors are not retained.
Actual template and part selection, prepared frame, provider state,
schema/locale, storage/readback, property application and rendered output
remain unresolved, as do ability availability, scoring and historical behavior.
