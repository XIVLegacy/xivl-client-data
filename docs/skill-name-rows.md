# Skill-name rows

`xtx_text_skillName.csv` has every key from 1 through 52, with a nonblank
English label at logical column 1. These are static sheet keys; they do not
establish that every named skill was playable or populated in runtime state.

| Sheet key | English label |
| ---: | --- |
| 1 | Unarmed |
| 2 | Hand-to-Hand |
| 3 | Sword |
| 4 | Axe |
| 5 | Fencing |
| 6 | Club |
| 7 | Archery |
| 8 | Polearm |
| 9 | Gunnery |
| 10 | Shield |
| 11 | Great Katana |
| 12 | Staff |
| 13 | Dark Arts |
| 14 | Whip |
| 15 | Monk |
| 16 | Paladin |
| 17 | Warrior |
| 18 | Bard |
| 19 | Dragoon |
| 20 | Weapon 20 |
| 21 | Mysticism |
| 22 | Thaumaturgy |
| 23 | Conjury |
| 24 | Arcanima |
| 25 | Musical |
| 26 | Black Mage |
| 27 | White Mage |
| 28 | Magic 8 |
| 29 | Woodworking |
| 30 | Smithing |
| 31 | Armorcraft |
| 32 | Goldsmithing |
| 33 | Leatherworking |
| 34 | Clothcraft |
| 35 | Alchemy |
| 36 | Cooking |
| 37 | Craft 9 |
| 38 | Craft 10 |
| 39 | Mining |
| 40 | Botany |
| 41 | Fishing |
| 42 | Herding |
| 43 | DoL 5 |
| 44 | DoL 6 |
| 45 | Main Hand Weapon |
| 46 | Off Hand Weapon |
| 47 | Two-Handed Weapon |
| 48 | Casting |
| 49 | Shield Defense |
| 50 | Throwing |
| 51 | Evasion |
| 52 | Parrying |

The native declaration independently gives `skillLevel` and `skillLevelCap`
as 52-element integer16 arrays, and `skillPoint` as a 52-element integer32
array. The whole `skillLevel` array has local binding 2001. Those declarations
and bindings belong to `xivl-client-structs:docs/work-binder-native-contract.md`.
Equal counts do not prove an ID-minus-one accessor, runtime nonzero values,
caps or historical availability.

The complete text member SHA-256 is
`170FD51685AB160989DD836C1D67DDF87E95627180CF17AB86DEE271D04AB746`,
recorded in [tables.json](../manifests/tables.json), extraction `2012.09.19.0001`.
