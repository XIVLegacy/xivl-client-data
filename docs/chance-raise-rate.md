# Chance Raise probability boundary

An exact retail identity for the name `Chance Raise`, its success probability
and its modifiers are not established. Company-issue Expectorant is a concrete
retail revival-item candidate, with a raw parameter value of `0.6`; the
inspected consumer does not identify that value as a success probability.

## Retail candidate and raw value

Extraction `2012.09.19.0001` joins the following rows. Sheet columns use the
numeric CSV header after the row ID.

| Source | Row and column | Type | Exact value or supported meaning |
|---|---|---|---|
| `csv/_item.csv` | 3020411, 0 | `str` | `Normal/RaiseItem` |
| `csv/xtx_itemName.csv` | 3020411, 5 | `str` | `Company-issue Expectorant` |
| `csv/xtx_itemName.csv` | 3020411, 26 | `str` | Revival description explicitly says recovery is not guaranteed. |
| `csv/itemData.csv` | 3020411, 50 | `float` | `0.6` |
| `csv/itemData.csv` | 3020411, 49 and 51 | untyped | Empty grow-selector and compatibility-adjustment cells. |

The same class is assigned to rows 3020412, Company-issue Tonic, and 3020413,
Over-aspected Cluster. Their column-50 values are both `1`. Tonic's English
description describes guaranteed recovery. This contrast is consistent with
a probability interpretation, but it does not establish the unit, consumer
or exact trial rule for `0.6`.

`xivl-client-scripts:lua/scripts/item/normal/raiseitem.lua:11-47` defines
relation and target-use predicates: dead targets are accepted, live targets
are rejected, and detailed use returns `(true, 0)`. It supplies no random
trial, success threshold or modifier computation.

`xivl-client-scripts:lua/scripts/item/itembaseclass_common.lua:1579-1630`
reads column 50 as parameter 1 and contains generic level and compatibility
adjustment paths. A generic getter does not prove which subsystem consumes
that parameter for revival. The separate
`command/game/magic/raisemagic.lua:11-35` supplies target and range-selection
predicates, not a probability formula or a `Chance Raise` identity.

## Missing probability contract

No value is established for the requested base success rate, quality effect,
caster/target level effect, attribute or status modifiers, stacking order,
clamping, random-number domain, comparison operator, or rounding. In
particular, `0.6` must not be published as an observed 60% success rate or a
universal Raise rule without the missing parameter-to-trial join.

The first missing input is an attributable retail display, command, item or
status record identifying what `Chance Raise` names. A static closure would
then require the consuming probability producer and its inputs. Historical
observations would instead need eligible attempts with exact item/command
identity, quality, caster and target state, modifiers and success/failure
outcomes, with rejected uses separated from completed trials. Repeated
controlled strata could estimate rates with uncertainty; no finite sample
alone proves the exact server probability or modifier formula. New retail
acquisition is unavailable, and no such experiment was performed.

## Source identity and search scope

The CSV and Lua archives and every member matched the declarations in
`manifests/private_csv_corpus.json`, `manifests/tables.json`,
`xivl-client-scripts:manifests/private_lua_corpus.json` and
`xivl-client-scripts:manifests/scripts.json`. Selected SHA-256 identities:

| Member | SHA-256 |
|---|---|
| `csv/_item.csv` | `f41dba38473a8a4014826c5b0cd639e12c6652700c9f760660fcb241d7469dda` |
| `csv/itemData.csv` | `f17193d832b375761cd01a37b25ff7d2c2947967ddc5ba4c2b16c0507d422912` |
| `csv/xtx_itemName.csv` | `917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2` |
| `item/normal/raiseitem.lua` | `1e339ae3182e3be1b9159c8fef3b4ceb7188d222c89db0a673c1e5a4fba10aa3` |
| `item/itembaseclass_common.lua` | `7620492917230c3e060ed84d3197bf164c234a3ab73e48a0939bc65107f6b7fa` |
| `command/game/magic/raisemagic.lua` | `b357907b3880309b826f0042b1922d54ad24ae0977ab619a24f5912689a97fe3` |

Case-insensitive `chance[ _-]*raise` searches found no match in the complete
authenticated CSV or canonical Lua corpus. Revival, Raise, item, command and
status text searches led to the candidate above. Absence of that spelling does
not exclude a composed display label, another localization or another retail
identity, and metadata names alone do not close the identity join.
