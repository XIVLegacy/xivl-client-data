# Guildleve 12468 client rows

`guildleve.csv` row `12468`, [Leaders of the Pack](guildleve-names.md),
stores item ID `12000101` in position 58 (`item4`). That ID joins directly to
the extracted item name `Evenfall Firefly`. The static rows do not bind the
item to a reveal command or establish a completed reveal interaction.

## Leve row

Positions are zero-based data fields after `row_ID`, following
[`tools/mappings/guildleve.py`](../tools/mappings/guildleve.py).
Names below are mapping labels, not independently recovered runtime roles.
All nonblank fields in row `12468` are listed:

| Positions | Mapping labels | Raw values |
| --- | --- | --- |
| 1, 2 | `classType`, `location` | `1`, `2` |
| 4, 5 | `factionCreditRequired`, `level` | `0`, `20` |
| 6, 7, 8 | `aetheryte`, `plateId`, `borderId` | `1280066`, `20028`, `20004` |
| 17, 18, 19, 20 | `objective`, `partyRecommended`, `targetLocation`, `authority` | `10041`, `0`, `0`, `40061` |
| 21, 23, 24 | `timeLimit`, `skill`, `favorCount` | `30`, `0`, `10` |
| 39, 40, 41, 42 | `aimNum1` through `aimNum4` | `4`, `0`, `0`, `0` |
| 55, 56, 57, 58 | `item1` through `item4` | `0`, `0`, `0`, `12000101` |
| 59, 60, 61, 62 | `mob1` through `mob4` | `3202603`, `3200105`, `0`, `3205803` |

Fields 0, 3, 9-16, 22, 25-38 and 43-54 are empty strings. Empty cells are
distinct from the stored zeroes above. The `aimNum` tuple alone does not
establish pair counts, actor counts, search areas, item supply or completion
rules. See [selected row values](guildleve-selected-row-values.md).

The objective value `10041` equals `xtx_guildleveText.csv` row ID `10041`.
Its English field 1 is `Uncover and eliminate the target enemies.`
The title remains the existing same-ID join in
[`derived/guildleve_names.csv`](../derived/guildleve_names.csv), row `12468`.

## Item identity

The [item mapping](../tools/mappings/items.py) joins `_item.csv`,
`xtx_itemName.csv` and `itemData.csv` by the same row ID. These selected cells
all belong to row `12000101`:

| Source | Positions | Raw values |
| --- | --- | --- |
| `xtx_itemName.csv` | 4, 5 | `\u521d\u86cd`, `Evenfall Firefly` |
| `_item.csv` | 0, 1, 2, 3 | `Normal/DummyItem`, `1`, `false`, `true` |
| `itemData.csv` | 36, 40, 41, 43 | `60739`, `1016`, `1`, `0` |
| `itemData.csv` | 47, 48, 61, 63 | `1`, `1001`, `0`, `-1` |

The Japanese source name is written as Unicode escapes. It equals the item
token in `xivl-captures:studies/elemen-battlecraft-leve-objectives/derived/battlecraft-leve-objectives.csv`,
row `12468`. That retained web-tables objective has the study's **wiki**
evidence tier and remains **CALIBRATION-grade**, as stated in
`xivl-captures:studies/elemen-battlecraft-leve-objectives/README.md`.
The static equality authenticates its named item ID, not its encounter details.

The mapping calls `_item` positions 1-3 `maxStack`, `isRare` and
`isExclusive`. It calls `itemData` positions 36, 40, 41 and 43 `icon`, `kind`,
`rarity` and `isUseable`, and positions 47, 48, 61 and 63 `level`,
`compatibility`, `recastTime` and `recastGroup`. These labels and the stored
`isUseable` value `0` do not establish whether a separate system-menu command
can consume or present this item. `maxStack` is not a drop or supply count.

## Target-name and actor-row correlations

Each nonzero `mob` value equals an `xtx_displayName.csv` row ID. English
display text is field 1. The
[actor-class mapping](../tools/mappings/actor_class.py) labels
`actorclass.csv` field 5 `displayNameId`. Selecting that field by these three
exact values returns one actor-class row per name in this extraction:

| Leve field | Display-name row ID | English field 1 | Actor-class row ID |
| --- | ---: | --- | ---: |
| 59 (`mob1`) | 3202603 | `firestarter imp` | 2202603 |
| 60 (`mob2`) | 3200105 | `ringtail pteroc` | 2200105 |
| 62 (`mob4`) | 3205803 | `evenfall firefly` | 2205803 |

Each selected actor-class ID has a same-ID `actorclass_graphic.csv` row,
following the [published row correlation](actor-appearance-crosswalk.md#raw-row-correlations).
The [appearance mapping](../tools/mappings/actor_appearance.py) names fields
6, 7, 32 and 33 `base`, `size`, `head` and `body`:

| Graphic row ID | Field 6 | Field 7 | Field 32 | Field 33 |
| ---: | ---: | ---: | ---: | ---: |
| 2202603 | 10038 | 3 | 0 | 1024 |
| 2200105 | 10002 | 2 | 0 | 1056 |
| 2205803 | 10515 | 3 | 0 | 1024 |

The seven packed fields 25-31 are all stored `0` on these rows. These are
static name/class/appearance correlations, not a historical spawn roster or
a transformation sequence. The raw `mob` values are display-name keys in
this join, not static-actor script IDs. The returned actor-class IDs also
have no record in the existing `staticactor_class_paths.json`; that catalog
negative does not exclude a server-bound actor. These raw values do not
establish runtime resource selection.

The published base-model split and directory-prefix contract in
`xivl-decomp:docs/actor/appearance-path-decoder.md` gives the following
conditional candidates **if** the corresponding field 6 value is actually
supplied as native record dword 0 (`B`):

| Supplied `B` | Conditional model directory |
| ---: | --- |
| 10038 | `/client/chara/mon/m038/` |
| 10002 | `/client/chara/mon/m002/` |
| 10515 | `/client/chara/mon/m515/` |

For these values, the decoder selects category 1 and number `B - 10000`.
The existing transformation finding cited below pins BID resources for
`m038`, `m002` and `m515`. Neither published contract establishes the
sheet-field-to-runtime-`B` alias or a historical disguise transition for
`12468`; the directory candidates are conditional arithmetic, not observed
resource requests.

## Content-command text and first unbound relation

The retained objective names system-menu token `\u898b\u7834\u308a`.
No cell in the authenticated `xtx_command.csv` equals that token or the
grammatical alternative `\u898b\u7834\u308b`. The shared stem
`\u898b\u7834` also has no cell substring match. The alternative was a
bounded label lookup, not an established translation or command identity.

The separate `xtx_command_content.csv` text domain has two exact noun-label
matches. Both cells below are exact source text, with Japanese escaped:

| Text row ID | Japanese field 0 | English field 1 |
| ---: | --- | --- |
| 10002 | `\u898b\u7834\u308a` | `Detect` |
| 40002 | `\u898b\u7834\u308a` | `Detect` |

These are the complete shared-stem matches in this member; the verb ending
has none. Thus the ordinary-command negative does not exclude a distinct
content-command label. The two text row IDs remain ambiguous keys.

The existing script finding
`xivl-client-scripts:docs/content-command-client-route.md` records the
retained `contentCommand`/`contentCommandSub` work and main-menu forwarding
for command `24302`, mapped to `/Command/System/ContentCommand` by
[`staticactor_class_paths.json`](../manifests/staticactor_class_paths.json).
It does not identify a producer's selected historical variation or server
operation. Label equality here does not establish that either text key was
the retained variation for leve `12468` or that this command was invoked.

The first unbound command relation is the producer selecting the content
variation for `12468`; actual invocation, item handling and server reply
remain separate. The actor rows do not bind a historical spawn, state
transition or BID resource producer. They also do not identify a Director,
supplies or settlement behavior. The broader presentation boundary remains
`xivl-decomp:docs/actor/guildleve-transformation.md`.

## Source identity and verification

The sources are extraction `2012.09.19.0001`, evidence class
`client_extraction`. Complete member bytes were authenticated against
[`manifests/tables.json`](../manifests/tables.json) inside the archive pinned
by [`manifests/private_csv_corpus.json`](../manifests/private_csv_corpus.json).
The archive is 70110686 bytes, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `guildleve.csv` | 80881 | `74ee8061449bf538d504443017c776f994c06fd1bcd2fd008bbee18284d93b2d` |
| `xtx_guildleveText.csv` | 129280 | `6c5901c244f6927c03ecbf9b7cc178da9dd56d0be39cda2cc46c9f543d9ac6dd` |
| `xtx_itemName.csv` | 4428170 | `917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2` |
| `_item.csv` | 350672 | `f41dba38473a8a4014826c5b0cd639e12c6652700c9f760660fcb241d7469dda` |
| `itemData.csv` | 1634758 | `f17193d832b375761cd01a37b25ff7d2c2947967ddc5ba4c2b16c0507d422912` |
| `xtx_command.csv` | 987740 | `2aa0b20822df0b2270918d9ac5525c86a34a941d7c66d17a106add1b2d6567d3` |
| `xtx_command_content.csv` | 1719 | `b5f0230a63f58b335860e30a8f660e541db0427600f5362a1d8d9b21b6816965` |
| `xtx_displayName.csv` | 838262 | `36c5dfba312695d9f4ee090dba123dfd7792feba55d88b0062c070d98abc0505` |
| `actorclass.csv` | 157327 | `3ac9f8d1812d49101f367e2a41356be96b5d64b1fc5ca29949195f50ebe1d984` |
| `actorclass_graphic.csv` | 892164 | `7da8241400530885e0a28ded04a03acf2771b0580a79c1f49f46ee0861010611` |

To reproduce, authenticate those complete members, parse the CSV headers,
and select the named row IDs and data-field positions above. Require the
`guildleve.58` value to equal all three item row IDs, preserve empty cells,
and test the two exact command labels and their shared stem in each named
text domain. Select actor-class field 5 by the three exact nonzero mob keys,
then correlate same-ID graphic rows. Preserve duplicate content-label rows
and stop before assigning a historical variation or resource pathname.
This verifies static row equality and bounded text matches without executing
a client.
