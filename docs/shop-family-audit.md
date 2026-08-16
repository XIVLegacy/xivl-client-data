# Shop-family implementation audit

Audit date: 2026-08-15. Corpus: extraction `2012.09.19.0001`, game
version `1.23b`. The retail generic-shop catalog is
`derived/shop_catalog.csv`, generated from the inclusive
`shopBase.csv -> shopItem.csv` range join documented in
`docs/shop-catalogs.md`.

## Verdicts

### Regular and guild shop membership - confirmed

The supplied hardcoded range table has all 239 nonzero retail shop ids. Every
start and end key matches `shopBase.csv`, with no missing, extra, or changed
range. Expanding both sides therefore gives 1,804/1,804 matching shop-to-item
associations. This includes the deliberate overlap in which shops 4001 and
4002 both own rows 1064001 through 1064011.

The guild path selects packs from the same range table. Its pack ids 120
through 144 therefore use the confirmed retail memberships. The localized
`populaceGuildShop.csv` and `populaceShopSalesman.csv` sheets remain dialogue
only and do not own inventory rows.

### Regular and guild shop buy prices - corrected

The supplied implementation prices purchases with each item's SQL
`sell_price`. That field is not the retail shop price. Across the 239 shops,
0/1,804 SQL `sell_price` values equal `shopItem.csv` column 2. Every shop is a
price mismatch. The corrected buy price for every association is the `price`
column in `derived/shop_catalog.csv`.

Representative corrections show the scale and direction of the mismatch:

| Shop | Item | Retail buy price | SQL `sell_price` |
|---:|---:|---:|---:|
| 101 | 13000001 | 6000 | 0 |
| 120 | 10100001 | 2000 | 36 |
| 1001 | 3011106 | 67 | 14 |
| 5001 | 4030010 | 600 | 0 |
| 5123 | 1000018 | 21000 | 168 |

The retail item id is `shopItem.csv` column 0. The selected shop row key is
not an item id and must first be resolved through the catalog. This audit does
not assign a retail resale price: `shopItem.csv` column 2 is the shop's buy
price, not evidence for what an NPC pays the player.

### Black market and materia service - outside this join

The black-market table is not keyed by the generic `shopBase` ranges, so the
generic client-data join cannot confirm its hardcoded items or its two
currency prices. `populaceShopMateriaRemover.csv` is localized service
dialogue and has no item catalog. Neither surface is evidence-cleared by the
1,804-row result.

### Chocobo rental fee - not confirmed

`populaceChocoboLender.csv` has five string columns. Its dialogue contains
runtime number macros for a fee and duration, but no numeric fee field.
`shopBase.csv` has only two labeled numeric columns after the row id: the
inclusive start and end keys of a `shopItem` range. It has no row or column
that owns a chocobo rental fee, and no field equal to 800. Occurrences of the
digits `800` inside range keys such as 1008001 are not fee evidence.

The retail client-data corpus therefore neither confirms 800 gil nor supports
a corrected fee. The hardcoded 800-gil value remains unevidenced pending a
labeled numeric source outside these sheets.

## Per-shop counts

Each entry is `shop id: matching memberships/retail memberships, matching
prices/retail prices`.

```text
101:10/10,0/10 102:10/10,0/10 103:10/10,0/10 104:10/10,0/10 105:10/10,0/10 106:10/10,0/10 107:10/10,0/10 108:17/17,0/17
109:15/15,0/15 110:18/18,0/18 111:18/18,0/18 112:18/18,0/18 113:19/19,0/19 114:15/15,0/15 115:15/15,0/15 116:10/10,0/10
117:10/10,0/10 118:10/10,0/10 120:12/12,0/12 121:12/12,0/12 122:12/12,0/12 123:12/12,0/12 124:12/12,0/12 125:12/12,0/12
126:12/12,0/12 127:12/12,0/12 128:12/12,0/12 129:16/16,0/16 130:12/12,0/12 131:12/12,0/12 132:12/12,0/12 133:12/12,0/12
134:16/16,0/16 135:12/12,0/12 136:12/12,0/12 137:12/12,0/12 138:12/12,0/12 139:12/12,0/12 140:12/12,0/12 141:12/12,0/12
142:12/12,0/12 143:16/16,0/16 144:18/18,0/18 145:2/2,0/2 146:6/6,0/6
1001:8/8,0/8 1002:8/8,0/8 1003:7/7,0/7 1004:2/2,0/2 1005:17/17,0/17 1006:6/6,0/6 1007:10/10,0/10 1008:9/9,0/9
1009:12/12,0/12 1010:14/14,0/14 1011:10/10,0/10 1012:7/7,0/7 1013:11/11,0/11 1014:6/6,0/6 1015:7/7,0/7 1016:16/16,0/16
1017:10/10,0/10 1018:13/13,0/13 1019:5/5,0/5 1020:4/4,0/4 1021:5/5,0/5
2001:8/8,0/8 2002:6/6,0/6 2003:7/7,0/7 2004:8/8,0/8 2005:3/3,0/3 2006:8/8,0/8 2007:6/6,0/6 2008:4/4,0/4
2009:16/16,0/16 2010:9/9,0/9 2011:8/8,0/8 2012:10/10,0/10 2013:10/10,0/10 2014:12/12,0/12 2015:15/15,0/15 2016:13/13,0/13
2017:6/6,0/6 2018:6/6,0/6 2019:8/8,0/8 2020:9/9,0/9 2021:10/10,0/10 2022:5/5,0/5 2023:6/6,0/6 2024:6/6,0/6
3001:8/8,0/8 3002:8/8,0/8 3003:8/8,0/8 3004:8/8,0/8 3005:10/10,0/10 3006:8/8,0/8 3007:6/6,0/6 3008:16/16,0/16
3009:13/13,0/13 3010:8/8,0/8 3011:9/9,0/9 3012:10/10,0/10 3013:6/6,0/6 3014:13/13,0/13 3015:5/5,0/5 3016:8/8,0/8
3017:11/11,0/11 3018:7/7,0/7 3019:11/11,0/11 3020:14/14,0/14 3021:16/16,0/16 3022:4/4,0/4 3023:8/8,0/8 3024:4/4,0/4
4001:11/11,0/11 4002:11/11,0/11
5001:18/18,0/18 5002:6/6,0/6 5003:10/10,0/10 5004:9/9,0/9 5005:10/10,0/10 5006:12/12,0/12 5007:10/10,0/10 5008:16/16,0/16
5009:7/7,0/7 5010:4/4,0/4 5011:4/4,0/4 5012:4/4,0/4 5013:4/4,0/4 5014:4/4,0/4 5015:4/4,0/4 5016:4/4,0/4
5017:4/4,0/4 5018:4/4,0/4 5019:4/4,0/4 5020:4/4,0/4 5021:4/4,0/4 5022:4/4,0/4 5023:4/4,0/4 5024:4/4,0/4
5025:4/4,0/4 5026:4/4,0/4 5027:7/7,0/7 5028:4/4,0/4 5029:4/4,0/4 5030:4/4,0/4 5031:4/4,0/4 5032:4/4,0/4
5033:4/4,0/4 5034:4/4,0/4 5035:4/4,0/4 5036:4/4,0/4 5037:4/4,0/4 5038:4/4,0/4 5039:7/7,0/7 5040:4/4,0/4
5041:4/4,0/4 5042:4/4,0/4 5043:4/4,0/4 5044:4/4,0/4 5045:7/7,0/7 5046:4/4,0/4 5047:4/4,0/4 5048:4/4,0/4
5049:4/4,0/4 5050:4/4,0/4 5051:6/6,0/6 5052:4/4,0/4 5053:4/4,0/4 5054:4/4,0/4 5055:4/4,0/4 5056:4/4,0/4
5057:6/6,0/6 5058:4/4,0/4 5059:4/4,0/4 5060:4/4,0/4 5061:4/4,0/4 5062:4/4,0/4 5063:6/6,0/6 5064:4/4,0/4
5065:4/4,0/4 5066:4/4,0/4 5067:4/4,0/4 5068:4/4,0/4 5069:6/6,0/6 5070:4/4,0/4 5071:4/4,0/4 5072:4/4,0/4
5073:4/4,0/4 5074:4/4,0/4 5075:6/6,0/6 5076:4/4,0/4 5077:4/4,0/4 5078:4/4,0/4 5079:4/4,0/4 5080:4/4,0/4
5081:6/6,0/6 5082:4/4,0/4 5083:4/4,0/4 5084:4/4,0/4 5085:4/4,0/4 5086:4/4,0/4 5087:6/6,0/6 5088:4/4,0/4
5089:4/4,0/4 5090:4/4,0/4 5091:4/4,0/4 5092:4/4,0/4 5093:6/6,0/6 5094:4/4,0/4 5095:4/4,0/4 5096:4/4,0/4
5097:4/4,0/4 5098:4/4,0/4 5099:6/6,0/6 5100:4/4,0/4 5101:4/4,0/4 5102:4/4,0/4 5103:4/4,0/4 5104:4/4,0/4
5105:6/6,0/6 5106:4/4,0/4 5107:4/4,0/4 5108:4/4,0/4 5109:4/4,0/4 5110:4/4,0/4 5111:6/6,0/6 5112:4/4,0/4
5113:4/4,0/4 5114:4/4,0/4 5115:4/4,0/4 5116:4/4,0/4 5117:6/6,0/6 5118:8/8,0/8 5119:8/8,0/8 5120:8/8,0/8
5121:8/8,0/8 5122:10/10,0/10 5123:11/11,0/11
```

## Evidence boundary

The catalog values and counts are client-extraction facts pinned by
`manifests/shop_catalogs.json`. The implementation comparison is a bounded
audit of the supplied hardcoded tables and SQL price field. It does not make
the external implementation an evidence authority. Regenerate the retail
catalog with `python tools/build_shop_catalogs.py` and verify it without
writing with `python tools/build_shop_catalogs.py --check`.
