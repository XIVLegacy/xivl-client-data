# Hamlet score title and total text

The selected English UI cells contain a parameterized title, a `kilo`
control and its multiplier-prefixed variant. The supplied score form declares
the six requested TextBlocks and one Label. These static facts qualify the
published score requests under explicit adapter, native-frame and provider
conditions. They establish no rendered score, Hamlet identity, time unit,
historical clear or reward.

## Selected sources and static text

The source is retail FFXIV 1.23b extraction `2012.09.19.0001`, evidence class
`client_extraction`. [tables.json](../manifests/tables.json),
`xtx__text_ui.csv`, pins the 1284564-byte member, SHA-256
`23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece`.
Its containing 70110686-byte `csv.zip`, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`,
is pinned by [private_csv_corpus.json](../manifests/private_csv_corpus.json).

Only English column label `1`, type `str`, was selected: zero-based field
index 2 including the row ID. The five exported data columns are `str`.
The [published schema mapping](parley-topic-text-arguments.md#selected-original-and-canonical-sources),
at revision `acab105024dd3e9e45169d3cae88db5c9cfd4e3e`, separately maps
original English logical field 1 to sole physical column 0. That adopted
mapping does not authenticate original resource bytes for these three rows.
CSV record numbers below count the two header records.

| Row | CSV record | Complete selected-cell structure |
| --- | ---: | --- |
| 225 | 27 | One `0x22` (`kilo`) control. Its two operands are `0xE8` with literal index 1, then a string containing only a comma. No outer literal run. |
| 3189 | 1120 | Literal space, lowercase `x`, space, followed by exactly the same control and operands as row 225. |
| 13012 | 2414 | One `0x2B` (`head`) control, literal ` (Lv. `, one `0x20` (`number`) control using `0xE8` with literal index 2, then `)`. The head operand is one rich string containing only the nested sheet control described below. |

The nested `0x28` (`sheet`) control has exactly three operands: literal
table name `xtx/raidDungeon`, `0xE8` with literal index 1, and literal logical
field 26. There are no trailing nested arguments. This identifies a reference
expression without selecting a referenced row, mapped field type or value.
The control names are export vocabulary. The adopted native sheet/head
contracts below separately qualify their interpretation. No native `kilo`
handler is established here: its comma operand does not establish grouping,
and the multiplier prefix performs no arithmetic.

Selected UTF-8 CSV-cell identities are 26 bytes / SHA-256
`b9a9b77ede0f394543398b469cde7f4f0da1e7ccfcf38a6ef299cb366d2ff92c`
for row 225, 29 bytes /
`acdf3417c673b0e91417a3655eec63999a69541a5b4893d342a478d8ad91a692`
for row 3189, and 97 bytes /
`5551ce70ef5bd117b2f073b564ea75a3502bf885b22cba24a29477540a0ecd09`
for row 13012. These are the lossless exported cells, not raw string frames.

The selected target candidate is `xtx_raidDungeon.csv`, row 9, CSV record 11,
column label `26`, `str`, zero-based field index 27 including the ID. The
2381-byte member has SHA-256
`24c7e9a071c5a16b8a38254588e350e7e7b043e2dfe4129ecd5363d2f05f6059`.
Its selected 24-byte ASCII cell, SHA-256
`4676d4b0b0e95dc38ea798a93c9387f689ae45770423027122db6e63f2135ee2`,
names the Battle for Hyrstmill with a lowercase initial article and contains
no controls. The same archive and table manifest authenticate this member.
Column label 26 alone proves no actual native logical-field mapping.

## Matching form declarations

`client/sqwt/widget/HamletDefenseScoreWidget.form` is 8982 bytes, SHA-256
`e363b46e172560ae10ff9af968bafc7b7eae317616dbc875932fa6276972832a`.
Its decoded document is 8974 bytes, SHA-256
`db0cf4f0cd46f53b2be3b129ffeb05317d0ea47224e8e9fdf7a42ae873734b26`.
The full SQEX signature `5351455800000000`, case-sensitive basename key,
little-endian Blowfish blocks, unchanged partial-block tail, strict UTF-8/XML
and byte-exact re-encryption were checked using
[xivl-tools:tools/blowfish.py, Blowfish](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/tools/blowfish.py#L60)
and [the SQEX container contract](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/docs/formats/sqex.md#what-the-container-is).
Their SHA-256 pins are respectively
`7c4208f5d3b7acf20bfb67ddcba706cbb10bf4d1c6c1677b4b11d8685774f90e`
and `72fb258459edbf256402255180812f8529ddf16aceaf6d2e46bd76acbd2fa3d0`.

Each selected Name occurs exactly once. All expanded element types use
namespace `http://namespace.square-enix.com/sqwt`. Their common root path is
Window / Grid / StackPanel, with root Name `Window_HamletDefenseScoreWidget`.
The table gives the remaining ancestor types before each destination.

| Destination Name | Actual type | Remaining ancestors |
| --- | --- | --- |
| `TextBlock_ContentsTitle` | TextBlock | Grid |
| `TextBlock_PointTotalValue` | TextBlock | StackPanel / Label `Label_PointTotal` / Grid |
| `TextBlock_CorrectionLevelValue` | TextBlock | StackPanel / Label `Label_CorrectionLevel` / Grid |
| `TextBlock_PointAfterCorrectionValue` | TextBlock | StackPanel / Label `Label_PointAfterCorrection` / Grid |
| `TextBlock_ClearTimeValue` | TextBlock | StackPanel / Label `Label_ClearTime` / Grid |
| `TextBlock_TotalPointsValue` | TextBlock | StackPanel / Label `Label_TotalPoints` / Grid |
| `Label_TotalPointsValue` | Label | StackPanel / Label `Label_TotalPoints` / Grid |

Other attributes, styles, templates and controls were not interpreted. Names,
types and containment do not prove actual form selection or native parts.

## Conditional request and provider composition

The accepted
[xivl-client-scripts:docs/hamlet-supply-ui-contract.md, Score widget requests and total-read order](https://github.com/XIVLegacy/xivl-client-scripts/blob/92ebcb3c67527d41ae6f982be11500f011c85057/docs/hamlet-supply-ui-contract.md#score-widget-requests-and-total-read-order)
owns the following ordered calls after its list update and totals read.
`v` is the supplied title value with only nil replaced by literal 9.
`t1..t5` are exactly the first five totals results, padded with nil.

| Method and destination | Key | Complete format tail |
| --- | ---: | --- |
| setText, `TextBlock_ContentsTitle` | 13012 | `v, t2` |
| setText, `TextBlock_PointTotalValue` | 225 | `t1` |
| setText, `TextBlock_CorrectionLevelValue` | 3189 | `t2` |
| setText, `TextBlock_PointAfterCorrectionValue` | 225 | `t3` |
| setText, `TextBlock_ClearTimeValue` | 225 | `t4` |
| setText, `TextBlock_TotalPointsValue` | 225 | `t5` |
| setContent, `Label_TotalPointsValue` | 225 | `t5` |

Adopt the complete `setText`/`setItemText` forwarding from
[the published text-wrapper projection](https://github.com/XIVLegacy/xivl-client-scripts/blob/26e98d3be5c2d105c8a6ef52c9b504cc9748ca15/docs/parley-topic-text-provider.md#request-and-wrapper-projection),
the [setContent adapter](https://github.com/XIVLegacy/xivl-client-scripts/blob/26e98d3be5c2d105c8a6ef52c9b504cc9748ca15/docs/parley-content-property-request.md#supplied-frame-and-call-order),
and the [numeric projection](https://github.com/XIVLegacy/xivl-client-scripts/blob/26e98d3be5c2d105c8a6ef52c9b504cc9748ca15/docs/common-ask-answer-list.md#numeric-named-context-projection).
With those dynamic bindings and normal completion, each call requests
`_setTextProperty(W,nil,destination,property,key,...)`, preserving its entire
tail and nil/false/zero positions. The property is `Text` for the six
TextBlocks and `Content` for the Label. The numeric projection requires the
reached `type(key)` result to be exactly `"number"` and captures the native
method after that call. It discards results and returns zero values.

The [published native property contract](https://github.com/XIVLegacy/xivl-client-structs/blob/180ab8aaa49b0157fee8996abe4d27e05b588bda/docs/widget-native-call-contract.md#property-access)
requires actual binding, marshalling and preparation to preserve a matching
typed native frame, including leading-Nil admission. A non-Nil identifier
serializes as `@key`; admitted integer/string cells append `/i` or `/s`.
The first actual Nil scan cell ends the tail. Exactly two native title
arguments require both prepared cells and a following Nil. Exactly one
total argument requires its prepared cell and a following Nil. Lua nil
positions can terminate the scan early; forwarded false proves no admitted
integer tag. Admitted integer zero remains zero. Supported strings retain
the restricted printable-ASCII/no-slash reference grammar.

The adopted [TextBlock provider composition](https://github.com/XIVLegacy/xivl-client-scripts/blob/26e98d3be5c2d105c8a6ef52c9b504cc9748ca15/docs/tutorial-text-reference-provider.md#selected-request-and-native-property-route)
and [Content route](https://github.com/XIVLegacy/xivl-client-scripts/blob/26e98d3be5c2d105c8a6ef52c9b504cc9748ca15/docs/parley-content-property-request.md#conditional-numeric-content-route)
remain conditional on form record/part lookup, visibility and owner gates,
selected property info/descriptor, property flags, TLS, interface/tables,
preliminary-helper effects including aliased input, reference admission and
normal helper completion. They use distinct TextBlock.Text and inherited
Label.Content storage. On the constructor-selected reference path,
TextModule defaults to `xtx/_text_ui` only when a pending override does not
replace it. English selection, loaded schema, ready row, mapped `str`/native
type 10, argument parsing/copying and formatter success remain required.

Under those premises, the title's trailing `0x20` may use actual formatter
position 2 only if preceding head/sheet processing completes. The adopted
[SQTP-04..06 contracts](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-plain-text-reference-lookup.md#sqtp-04-supplied-argument-selectors-and-output-handlers)
make `0xE8` one-based and require integer variant tag 0. Out-of-range access
yields zero; a mismatched tag throws `std::bad_cast` on the studied path.
With actual preserved integer cells `(v,t2)`, the title's number uses `t2`
and the published signed-decimal conversion. Structural indices alone do
not establish native positions, handler invocation or actual values.

Adopt [RT-03 and RT-04's 0x2B handler](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/rich-text-sheet-and-case-handlers.md#rt-03-handler-0x28-named-sheet-text),
16045 bytes, SHA-256
`38cf9f02808529a3486a75fadf973674d37a1d31dce852239122cd8730d08aea`.
RT-03 decodes sheet name, row and logical field in that order. Thus the
title's nested reference uses preserved integer `v` as the row key and
logical field 26. Its empty remainder constructs an empty child argument
container. The referenced cell does not inherit `(v,t2)`. Missing sheet,
missing row or an unmapped type fails the whole formatter row on this path.
Loaded mapping, string type, readiness and successful lookup/formatting
remain required. RT-04's `0x2B` skips leading tokens, then applies its
byte-level word-start case operation at the first character position. It
does not establish general Unicode capitalization or an all-word operation.

For a nil supplied title value, the caller's fallback is literal 9. If actual
native preparation preserves integer cells `(9,t2)` and termination, the
loaded referenced schema maps logical field 26 to the selected canonical
column-26 value, and the preceding lookup/case/formatting conditions hold,
the candidate title is `The Battle for Hyrstmill (Lv. D)`, where D is the
published signed-decimal representation of the actual integer `t2`.
The case operation changes the source's initial ASCII `t` to `T`. Supplied
false or zero does not select this fallback. This is a conditional string
construction, without an invoked Hamlet variant or rendered-title claim.
The unstudied native `kilo` handler still prevents a native total-formatting
conclusion.

The separately published
[Hamlet getter contract, opcode 0x01a8](https://github.com/XIVLegacy/xivl-client-structs/blob/180ab8aaa49b0157fee8996abe4d27e05b588bda/manifests/hamlet_wire_contract.json)
identifies `(sum, signed correction, sum*correction, additive,
sum*correction+additive)` only under its actual player/cache binding.
That read consumes the cache before these presentation calls. The caller
does not recompute the totals or replace title nil with the fourth total.
The `Lv.` wording, multiplier prefix and control names establish neither
score/time units nor Hamlet identity, score production, timing or payout.

## Verification and remaining boundary

Source/archive/member pins, exact headers/English positions, selected row
uniqueness, complete token framing/expressions and lossless re-export were
checked in memory. Independent authored fixtures reconstructed all selected
controls, literal runs and the complete target phrase. Rejecting controls
changed row/column, literal
order, reference table/field/index, nested-tail count, control kind, comma,
type/namespace/uniqueness/ancestry and adapter/native-tail premises.
The form passed exact decrypt/re-encrypt checks. No raw cell, XML, payload,
complete byte vector or AST was retained. Actual dynamic/native bindings,
part selection, provider/locale/readiness, formatter completion, applied
property and rendering remain unobserved. Other referenced rows/columns,
other languages, row 13019 and its list-text helper are outside this finding.
