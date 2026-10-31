# Job artifact armor and relic item rows

These are authenticated extraction 2012.09.19.0001 item rows, not a retail obtainability census. Static presence, a quest offer and a historical award are separate facts. No listed row is established as never obtainable. Every historical award and complete stage progression remains unresolved. Selected same-key reward references and presentation calls are listed separately. Names and positions are source values; staged names do not prove upgrade ordering.

Raw equipment-point codes are equipment.csv column 69 (s32). They are not
joined directly to the same-numbered xtx_text_equipPtName.csv row. The consumer
getEquipmentEquipPointDetail maps those codes to ordinary fit-point lists;
isFitForEquipPoint checks membership in the first returned list. Names below
use PcProfileWidget's ordinary-slot dispatch, not a raw-code-to-text-row join.
They describe recovered fit points, not an observed equip operation or full
eligibility. Item names use xtx_itemName.csv column 5. Compatibility uses
itemData column 48 and compatibility column 8+(job skill-1), as in
item-compatibility-inspector.md. The 35 armor identities remain canonical in
docs/armoire-item-rows.md:44.

| Job | Item ID | Client name | Raw equipment.69; consumer fit points | Stage | Source locators | Quest/reward reference |
| --- | ---: | --- | --- | --- | --- | --- |
| Paladin | 4030601 | Unfinished Curtana | 36; {1,2} main or sub weapon | Unfinished | xtx_itemName.csv:696 col5; _item.csv:696 col0=Normal/StandardItem; itemData.csv:696 col48=2120; compatibility row2120 col23=100; equipment.csv:579 col69=36 | unresolved |
| Paladin | 4030602 | Curtana | 36; {1,2} main or sub weapon | named weapon/shield | xtx_itemName.csv:697 col5; _item.csv:697 col0=Normal/StandardItem; itemData.csv:697 col48=2120; compatibility row2120 col23=100; equipment.csv:580 col69=36 | unresolved |
| Paladin | 4100810 | Holy Shield | 2; {2} sub weapon | named weapon/shield | xtx_itemName.csv:976 col5; _item.csv:976 col0=Normal/ShieldItem; itemData.csv:976 col48=2120; compatibility row2120 col23=100; equipment.csv:859 col69=2 | unresolved |
| Paladin | 8013501 | Gallant Coronet | 9; {9} head | artifact armor | xtx_itemName.csv:2147 col5; _item.csv:2147 col0=Normal/StandardItem; itemData.csv:2147 col48=2120; compatibility row2120 col23=100; equipment.csv:2030 col69=9 | unresolved |
| Paladin | 8032701 | Gallant Surcoat | 11; {11} body | artifact armor | xtx_itemName.csv:2974 col5; _item.csv:2974 col0=Normal/StandardItem; itemData.csv:2974 col48=2120; compatibility row2120 col23=100; equipment.csv:2857 col69=11 | quest_new_reward.csv:403 row111286 col107 (Keeping the Oath) |
| Paladin | 8051401 | Gallant Cuisses | 13; {13} legs | artifact armor | xtx_itemName.csv:3593 col5; _item.csv:3593 col0=Normal/StandardItem; itemData.csv:3593 col48=2120; compatibility row2120 col23=100; equipment.csv:3476 col69=13 | unresolved |
| Paladin | 8071401 | Gallant Gauntlets | 14; {14} hands | artifact armor | xtx_itemName.csv:4100 col5; _item.csv:4100 col0=Normal/StandardItem; itemData.csv:4100 col48=2120; compatibility row2120 col23=100; equipment.csv:3983 col69=14 | unresolved |
| Paladin | 8081801 | Gallant Sollerets | 15; {15} feet | artifact armor | xtx_itemName.csv:4583 col5; _item.csv:4583 col0=Normal/StandardItem; itemData.csv:4583 col48=2120; compatibility row2120 col23=100; equipment.csv:4466 col69=15 | unresolved |
| Paladin | 11000353 | Timeworn Curtana | no equipment row; not an equipment slot | Timeworn | xtx_itemName.csv:7454 col5; _item.csv:7454 col0=Normal/DummyItem; itemData.csv:7454 col48=1001; compatibility row1001 col23=100 | unresolved |
| Monk | 4020401 | Unfinished Sphairai | 37; {1} main weapon | Unfinished | xtx_itemName.csv:626 col5; _item.csv:626 col0=Normal/StandardItem; itemData.csv:626 col48=2119; compatibility row2119 col22=100; equipment.csv:509 col69=37 | unresolved |
| Monk | 4020402 | Sphairai | 37; {1} main weapon | named weapon/shield | xtx_itemName.csv:627 col5; _item.csv:627 col0=Normal/StandardItem; itemData.csv:627 col48=2119; compatibility row2119 col22=100; equipment.csv:510 col69=37 | unresolved |
| Monk | 8013502 | Temple Circlet | 9; {9} head | artifact armor | xtx_itemName.csv:2148 col5; _item.csv:2148 col0=Normal/StandardItem; itemData.csv:2148 col48=2119; compatibility row2119 col22=100; equipment.csv:2031 col69=9 | unresolved |
| Monk | 8032702 | Temple Cyclas | 11; {11} body | artifact armor | xtx_itemName.csv:2975 col5; _item.csv:2975 col0=Normal/StandardItem; itemData.csv:2975 col48=2119; compatibility row2119 col22=100; equipment.csv:2858 col69=11 | quest_new_reward.csv:385 row111226 col107 (Return of the King...of Ruin) |
| Monk | 8051402 | Temple Gaskins | 13; {13} legs | artifact armor | xtx_itemName.csv:3594 col5; _item.csv:3594 col0=Normal/StandardItem; itemData.csv:3594 col48=2119; compatibility row2119 col22=100; equipment.csv:3477 col69=13 | unresolved |
| Monk | 8071402 | Temple Gloves | 14; {14} hands | artifact armor | xtx_itemName.csv:4101 col5; _item.csv:4101 col0=Normal/StandardItem; itemData.csv:4101 col48=2119; compatibility row2119 col22=100; equipment.csv:3984 col69=14 | unresolved |
| Monk | 8081802 | Temple Boots | 15; {15} feet | artifact armor | xtx_itemName.csv:4584 col5; _item.csv:4584 col0=Normal/StandardItem; itemData.csv:4584 col48=2119; compatibility row2119 col22=100; equipment.csv:4467 col69=15 | unresolved |
| Monk | 11000354 | Timeworn Sphairai | no equipment row; not an equipment slot | Timeworn | xtx_itemName.csv:7455 col5; _item.csv:7455 col0=Normal/DummyItem; itemData.csv:7455 col48=1001; compatibility row1001 col22=100 | unresolved |
| Warrior | 4040501 | Unfinished Bravura | 37; {1} main weapon | Unfinished | xtx_itemName.csv:762 col5; _item.csv:762 col0=Normal/StandardItem; itemData.csv:762 col48=2121; compatibility row2121 col24=100; equipment.csv:645 col69=37 | unresolved |
| Warrior | 4040502 | Bravura | 37; {1} main weapon | named weapon/shield | xtx_itemName.csv:763 col5; _item.csv:763 col0=Normal/StandardItem; itemData.csv:763 col48=2121; compatibility row2121 col24=100; equipment.csv:646 col69=37 | unresolved |
| Warrior | 8013503 | Fighter's Burgeonet | 9; {9} head | artifact armor | xtx_itemName.csv:2149 col5; _item.csv:2149 col0=Normal/StandardItem; itemData.csv:2149 col48=2121; compatibility row2121 col24=100; equipment.csv:2032 col69=9 | unresolved |
| Warrior | 8032703 | Fighter's Cuirass | 11; {11} body | artifact armor | xtx_itemName.csv:2976 col5; _item.csv:2976 col0=Normal/StandardItem; itemData.csv:2976 col48=2121; compatibility row2121 col24=100; equipment.csv:2859 col69=11 | quest_new_reward.csv:379 row111206 col107 (How to Quit You) |
| Warrior | 8051403 | Fighter's Breeches | 13; {13} legs | artifact armor | xtx_itemName.csv:3595 col5; _item.csv:3595 col0=Normal/StandardItem; itemData.csv:3595 col48=2121; compatibility row2121 col24=100; equipment.csv:3478 col69=13 | unresolved |
| Warrior | 8071403 | Fighter's Gauntlets | 14; {14} hands | artifact armor | xtx_itemName.csv:4102 col5; _item.csv:4102 col0=Normal/StandardItem; itemData.csv:4102 col48=2121; compatibility row2121 col24=100; equipment.csv:3985 col69=14 | unresolved |
| Warrior | 8081803 | Fighter's Jackboots | 15; {15} feet | artifact armor | xtx_itemName.csv:4585 col5; _item.csv:4585 col0=Normal/StandardItem; itemData.csv:4585 col48=2121; compatibility row2121 col24=100; equipment.csv:4468 col69=15 | unresolved |
| Warrior | 11000355 | Timeworn Bravura | no equipment row; not an equipment slot | Timeworn | xtx_itemName.csv:7456 col5; _item.csv:7456 col0=Normal/DummyItem; itemData.csv:7456 col48=1001; compatibility row1001 col24=100 | unresolved |
| Dragoon | 4080501 | Unfinished Gae Bolg | 37; {1} main weapon | Unfinished | xtx_itemName.csv:883 col5; _item.csv:883 col0=Normal/StandardItem; itemData.csv:883 col48=2123; compatibility row2123 col26=100; equipment.csv:766 col69=37 | unresolved |
| Dragoon | 4080502 | Gae Bolg | 37; {1} main weapon | named weapon/shield | xtx_itemName.csv:884 col5; _item.csv:884 col0=Normal/StandardItem; itemData.csv:884 col48=2123; compatibility row2123 col26=100; equipment.csv:767 col69=37 | unresolved |
| Dragoon | 8013504 | Drachen Armet | 9; {9} head | artifact armor | xtx_itemName.csv:2150 col5; _item.csv:2150 col0=Normal/StandardItem; itemData.csv:2150 col48=2123; compatibility row2123 col26=100; equipment.csv:2033 col69=9 | unresolved |
| Dragoon | 8032704 | Drachen Mail | 11; {11} body | artifact armor | xtx_itemName.csv:2977 col5; _item.csv:2977 col0=Normal/StandardItem; itemData.csv:2977 col48=2123; compatibility row2123 col26=100; equipment.csv:2860 col69=11 | quest_new_reward.csv:415 row111326 col107 (Into the Dragon's Maw) |
| Dragoon | 8051404 | Drachen Breeches | 13; {13} legs | artifact armor | xtx_itemName.csv:3596 col5; _item.csv:3596 col0=Normal/StandardItem; itemData.csv:3596 col48=2123; compatibility row2123 col26=100; equipment.csv:3479 col69=13 | unresolved |
| Dragoon | 8071404 | Drachen Gauntlets | 14; {14} hands | artifact armor | xtx_itemName.csv:4103 col5; _item.csv:4103 col0=Normal/StandardItem; itemData.csv:4103 col48=2123; compatibility row2123 col26=100; equipment.csv:3986 col69=14 | unresolved |
| Dragoon | 8081804 | Drachen Greaves | 15; {15} feet | artifact armor | xtx_itemName.csv:4586 col5; _item.csv:4586 col0=Normal/StandardItem; itemData.csv:4586 col48=2123; compatibility row2123 col26=100; equipment.csv:4469 col69=15 | unresolved |
| Dragoon | 11000356 | Timeworn Gae Bolg | no equipment row; not an equipment slot | Timeworn | xtx_itemName.csv:7457 col5; _item.csv:7457 col0=Normal/DummyItem; itemData.csv:7457 col48=1001; compatibility row1001 col26=100 | unresolved |
| Bard | 4070401 | Unfinished Artemis Bow | 38; {1} main weapon | Unfinished | xtx_itemName.csv:823 col5; _item.csv:823 col0=Normal/StandardItem; itemData.csv:823 col48=2122; compatibility row2122 col25=100; equipment.csv:706 col69=38 | unresolved |
| Bard | 4070402 | Artemis Bow | 38; {1} main weapon | named weapon/shield | xtx_itemName.csv:824 col5; _item.csv:824 col0=Normal/StandardItem; itemData.csv:824 col48=2122; compatibility row2122 col25=100; equipment.csv:707 col69=38 | unresolved |
| Bard | 8013505 | Choral Chapeau | 9; {9} head | artifact armor | xtx_itemName.csv:2151 col5; _item.csv:2151 col0=Normal/StandardItem; itemData.csv:2151 col48=2122; compatibility row2122 col25=100; equipment.csv:2034 col69=9 | unresolved |
| Bard | 8032705 | Choral Shirt | 11; {11} body | artifact armor | xtx_itemName.csv:2978 col5; _item.csv:2978 col0=Normal/StandardItem; itemData.csv:2978 col48=2122; compatibility row2122 col25=100; equipment.csv:2861 col69=11 | quest_new_reward.csv:409 row111306 col107 (Requiem for the Fallen) |
| Bard | 8051405 | Choral Tights | 13; {13} legs | artifact armor | xtx_itemName.csv:3597 col5; _item.csv:3597 col0=Normal/StandardItem; itemData.csv:3597 col48=2122; compatibility row2122 col25=100; equipment.csv:3480 col69=13 | unresolved |
| Bard | 8071405 | Choral Ringbands | 14; {14} hands | artifact armor | xtx_itemName.csv:4104 col5; _item.csv:4104 col0=Normal/StandardItem; itemData.csv:4104 col48=2122; compatibility row2122 col25=100; equipment.csv:3987 col69=14 | unresolved |
| Bard | 8081805 | Choral Sandals | 15; {15} feet | artifact armor | xtx_itemName.csv:4587 col5; _item.csv:4587 col0=Normal/StandardItem; itemData.csv:4587 col48=2122; compatibility row2122 col25=100; equipment.csv:4470 col69=15 | unresolved |
| Bard | 11000357 | Timeworn Artemis Bow | no equipment row; not an equipment slot | Timeworn | xtx_itemName.csv:7458 col5; _item.csv:7458 col0=Normal/DummyItem; itemData.csv:7458 col48=1001; compatibility row1001 col25=100 | unresolved |
| White Mage | 5030401 | Unfinished Thyrus | 37; {1} main weapon | Unfinished | xtx_itemName.csv:1114 col5; _item.csv:1114 col0=Normal/StandardItem; itemData.csv:1114 col48=2125; compatibility row2125 col34=100; equipment.csv:997 col69=37 | unresolved |
| White Mage | 5030402 | Thyrus | 37; {1} main weapon | named weapon/shield | xtx_itemName.csv:1115 col5; _item.csv:1115 col0=Normal/StandardItem; itemData.csv:1115 col48=2125; compatibility row2125 col34=100; equipment.csv:998 col69=37 | unresolved |
| White Mage | 8013506 | Healer's Circlet | 9; {9} head | artifact armor | xtx_itemName.csv:2152 col5; _item.csv:2152 col0=Normal/StandardItem; itemData.csv:2152 col48=2125; compatibility row2125 col34=100; equipment.csv:2035 col69=9 | unresolved |
| White Mage | 8032706 | Healer's Robe | 11; {11} body | artifact armor | xtx_itemName.csv:2979 col5; _item.csv:2979 col0=Normal/StandardItem; itemData.csv:2979 col48=2125; compatibility row2125 col34=100; equipment.csv:2862 col69=11 | unresolved |
| White Mage | 8051406 | Healer's Culottes | 13; {13} legs | artifact armor | xtx_itemName.csv:3598 col5; _item.csv:3598 col0=Normal/StandardItem; itemData.csv:3598 col48=2125; compatibility row2125 col34=100; equipment.csv:3481 col69=13 | unresolved |
| White Mage | 8071406 | Healer's Gloves | 14; {14} hands | artifact armor | xtx_itemName.csv:4105 col5; _item.csv:4105 col0=Normal/StandardItem; itemData.csv:4105 col48=2125; compatibility row2125 col34=100; equipment.csv:3988 col69=14 | unresolved |
| White Mage | 8081806 | Healer's Boots | 15; {15} feet | artifact armor | xtx_itemName.csv:4588 col5; _item.csv:4588 col0=Normal/StandardItem; itemData.csv:4588 col48=2125; compatibility row2125 col34=100; equipment.csv:4471 col69=15 | unresolved |
| White Mage | 11000358 | Timeworn Thyrus | no equipment row; not an equipment slot | Timeworn | xtx_itemName.csv:7459 col5; _item.csv:7459 col0=Normal/DummyItem; itemData.csv:7459 col48=1001; compatibility row1001 col34=100 | unresolved |
| Black Mage | 5020401 | Unfinished Stardust Rod | 37; {1} main weapon | Unfinished | xtx_itemName.csv:1034 col5; _item.csv:1034 col0=Normal/StandardItem; itemData.csv:1034 col48=2124; compatibility row2124 col33=100; equipment.csv:917 col69=37 | unresolved |
| Black Mage | 5020402 | Stardust Rod | 37; {1} main weapon | named weapon/shield | xtx_itemName.csv:1035 col5; _item.csv:1035 col0=Normal/StandardItem; itemData.csv:1035 col48=2124; compatibility row2124 col33=100; equipment.csv:918 col69=37 | unresolved |
| Black Mage | 8013507 | Wizard's Petasos | 9; {9} head | artifact armor | xtx_itemName.csv:2153 col5; _item.csv:2153 col0=Normal/StandardItem; itemData.csv:2153 col48=2124; compatibility row2124 col33=100; equipment.csv:2036 col69=9 | unresolved |
| Black Mage | 8032707 | Wizard's Coat | 11; {11} body | artifact armor | xtx_itemName.csv:2980 col5; _item.csv:2980 col0=Normal/StandardItem; itemData.csv:2980 col48=2124; compatibility row2124 col33=100; equipment.csv:2863 col69=11 | quest_new_reward.csv:397 row111266 col107 (Always Bet on Black) |
| Black Mage | 8051407 | Wizard's Tonban | 13; {13} legs | artifact armor | xtx_itemName.csv:3599 col5; _item.csv:3599 col0=Normal/StandardItem; itemData.csv:3599 col48=2124; compatibility row2124 col33=100; equipment.csv:3482 col69=13 | unresolved |
| Black Mage | 8071407 | Wizard's Gloves | 14; {14} hands | artifact armor | xtx_itemName.csv:4106 col5; _item.csv:4106 col0=Normal/StandardItem; itemData.csv:4106 col48=2124; compatibility row2124 col33=100; equipment.csv:3989 col69=14 | unresolved |
| Black Mage | 8081807 | Wizard's Crakows | 15; {15} feet | artifact armor | xtx_itemName.csv:4589 col5; _item.csv:4589 col0=Normal/StandardItem; itemData.csv:4589 col48=2124; compatibility row2124 col33=100; equipment.csv:4472 col69=15 | unresolved |
| Black Mage | 11000359 | Timeworn Stardust Rod | no equipment row; not an equipment slot | Timeworn | xtx_itemName.csv:7460 col5; _item.csv:7460 col0=Normal/DummyItem; itemData.csv:7460 col48=1001; compatibility row1001 col33=100 | unresolved |

## Stage and obtainability boundary

Exact-name search over all authenticated xtx_itemName.csv rows found Unfinished and named equipment forms for all seven weapons, Timeworn forms in Normal/DummyItem for all seven, and Holy Shield for Paladin. No complete absence claim follows from this selected vocabulary. Relic quest award consumers, all prerequisite/exchange steps and historical obtainability are unresolved. The Timeworn items have no equipment.csv rows, so assigning them main-hand slots would be incorrect. The compatibility cells shown are a local rejection input, not complete eligibility or retail availability.

## Row checks

All 35 selected artifact IDs and 22 relic-name candidates join exactly to item/name/data; 15 relic equipment rows plus all 35 armor rows join equipment; seven Timeworn candidates have no equipment row. Full selected member sizes and SHA-256 match manifests/tables.json.

## Selected reward and script crosswalk

The six chest references in quest_new_reward.csv are the marker 100 block at
base 104: type -10 at column 105, item ID at 107, count 1 at 109, with marker
301 at base 117. Exact item/quest matches are listed above. The recovered
QuestDetailWidget branch at lines 693-697 does not establish the -10 display
consumer, so these remain typed reward-row references, not a verified grant or
rendered offer. Quest names are xtx_quest.csv English column 2; all fields in
quest_new_reward.csv are s32.

White Mage chest 8032706 has a separate selected presentation path:
quest/scenario/whm/whm0j6.lua:468-481 (processEvent_getAF_info, method binding
at 488) passes it to openPublicInformLongDialogWidget with text 49 and then
to showGetJobItemWidget. whm0j6.csv row 49, line 45, English column 1 describes
Oha-Sok entrusting herself in the form of the formatted item. Quest 111246
binds /Quest/Scenario/Whm/Whm0j6 in staticactor_class_paths.json:8246. This
establishes authored acquisition presentation, not receipt. Dragoon chest
8032704 is likewise passed to showGetJobItemWidget in drg0j6.lua:277-280.

Quest 110868 is A Relic Reborn (xtx_quest.csv:381 column 2) and binds
/Quest/Scenario/Etc/Etc106 in staticactor_class_paths.json:8166. The authenticated
etc106.lua processEvent020 selects Timeworn IDs 11000353..11000359 for supplied
weapon selectors 1..7 (lines 2929-2962) and passes the selected ID to dialogue
rows 117 and 118 (2967-2995). These are dialogue selections, not reward grants.
The authored etc106.csv text names relic restoration (row 24 line 25), allows
one weapon trial at a time (same row), and says to complete or abandon A Relic
Reborn before switching weapon (row 25 line 26). Row 38 line 39 mentions an
accompanying shield. These facts identify a restoration narrative, without
establishing the complete exchange chain or historical availability.

The fourteen selected job quest scripts (war/mnk/whm/blm/pld/brd/drg 0j5 and
0j6), etc106 and QuestDetailWidget were authenticated against scripts.json.
No exact armor or candidate relic ID occurs in those selected job chunks
except the White Mage and Dragoon chest literals described above. This is a
bounded literal search; it does not rule out helper-selected rewards or
other quest members. All head/hands/legs/feet quest awards remain unresolved.

## Equipment-point consumer and label boundary

`item/itembaseclass_common.lua:2255-2267` implements
getEquipmentEquipPoint by reading equipmentSheet at the item's catalog ID,
column 69. The original CSV header names that column only `69`, type `s32`.
There is no foreign-key declaration to xtx_text_equipPtName in that header.

`getEquipmentEquipPointDetail` (`:2324-2550`) returns two lists. For selected
raw values at most 27 it returns `{raw}, nil` (`:2331-2335`). Raw 36 returns
`{1,2}, nil` (`:2391-2396`); raw 37 returns `{1}, {1,2}` (`:2338-2344`);
raw 38 also returns `{1}, {1,2}` (`:2347-2353`). The second list is recorded
without assigning a blocking or reservation meaning here. The first list is
consumed by isFitForEquipPoint (`:2285-2309`): a matching supplied point
returns true after isEquipment, otherwise false. The helper's isEquipment
predicate uses catalog IDs 3900000..9999999 (`:113-127`); this includes the
50 selected equipment rows and excludes the seven Timeworn IDs.

`widget/pcprofilewidget.lua:1043-1046` reads `_getEquippingItem(A3_2)` and
then dispatches that same slot argument to `setMainWeapon` for 1 (:1100-1110),
`setSubWeapon` for 2 (:1192-1201), `setHead` for 9 (:1244-1253), `setBody`
for 11 (:1257-1266), `setLegs` for 13 (:1283-1292), `setHands` for 14
(:1309-1318) and `setFeet` for 15 (:1322-1331). These recovered ordinary-slot
consumers support the descriptive names in the table. A direct text-sheet
foreign key for the composite raw codes remains unestablished. In particular,
raw 38 must not be called Full Body Armor from text row 38: its selected
consumer maps it to the main-weapon fit point 1.

## Source identities

CSV positions exclude the leading row ID. Complete CSV identities are in [`manifests/tables.json`](../manifests/tables.json), extraction `2012.09.19.0001`. The [Armoire record](armoire-item-rows.md#job-artifacts-native-category-0-35-rows) owns the artifact item-name/category joins.

Decoded Lua paths in this finding are under `xivl-client-scripts:lua/scripts/`. Each complete member was authenticated against `xivl-client-scripts:manifests/scripts.json`. The scripts establish recovered client calls, without a recorded execution or server award.

| Selected source | Bytes | SHA-256 |
| --- | ---: | --- |
| `xtx_itemName.csv` | 4428170 | `917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2` |
| `_item.csv` | 350672 | `f41dba38473a8a4014826c5b0cd639e12c6652700c9f760660fcb241d7469dda` |
| `equipment.csv` | 961673 | `acb958ef75422726f84de5a087b5f335ebe148aa5c3c754e7f8b8e26f6084b9b` |
| `itemData.csv` | 1634758 | `f17193d832b375761cd01a37b25ff7d2c2947967ddc5ba4c2b16c0507d422912` |
| `compatibility.csv` | 29873 | `0b084a0aa4ab01ab2e2a3de4ba0ee9c97257d5766f7855841d705854c0d862fe` |
| `xtx_quest.csv` | 2953504 | `938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719` |
| `quest_new_reward.csv` | 326803 | `496d5e7d2e5057852f990e18f404524426d456c52cbcbd95544652494350ff66` |
| `lua/scripts/quest/scenario/whm/whm0j6.lua` | 13930 | `894c00c20b7c6ad83cbc79aa44d32a1111c949ad6817a0f71e738d4c867dd959` |
| `lua/scripts/quest/scenario/drg/drg0j6.lua` | 7497 | `529d76bbd4830921d4211ef405e08b2881a0b7249bffdc5edf6eba6942972733` |
| `lua/scripts/quest/scenario/etc/etc106.lua` | 118972 | `6e15c5f1da729837d360faa117a7bafc14bbca3eea68c6b0fab8fa2a9c8a3c10` |
| `lua/scripts/item/itembaseclass_common.lua` | 87762 | `7620492917230c3e060ed84d3197bf164c234a3ab73e48a0939bc65107f6b7fa` |
| `lua/scripts/item/normal/normalitembaseclass_common.lua` | 14399 | `35a05383355d7205f58ad999710e5eaf92331c899c683873b823aead755645f0` |
| `lua/scripts/widget/pcprofilewidget.lua` | 50225 | `8db01acb3ca10557cff4b5e5946252b71f8cf4005e25fa641376f81c77f324d6` |
