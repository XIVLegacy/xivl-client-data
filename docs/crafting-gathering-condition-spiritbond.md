# Crafting and gathering condition and spiritbond

The retail 1.23b extraction does not establish a condition loss or spiritbond
gain per crafting or gathering action. Its instructional text establishes
qualitative eligibility restrictions. The inspected item consumers expose
state and display calculations without a per-action state producer.

## Retail text and consumers

The source is extraction `2012.09.19.0001`. Sheet column numbers below use
the numeric CSV header after the row ID.

`csv/materiaBook.csv` rows 23 and 24, column 1 (`str`), say that spiritbond
increases through battle, crafting or gathering while the item is equipped,
that an optimal rank above the owner's rank or zero condition inhibits its
development, and that trading or selling dissolves it. These are instructional
statements, not a numerical action schedule. [Materia](materia.md) owns the
derived book export.

`xivl-client-scripts:lua/scripts/item/normal/normalitembaseclass_common.lua`
contains these recovered consumers:

| Method and lines | Supported result |
|---|---|
| `getNormalItemLife`, 4-16 | Returns the smaller of `getItemLifeMax()` and synchronized `normalItemWork.life`. |
| `getNormalItemFitness`, 69-76 | Returns synchronized `normalItemWork.fitness` without incrementing it. The field name alone does not establish a spiritbond unit. |
| `getDegradeRate`, 733-805 | Reads equipment eligibility, level adjustment, compatibility and current condition, then returns a factor. It has no action argument or condition subtraction. |

The maximum-life getter reads `itemDataSheet` column 33 in
`xivl-client-scripts:lua/scripts/item/itembaseclass_common.lua:1319-1327`.
The item-detail consumer forwards fitness to a list property at
`xivl-client-scripts:lua/scripts/widget/desktopwidget_itemdetail.lua:1562-1571`.
Neither edge supplies an action-to-increment rule. Crafting progress and
synthesis-material durability are separate from equipped-gear condition;
`xivl-client-scripts:docs/craft-command-progress-contracts.md` records that
client UI boundary.

## Numerical boundary

| Requested case | Established eligibility | Condition amount | Spiritbond amount |
|---|---|---|---|
| Individual synthesis command | Book text names equipped crafting use, without identifying a command or completion trigger. | Not established. | Not established. |
| Completed synthesis, including failure | The text does not distinguish success, failure or completion. | Not established. | Not established. |
| Gathering attempt or obtained item | Book text names equipped gathering use, without separating attempts, successes, failures or yield. | Not established. | Not established. |

The inspected sources do not provide the authoritative increment producer,
slot eligibility, class/level or item-level scaling, quality effects, modifier
order, rounding unit, or hidden fractional accumulator. The parameter label
`Increased Spiritbond Gain` exists at `csv/xtx_text_paramName.csv` row 15058,
column 1 (`str`); a label does not supply its calculation. No universal delta
can be inferred from the book text or from a single before/after value.

An attributable historical observation would need one isolated action joined
to item records immediately before and after it, with the action ID and
outcome, equipped slots and item identities, class and level, item quality,
condition, spiritbond and active modifiers preserved. Repeated isolated
actions and a no-action control would distinguish action boundaries and
visible quantization. A raw spiritbond-field mapping and repeated transitions
are still required to distinguish rounding from fractional accumulation.
New retail acquisition is unavailable; this is a discriminator for retained
historical evidence, not a performed experiment.

## Source identity and search scope

The fixed CSV and Lua archives matched their size and SHA-256 declarations in
`manifests/private_csv_corpus.json` and
`xivl-client-scripts:manifests/private_lua_corpus.json`. Every CSV and canonical
Lua member matched the owning `manifests/tables.json` or
`xivl-client-scripts:manifests/scripts.json` pin. Selected member SHA-256 values:

| Member | SHA-256 |
|---|---|
| `csv/materiaBook.csv` | `f341265cc9e109e5c2b43f0acc8bd672510cca448d267b92cdafe956d7fc8e1e` |
| `csv/xtx_text_paramName.csv` | `aebca8a881055ecf060a03347300a3107294951b8d11f7b0c2eaf5ba4d60c0ba` |
| `item/normal/normalitembaseclass_common.lua` | `35a05383355d7205f58ad999710e5eaf92331c899c683873b823aead755645f0` |
| `item/itembaseclass_common.lua` | `7620492917230c3e060ed84d3197bf164c234a3ab73e48a0939bc65107f6b7fa` |
| `widget/desktopwidget_itemdetail.lua` | `b1e5066fef70d5b7002abcd0fcb5440348f3db46062a8d2f23704957d2cc6dad` |

The decoded corpus search covered spiritbond, condition, degradation,
durability, life, fitness and item-state getters, followed by the named item
and detail consumers. It found no supported per-action numerical join. This
is a boundary of the inspected extraction, not a claim that retail servers
lacked such rules.
