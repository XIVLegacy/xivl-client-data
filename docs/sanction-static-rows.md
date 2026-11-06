# Sanction static rows

The extraction `2012.09.19.0001` contains Sanction dialogue, a status name
and description, a scroll item, and a conditional equipment label. These
are separate static identities. Their matching vocabulary does not establish
an item-to-status call, a status-to-parameter conversion, or a runtime gear
calculation.

## Sources and positions

The evidence class is `client_extraction`.
[tables.json](../manifests/tables.json) pins each source member by size and
SHA-256. The [private corpus declaration](../manifests/private_csv_corpus.json)
pins the transport archive. Column numbers below are zero-based positions
after the CSV row ID, authenticated against both decoded header rows.

| Source member | Sheet width | Selected rows and fields |
|---|---:|---|
| `populaceCompanyBuffer.csv` | 5 | Rows 2, 5, 8-15, 17, 18 and 20, English column 1 (`str`) |
| `status.csv` | 59 | Row 223992, the typed positions already preserved by the status export |
| `xtx_status.csv` | 69 | Row 223992, English name column 3 and description column 21 (`str`) |
| `_item.csv` | 4 | Row 3020506, class path column 0 (`str`) |
| `xtx_itemName.csv` | 135 | Row 3020506, English name column 6 and description column 26 (`str`) |
| `equipment.csv` | 140 | Rows selected by column 71 = `16010`, columns 71-74 (`s16`) |
| `xtx_text_paramName.csv` | 10 | Row 16010, English label column 1 (`str`) |

The source row ID is the key. Neither row order nor a display name supplies
an alternative key. The status, rank and shop products cited below retain
their own [export](../manifests/retail_sheet_exports.json) and
[shop](../manifests/shop_catalogs.json) provenance.

## Authored CompanyBuffer text

The selected English cells describe the service as follows. These are
paraphrases of authored dialogue, rather than observations of its delivery
or effect.

| Row IDs | Authored content |
|---|---|
| 2, 15, 17 | Introductions identify an official responsible for bestowing sanction and describe a qualifying rank. Their rank tokens contain Chief Storm Sergeant, Chief Serpent Sergeant and Chief Flame Sergeant. |
| 5 | The option label is `Have sanction bestowed.` |
| 8 | A ritual address requests divine favor. |
| 9 | A completion message says the organization's sanction has been bestowed. |
| 10-11 | An equipment-development explanation describes enhancing spells cast on gear crafted to harbor enchantments. |
| 12 | The explanation describes manufacturing and restricts Sanction to the named rank or above. |
| 13 | The description supplies a minutes placeholder and says sanction improves the efficacy of certain gear. |
| 14 | The description directs the reader to item details in the inventory interface to identify that gear. |
| 18, 20 | Further introductory variants identify the sanction official. Their presence alone does not select a company or player-state branch. |

Row 13 preserves the decoded token `[@number:022003e80203]` before the
minutes wording. The token and authored unit do not establish the actual
value supplied to it, a selected locale, or an applied duration. The rank
names occur inside decoded `switch` tokens, not as a numeric company mapping.
The tokens remain source content. Their presence does not prove which branch
was evaluated in a particular interaction.

The retained [Grand Company rank product](../derived/gc_rank.csv) separately
contains row 27 with positional English variants 0, 1 and 2 named Chief Storm
Sergeant, Chief Serpent Sergeant and Chief Flame Sergeant. As the
[rank contract](gc-rank.md) explains, its company field remains `unresolved`.
Matching rank labels do not resolve company-to-variant selection, eligibility
for every exported rank, or a runtime promotion requirement.

A text request must still bind its provider, schema and locale before its
numeric row argument identifies one of these cells. The presence of row 5
in the sheet does not establish that a menu helper requested it. Likewise,
the authored completion message in row 9 does not prove a status mutation.

## Status identity

Both `status.csv` and `xtx_status.csv` contain row 223992. Its English name
is `Sanction`. The English description describes receiving gear-enhancing
benefits from the player's Grand Company sanction. The exact description
cell has UTF-8 SHA-256
`680ed9c22b76d529c769ba38dfcdeffb5ebc48a6c10af3bfc8913d4487bbcafc`.

The existing [status export](../derived/status_names.csv) preserves row
223992's typed values under their positional `status_col_N` names. The
[status contract](status-names.md#columns-and-limits) owns those raw types
and limits. Column 47 is the `float` value `10800`.

The conditional provider composition in
`xivl-client-scripts:docs/sanction-status-base-contract.md`, "Conditional
Sanction composition," identifies this as the base-life value queried by
`StatusBaseClass.getStatusLifeAtSheet` under the actual inherited/native
bindings, unchanged row/column keys, selected table/schema and loaded-cache
premises described there. The native identity and row/column interpretations
retain their `INFERRED` tiers. The source contract is 18307 bytes, SHA-256
`e59f43a4bce76c406823621b0dc692909d41899660d656dc8baad13857607843`.

That query assigns no time unit and proves no applied duration, expiry,
actual death removal, refresh, stacking or server-application policy. Blank,
zero and `-1` remain distinct raw values.

### Declared status class

The published [static-actor class map](../manifests/staticactor_class_paths.json)
declares `id: 223992` with `classPath: /Status/GrandCompanyStatus`.
At revision `6f4def61dcec1c4abe1dd8154be15eb86f742770`, that publication is
248434 bytes, SHA-256
`d612438827e5997422ab6f64a807e567ddf1b953c532e8a319d67b93c53c9db0`.
Its provenance identifies evidence class `client_extraction`, source
`client/script/rq9q1797qvs.san` and generator
`tools/extract_staticactor_san.py`. This adopts the published record, without
reinterpreting the raw SAN or establishing runtime class resolution.

The selected leaf module is
`xivl-client-scripts:lua/scripts/status/grandcompanystatus.lua`, lines 1-8,
at revision `b407618eab0655b6d769580c6d9fae550366a46a`.
`xivl-client-scripts:manifests/scripts.json` pins its canonical identity;
`xivl-client-scripts:manifests/retail_lua_coverage.json`, resource
`rq9qpr/3s9w67vxu9wlrq9qpr.le.lpb`, pins the original and decoded payload:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Canonical Lua | 172 | `93c83032988b5f20a564df53a90912a32533ae6d31bda637691446e890230bc7` |
| Original LPB | 202 | `fbcbe98a7bc1027dfe16bda26a3df96a2709bc99985f1f378735461e315b02dd` |
| Decoded payload | 189 | `e725b787a9b8c8673dc550315346206920e017d70e9e34820933171fccb040fd` |

The authenticated original root has eight instructions starting at decoded
byte offset 32, zero fixed parameters, vararg flag 2, zero upvalues and zero
child prototypes. Its direct requests match the canonical Lua:

| Global call | Literal arguments, in order | Arguments / retained results | Original root PC / byte offset | Canonical line |
| --- | --- | --- | --- | ---: |
| `require` | `/Status/StatusBaseClass` | 1 / 0 | 2 / 40 | 4 |
| `_defineClass` | `GrandCompanyStatus`, `StatusBaseClass` | 2 / 0 | 6 / 56 | 8 |

PCs and offsets are zero-based. These ordinary global calls have no implicit
receiver. The root reads `_defineClass` after `require` returns normally.
A `require` exception prevents that class request; an `_defineClass`
exception prevents normal completion. On normal completion, root PC 7 at
byte offset 60 returns zero values. Neither helper's result is assigned or
returned by this module.

The inspected root contains no function or method definitions or direct
field assignments. This does not establish an absence of inherited callbacks
or helper side effects. `require`, `StatusBaseClass`, `_defineClass` and the
registry or native bindings they may reach remain uninspected dependencies.
The declared path and class request establish neither a registered status
object nor status grant, duration or equipment-bonus policy.

### Conditional status-wire lookup

The published native status-key translation gives one wire operand whose
lookup key equals Sanction row `223992`: decimal `23992`, hex `0x5DB8`.
It is in the low branch, where the key is `200000 + wire`. The high branch
starts at key `250001`, so it supplies no second encoding for this row.
This is a published-contract and arithmetic composition, without an observed
Sanction status event.

The native source is `xivl-decomp:docs/actor/status-wire-translation.md`,
"Translation," "Producers" and "Sheet row space," revision
`4081fda7ba8b8493e9b59e875bf335aa29ddb8ce`, 14,181 bytes, SHA-256
`3ebe5ba0ab0df66f98ec186bca179b3d6d2ad447a17ef5dd1cc20d76b84b1d6f`.
Its selected single-slot `0x0177` and twenty-slot `0x0179` routes share that
translation. The publication owns the native routing, slot extents and
readiness conditions; a matching lookup key alone does not establish a
resolved registered status object or successful application to an actor.

The existing `xivl-captures:studies/status-wire-projection-census/` finding
reported 831 admitted `0x0179` events in its 54-capture corpus. Its three
observed nonzero status rows were `223129`, `223263` and `223999`; row
`223992` was absent. This limit applies to the study's admitted lanes and
that opcode. It does not assess `0x0177` or other delivery paths.

The census inputs to this comparison are pinned at Captures revision
`09e8ab90411499f2b5f9c6e67b10526e378b33fc`:

| Published artifact under the study | Bytes | SHA-256 |
| --- | ---: | --- |
| `derived/verdicts.md` | 1824 | `3d0ce530da75ca2f6e5038e14939fd6174e0f2fb5e7e1726f00b16faf6830d0a` |
| `derived/status-projections.csv` | 361 | `764ae1e35272b10a66117a37f766a656fe845cf7b91c4d696f8431574fee3e4e` |

A runtime witness still needs the actual owner actor and slot, selected
message route, registered status resolution and same-actor application.
Linking that observation to an NPC service or scroll, measuring expiry and
joining equipment changes remain separate requirements. The candidate wire
operand establishes none of those causal or state transitions.

## Scroll identity and retained shop offers

Row 3020506 joins exactly from `_item.csv` class path
`Normal/CmnGoodStatusItem` to `xtx_itemName.csv` English name
`scroll of Sanction`. This establishes a named catalog item and its declared
class, without executing that class or identifying a target status argument.

The English description at column 26, CSV record 464 including the headers,
presents reading the scroll as invoking Sanction. It supplies no numeric
duration. The UTF-8 cell has SHA-256
`e0018aea69127d4b9a7e5f0d7dfd688403ead5b526337e9424590bc8670622d5`.
This is authored use intent; it does not identify a numeric target-status
argument or establish actual use, item consumption or status application.

The existing [GC seal catalog](../derived/gc_seal_shop_catalog.csv) contains
three offers for item 3020506, at shop rows 100032, 200032 and 300032. Each
retains quality 1, quantity 1, seal cost 300, rank requirement 31 and event
flag requirement 0. Their company codes are 1, 2 and 3 respectively. The
[shop mapping](shop-catalogs.md#2-gc-seal-shop-mapping) owns the widget-field
interpretation. These are static scroll offers. They do not price the
CompanyBuffer dialogue service, prove a seal debit, or show that using the
scroll applied status 223992. The offer's raw rank value 31 is not joined to
a localized rank name here.

## Conditional equipment identity

Exactly 33 `equipment.csv` rows have column 71 = `16010`. Every selected
row has column 72 = `1`. All four selected columns 71-74 are declared `s16`.
The exact row-ID join to `xtx_text_paramName.csv` row 16010 yields
`Sanction: `, including its trailing space.

The [equipment crosswalk](item-equipment-columns.md#parameter-id-joins)
owns the interpretation boundary: columns 71-74 are four returned condition
scalars. Columns 71/73 have an ID-like shape and columns 72/74 a value-like
shape. A label join does not establish units, actor parameter indices or
whether a runtime consumer treated column 72 as a threshold. The label and
33-row selection reproduce the condition-16010 finding in
`xivl-captures:studies/gamerescape-tables/derived/client-column-map-notes.md`,
section `What Sanction is, and where the other side of it lives`.

For exact reproduction, sort the selected rows by numeric row ID. Encode
each row as the row ID followed by columns 71, 72, 73 and 74, separated by
TAB and terminated by LF, with UTF-8 encoding. The resulting selection has
SHA-256 `c5b1518d9451e8663f475dc111c417a9723154916065593a4be5391f7f36f3b7`.
This digest preserves duplicate projections without publishing a gear list.

## Reproduction and remaining edges

Authenticate the archive against its declaration, then authenticate each
selected member against `tables.json` before parsing it in memory. Require
contiguous zero-based column labels, matching label/type widths, the declared
selected types, unique selected row IDs and complete selected-row widths.
Check the English column independently of the numeric row keys. Compare the
status typed positions with the retained status export, and compare the
three scroll offers with the retained shop catalog. No hydration or corpus
regeneration is required for these checks.

A useful rejection check changes a source digest, shifts a header label,
selects column 2 in place of English column 1, removes row 15, changes an
equipment `s16` type, or tests column 72 instead of 71 for `16010`. Each must
fail its intended check. Keep raw blanks, literal zeroes and `-1` separate.
Do not deduplicate repeated labels or projections.

The first unresolved edges are the selected text-provider/schema/locale
binding, scroll execution and status application, and the runtime consumer
that tests the condition and applies a gear bonus. The numbers 16010,
223992 and 3020506 belong to different row domains. No numeric or causal
conversion between them is established. Authored rank and minutes text does
not establish server settlement, an applied duration, or measured gear
behavior.
