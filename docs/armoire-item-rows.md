# Armoire stored-item catalog rows

This finding records the 130 nonzero stored-item catalog IDs recovered from the Armoire bit relation. Each ID joins by exact row ID in `_item.csv` and `xtx_itemName.csv`; the optional `itemData.csv` row is also present for typed consistency. Rows remain distinct by catalog ID, including duplicate English names.

`_item.csv` data column 0 is the raw catalog category path. `xtx_itemName.csv` data column 5 is the English Title. In the CSV text these are fields 1 and 6 because field 0 is the row ID. The item table below gives the source line for all three exact joins in the order `_item.csv / xtx_itemName.csv / itemData.csv`.

## Source identity and checks

The selected files are the retail decoded CSV extraction version `2012.09.19.0001` (`1.23b`). Their bytes and hashes match the entries in [`manifests/tables.json`](../manifests/tables.json):

| source | bytes | SHA-256 | lines | data rows |
| --- | ---: | --- | ---: | ---: |
| `_item.csv` | 350672 | `F41DBA38473A8A4014826C5B0CD639E12C6652700C9F760660FCB241D7469DDA` | 8405 | 8403 |
| `xtx_itemName.csv` | 4428170 | `917C34EB0621B7D7A8261145023D0BB95CD8CA9EB52288CEB66E80D08F0D78C2` | 8405 | 8403 |
| `itemData.csv` | 1634758 | `F17193D832B375761CD01A37B25FF7D2C2947967DDC5BA4C2B16C0507D422912` | 8405 | 8403 |
| `objectItemStorage.csv` | 3325 | `A4CCCD7E997756D1627E0C649FE94235FDAA2C3A4802143D18D9BE0C63F85E16` | 15 | 13 |

The 130 IDs have an exact row in all three item sources. No item ID is unresolved. The source row numbers below include the two CSV header rows.

## Authored Armoire menu text

`objectItemStorage.csv` is a 13-row extrasheet. Its English text is data column 1. Rows 9-12 author the four gear category labels:

| menu row | English text | source pin |
| ---: | --- | --- |
| 1 | What would you like to do? | `objectItemStorage.csv:3 column 1` |
| 2 | Store an item. | `objectItemStorage.csv:4 column 1` |
| 3 | Remove an item. | `objectItemStorage.csv:5 column 1` |
| 4 | Learn about the armoire. | `objectItemStorage.csv:6 column 1` |
| 5 | Nothing. | `objectItemStorage.csv:7 column 1` |
| 6 | The armoire is a kind of cabinet that adventurers can use to store certain prized possessions. Armoires are connected across all city-states, and items stored at one inn room can be reclaimed at another. | `objectItemStorage.csv:8 column 1` |
| 7 | Please note that certain restrictions apply when using the armoire. Firstly, only items whose condition is 100% can be stored. Secondly, storing an item resets any spiritbond you have gained with it. (Items possessed of neither condition nor spiritbond are exempt.) | `objectItemStorage.csv:9 column 1` |
| 8 | Select a gear category. | `objectItemStorage.csv:10 column 1` |
| 9 | Job artifacts. | `objectItemStorage.csv:11 column 1` |
| 10 | Seasonal events. | `objectItemStorage.csv:12 column 1` |
| 11 | Achievement rewards. | `objectItemStorage.csv:13 column 1` |
| 12 | Bonus items. | `objectItemStorage.csv:14 column 1` |
| 13 | Return. | `objectItemStorage.csv:15 column 1` |

The recovered native category values 0, 1, 2, and 3 occur with counts 35, 65, 26, and 4. The table labels those groups with menu rows 9-12 in that order: 0 = Job artifacts, 1 = Seasonal events, 2 = Achievement rewards, and 3 = Bonus items. This is a qualified ordinal crosswalk between the recovered category field and the authored menu; the CSV item rows do not carry a direct foreign key to `objectItemStorage.csv`. The full bit relation remains owned by `xivl-decomp:docs/net/armoire-storage-state.md`.

## Resolved catalog rows

### Job artifacts (native category 0; 35 rows)

| catalog ID | English name | catalog category path | exact source rows |
| ---: | --- | --- | --- |
| 8013501 | Gallant Coronet | `Normal/StandardItem` | `_item.csv:2147 col 0` / `xtx_itemName.csv:2147 col 5` / `itemData.csv:2147 row ID` |
| 8032701 | Gallant Surcoat | `Normal/StandardItem` | `_item.csv:2974 col 0` / `xtx_itemName.csv:2974 col 5` / `itemData.csv:2974 row ID` |
| 8051401 | Gallant Cuisses | `Normal/StandardItem` | `_item.csv:3593 col 0` / `xtx_itemName.csv:3593 col 5` / `itemData.csv:3593 row ID` |
| 8071401 | Gallant Gauntlets | `Normal/StandardItem` | `_item.csv:4100 col 0` / `xtx_itemName.csv:4100 col 5` / `itemData.csv:4100 row ID` |
| 8081801 | Gallant Sollerets | `Normal/StandardItem` | `_item.csv:4583 col 0` / `xtx_itemName.csv:4583 col 5` / `itemData.csv:4583 row ID` |
| 8013502 | Temple Circlet | `Normal/StandardItem` | `_item.csv:2148 col 0` / `xtx_itemName.csv:2148 col 5` / `itemData.csv:2148 row ID` |
| 8032702 | Temple Cyclas | `Normal/StandardItem` | `_item.csv:2975 col 0` / `xtx_itemName.csv:2975 col 5` / `itemData.csv:2975 row ID` |
| 8051402 | Temple Gaskins | `Normal/StandardItem` | `_item.csv:3594 col 0` / `xtx_itemName.csv:3594 col 5` / `itemData.csv:3594 row ID` |
| 8071402 | Temple Gloves | `Normal/StandardItem` | `_item.csv:4101 col 0` / `xtx_itemName.csv:4101 col 5` / `itemData.csv:4101 row ID` |
| 8081802 | Temple Boots | `Normal/StandardItem` | `_item.csv:4584 col 0` / `xtx_itemName.csv:4584 col 5` / `itemData.csv:4584 row ID` |
| 8013503 | Fighter's Burgeonet | `Normal/StandardItem` | `_item.csv:2149 col 0` / `xtx_itemName.csv:2149 col 5` / `itemData.csv:2149 row ID` |
| 8032703 | Fighter's Cuirass | `Normal/StandardItem` | `_item.csv:2976 col 0` / `xtx_itemName.csv:2976 col 5` / `itemData.csv:2976 row ID` |
| 8051403 | Fighter's Breeches | `Normal/StandardItem` | `_item.csv:3595 col 0` / `xtx_itemName.csv:3595 col 5` / `itemData.csv:3595 row ID` |
| 8071403 | Fighter's Gauntlets | `Normal/StandardItem` | `_item.csv:4102 col 0` / `xtx_itemName.csv:4102 col 5` / `itemData.csv:4102 row ID` |
| 8081803 | Fighter's Jackboots | `Normal/StandardItem` | `_item.csv:4585 col 0` / `xtx_itemName.csv:4585 col 5` / `itemData.csv:4585 row ID` |
| 8013504 | Drachen Armet | `Normal/StandardItem` | `_item.csv:2150 col 0` / `xtx_itemName.csv:2150 col 5` / `itemData.csv:2150 row ID` |
| 8032704 | Drachen Mail | `Normal/StandardItem` | `_item.csv:2977 col 0` / `xtx_itemName.csv:2977 col 5` / `itemData.csv:2977 row ID` |
| 8051404 | Drachen Breeches | `Normal/StandardItem` | `_item.csv:3596 col 0` / `xtx_itemName.csv:3596 col 5` / `itemData.csv:3596 row ID` |
| 8071404 | Drachen Gauntlets | `Normal/StandardItem` | `_item.csv:4103 col 0` / `xtx_itemName.csv:4103 col 5` / `itemData.csv:4103 row ID` |
| 8081804 | Drachen Greaves | `Normal/StandardItem` | `_item.csv:4586 col 0` / `xtx_itemName.csv:4586 col 5` / `itemData.csv:4586 row ID` |
| 8013505 | Choral Chapeau | `Normal/StandardItem` | `_item.csv:2151 col 0` / `xtx_itemName.csv:2151 col 5` / `itemData.csv:2151 row ID` |
| 8032705 | Choral Shirt | `Normal/StandardItem` | `_item.csv:2978 col 0` / `xtx_itemName.csv:2978 col 5` / `itemData.csv:2978 row ID` |
| 8051405 | Choral Tights | `Normal/StandardItem` | `_item.csv:3597 col 0` / `xtx_itemName.csv:3597 col 5` / `itemData.csv:3597 row ID` |
| 8071405 | Choral Ringbands | `Normal/StandardItem` | `_item.csv:4104 col 0` / `xtx_itemName.csv:4104 col 5` / `itemData.csv:4104 row ID` |
| 8081805 | Choral Sandals | `Normal/StandardItem` | `_item.csv:4587 col 0` / `xtx_itemName.csv:4587 col 5` / `itemData.csv:4587 row ID` |
| 8013506 | Healer's Circlet | `Normal/StandardItem` | `_item.csv:2152 col 0` / `xtx_itemName.csv:2152 col 5` / `itemData.csv:2152 row ID` |
| 8032706 | Healer's Robe | `Normal/StandardItem` | `_item.csv:2979 col 0` / `xtx_itemName.csv:2979 col 5` / `itemData.csv:2979 row ID` |
| 8051406 | Healer's Culottes | `Normal/StandardItem` | `_item.csv:3598 col 0` / `xtx_itemName.csv:3598 col 5` / `itemData.csv:3598 row ID` |
| 8071406 | Healer's Gloves | `Normal/StandardItem` | `_item.csv:4105 col 0` / `xtx_itemName.csv:4105 col 5` / `itemData.csv:4105 row ID` |
| 8081806 | Healer's Boots | `Normal/StandardItem` | `_item.csv:4588 col 0` / `xtx_itemName.csv:4588 col 5` / `itemData.csv:4588 row ID` |
| 8013507 | Wizard's Petasos | `Normal/StandardItem` | `_item.csv:2153 col 0` / `xtx_itemName.csv:2153 col 5` / `itemData.csv:2153 row ID` |
| 8032707 | Wizard's Coat | `Normal/StandardItem` | `_item.csv:2980 col 0` / `xtx_itemName.csv:2980 col 5` / `itemData.csv:2980 row ID` |
| 8051407 | Wizard's Tonban | `Normal/StandardItem` | `_item.csv:3599 col 0` / `xtx_itemName.csv:3599 col 5` / `itemData.csv:3599 row ID` |
| 8071407 | Wizard's Gloves | `Normal/StandardItem` | `_item.csv:4106 col 0` / `xtx_itemName.csv:4106 col 5` / `itemData.csv:4106 row ID` |
| 8081807 | Wizard's Crakows | `Normal/StandardItem` | `_item.csv:4589 col 0` / `xtx_itemName.csv:4589 col 5` / `itemData.csv:4589 row ID` |

### Seasonal events (native category 1; 65 rows)

| catalog ID | English name | catalog category path | exact source rows |
| ---: | --- | --- | --- |
| 8012604 | Dragon Kabuto | `Normal/StandardItem` | `_item.csv:2071 col 0` / `xtx_itemName.csv:2071 col 5` / `itemData.csv:2071 row ID` |
| 8012605 | Crimson Dragon Kabuto | `Normal/StandardItem` | `_item.csv:2072 col 0` / `xtx_itemName.csv:2072 col 5` / `itemData.csv:2072 row ID` |
| 8012606 | Golden Dragon Kabuto | `Normal/StandardItem` | `_item.csv:2073 col 0` / `xtx_itemName.csv:2073 col 5` / `itemData.csv:2073 row ID` |
| 8012607 | Black Dragon Kabuto | `Normal/StandardItem` | `_item.csv:2074 col 0` / `xtx_itemName.csv:2074 col 5` / `itemData.csv:2074 row ID` |
| 9040019 | Paramour's Pendant | `Normal/StandardItem` | `_item.csv:4864 col 0` / `xtx_itemName.csv:4864 col 5` / `itemData.csv:4864 row ID` |
| 9040020 | Platinum Paramour's Pendant | `Normal/StandardItem` | `_item.csv:4865 col 0` / `xtx_itemName.csv:4865 col 5` / `itemData.csv:4865 row ID` |
| 9040021 | Band of Eternal Passion | `Normal/StandardItem` | `_item.csv:4866 col 0` / `xtx_itemName.csv:4866 col 5` / `itemData.csv:4866 row ID` |
| 9030053 | Peach Blossom | `Normal/StandardItem` | `_item.csv:4833 col 0` / `xtx_itemName.csv:4833 col 5` / `itemData.csv:4833 row ID` |
| 8012801 | Pristine Egg Cap | `Normal/StandardItem` | `_item.csv:2114 col 0` / `xtx_itemName.csv:2114 col 5` / `itemData.csv:2114 row ID` |
| 8012802 | Vibrant Egg Cap | `Normal/StandardItem` | `_item.csv:2115 col 0` / `xtx_itemName.csv:2115 col 5` / `itemData.csv:2115 row ID` |
| 8012803 | Brilliant Egg Cap | `Normal/StandardItem` | `_item.csv:2116 col 0` / `xtx_itemName.csv:2116 col 5` / `itemData.csv:2116 row ID` |
| 8012804 | Midnight Egg Cap | `Normal/StandardItem` | `_item.csv:2117 col 0` / `xtx_itemName.csv:2117 col 5` / `itemData.csv:2117 row ID` |
| 8012805 | Chocobo Egg Cap | `Normal/StandardItem` | `_item.csv:2118 col 0` / `xtx_itemName.csv:2118 col 5` / `itemData.csv:2118 row ID` |
| 9050058 | Pristine Egg Ring | `Normal/StandardItem` | `_item.csv:4971 col 0` / `xtx_itemName.csv:4971 col 5` / `itemData.csv:4971 row ID` |
| 9050061 | Vibrant Egg Ring | `Normal/StandardItem` | `_item.csv:4974 col 0` / `xtx_itemName.csv:4974 col 5` / `itemData.csv:4974 row ID` |
| 9050060 | Brilliant Egg Ring | `Normal/StandardItem` | `_item.csv:4973 col 0` / `xtx_itemName.csv:4973 col 5` / `itemData.csv:4973 row ID` |
| 9050059 | Midnight Egg Ring | `Normal/StandardItem` | `_item.csv:4972 col 0` / `xtx_itemName.csv:4972 col 5` / `itemData.csv:4972 row ID` |
| 9050062 | Chocobo Egg Ring | `Normal/StandardItem` | `_item.csv:4975 col 0` / `xtx_itemName.csv:4975 col 5` / `itemData.csv:4975 row ID` |
| 8032401 | Red Summer Top | `Normal/StandardItem` | `_item.csv:2956 col 0` / `xtx_itemName.csv:2956 col 5` / `itemData.csv:2956 row ID` |
| 8032402 | Green Summer Top | `Normal/StandardItem` | `_item.csv:2957 col 0` / `xtx_itemName.csv:2957 col 5` / `itemData.csv:2957 row ID` |
| 8032403 | Blue Summer Top | `Normal/StandardItem` | `_item.csv:2958 col 0` / `xtx_itemName.csv:2958 col 5` / `itemData.csv:2958 row ID` |
| 8032404 | Solar Summer Top | `Normal/StandardItem` | `_item.csv:2959 col 0` / `xtx_itemName.csv:2959 col 5` / `itemData.csv:2959 row ID` |
| 8032405 | Lunar Summer Top | `Normal/StandardItem` | `_item.csv:2960 col 0` / `xtx_itemName.csv:2960 col 5` / `itemData.csv:2960 row ID` |
| 8032406 | Red Summer Halter | `Normal/StandardItem` | `_item.csv:2961 col 0` / `xtx_itemName.csv:2961 col 5` / `itemData.csv:2961 row ID` |
| 8032407 | Green Summer Halter | `Normal/StandardItem` | `_item.csv:2962 col 0` / `xtx_itemName.csv:2962 col 5` / `itemData.csv:2962 row ID` |
| 8032408 | Blue Summer Halter | `Normal/StandardItem` | `_item.csv:2963 col 0` / `xtx_itemName.csv:2963 col 5` / `itemData.csv:2963 row ID` |
| 8032409 | Solar Summer Halter | `Normal/StandardItem` | `_item.csv:2964 col 0` / `xtx_itemName.csv:2964 col 5` / `itemData.csv:2964 row ID` |
| 8032410 | Lunar Summer Halter | `Normal/StandardItem` | `_item.csv:2965 col 0` / `xtx_itemName.csv:2965 col 5` / `itemData.csv:2965 row ID` |
| 8051301 | Red Summer Trunks | `Normal/StandardItem` | `_item.csv:3583 col 0` / `xtx_itemName.csv:3583 col 5` / `itemData.csv:3583 row ID` |
| 8051302 | Green Summer Trunks | `Normal/StandardItem` | `_item.csv:3584 col 0` / `xtx_itemName.csv:3584 col 5` / `itemData.csv:3584 row ID` |
| 8051303 | Blue Summer Trunks | `Normal/StandardItem` | `_item.csv:3585 col 0` / `xtx_itemName.csv:3585 col 5` / `itemData.csv:3585 row ID` |
| 8051304 | Solar Summer Trunks | `Normal/StandardItem` | `_item.csv:3586 col 0` / `xtx_itemName.csv:3586 col 5` / `itemData.csv:3586 row ID` |
| 8051305 | Lunar Summer Trunks | `Normal/StandardItem` | `_item.csv:3587 col 0` / `xtx_itemName.csv:3587 col 5` / `itemData.csv:3587 row ID` |
| 8051306 | Red Summer Tanga | `Normal/StandardItem` | `_item.csv:3588 col 0` / `xtx_itemName.csv:3588 col 5` / `itemData.csv:3588 row ID` |
| 8051307 | Green Summer Tanga | `Normal/StandardItem` | `_item.csv:3589 col 0` / `xtx_itemName.csv:3589 col 5` / `itemData.csv:3589 row ID` |
| 8051308 | Blue Summer Tanga | `Normal/StandardItem` | `_item.csv:3590 col 0` / `xtx_itemName.csv:3590 col 5` / `itemData.csv:3590 row ID` |
| 8051309 | Solar Summer Tanga | `Normal/StandardItem` | `_item.csv:3591 col 0` / `xtx_itemName.csv:3591 col 5` / `itemData.csv:3591 row ID` |
| 8051310 | Lunar Summer Tanga | `Normal/StandardItem` | `_item.csv:3592 col 0` / `xtx_itemName.csv:3592 col 5` / `itemData.csv:3592 row ID` |
| 8013301 | Pumpkin Head | `Normal/StandardItem` | `_item.csv:2139 col 0` / `xtx_itemName.csv:2139 col 5` / `itemData.csv:2139 row ID` |
| 8013302 | Unripened Pumpkin Head | `Normal/StandardItem` | `_item.csv:2140 col 0` / `xtx_itemName.csv:2140 col 5` / `itemData.csv:2140 row ID` |
| 8013303 | White Pumpkin Head | `Normal/StandardItem` | `_item.csv:2141 col 0` / `xtx_itemName.csv:2141 col 5` / `itemData.csv:2141 row ID` |
| 8013304 | Ripened Pumpkin Head | `Normal/StandardItem` | `_item.csv:2142 col 0` / `xtx_itemName.csv:2142 col 5` / `itemData.csv:2142 row ID` |
| 8012502 | Reindeer Antlers | `Normal/StandardItem` | `_item.csv:2067 col 0` / `xtx_itemName.csv:2067 col 5` / `itemData.csv:2067 row ID` |
| 8032102 | Reindeer Suit | `Normal/StandardItem` | `_item.csv:2899 col 0` / `xtx_itemName.csv:2899 col 5` / `itemData.csv:2899 row ID` |
| 9030020 | Moonlet | `Normal/StandardItem` | `_item.csv:4800 col 0` / `xtx_itemName.csv:4800 col 5` / `itemData.csv:4800 row ID` |
| 9040018 | Patriot's Choker | `Normal/StandardItem` | `_item.csv:4863 col 0` / `xtx_itemName.csv:4863 col 5` / `itemData.csv:4863 row ID` |
| 8032834 | Lord's Yukata (Blue) | `Normal/StandardItem` | `_item.csv:3014 col 0` / `xtx_itemName.csv:3014 col 5` / `itemData.csv:3014 row ID` |
| 8032835 | Lord's Yukata (Green) | `Normal/StandardItem` | `_item.csv:3015 col 0` / `xtx_itemName.csv:3015 col 5` / `itemData.csv:3015 row ID` |
| 8032836 | Lord's Yukata (Grey) | `Normal/StandardItem` | `_item.csv:3016 col 0` / `xtx_itemName.csv:3016 col 5` / `itemData.csv:3016 row ID` |
| 8032837 | Lady's Yukata (Red) | `Normal/StandardItem` | `_item.csv:3017 col 0` / `xtx_itemName.csv:3017 col 5` / `itemData.csv:3017 row ID` |
| 8032838 | Lady's Yukata (Blue) | `Normal/StandardItem` | `_item.csv:3018 col 0` / `xtx_itemName.csv:3018 col 5` / `itemData.csv:3018 row ID` |
| 8032839 | Lady's Yukata (Black) | `Normal/StandardItem` | `_item.csv:3019 col 0` / `xtx_itemName.csv:3019 col 5` / `itemData.csv:3019 row ID` |
| 8051521 | Lord's Drawers (Black) | `Normal/StandardItem` | `_item.csv:3620 col 0` / `xtx_itemName.csv:3620 col 5` / `itemData.csv:3620 row ID` |
| 8051522 | Lord's Drawers (White) | `Normal/StandardItem` | `_item.csv:3621 col 0` / `xtx_itemName.csv:3621 col 5` / `itemData.csv:3621 row ID` |
| 8051523 | Lord's Drawers (Gold) | `Normal/StandardItem` | `_item.csv:3622 col 0` / `xtx_itemName.csv:3622 col 5` / `itemData.csv:3622 row ID` |
| 8051524 | Lady's Knickers (Black) | `Normal/StandardItem` | `_item.csv:3623 col 0` / `xtx_itemName.csv:3623 col 5` / `itemData.csv:3623 row ID` |
| 8051525 | Lady's Knickers (White) | `Normal/StandardItem` | `_item.csv:3624 col 0` / `xtx_itemName.csv:3624 col 5` / `itemData.csv:3624 row ID` |
| 8051526 | Lady's Knickers (Gold) | `Normal/StandardItem` | `_item.csv:3625 col 0` / `xtx_itemName.csv:3625 col 5` / `itemData.csv:3625 row ID` |
| 8081921 | Lord's Clogs | `Normal/StandardItem` | `_item.csv:4610 col 0` / `xtx_itemName.csv:4610 col 5` / `itemData.csv:4610 row ID` |
| 8081922 | Lady's Clogs | `Normal/StandardItem` | `_item.csv:4611 col 0` / `xtx_itemName.csv:4611 col 5` / `itemData.csv:4611 row ID` |
| 8010932 | Woolen Sugarloaf Hat (Red) | `Normal/StandardItem` | `_item.csv:1807 col 0` / `xtx_itemName.csv:1807 col 5` / `itemData.csv:1807 row ID` |
| 8050521 | Star-Spangled Subligar | `Normal/StandardItem` | `_item.csv:3403 col 0` / `xtx_itemName.csv:3403 col 5` / `itemData.csv:3403 row ID` |
| 8012102 | Peregrine Helm | `Normal/StandardItem` | `_item.csv:2007 col 0` / `xtx_itemName.csv:2007 col 5` / `itemData.csv:2007 row ID` |
| 8013623 | Scarf of Wondrous Wit | `Normal/StandardItem` | `_item.csv:2176 col 0` / `xtx_itemName.csv:2176 col 5` / `itemData.csv:2176 row ID` |
| 9030063 | White Ravens | `Normal/StandardItem` | `_item.csv:4843 col 0` / `xtx_itemName.csv:4843 col 5` / `itemData.csv:4843 row ID` |

### Achievement rewards (native category 2; 26 rows)

| catalog ID | English name | catalog category path | exact source rows |
| ---: | --- | --- | --- |
| 8013401 | Butcher's Crown | `Normal/StandardItem` | `_item.csv:2143 col 0` / `xtx_itemName.csv:2143 col 5` / `itemData.csv:2143 row ID` |
| 8013402 | Chronicler's Crown | `Normal/StandardItem` | `_item.csv:2144 col 0` / `xtx_itemName.csv:2144 col 5` / `itemData.csv:2144 row ID` |
| 8013403 | Paragon's Crown | `Normal/StandardItem` | `_item.csv:2145 col 0` / `xtx_itemName.csv:2145 col 5` / `itemData.csv:2145 row ID` |
| 8013404 | Gambler's Crown | `Normal/StandardItem` | `_item.csv:2146 col 0` / `xtx_itemName.csv:2146 col 5` / `itemData.csv:2146 row ID` |
| 6010016 | Saw of the Luminary | `Normal/ToolItem` | `_item.csv:1141 col 0` / `xtx_itemName.csv:1141 col 5` / `itemData.csv:1141 row ID` |
| 6020015 | Hammer of the Luminary | `Normal/ToolItem` | `_item.csv:1164 col 0` / `xtx_itemName.csv:1164 col 5` / `itemData.csv:1164 row ID` |
| 6030016 | Mallet of the Luminary | `Normal/ToolItem` | `_item.csv:1191 col 0` / `xtx_itemName.csv:1191 col 5` / `itemData.csv:1191 row ID` |
| 6040016 | Gavel of the Luminary | `Normal/ToolItem` | `_item.csv:1215 col 0` / `xtx_itemName.csv:1215 col 5` / `itemData.csv:1215 row ID` |
| 6050016 | Knife of the Luminary | `Normal/ToolItem` | `_item.csv:1239 col 0` / `xtx_itemName.csv:1239 col 5` / `itemData.csv:1239 row ID` |
| 6060015 | Needle of the Luminary | `Normal/ToolItem` | `_item.csv:1262 col 0` / `xtx_itemName.csv:1262 col 5` / `itemData.csv:1262 row ID` |
| 6070016 | Alembic of the Luminary | `Normal/ToolItem` | `_item.csv:1287 col 0` / `xtx_itemName.csv:1287 col 5` / `itemData.csv:1287 row ID` |
| 6080016 | Pan of the Luminary | `Normal/ToolItem` | `_item.csv:1311 col 0` / `xtx_itemName.csv:1311 col 5` / `itemData.csv:1311 row ID` |
| 7010017 | Pick of the Luminary | `Normal/ToolItem` | `_item.csv:1336 col 0` / `xtx_itemName.csv:1336 col 5` / `itemData.csv:1336 row ID` |
| 7020016 | Axe of the Luminary | `Normal/ToolItem` | `_item.csv:1361 col 0` / `xtx_itemName.csv:1361 col 5` / `itemData.csv:1361 row ID` |
| 7030016 | Rod of the Luminary | `Normal/ToolItem` | `_item.csv:1386 col 0` / `xtx_itemName.csv:1386 col 5` / `itemData.csv:1386 row ID` |
| 4100801 | Maelstrom Escutcheon | `Normal/ShieldItem` | `_item.csv:967 col 0` / `xtx_itemName.csv:967 col 5` / `itemData.csv:967 row ID` |
| 4100802 | Immortal Flames Escutcheon | `Normal/ShieldItem` | `_item.csv:968 col 0` / `xtx_itemName.csv:968 col 5` / `itemData.csv:968 row ID` |
| 4100803 | Twin Adder Escutcheon | `Normal/ShieldItem` | `_item.csv:969 col 0` / `xtx_itemName.csv:969 col 5` / `itemData.csv:969 row ID` |
| 9030050 | Crimson Standard Earring | `Normal/StandardItem` | `_item.csv:4830 col 0` / `xtx_itemName.csv:4830 col 5` / `itemData.csv:4830 row ID` |
| 9030051 | Tipping Scales Earring | `Normal/StandardItem` | `_item.csv:4831 col 0` / `xtx_itemName.csv:4831 col 5` / `itemData.csv:4831 row ID` |
| 9030052 | Lily and Serpent Earring | `Normal/StandardItem` | `_item.csv:4832 col 0` / `xtx_itemName.csv:4832 col 5` / `itemData.csv:4832 row ID` |
| 9050055 | Crimson Standard Ring | `Normal/StandardItem` | `_item.csv:4968 col 0` / `xtx_itemName.csv:4968 col 5` / `itemData.csv:4968 row ID` |
| 9050056 | Tipping Scales Ring | `Normal/StandardItem` | `_item.csv:4969 col 0` / `xtx_itemName.csv:4969 col 5` / `itemData.csv:4969 row ID` |
| 9050057 | Lily and Serpent Ring | `Normal/StandardItem` | `_item.csv:4970 col 0` / `xtx_itemName.csv:4970 col 5` / `itemData.csv:4970 row ID` |
| 8013626 | Chocobo Mask | `Normal/StandardItem` | `_item.csv:2179 col 0` / `xtx_itemName.csv:2179 col 5` / `itemData.csv:2179 row ID` |
| 8013635 | Dalamud Horn | `Normal/StandardItem` | `_item.csv:2188 col 0` / `xtx_itemName.csv:2188 col 5` / `itemData.csv:2188 row ID` |

### Bonus items (native category 3; 4 rows)

| catalog ID | English name | catalog category path | exact source rows |
| ---: | --- | --- | --- |
| 8010225 | Garlond Goggles | `Normal/SpecialEquipItem` | `_item.csv:1486 col 0` / `xtx_itemName.csv:1486 col 5` / `itemData.csv:1486 row ID` |
| 8012101 | Onion Helm | `Normal/SpecialEquipItem` | `_item.csv:2006 col 0` / `xtx_itemName.csv:2006 col 5` / `itemData.csv:2006 row ID` |
| 8070512 | Asuran Armguards | `Normal/SpecialEquipItem` | `_item.csv:3937 col 0` / `xtx_itemName.csv:3937 col 5` / `itemData.csv:3937 row ID` |
| 8080512 | Hermes' Shoes | `Normal/EnchantItem` | `_item.csv:4354 col 0` / `xtx_itemName.csv:4354 col 5` / `itemData.csv:4354 row ID` |
