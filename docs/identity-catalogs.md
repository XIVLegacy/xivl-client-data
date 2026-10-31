# Identity catalogs and domain boundaries

These catalogs identify retail 1.23b values and their source joins. A static
label does not establish historical availability, a populated player field or
a server eligibility rule. Placeholder text is preserved as source text and
does not supply a descriptive enum name. Keep the key domains below separate.

## Member sets

| Domain | Canonical members and joins | Confidence and unresolved boundary |
| --- | --- | --- |
| Soul crystals | `xivl-decomp:docs/script/equipment-soulstones.md#important-item-backing` gives all seven important items 2000201-2000207, their names, icons, base classes and jobs. | High static identity. No member from that seven-item UI filter is missing. Secondary-class unlock enforcement is a separate question. |
| Tribe, race and sex | [Tribe row domains](tribe-row-domains.md) gives all 16 tribe rows, the three source columns and independent race-name text pairs. | High static cells and labels. The sex-shaped column has 0 on male-labelled rows, 1 on female-labelled rows and 2 on Clanless. A separate player-race numeric carrier and creation availability remain unresolved. |
| Skill names and arrays | [Skill-name rows](skill-name-rows.md) gives every label at keys 1-52. `xivl-client-structs:docs/work-binder-native-contract.md` records 52-element level, cap and point arrays. | High labels and array declarations. No text row is blank. This does not prove sheet-ID-minus-one indexing, runtime-populated slots, individual caps or playable classes. Literal placeholder labels retain their limited meaning. |
| Achievements and titles | [Achievement name joins](achievement-name-joins.md) gives 208 title-linked achievement names, title keys and both English selector strings. `xivl-decomp:config/achievement_title_map.json` owns the native title predicates; `xivl-decomp:config/achievement_completion_ordinals.json` owns the complete achievement completion map. | High static joins. Achievement IDs, title IDs, direct completion ordinals and predicate-parent joins are separate fields. Award rules and historical availability are unresolved. |
| Calendar and moon values | `xivl-client-structs:docs/zone-in-native-contract.md#calendar` and `xivl-decomp:docs/actor/world-master.md` own calendar formulas. `xivl-decomp:docs/resource/sun-moon-orientation.md#moon-phase-index` owns rendering indices. | High selected formulas. The calendar moon return 1-8 and default rendering index 0-7 use distinct clocks/formulas. Named time-phase/weekday members and a cross-domain phase-name mapping remain unresolved. |
| Damage attributes and elements | [Command battle parameters](command-battle-params.md#4-decoded-enums) separates damage attribute column 108, element column 110 and their weights. The [command catalog](../derived/command_battle_params.csv) preserves raw values beside derived labels. | Getter positions and typed cells are established; label qualifications remain in the finding. These scalar enums do not establish an action-property bit dictionary. |
| Language and search Region | `xivl-client-structs:docs/search-recruitment-wire-contract.md#result-region-mask-composition` owns the primary Region byte, additional mask and four zero-based comparison indices. `xivl-client-structs:docs/progfunc-native-call-contract.md` owns the separate client-language native observations. | High scoped encoding facts. Session language, the client selector and search Region need an exact crosswalk before assigning shared language names. |
| Mob identities and immunity | `xivl-captures:studies/monster-actor-class-paths/derived/taxonomy.csv` owns selected actor/display/model joins. The [reported-taxonomy study](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/gamerescape-tables/README.md) owns the separate race/family crosscheck and family catalog. | High qualified artifact identity. Reported race/family/species labels do not establish a complete internal numeric taxonomy, pool identity or immunity bits. No retail immunity-bit catalog is admitted by these sources. |
| Commands and animation selectors | The [command catalog](../derived/command_battle_params.csv) and [static-actor class map](../manifests/staticactor_class_paths.json) supply command identities. `xivl-decomp:docs/actor/emote-animation-ids.md` and `xivl-decomp:config/emote_animation_catalog.json` separate ordinary emotes, packed selectors and composition evidence. | Static command names/classes, packed fields, resource composition and observed playback retain separate confidence. A command ID, emote ID, packed selector and motion-pack number are separate domains. |
| Guildleve display names | [Guildleve names](guildleve-names.md#placeholder-and-duplicate-names) and the [624-row catalog](../derived/guildleve_names.csv) preserve exact names and placeholder flags. | High static labels. Row 12402 is `dummy` in both English and Japanese. The full placeholder sets are listed in the finding. No nonplaceholder name or playable status is established for it. |
| Idle motion pack 1041 | `xivl-decomp:docs/actor/idle-bank-selection.md` owns the common idle-bank field, setter and path-selection evidence. | The selected 1041 motion-pack producer/model/resource join remains unresolved. A bank-field width or a coincidentally numbered record does not identify its pose. |

The title-linked catalog is a subset of the complete native achievement
domain: 746 achievement IDs, 741 proven completion ordinals and five unresolved
inverse mappings at IDs 1107, 1108, 1109, 1110 and 1221. Achievement 100 has
completion ordinal 0. A missing parent join does not remove a direct
completion bit. The native catalogs retain these distinctions.

## Time vocabulary

The [calendar callbacks](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/zone-in-native-contract.md#calendar)
return month 1..12, day 1..32, hour 0..23, minute 0..59 and moon 1..8 from a
caller-supplied unsigned second count. The
[rendering moon index](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/sun-moon-orientation.md#moon-phase-index)
instead uses the Eorzea clock and defaults to 0..7, changing every fourth day
at 12:00. Its nonnegative override is unmasked. These domains have no established
named phase crosswalk. Complete named TimePhase and weekday enums remain
unresolved. The
[day/night predicate](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/actor/world-master.md#hydaelyn-calendar---confirmed-formulas)
and [shipped 19:00-05:00 journal text](https://github.com/XIVLegacy/xivl-client-scripts/blob/main/docs/impish-impositions-client-contract.md#limsa-runner-and-exchange-presentation)
are narrower facts.

## Action flags and damage elements

The [decoded enums](command-battle-params.md#4-decoded-enums) own all supported
damage-element values and qualified damage-attribute names. Column 108 is the
attribute enum and column 110 is the element enum. Element -1 means no element
field, while 13 means Unaspected. Neither enum establishes an action-property
bitmask. A retail carrier and meanings for the proposed property bits remain
unresolved.

## Language and search Region

The [search Region composition](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/search-recruitment-wire-contract.md#result-region-mask-composition)
sets each local bit k for k=0..3 when primary Region equals k or the
additional Region mask contains that bit. The primary and additional bytes
remain distinct. The
[language getter](https://github.com/XIVLegacy/xivl-client-structs/blob/main/docs/progfunc-native-call-contract.md#operation-3-value)
returns a separate signed 32-bit field. Values 4 and 5 match the
[Chinese predicate](https://github.com/XIVLegacy/xivl-client-scripts/blob/main/docs/chocobo-mount-script-contracts.md#naming-widget),
without individual locale labels. A complete language enum and a crosswalk to
search Region or session-language codes remain unresolved.

## Mob taxonomy and immunity

The [selected actor taxonomy](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/monster-actor-class-paths/README.md#evidence-boundary)
keeps 52 population candidates, decoded-race labels, wiki families and retained
instance paths distinct. The
[wiki study](https://github.com/XIVLegacy/xivl-captures/blob/main/studies/gamerescape-tables/README.md#study-contents)
owns 82 client-race/family crosscheck records and 52 family records, with source
page revisions and wiki-tier qualifications. These are bounded associations,
not a complete internal runtime taxonomy. No retail immunity-bit carrier or
dictionary is established. Application-defined pool IDs belong to the application that authors them.
These client and reported-taxonomy products supply no retail pool-ID catalog;
reported profile values do not establish retail field semantics.

## Packed selectors and commands

The [selector catalog](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/actor/emote-animation-ids.md#packed-playback-selectors)
and [bank routing](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/actor/animation-bank-routing.md#packed-selector)
own the packed representation and category names. The selected values split
as follows. Category names are lib=4, emt=5, cft=16 and pic=20.
Catalog coverage is independent of resource validity and visual
meaning.

| Selector | Category name | Character bank | Effect bank | Supported identity |
|---|---|---:|---:|---|
|0x04000FFA|lib|0|4090|Catalog script literal; visual unknown|
|0x04000FFB|lib|0|4091|Catalog script literal; visual unknown|
|0x05FA1001|emt|4001|1|Published generic self-item/potion effect composition; no catalog row|
|0x05FA2066|emt|4002|102|Catalog standing c001 drink motion/item parent composition|
|0x05FA3065|emt|4003|101|Catalog standing c001 eat motion/bread parent composition|
|0x05FA4000|emt|4004|0|No curated selector row; visual unknown|
|0x10001000|cft|1|0|No curated selector row; visual unknown|
|0x10002000|cft|2|0|No curated selector row; visual unknown|
|0x10003000|cft|3|0|No curated selector row; visual unknown|
|0x10009002|cft|9|2|No curated selector row; visual unknown|
|0x14001000|pic|1|0|No curated selector row; visual unknown|
|0x14002000|pic|2|0|No curated selector row; visual unknown|
|0x14003000|pic|3|0|No curated selector row; visual unknown|

Four matches and nine absences describe coverage of the 243-entry catalog.
The [item composition finding](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/actor/animation-bank-routing.md#food-and-drink-bank-composition)
also documents 0x05FA1001. No universal medicine mapping or arbitrary
actor/posture playback follows from these resource compositions.

The [command catalog](../derived/command_battle_params.csv) owns exact display
strings, and the [static-class join](command-script-identity.md#evidence-for-the-join)
owns command-to-script identity. Selected rows retain these names:

| ID | English display | Static class path |
|---:|---|---|
|12004|Battle Regimen|/Command/Game/CombinationStartCommand|
|12005|Attribute Points|/Command/Game/BonusPointCommand|
|12007|Skill Change|/Command/Game/ChangeEquipSetCommand|
|12009|Equip|/Command/EquipCommand|
|12010|Set Abilities|/Command/EquipAbilityCommand|
|12011|Enemy Marks|/Command/Game/PartyTargetCommand|
|21001|Active Mode|/Command/Game/ActivateCommand|
|21002|Passive Mode|/Command/Game/ActivateCommand|
|21005|Rush|/Command/Game/CommandCancelCommand|
|21006|Interrupt|/Command/Game/CommandCancelCommand|
|21007|Use Item|/Command/ItemCommand|
|22001|Synthesize|/Command/Game/CraftCommand|
|22013|Repair|/Command/Game/CraftCommand|
|22015|`***`|/Command/Game/CraftCommand|
|22104|Attack|/Command/Game/AttackCommand|
|29497|Parley|/Command/Game/NegotiationCommand|

The 22015 display remains the shipped placeholder. Class identity does not
provide a more specific display name or bind a command to a packed selector.

## Idle motion-pack 1041

The [idle bank finding](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/actor/idle-bank-selection.md#writers)
establishes the u16 common-bank field and kind 0 resource path, but identifies
no caller of its setter. Motion-pack 1041 has no established retail producer,
actor/model, resource or pose join. The native field width supplies no such
identity. UI text category 1041 belongs to a separate namespace.

## Evidence use

Client extraction identities are pinned by [tables.json](../manifests/tables.json)
for build `2012.09.19.0001`. Native findings preserve their executable,
addresses and proof limits in their owning repositories. Packet and community
catalogs preserve their own manifests and evidence classes. A member inherits
the qualification of its actual source and join, rather than the confidence
of another catalog with a similar number or label.
