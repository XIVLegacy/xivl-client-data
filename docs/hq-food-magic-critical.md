# Food magic-critical potency and quality

The retail client consumption-detail helper predicts a fixed magic-critical
potency value of `5` for Dried Prunes and Pearl Chocolate at normalized main
quality 1, and `6` when normalized main quality is greater than 1. This is a
dedicated food/consumable display calculation. The extraction does not close
the mapping from those quality states to observed NQ/HQ food or prove the
stat change applied by the server.

## Food and parameter joins

Extraction `2012.09.19.0001` supplies both items. Column numbers below use the
numeric sheet header after the CSV row ID.

| Item row | `xtx_itemName` column 5 (`str`) | `_item` column 0 (`str`) |
|---|---|---|
| 3010403 | `Dried Prunes` | `Normal/FoodItem` |
| 3010413 | `Pearl Chocolate` | `Normal/FoodItem` |

Both matching `csv/equipment.csv` rows contain these exact fields:

| Column | Type | Value | Consumption-helper role |
|---|---|---:|---|
| 78 | `s16` | 10 | Quality adjustment divided by 100. |
| 81 | `s32` | 15038 | Second consumption parameter ID. |
| 82 | `s16` | 5 | Second consumption parameter value. |
| 88 | `s16` | 0 | Second consumption parameter limit. |

`csv/xtx_text_paramName.csv` row 15038, column 1 (`str`), is
`Magic Critical Hit Potency`. Row 15036 is the separate
`Magic Critical Hit Rating` label. This finding concerns potency, not the
probability of landing a critical spell. The unoffset ID 15038 also follows
the ordinary-unit branch of `DesktopWidget.getParameterUnit` at
`xivl-client-scripts:lua/scripts/widget/desktopwidget_itemdetail.lua:2550-2565`;
the helper reserves the million-offset IDs for a different unit code.

## Dedicated consumption calculation

`ItemBaseClass.getItemConsumptionBonus` at
`xivl-client-scripts:lua/scripts/item/itembaseclass_common.lua:1795-1919`
reads three parameter IDs and values from column pairs 79/80, 81/82 and 83/84,
and their limits from columns 86, 88 and 90. An ID of -1 skips a pair.
For normalized main quality greater than 1, it uses:

```text
multiplier = 1 + equipment.column78 / 100
positive value or limit -> ceil(value * multiplier - 0.0001)
negative value or limit -> floor(value * multiplier + 0.0001)
zero -> zero
```

The quality branch is at lines 1837-1849, value rounding at 1850-1868 and
limit rounding at 1871-1889. For both selected food rows, the second tuple is
therefore `(15038, 5, 0)` at normalized main quality 1 and `(15038, 6, 0)`
above 1: `ceil(5 * 1.1 - 0.0001) = 6`. The cap stays zero. This result comes
from the consumed-food parameter pair and its own adjustment column, without
using the weapon/armor HQ helper.

`getMainQuality` at the same script's lines 3437-3454 delegates to the
synchronized getter in `item/normal/normalitembaseclass_common.lua:625-637`,
which returns `normalItemWork.mainQuality` with stored zero normalized to 1.
`FoodItem` inherits the item helpers and its
level-adjustment overrides at `item/normal/fooditem.lua:21-90` return zero;
the selected consumption helper itself performs no actor-level lookup.

The item-detail route calls the helper and forwards its arrays to
`fpParamKind`, `fpParamValue` and `fpParamLimit` properties at
`widget/desktopwidget_itemdetail.lua:1258-1359`, with another route at
8730-8837. Those consumers establish client detail values, not status mutation.

## NQ/HQ and applied-effect boundary

The missing runtime join is an identified retail food instance whose NQ/HQ
presentation is correlated with synchronized main quality and the selected
consumption tuple. The recovered quality comparison alone does not prove
that a historical HQ item had that stored quality state.

`csv/xtx_status.csv` row 223999, column 3 (`str`), names `Well Fed`. Neither
that name nor the selected helper supplies an item/quality-to-status-instance
join, status power assignment, or authoritative applied-stat calculation.
The server's actual increment, any level scaling or cap, rounding order and
stacking with other effects remain unestablished. A client detail prediction
of 6 is not an observed applied increase of 6.

An attributable historical comparison would need the same food ID in NQ and
HQ instances, their displayed quality and synchronized state, baseline magic
critical potency, the consumption result and status identity, and the stat
after consumption with gear and other modifiers held fixed. It must preserve
raw values and display resolution to distinguish applied rounding from UI
rounding. New retail acquisition is unavailable; no such experiment was
performed. Secondary food tables do not fill these runtime joins.

## Source identity

Both fixed archives and all their members matched the declarations in
`manifests/private_csv_corpus.json`, `manifests/tables.json`,
`xivl-client-scripts:manifests/private_lua_corpus.json` and
`xivl-client-scripts:manifests/scripts.json`. Selected member SHA-256 values:

| Member | SHA-256 |
|---|---|
| `csv/_item.csv` | `f41dba38473a8a4014826c5b0cd639e12c6652700c9f760660fcb241d7469dda` |
| `csv/equipment.csv` | `acb958ef75422726f84de5a087b5f335ebe148aa5c3c754e7f8b8e26f6084b9b` |
| `csv/xtx_itemName.csv` | `917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2` |
| `csv/xtx_text_paramName.csv` | `aebca8a881055ecf060a03347300a3107294951b8d11f7b0c2eaf5ba4d60c0ba` |
| `csv/xtx_status.csv` | `60eca3b76d1d9799589d9059adeb1e7c3d142e07609a1ad0a053c5e75d9b96ee` |
| `item/itembaseclass_common.lua` | `7620492917230c3e060ed84d3197bf164c234a3ab73e48a0939bc65107f6b7fa` |
| `item/normal/normalitembaseclass_common.lua` | `35a05383355d7205f58ad999710e5eaf92331c899c683873b823aead755645f0` |
| `item/normal/fooditem.lua` | `29dd2fa4a17c5bb9f70711fbe9552a4a9e7da01f0aa10cf43b4b447e37c806e2` |
| `widget/desktopwidget_itemdetail.lua` | `b1e5066fef70d5b7002abcd0fcb5440348f3db46062a8d2f23704957d2cc6dad` |
