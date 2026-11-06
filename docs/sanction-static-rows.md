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
| `xtx_itemName.csv` | 135 | Row 3020506, English name column 6 (`str`) |
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
[status contract](status-names.md#columns-and-limits) owns those types and
limits. In particular, the literal `10800` in column 47 remains an unnamed
`float` sheet value. It is not an independently established applied duration.
Blank, zero and `-1` remain distinct raw values. No duration, flag, icon,
refresh, death, stacking or server-application semantics are assigned here.

## Scroll identity and retained shop offers

Row 3020506 joins exactly from `_item.csv` class path
`Normal/CmnGoodStatusItem` to `xtx_itemName.csv` English name
`scroll of Sanction`. This establishes a named catalog item and its declared
class, without executing that class or identifying a target status argument.

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
