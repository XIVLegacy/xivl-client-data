# Achievement and title display-name joins

The table joins all 208 `achievement.csv` rows with a nonzero title key to
their English achievement name and both English title selector strings in
retail FFXIV 1.23b extraction `2012.09.19.0001`. Achievement IDs and title IDs
remain distinct keys. Repeated title IDs and names remain separate rows.

## Source cells and identities

All column positions are zero-based after the leading row ID. The achievement
row ID joins directly to `xtx_achievement.csv` row ID. `achievement.csv`
column 3 supplies the title ID, which joins to `xtx_title.csv` row ID.
The English achievement name is `xtx_achievement.csv` column 8. English title
selectors 0 and 1 are `xtx_title.csv` columns 3 and 4 respectively.

The complete member identities are recorded in
[tables.json](../manifests/tables.json), extraction `2012.09.19.0001`.
The named archive identity is pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json): 70110686 bytes,
SHA-256 `006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
The join uses only these three decoded members:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `achievement.csv` | 28895 | `3aecdc3005619b76c813318b12ba7e9b38588d0e3007811d43668a307a68243f` |
| `xtx_achievement.csv` | 297212 | `149f932d206dfb21dd271bd64c6028ead8ec4d3eb2adcc4258947863b05c85b5` |
| `xtx_title.csv` | 21050 | `490c6346ed541f78e50e78f087f8a4b01975bee7648359f6acd25ac5ca94f1e4` |

The source rows are located by the achievement and title IDs in each table
entry below. The two text members contain 746 achievement rows and 116 title
rows. Each displayed cell preserves its decoded spelling, punctuation and
capitalization. The title selector is a presentation input, not another title
ID. Its player-sex and tribe consumers are documented in
[`xivl-decomp:docs/script/player-achievement-titles.md`, Display consumers and limits](https://github.com/XIVLegacy/xivl-decomp/blob/69b6945b3f172c547d8c1bcbc8bdc64dc52ef579/docs/script/player-achievement-titles.md#display-consumers-and-limits).

## Display-name table

| Achievement ID | English achievement name | Title ID | English title selector 0 | English title selector 1 |
| ---: | --- | ---: | --- | --- |
| 106 | To Crush Your Enemies VI | 200 | the Exterminator | the Exterminator |
| 115 | Notorious Monster Hunting | 201 | Notorious Monster Hunter | Notorious Monster Hunter |
| 197 | To Crush Your Enemies IV | 200 | the Exterminator | the Exterminator |
| 198 | Notorious Monster Hunting | 201 | Notorious Monster Hunter | Notorious Monster Hunter |
| 226 | Mastering War | 400 | Warmonger | Warmonger |
| 237 | Mastering Magic | 401 | Archmage | Archmage |
| 279 | Mastering the Hand | 402 | Builder of the Realm | Builder of the Realm |
| 295 | Mastering the Land | 403 | Provider of the Realm | Provider of the Realm |
| 390 | Mastering War | 400 | Warmonger | Warmonger |
| 391 | Mastering Magic | 401 | Archmage | Archmage |
| 392 | Mastering the Hand | 402 | Builder of the Realm | Builder of the Realm |
| 393 | Mastering the Land | 403 | Provider of the Realm | Provider of the Realm |
| 406 | Who Wants to Be a Gillionaire? | 300 | Honest Gillionaire | Honest Gillionaire |
| 412 | Never Met a Corpse I Couldn't Rifle | 301 | Ruthless Gillionaire | Ruthless Gillionaire |
| 498 | Who Wants to Be a Gillionaire? | 300 | Honest Gillionaire | Honest Gillionaire |
| 499 | Never Met a Corpse I Couldn't Rifle | 301 | Ruthless Gillionaire | Ruthless Gillionaire |
| 504 | Raising the Curtana | 102 | the True | the True |
| 505 | Enter the Coeurl | 103 | Coeurlfist | Coeurlfist |
| 506 | Cleaving to Tradition | 104 | Ironeater | Ironeater |
| 507 | Having a Gae Old Time | 105 | of the Vengeful Lance | of the Vengeful Lance |
| 508 | Hard to Miss | 106 | the Godsbow | the Godsbow |
| 509 | Dressed to Heal | 107 | the White | the White |
| 510 | Ohohohohoho! | 108 | Starcaller | Starcaller |
| 511 | Armed to the Teeth | 101 | the Insatiable | the Insatiable |
| 592 | Raising the Curtana | 102 | the True | the True |
| 593 | Enter the Coeurl | 103 | Coeurlfist | Coeurlfist |
| 594 | Cleaving to Tradition | 104 | Ironeater | Ironeater |
| 595 | Having a Gae Old Time | 105 | of the Vengeful Lance | of the Vengeful Lance |
| 596 | Hard to Miss | 106 | the Godsbow | the Godsbow |
| 597 | Dressed to Heal | 107 | the White | the White |
| 598 | Ohohohohoho! | 108 | Starcaller | Starcaller |
| 599 | Armed to the Teeth | 101 | the Insatiable | the Insatiable |
| 605 | Going with the Grain: Artisan | 500 | of the Golden Saw | of the Golden Saw |
| 611 | Working the Bellows: Artisan | 501 | of the Golden Anvil | of the Golden Anvil |
| 617 | Pounding Out the Dents: Artisan | 502 | of the Golden Hammer | of the Golden Hammer |
| 623 | Cutting the Carats: Artisan | 503 | of the Golden Leaf | of the Golden Leaf |
| 629 | Hiding in Plain Sight: Artisan | 504 | of the Golden Hide | of the Golden Hide |
| 635 | Threading the Needle: Artisan | 505 | of the Golden Needle | of the Golden Needle |
| 641 | Mixing It Up: Artisan | 506 | of the Golden Lead | of the Golden Lead |
| 647 | Savoring the Realm: Artisan | 507 | of the Golden Ladle | of the Golden Ladle |
| 683 | Going with the Grain: Artisan | 500 | of the Golden Saw | of the Golden Saw |
| 684 | Working the Bellows: Artisan | 501 | of the Golden Anvil | of the Golden Anvil |
| 685 | Pounding Out the Dents: Artisan | 502 | of the Golden Hammer | of the Golden Hammer |
| 686 | Cutting the Carats: Artisan | 503 | of the Golden Leaf | of the Golden Leaf |
| 687 | Hiding in Plain Sight: Artisan | 504 | of the Golden Hide | of the Golden Hide |
| 688 | Threading the Needle: Artisan | 505 | of the Golden Needle | of the Golden Needle |
| 689 | Mixing It Up: Artisan | 506 | of the Golden Lead | of the Golden Lead |
| 690 | Savoring the Realm: Artisan | 507 | of the Golden Ladle | of the Golden Ladle |
| 706 | A Miner's Life for Me: La Noscea | 600 | Meadowbreaker | Meadowbreaker |
| 712 | A Miner's Life for Me: Black Shroud | 601 | Forestbreaker | Forestbreaker |
| 718 | A Miner's Life for Me: Thanalan | 602 | Desertbreaker | Desertbreaker |
| 725 | I'd Rather Be Quarrying: La Noscea | 603 | of the Meadow Mines | of the Meadow Mines |
| 731 | I'd Rather Be Quarrying: Black Shroud | 604 | of the Forest Mines | of the Forest Mines |
| 737 | I'd Rather Be Quarrying: Thanalan | 605 | of the Desert Mines | of the Desert Mines |
| 743 | A Botanist's Life for Me: La Noscea | 606 | Meadowreaper | Meadowreaper |
| 749 | A Botanist's Life for Me: Black Shroud | 607 | Forestreaper | Forestreaper |
| 755 | A Botanist's Life for Me: Thanalan | 608 | Desertreaper | Desertreaper |
| 762 | I'd Rather Be Harvesting: La Noscea | 609 | of the Meadow Grasses | of the Meadow Grasses |
| 768 | I'd Rather Be Harvesting: Black Shroud | 610 | of the Forest Grasses | of the Forest Grasses |
| 774 | I'd Rather Be Harvesting: Thanalan | 611 | of the Desert Grasses | of the Desert Grasses |
| 780 | A Fisher's Life for Me: La Noscea | 612 | Meadowcaster | Meadowcaster |
| 786 | A Fisher's Life for Me: Black Shroud | 613 | Forestcaster | Forestcaster |
| 792 | A Fisher's Life for Me: Thanalan | 614 | Desertcaster | Desertcaster |
| 799 | I'd Rather Be Spearfishing: La Noscea | 615 | of the Meadow Pools | of the Meadow Pools |
| 805 | I'd Rather Be Spearfishing: Black Shroud | 616 | of the Forest Pools | of the Forest Pools |
| 811 | I'd Rather Be Spearfishing: Thanalan | 617 | of the Desert Pools | of the Desert Pools |
| 879 | A Miner's Life for Me: La Noscea | 600 | Meadowbreaker | Meadowbreaker |
| 880 | A Miner's Life for Me: Black Shroud | 601 | Forestbreaker | Forestbreaker |
| 881 | A Miner's Life for Me: Thanalan | 602 | Desertbreaker | Desertbreaker |
| 882 | I'd Rather Be Quarrying: La Noscea | 603 | of the Meadow Mines | of the Meadow Mines |
| 883 | I'd Rather Be Quarrying: Black Shroud | 604 | of the Forest Mines | of the Forest Mines |
| 884 | I'd Rather Be Quarrying: Thanalan | 605 | of the Desert Mines | of the Desert Mines |
| 885 | A Botanist's Life for Me: La Noscea | 606 | Meadowreaper | Meadowreaper |
| 886 | A Botanist's Life for Me: Black Shroud | 607 | Forestreaper | Forestreaper |
| 887 | A Botanist's Life for Me: Thanalan | 608 | Desertreaper | Desertreaper |
| 888 | I'd Rather Be Harvesting: La Noscea | 609 | of the Meadow Grasses | of the Meadow Grasses |
| 889 | I'd Rather Be Harvesting: Black Shroud | 610 | of the Forest Grasses | of the Forest Grasses |
| 890 | I'd Rather Be Harvesting: Thanalan | 611 | of the Desert Grasses | of the Desert Grasses |
| 891 | A Fisher's Life for Me: La Noscea | 612 | Meadowcaster | Meadowcaster |
| 892 | A Fisher's Life for Me: Black Shroud | 613 | Forestcaster | Forestcaster |
| 893 | A Fisher's Life for Me: Thanalan | 614 | Desertcaster | Desertcaster |
| 894 | I'd Rather Be Spearfishing: La Noscea | 615 | of the Meadow Pools | of the Meadow Pools |
| 895 | I'd Rather Be Spearfishing: Black Shroud | 616 | of the Forest Pools | of the Forest Pools |
| 896 | I'd Rather Be Spearfishing: Thanalan | 617 | of the Desert Pools | of the Desert Pools |
| 997 | Materia Hysteria | 700 | Carrier of the Cauldron | Carrier of the Cauldron |
| 998 | Living in a Materia World | 701 | the Assimilator | the Assimilator |
| 1005 | Tales of War | 800 | Seeker of Blood | Seeker of Blood |
| 1006 | Tales of Magic | 801 | Seeker of Truth | Seeker of Truth |
| 1007 | Tales of the Hand | 802 | Seeker of Skill | Seeker of Skill |
| 1008 | Tales of the Land | 803 | Seeker of Bounty | Seeker of Bounty |
| 1013 | Sideways | 804 | Sidestepper | Sidestepper |
| 1019 | All the More Region to Leve VI | 805 | Lord Protector | Lady Protector |
| 1026 | Think Global, Quest Local VI | 806 | Lord Creator | Lady Creator |
| 1030 | A Slave to Faction III | 807 | Peacemaker | Peacemaker |
| 1037 | Serving a Greater Cause VI | 808 | the Last Resort | the Last Resort |
| 1047 | And All I Got Was This Lousy Achievement: La Noscea | 809 | the Sword of La Noscea | the Sword of La Noscea |
| 1055 | And All I Got Was This Lousy Achievement: Black Shroud | 810 | the Sword of the Shroud | the Sword of the Shroud |
| 1063 | And All I Got Was This Lousy Achievement: Thanalan | 811 | the Sword of Thanalan | the Sword of Thanalan |
| 1064 | Globetrotter | 812 | the Sword of Eorzea | the Sword of Eorzea |
| 1073 | La Noscea Got Served...and Protected | 813 | the Shield of La Noscea | the Shield of La Noscea |
| 1081 | The Black Shroud Got Served...and Protected | 814 | the Shield of the Shroud | the Shield of the Shroud |
| 1089 | Thanalan Got Served...and Protected | 815 | the Shield of Thanalan | the Shield of Thanalan |
| 1090 | Eorzea Got Served...and Protected | 816 | the Shield of Eorzea | the Shield of Eorzea |
| 1092 | Love Thy Brother | 817 | Brother of the Broken Blade | Sister of the Broken Blade |
| 1094 | Another Brick in the Shield Wall | 818 | the Warden's Wall | the Warden's Wall |
| 1096 | A Helping Horn | 819 | Bearer of the Horn | Bearer of the Horn |
| 1097 | Commitment Issues | 820 | the Uncommitted | the Uncommitted |
| 1105 | Career Opportunities | 825 | the Professional | the Professional |
| 1157 | Patricide | 826 | Inquisitor | Inquisitor |
| 1158 | To Kill a Mocking Bird | 827 | Divine Crusher | Divine Crusher |
| 1159 | Pounding the Spike | 828 | Stonesplitter | Stonesplitter |
| 1160 | First Blood: Aleport | 829 | A Kobold's Worst Nightmare | A Kobold's Worst Nightmare |
| 1161 | First Blood: Hyrstmill | 830 | An Ixal's Worst Nightmare | An Ixal's Worst Nightmare |
| 1162 | First Blood: Golden Bazaar | 831 | An Amalj'aa's Worst Nightmare | An Amalj'aa's Worst Nightmare |
| 1163 | To Be or Not to Be the Guardian of Aleport | 832 | the Guardian of Aleport | the Guardian of Aleport |
| 1164 | To Be or Not to Be the Guardian of Hyrstmill | 833 | the Guardian of Hyrstmill | the Guardian of Hyrstmill |
| 1165 | To Be or Not to Be the Guardian of the Golden Bazaar | 834 | the Guardian of the Golden Bazaar | the Guardian of the Golden Bazaar |
| 1166 | To Be or Not to Be the Wind of Aleport | 835 | the Wind of Aleport | the Wind of Aleport |
| 1167 | To Be or Not to Be the Wind of Hyrstmill | 836 | the Wind of Hyrstmill | the Wind of Hyrstmill |
| 1168 | To Be or Not to Be the Wind of the Golden Bazaar | 837 | the Wind of the Golden Bazaar | the Wind of the Golden Bazaar |
| 1169 | To Be or Not to Be the Hand of Aleport | 838 | the Hand of Aleport | the Hand of Aleport |
| 1171 | To Be or Not to Be the Hand of Hyrstmill | 839 | the Hand of Hyrstmill | the Hand of Hyrstmill |
| 1172 | To Be or Not to Be the Hand of the Golden Bazaar | 840 | the Hand of the Golden Bazaar | the Hand of the Golden Bazaar |
| 1173 | A Slave to Faction III | 807 | Peacemaker | Peacemaker |
| 1174 | Serving a Greater Cause VI | 808 | the Last Resort | the Last Resort |
| 1175 | And All I Got Was This Lousy Achievement: La Noscea | 809 | the Sword of La Noscea | the Sword of La Noscea |
| 1176 | And All I Got Was This Lousy Achievement: Black Shroud | 810 | the Sword of the Shroud | the Sword of the Shroud |
| 1177 | And All I Got Was This Lousy Achievement: Thanalan | 811 | the Sword of Thanalan | the Sword of Thanalan |
| 1178 | Globetrotter | 812 | the Sword of Eorzea | the Sword of Eorzea |
| 1179 | La Noscea Got Served...and Protected | 813 | the Shield of La Noscea | the Shield of La Noscea |
| 1180 | The Black Shroud Got Served...and Protected | 814 | the Shield of the Shroud | the Shield of the Shroud |
| 1181 | Thanalan Got Served...and Protected | 815 | the Shield of Thanalan | the Shield of Thanalan |
| 1182 | Eorzea Got Served...and Protected | 816 | the Shield of Eorzea | the Shield of Eorzea |
| 1183 | Love Thy Brother | 817 | Brother of the Broken Blade | Sister of the Broken Blade |
| 1184 | Another Brick in the Shield Wall | 818 | the Warden's Wall | the Warden's Wall |
| 1185 | A Helping Horn | 819 | Bearer of the Horn | Bearer of the Horn |
| 1186 | Commitment Issues | 820 | the Uncommitted | the Uncommitted |
| 1187 | Career Opportunities | 825 | the Professional | the Professional |
| 1188 | Sideways | 804 | Sidestepper | Sidestepper |
| 1189 | All the More Region to Leve VI | 805 | Lord Protector | Lady Protector |
| 1190 | Think Global, Quest Local VI | 806 | Lord Creator | Lady Creator |
| 1191 | Tales of War | 800 | Seeker of Blood | Seeker of Blood |
| 1192 | Tales of Magic | 801 | Seeker of Truth | Seeker of Truth |
| 1193 | Tales of the Hand | 802 | Seeker of Skill | Seeker of Skill |
| 1194 | Tales of the Land | 803 | Seeker of Bounty | Seeker of Bounty |
| 1201 | It's Reining Deer | 905 | Wild Thing | Wild Thing |
| 1206 | Get All the Things! | 906 | the Winter Wyrm | the Winter Wyrm |
| 1210 | Love Makes the World Go Round | 907 | Messenger of Love | Messenger of Love |
| 1211 | Royal Audience | 908 | Royal Seneschal | Princess for a Day |
| 1217 | Seven Short of a Dozen | 909 | Dreamseeker | Dreamseeker |
| 1225 | Cascadier for Life | 910 | Cascadier | Cascadier |
| 1226 | Chock-full of Elemental Goodness | 911 | Crystal Bearer | Crystal Bearer |
| 1281 | It's Reining Deer | 905 | Wild Thing | Wild Thing |
| 1282 | Get All the Things! | 906 | the Winter Wyrm | the Winter Wyrm |
| 1283 | Love Makes the World Go Round | 907 | Messenger of Love | Messenger of Love |
| 1284 | Royal Audience | 908 | Royal Seneschal | Princess for a Day |
| 1285 | Seven Short of a Dozen | 909 | Dreamseeker | Dreamseeker |
| 1286 | Cascadier for Life | 910 | Cascadier | Cascadier |
| 1287 | Chock-full of Elemental Goodness | 911 | Crystal Bearer | Crystal Bearer |
| 1406 | Been There, Done That | 1100 | the Wanderer's Shadow | the Wanderer's Shadow |
| 1499 | Been There, Done That | 1100 | the Wanderer's Shadow | the Wanderer's Shadow |
| 1506 | A Storm of Seals III | 1000 | Stormlord | Stormlady |
| 1510 | A Snake in the Brass III | 1001 | Serpentlord | Serpentlady |
| 1514 | Burning a Hole in My Pocket III | 1002 | Flamelord | Flamelady |
| 1518 | In Good Company: Maelstrom III | 1003 | the Stormsworn | the Stormsworn |
| 1522 | In Good Company: Twin Adder III | 1004 | the Serpentsworn | the Serpentsworn |
| 1526 | In Good Company: Immortal Flames III | 1005 | the Flamesworn | the Flamesworn |
| 1530 | Fueling the Storm III | 1006 | Stormcarrier | Stormcarrier |
| 1534 | Feeding the Serpent III | 1007 | Serpentcarrier | Serpentcarrier |
| 1538 | Fanning the Flames III | 1008 | Flamecarrier | Flamecarrier |
| 1542 | To Each According to His Need: Maelstrom III | 1009 | Stormbringer | Stormbringer |
| 1546 | To Each According to His Need: Twin Adder III | 1010 | Serpentbringer | Serpentbringer |
| 1550 | To Each According to His Need: Immortal Flames III | 1011 | Flamebringer | Flamebringer |
| 1554 | Eight Minutes or Less or Your Cargo's Free | 1012 | Featherfoot | Featherfoot |
| 1557 | Gone in Eight Minutes | 1014 | Lightning | Lightning |
| 1561 | Handle with Care IV | 1013 | A Bo's Best Friend | A Bo's Best Friend |
| 1565 | Pimp Your Ride | 1015 | Cavalier | Cavalier |
| 1671 | A Storm of Seals III | 1000 | Stormlord | Stormlady |
| 1673 | A Snake in the Brass III | 1001 | Serpentlord | Serpentlady |
| 1675 | Burning a Hole in My Pocket III | 1002 | Flamelord | Flamelady |
| 1677 | In Good Company: Maelstrom III | 1003 | the Stormsworn | the Stormsworn |
| 1679 | In Good Company: Twin Adder III | 1004 | the Serpentsworn | the Serpentsworn |
| 1681 | In Good Company: Immortal Flames III | 1005 | the Flamesworn | the Flamesworn |
| 1683 | Fueling the Storm III | 1006 | Stormcarrier | Stormcarrier |
| 1685 | Feeding the Serpent III | 1007 | Serpentcarrier | Serpentcarrier |
| 1687 | Fanning the Flames III | 1008 | Flamecarrier | Flamecarrier |
| 1689 | To Each According to His Need: Maelstrom III | 1009 | Stormbringer | Stormbringer |
| 1691 | To Each According to His Need: Twin Adder III | 1010 | Serpentbringer | Serpentbringer |
| 1693 | To Each According to His Need: Immortal Flames III | 1011 | Flamebringer | Flamebringer |
| 1695 | Eight Minutes or Less or Your Cargo's Free | 1012 | Featherfoot | Featherfoot |
| 1696 | Gone in Eight Minutes | 1014 | Lightning | Lightning |
| 1697 | Handle with Care IV | 1013 | A Bo's Best Friend | A Bo's Best Friend |
| 1699 | Pimp Your Ride | 1015 | Cavalier | Cavalier |
| 2001 | Patricide | 826 | Inquisitor | Inquisitor |
| 2006 | To Kill a Mocking Bird | 827 | Divine Crusher | Divine Crusher |
| 2011 | Pounding the Spike | 828 | Stonesplitter | Stonesplitter |
| 2020 | First Blood: Aleport | 829 | A Kobold's Worst Nightmare | A Kobold's Worst Nightmare |
| 2025 | First Blood: Hyrstmill | 830 | An Ixal's Worst Nightmare | An Ixal's Worst Nightmare |
| 2030 | First Blood: Golden Bazaar | 831 | An Amalj'aa's Worst Nightmare | An Amalj'aa's Worst Nightmare |
| 2035 | To Be or Not to Be the Guardian of Aleport | 832 | the Guardian of Aleport | the Guardian of Aleport |
| 2040 | To Be or Not to Be the Guardian of Hyrstmill | 833 | the Guardian of Hyrstmill | the Guardian of Hyrstmill |
| 2045 | To Be or Not to Be the Guardian of the Golden Bazaar | 834 | the Guardian of the Golden Bazaar | the Guardian of the Golden Bazaar |
| 2050 | To Be or Not to Be the Wind of Aleport | 835 | the Wind of Aleport | the Wind of Aleport |
| 2055 | To Be or Not to Be the Wind of Hyrstmill | 836 | the Wind of Hyrstmill | the Wind of Hyrstmill |
| 2060 | To Be or Not to Be the Wind of the Golden Bazaar | 837 | the Wind of the Golden Bazaar | the Wind of the Golden Bazaar |
| 2065 | To Be or Not to Be the Hand of Aleport | 838 | the Hand of Aleport | the Hand of Aleport |
| 2070 | To Be or Not to Be the Hand of Hyrstmill | 839 | the Hand of Hyrstmill | the Hand of Hyrstmill |
| 2075 | To Be or Not to Be the Hand of the Golden Bazaar | 840 | the Hand of the Golden Bazaar | the Hand of the Golden Bazaar |

## Native completion and availability boundaries

The canonical native mappings remain in:

- [`xivl-decomp:config/achievement_title_map.json`](https://github.com/XIVLegacy/xivl-decomp/blob/69b6945b3f172c547d8c1bcbc8bdc64dc52ef579/config/achievement_title_map.json), all title-linked achievement IDs, own completion ordinals, available-title admission and independently checked predicate-parent joins.
- [`xivl-decomp:config/achievement_completion_ordinals.json`](https://github.com/XIVLegacy/xivl-decomp/blob/69b6945b3f172c547d8c1bcbc8bdc64dc52ef579/config/achievement_completion_ordinals.json), the complete achievement completion catalog.
- [`xivl-decomp:docs/script/player-achievement-titles.md`, Complete title-linked achievement map](https://github.com/XIVLegacy/xivl-decomp/blob/69b6945b3f172c547d8c1bcbc8bdc64dc52ef579/docs/script/player-achievement-titles.md#complete-title-linked-achievement-map), the native evidence and interpretation.

This static name join does not establish server award criteria, historical
availability, completion ordinals from sheet order, or an ordering by name.
The title key alone does not establish available-title admission.
