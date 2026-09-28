# Finding: Shop and GC seal catalogs

The Grand Company seal inventory is a complete client sheet, not a text-side
catalog. The generic shop family uses a separate range join from
`shopBase.csv` to `shopItem.csv`. The four `populace*Shop` sheets in this audit
contain localized dialogue only.

- Derived GC table: `derived/gc_seal_shop_catalog.csv`.
- Derived generic table: `derived/shop_catalog.csv`.
- Provenance manifest: `manifests/shop_catalogs.json`.
- Generator: `tools/build_shop_catalogs.py`.
- Source extraction: FFXIV 1.23b, `2012.09.19.0001`.
- Source evidence class: `client_extraction`.

## 1. Fidelity verdicts

The repository manifest pins every source by sha256. The generator also
checks each data-row count against `manifests/tables.json` and rejects any row
whose width differs from the two source header rows.

| Sheet | Inventory source | Rows | Columns | Verdict |
|---|---:|---:|---:|---|
| `gcSealShopItem.csv` | game schema | 402 | 9 | Complete pinned client extraction |
| `populaceCompanyShop.csv` | extrasheets | 140 | 5 strings | Complete pinned client extraction; localized text only |
| `populaceGuildShop.csv` | extrasheets | 129 | 5 strings | Complete pinned client extraction; localized text only |
| `populaceShopMateriaRemover.csv` | extrasheets | 25 | 5 strings | Complete pinned client extraction; localized text only |
| `populaceShopSalesman.csv` | extrasheets | 501 | 5 strings | Complete pinned client extraction; localized text only |
| `shopBase.csv` | game schema | 240 | 2 | Complete pinned client extraction |
| `shopItem.csv` | game schema | 2543 | 3 | Complete pinned client extraction |

No sheet was re-decoded. Re-emitting any file under `csv/` would violate the
immutable corpus contract without a new extraction version.

## 2. GC seal shop mapping

The extracted client function
`xivl-client-scripts:lua/scripts/chara/npc/populace/populacecompanyshop.lua`
reads columns 0 through 4 and 6 at lines 2294-2329. It returns them in that
order at lines 2391-2398. The client widget consumes the return values as the
virtual item, quality, quantity, price, and `essentialRank` at
`xivl-client-scripts:lua/scripts/widget/ask/grandcompanyshopwidget.lua`
lines 832-849 and 923-1055.

| Sheet field | Derived column | Meaning | Example |
|---|---|---|---|
| row id | `shop_row_id` | Company/category-local inventory key | row 100001 |
| col 0 | `item_id` | Item catalog reference | 3010403 |
| col 1 | `item_quality` | Virtual-item quality | 1 |
| col 2 | `item_quantity` | Quantity per purchase | 10 |
| col 3 | `seal_cost` | Price shown by the GC shop widget | 20 |
| col 4 | `rank_requirement` | Widget `essentialRank` value | 0 |
| col 5 | `company_id` | Town/company code | 1 |
| col 6 | `event_flag_requirement` | Availability threshold | 0 |
| col 7 | `reserved_zero` | Unresolved; zero in all 402 rows | 0 |
| col 8 | `item_category` | Category code | 1 |

The source row `gcSealShopItem.csv:3` is
`100001,3010403,1,10,20,0,1,0,0,1`. Rows 100001, 200001, and 300001 carry
company codes 1, 2, and 3. The client script selects the matching key bands
from actor classes 1500202, 1500203, and 1500201 at lines 115-177. Its named
ranges identify category 1 as supplies, 2 as arms, 3 as festival, and 4 as
important items. Representative source rows are 101001 at CSV line 35,
102001 at line 129, and 103001 at line 131.

Column 6 is not merely a descriptive flag. The client compares it with the
shop's current event flag to admit or reject the row at lines 2382-2389.
Column 4 is independently presented as the required rank icon. Both values
must remain raw in a downstream catalog.

Every one of the 328 distinct item ids joins by row id to `_item.csv` and
`itemData.csv`. The derived table also joins `xtx_itemName.csv` on the same id
for the English name. For example, item 3010403 joins `_item.csv:190`,
`itemData.csv:190`, and `xtx_itemName.csv:190`.

## 3. Generic, guild, salesman, and materia-service shape

`shopBase.csv` maps its row id, the shop id, to an inclusive `shopItem.csv`
row-key range. The client reads the two endpoints in
`xivl-client-scripts:lua/scripts/chara/npc/populace/shop/shopbaseclass.lua`
lines 11-36. It then calculates `start + ordinal - 1` and reads `shopItem`
columns 0, 1, and 2 as item id, quality, and price at lines 265-305.

For example, `shopBase.csv:4` maps shop 101 to rows 101001 through 101010.
`shopItem.csv:4` maps row 101001 to item 13000001, quality 1, price 6000.
The range-expanded `derived/shop_catalog.csv` contains 1804 shop-to-item
associations for 239 nonzero shop ranges.

The generic range map is not a partition of every `shopItem` row. There are
750 unowned source rows. Eleven rows, 1064001 through 1064011, belong to both
shop 4001 and shop 4002. The derived table preserves those two associations
rather than selecting one owner. The source rows remain authoritative.

`PopulaceGuildShop` and `PopulaceShopSalesman` both inherit `ShopBaseClass`.
Their matching CSVs are loaded only as localized text at lines 11-20 of their
client scripts, so their inventory uses the generic `shopBase -> shopItem`
shape or event arguments, not the text rows. `PopulaceShopMateriaRemover`
also inherits the base class but its CSV is service dialogue, not an item
catalog.

## 4. Evidence ceilings

- `gcSealShopItem` column 7 has no client getter in the traced path. Its exact
  semantic remains unknown even though its all-zero distribution is proven.
- Raw rank values are proven as widget `essentialRank` values. This finding
  does not assign localized rank names to those numeric values.
- The generic derived table only expands ranges named by `shopBase`. It does
  not claim that unowned `shopItem` rows are unused by every native or event
  path.
- Localized `populace*Shop` rows describe dialogue. They do not establish an
  actor-to-shop-id relation by themselves.

Regenerate with `python tools/build_shop_catalogs.py`. Verify without writing
with `python tools/build_shop_catalogs.py --check`.
