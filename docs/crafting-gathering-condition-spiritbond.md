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

## Selected retained item records

Seven selected retail `0x0148` records supply no supported paired gear
state. They are packet observations from `pcap-1.23b`, separate from the
static extraction above. All locations below are s2c main lane `0`, with
zero-based frame/subevent indices and item record `0`. Each selected item lies between adjacent `0x0146` and `0x0147`
subevents in the same frame.

| Capture | Item frame:subevent | Catalog | English item name | Native package / slot | Modifier-present byte |
| --- | --- | --- | --- | --- | --- |
| `gather_wood.pcapng` | `91:2` | `10009610` | Tinolqa Mistletoe | `0 / 198` | `1` |
| `gather_wood.pcapng` | `96:2` | `1000006` | Earth Shard | `99 / 5` | `0` |
| `harvest.pcapng` | `24:2` | `10005202` | Moko Grass | `0 / 182` | `1` |
| `harvest.pcapng` | `72:2` | `10005202` | Moko Grass | `0 / 172` | `1` |
| `local_leve_complete.pcapng` | `501:2` | `8032501` | Hempen Kurta | `0 / 197` | `1` |
| `local_leve_complete.pcapng` | `501:7` | `1000013` | Lightning Crystal | `99 / 6` | `0` |
| `local_leve_complete.pcapng` | `501:12` | `1000001` | Gil | `99 / 1` | `0` |

Hempen Kurta occurs once, without a selected before/after mate. The two
Moko Grass records have different slots and different first-eight-byte
values. No selected pair matches catalog, package, slot and that opaque
field, and none of these selected scopes
contains an equipment-link record. The first field is not a proved unique
instance ID: the two different currency catalogs in the last frame share
its value. Comparisons were capture-local. Neither that equality nor a
modifier-present flag establishes paired equipped gear.

The catalog joins use `_item.csv` column `0` and `xtx_itemName.csv` English
column `5`, authenticated by `manifests/tables.json`. The ordinary rows use
`Normal/StandardItem`, and the shard/crystal/gil rows use
`Money/MoneyStandard`; those class names do not prove equipped state.
This cohort supplies no supported before/after gear life or fitness
observation and no condition or spiritbond action delta.

The source is `xivl-captures:sources/pcap-1.23b/manifest.yaml`, with these
exact member identities:

| Capture | Bytes | SHA-256 |
| --- | --- | --- |
| `gather_wood.pcapng` | `157688` | `c308aa4c984eb3e1912383c06e5115c6924713978df43cdb8075335e1bac7d32` |
| `harvest.pcapng` | `60680` | `8522a844b6904207c3465ae1d1038599eddb8b9dc47800d5230c8a1c3ad0e440` |
| `local_leve_complete.pcapng` | `358296` | `4f0793f354140478725bf2c30642a3458a854460f47fb11a7af635c8881d95cd` |

Reconstruction used `xivl-captures:tools/extractors/extract_streams.py`,
functions `reconstruct_lanes`, `parse_outer_frames` and `maybe_inflate`.
`xivl-captures:tools/validate_framing.py:check` reported no compression-flag
mismatch for these three inputs. Its frame-clean stream result does not
establish completeness of every original TCP stream. The selected scopes
and record bounds reproduced completely.

Record decoding used Python `struct` little-endian reads. The record is
`112` bytes: catalog at `+12` is `u32`, slot at `+16` is `u16`, and
modifier-present at `+41` is `u8`. Package selection reads the byte at
`0x0146` application `+6`. These interpretations reuse
`xivl-client-structs:manifests/unmapped_payload_decoding.json`, batch `2`,
`s2c_0x0148.recordLayouts.InventoryItemRecord`, and
`xivl-client-structs:docs/bazaar-native-wire-contract.md`, "Incoming package
operations and publication". Catalog and slot also agreed with
`xivl-captures:tools/extractors/extract_equipment_property_correlation.py:_parse_item_rows`.
The original locator cohort is
`xivl-captures:studies/equipment-property-correlation/derived/matrix.csv`, events
`024,025,049,050,051,052,053`. No modifier-body or action-causality claim
follows from these records.

## Source identity and search scope

The fixed CSV and Lua archives matched their size and SHA-256 declarations in
`manifests/private_csv_corpus.json` and
`xivl-client-scripts:manifests/private_lua_corpus.json`. Every CSV and canonical
Lua member matched the owning `manifests/tables.json` or
`xivl-client-scripts:manifests/scripts.json` pin. Selected member SHA-256 values:

| Member | SHA-256 |
|---|---|
| `csv/_item.csv` | `f41dba38473a8a4014826c5b0cd639e12c6652700c9f760660fcb241d7469dda` |
| `csv/xtx_itemName.csv` | `917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2` |
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
