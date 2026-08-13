# Retail inventory cross-check

This cross-check compares the 1.23b retail server inventory packet emissions
captured in `data/vendor/captures/content_samples.json` with the client-side
item catalog under `csv/`.

Retail evidence: 0x0148 / 0x0149 / 0x014A inventory packets parsed
from 53 captures, yielding 481 item observations across 69 distinct
itemIds. The English Title (`xtx_itemName.csv` col 5) and the
internal category path (`_item.csv` col 0) come from the same
row_id that the server placed in the wire packet, confirming the
client CSVs are the correct lookup index for retail itemIds.

## Summary

- Retail observations: **481** across **53** captures
- Distinct retail itemIds: **69**
- Matched in `_item.csv`: **69** / 69
- Matched in `xtx_itemName.csv`: **69** / 69
- Matched in `itemData.csv`: **69** / 69
- Fully matched in all three sources: **69** / 69
- Partial match (1-2 sources): **0**
- Missing everywhere: **0**

## Top 10 retail items by frequency

| itemId | hex | retail count | captures | English Title | category | sample qty |
|---:|---|---:|---:|---|---|---:|
| 1000001 | `0x000f4241` | 22 | 13 | Gil | `Money/MoneyStandard` | 1346698 |
| 1000006 | `0x000f4246` | 14 | 11 | Earth Shard | `Money/MoneyStandard` | 1685 |
| 1000004 | `0x000f4244` | 13 | 10 | Ice Shard | `Money/MoneyStandard` | 1424 |
| 1000005 | `0x000f4245` | 13 | 9 | Wind Shard | `Money/MoneyStandard` | 1635 |
| 1000010 | `0x000f424a` | 13 | 9 | Ice Crystal | `Money/MoneyStandard` | 142 |
| 1000003 | `0x000f4243` | 12 | 9 | Fire Shard | `Money/MoneyStandard` | 1532 |
| 10009206 | `0x0098ba76` | 12 | 9 | Growth Formula Alpha | `Normal/StandardItem` | 1 |
| 1000008 | `0x000f4248` | 12 | 9 | Water Shard | `Money/MoneyStandard` | 1384 |
| 1000013 | `0x000f424d` | 12 | 9 | Lightning Crystal | `Money/MoneyStandard` | 128 |
| 10007507 | `0x0098b3d3` | 11 | 8 | Mole Sinew | `Normal/StandardItem` | 5 |

## Full ledger (all 69 retail itemIds)

| itemId | hex | retail count | captures | match | English Title | category | maxStack |
|---:|---|---:|---:|---|---|---|---:|
| 1000001 | `0x000f4241` | 22 | 13 | matched (item,name,data) | Gil | `Money/MoneyStandard` | 999999999 |
| 1000006 | `0x000f4246` | 14 | 11 | matched (item,name,data) | Earth Shard | `Money/MoneyStandard` | 9999 |
| 1000004 | `0x000f4244` | 13 | 10 | matched (item,name,data) | Ice Shard | `Money/MoneyStandard` | 9999 |
| 1000005 | `0x000f4245` | 13 | 9 | matched (item,name,data) | Wind Shard | `Money/MoneyStandard` | 9999 |
| 1000010 | `0x000f424a` | 13 | 9 | matched (item,name,data) | Ice Crystal | `Money/MoneyStandard` | 9999 |
| 1000003 | `0x000f4243` | 12 | 9 | matched (item,name,data) | Fire Shard | `Money/MoneyStandard` | 9999 |
| 10009206 | `0x0098ba76` | 12 | 9 | matched (item,name,data) | Growth Formula Alpha | `Normal/StandardItem` | 99 |
| 1000008 | `0x000f4248` | 12 | 9 | matched (item,name,data) | Water Shard | `Money/MoneyStandard` | 9999 |
| 1000013 | `0x000f424d` | 12 | 9 | matched (item,name,data) | Lightning Crystal | `Money/MoneyStandard` | 9999 |
| 10007507 | `0x0098b3d3` | 11 | 8 | matched (item,name,data) | Mole Sinew | `Normal/StandardItem` | 99 |
| 10009102 | `0x0098ba0e` | 11 | 8 | matched (item,name,data) | Silex | `Normal/StandardItem` | 99 |
| 10009505 | `0x0098bba1` | 11 | 8 | matched (item,name,data) | Puk Wing | `Normal/StandardItem` | 99 |
| 10009507 | `0x0098bba3` | 11 | 8 | matched (item,name,data) | Imp Wing | `Normal/StandardItem` | 99 |
| 10013001 | `0x0098c949` | 11 | 8 | matched (item,name,data) | Grade 1 Dark Matter | `Normal/StandardItem` | 99 |
| 10013002 | `0x0098c94a` | 11 | 8 | matched (item,name,data) | Grade 2 Dark Matter | `Normal/StandardItem` | 99 |
| 10013003 | `0x0098c94b` | 11 | 8 | matched (item,name,data) | Grade 3 Dark Matter | `Normal/StandardItem` | 99 |
| 1000007 | `0x000f4247` | 11 | 8 | matched (item,name,data) | Lightning Shard | `Money/MoneyStandard` | 9999 |
| 1000009 | `0x000f4249` | 11 | 8 | matched (item,name,data) | Fire Crystal | `Money/MoneyStandard` | 9999 |
| 1000011 | `0x000f424b` | 11 | 8 | matched (item,name,data) | Wind Crystal | `Money/MoneyStandard` | 9999 |
| 1000012 | `0x000f424c` | 11 | 8 | matched (item,name,data) | Earth Crystal | `Money/MoneyStandard` | 9999 |
| 1000014 | `0x000f424e` | 11 | 8 | matched (item,name,data) | Water Crystal | `Money/MoneyStandard` | 9999 |
| 1000015 | `0x000f424f` | 11 | 8 | matched (item,name,data) | Fire Cluster | `Money/MoneyStandard` | 9999 |
| 1000016 | `0x000f4250` | 11 | 8 | matched (item,name,data) | Ice Cluster | `Money/MoneyStandard` | 9999 |
| 1000017 | `0x000f4251` | 11 | 8 | matched (item,name,data) | Wind Cluster | `Money/MoneyStandard` | 9999 |
| 1000018 | `0x000f4252` | 11 | 8 | matched (item,name,data) | Earth Cluster | `Money/MoneyStandard` | 9999 |
| 1000019 | `0x000f4253` | 11 | 8 | matched (item,name,data) | Lightning Cluster | `Money/MoneyStandard` | 9999 |
| 1000020 | `0x000f4254` | 11 | 8 | matched (item,name,data) | Water Cluster | `Money/MoneyStandard` | 9999 |
| 1000201 | `0x000f4309` | 11 | 8 | matched (item,name,data) | Storm Seal | `Money/MoneyStandard` | 999999 |
| 1000202 | `0x000f430a` | 11 | 8 | matched (item,name,data) | Serpent Seal | `Money/MoneyStandard` | 999999 |
| 1000203 | `0x000f430b` | 11 | 8 | matched (item,name,data) | Flame Seal | `Money/MoneyStandard` | 999999 |
| 2000201 | `0x001e8549` | 11 | 8 | matched (item,name,data) | Soul of the Paladin | `Important/ImportantItemStandard` | 1 |
| 2000202 | `0x001e854a` | 11 | 8 | matched (item,name,data) | Soul of the Monk | `Important/ImportantItemStandard` | 1 |
| 2000205 | `0x001e854d` | 11 | 8 | matched (item,name,data) | Soul of the Bard | `Important/ImportantItemStandard` | 1 |
| 2000206 | `0x001e854e` | 11 | 8 | matched (item,name,data) | Soul of the White Mage | `Important/ImportantItemStandard` | 1 |
| 2000207 | `0x001e854f` | 11 | 8 | matched (item,name,data) | Soul of the Black Mage | `Important/ImportantItemStandard` | 1 |
| 2001005 | `0x001e886d` | 11 | 8 | matched (item,name,data) | Serpent Chocobo Issuance | `Important/ImportantItemStandard` | 1 |
| 2001007 | `0x001e886f` | 11 | 8 | matched (item,name,data) | Chocobo Whistle | `Important/ImportantItemStandard` | 1 |
| 10009211 | `0x0098ba7b` | 5 | 1 | matched (item,name,data) | Formic Acid | `Normal/StandardItem` | 99 |
| 10007504 | `0x0098b3d0` | 4 | 2 | matched (item,name,data) | Antelope Sinew | `Normal/StandardItem` | 99 |
| 3011006 | `0x002df1be` | 3 | 2 | matched (item,name,data) | Antelope Shank | `Normal/FoodItem` | 99 |
| 8011608 | `0x007a3f58` | 2 | 2 | matched (item,name,data) | Steel Sallet (Green) | `Normal/StandardItem` | 1 |
| 6060006 | `0x005c77e6` | 2 | 2 | matched (item,name,data) | Rusty Needle | `Normal/ToolItem` | 1 |
| 3011307 | `0x002df2eb` | 2 | 2 | matched (item,name,data) | Popoto | `Normal/FoodItem` | 99 |
| 4030013 | `0x003d7e3d` | 2 | 2 | matched (item,name,data) | Blunt Goblin Gladius | `Normal/StandardItem` | 1 |
| 4040405 | `0x003da6d5` | 2 | 2 | matched (item,name,data) | Iron Bill | `Normal/StandardItem` | 1 |
| 10005202 | `0x0098aad2` | 2 | 1 | matched (item,name,data) | Moko Grass | `Normal/StandardItem` | 99 |
| 10007016 | `0x0098b1e8` | 2 | 2 | matched (item,name,data) | Aldgoat Skin | `Normal/StandardItem` | 99 |
| 8050611 | `0x007ad7b3` | 2 | 2 | matched (item,name,data) | Cotton Kecks | `Normal/StandardItem` | 1 |
| 8080819 | `0x007b4db3` | 2 | 2 | matched (item,name,data) | Iron-plated Jackboots | `Normal/StandardItem` | 1 |
| 4100604 | `0x003e91fc` | 1 | 1 | matched (item,name,data) | Square Maple Shield | `Normal/ShieldItem` | 1 |
| 8030423 | `0x007a88d7` | 1 | 1 | matched (item,name,data) | Cotton Dalmatica | `Normal/StandardItem` | 1 |
| 8031609 | `0x007a8d79` | 1 | 1 | matched (item,name,data) | Iron Scale Mail | `Normal/StandardItem` | 1 |
| 8011108 | `0x007a3d64` | 1 | 1 | matched (item,name,data) | Steel Barbut | `Normal/StandardItem` | 1 |
| 7020002 | `0x006b1de2` | 1 | 1 | matched (item,name,data) | Weathered Hatchet | `Normal/ToolItem` | 1 |
| 7020108 | `0x006b1e4c` | 1 | 1 | matched (item,name,data) | Weathered Scythe | `Normal/ToolItem` | 1 |
| 10009610 | `0x0098bc0a` | 1 | 1 | matched (item,name,data) | Tinolqa Mistletoe | `Normal/StandardItem` | 99 |
| 8032501 | `0x007a90f5` | 1 | 1 | matched (item,name,data) | Hempen Kurta | `Normal/StandardItem` | 1 |
| 10006111 | `0x0098ae5f` | 1 | 1 | matched (item,name,data) | Scallop Shell | `Normal/StandardItem` | 99 |
| 4080008 | `0x003e4188` | 1 | 1 | matched (item,name,data) | Feathered Harpoon | `Normal/StandardItem` | 1 |
| 5030006 | `0x004cc076` | 1 | 1 | matched (item,name,data) | Budding Maple Wand | `Normal/StandardItem` | 1 |
| 8011404 | `0x007a3e8c` | 1 | 1 | matched (item,name,data) | Iron Elmo | `Normal/StandardItem` | 1 |
| 10007013 | `0x0098b1e5` | 1 | 1 | matched (item,name,data) | Dormouse Pelt | `Normal/StandardItem` | 99 |
| 8030920 | `0x007a8ac8` | 1 | 1 | matched (item,name,data) | Leather Jacket | `Normal/StandardItem` | 1 |
| 8070218 | `0x007b244a` | 1 | 1 | matched (item,name,data) | Iron Vambraces | `Normal/StandardItem` | 1 |
| 8090608 | `0x007b73f0` | 1 | 1 | matched (item,name,data) | Plundered Leather Belt | `Normal/StandardItem` | 1 |
| 9050052 | `0x008a17c4` | 1 | 1 | matched (item,name,data) | Bone Ring | `Normal/StandardItem` | 1 |
| 3011302 | `0x002df2e6` | 1 | 1 | matched (item,name,data) | Ogre Pumpkin | `Normal/FoodItem` | 99 |
| 3020410 | `0x002e167a` | 1 | 1 | matched (item,name,data) | The Keeper's Hymn | `Normal/CmnGoodStatusItem` | 99 |
| 2000203 | `0x001e854b` | 1 | 1 | matched (item,name,data) | Soul of the Warrior | `Important/ImportantItemStandard` | 1 |

## What this confirms

- The client item catalog at `csv/_item.csv`, `csv/xtx_itemName.csv`,
  and `csv/itemData.csv` is the correct lookup index for retail
  itemIds emitted by the 1.23b server. Match rates are reported above.
- Items in the 1000001-1000020 range are currency tokens (Gil, Crystal,
  elemental shards). The retail item seen most often is
  `1000001` (Gil), observed in 13 of 53 captures.
- This validates the inventory packet parser in
  https://github.com/XIVLegacy/xivl-captures/blob/main/tools/extractors/extract_content_samples.py
  and the 112-byte `InventoryItem` layout it relies on.

## Regenerating

```
python tools/retail_inventory_crosscheck.py
```

Input paths can be overridden with `--content`, `--csv-dir`, `--out`.
