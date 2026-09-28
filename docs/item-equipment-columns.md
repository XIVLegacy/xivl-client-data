# Retail item/equipment column crosswalk

This is the canonical extraction `2012.09.19.0001` crosswalk for the `itemDataSheet` columns used by the promoted client formulas. It joins operational roles from `xivl-client-scripts:docs/equipment-parameter-formulas.md` to the repository-local `itemData.csv` and `equipment.csv` schemas. Column numbers are zero-based. Regenerate or verify it with `python tools/build_item_equipment_crosswalk.py [--check]`.

The canonical sheet inventory identifies `itemData` as game-schema resource `0x01030129`, `equipment` as `0x010300A7`, and the localized parameter-name sheet `xtx/text_paramName` as `0x0B45007B`. The source CSV type rows, rather than inferred runtime widths, supply the stored types below.

## Column census

`Active` means nonblank for untyped columns, neither `0` nor `-1` for scalar columns, and not `-1` for data-shaped ID columns. `Examples` are deterministic `row_id=value` locators, not semantic labels.

| Sheet.column | Consumer role | Stored type | Blank | Zero | -1 | Active | Domain | Examples |
|---|---|---:|---:|---:|---:|---:|---|---|
| `itemData.49` | parameter 1 grow selector | `untyped` | 8403 | 0 | 0 | 0 | blank (8403) | none |
| `itemData.50` | parameter 1 base value | `float` | 0 | 7913 | 0 | 490 | -10..138; 65 distinct; top 0 (7913), 1 (379), 0.2 (7), 0.3 (7) | 4030107=-10, 4100810=138, 1000002=1 |
| `itemData.51` | parameter 1 compatibility adjustment | `untyped` | 8403 | 0 | 0 | 0 | blank (8403) | none |
| `itemData.52` | parameter 2 grow selector | `untyped` | 8403 | 0 | 0 | 0 | blank (8403) | none |
| `itemData.53` | parameter 2 base value | `float` | 0 | 8318 | 0 | 85 | 0..9000; 59 distinct; top 0 (8318), 94 (4), 11 (3), 14 (3) | 4020311=0.3, 3020505=9000, 3020504=9000 |
| `itemData.54` | parameter 2 compatibility adjustment | `untyped` | 8403 | 0 | 0 | 0 | blank (8403) | none |
| `itemData.55` | parameter 3 grow selector | `untyped` | 8403 | 0 | 0 | 0 | blank (8403) | none |
| `itemData.56` | parameter 3 base value | `float` | 0 | 8403 | 0 | 0 | 0 (8403) | none |
| `itemData.57` | parameter 3 compatibility adjustment | `untyped` | 8403 | 0 | 0 | 0 | blank (8403) | none |
| `itemData.58` | parameter 4 grow selector | `untyped` | 8403 | 0 | 0 | 0 | blank (8403) | none |
| `itemData.59` | parameter 4 base value | `float` | 0 | 8107 | 0 | 296 | 0 (8107), 10 (6), 15 (1), 20 (1), 30 (10), 40 (10), 60 (15), 300 (3), 600 (2), 1800 (243), 10800 (5) | 3020301=10, 3020510=10800, 3010001=1800 |
| `itemData.60` | parameter 4 compatibility adjustment | `untyped` | 8403 | 0 | 0 | 0 | blank (8403) | none |
| `equipment.71` | condition-parameter scalar 1; data-shaped parameter ID | `s16` | 0 | 0 | 4620 | 255 | -1 (4620), 16007 (74), 16008 (74), 16009 (74), 16010 (33) | 4020210=16007, 8081706=16010, 4020011=16009 |
| `equipment.72` | condition-parameter scalar 2; data-shaped value | `s16` | 0 | 4782 | 0 | 93 | 0 (4782), 1 (33), 2 (9), 3 (23), 4 (12), 5 (16) | 4020408=1, 8051518=5, 4020404=5 |
| `equipment.73` | condition-parameter scalar 3; data-shaped parameter ID | `s16` | 0 | 0 | 4782 | 93 | -1..15052; 26 distinct; top -1 (4782), 15018 (16), 15016 (10), 15001 (9) | 4100805=15001, 8051517=15052, 4020404=15018 |
| `equipment.74` | condition-parameter scalar 4; data-shaped value | `s16` | 0 | 4782 | 0 | 93 | -20..120; 22 distinct; top 0 (4782), 30 (14), 10 (8), 60 (8) | 8032820=-20, 8032605=120, 4020404=30 |
| `equipment.75` | base append-parameter ID | `s32` | 0 | 0 | 4555 | 320 | -1..1015063; 21 distinct; top -1 (4555), 1015063 (243), 20026 (35), 20013 (8) | 8010225=20001, 3011459=1015063, 3010001=1015063 |
| `equipment.76` | base append-parameter value | `s16` | 0 | 4632 | 0 | 243 | 0 (4632), 3 (243) | 3010001=3, 3011459=3 |
| `equipment.77` | quality-gated parameter ID | `s32` | 0 | 0 | 3301 | 1574 | -1..15052; 38 distinct; top -1 (3301), 15008 (114), 15001 (108), 15007 (107) | 4030603=15001, 9010053=15052, 4020403=15018 |
| `equipment.78` | quality-gated parameter value | `s16` | 0 | 3011 | 2 | 1862 | -1..50; 18 distinct; top 0 (3011), 1 (1027), 10 (294), 2 (215) | 9010043=-1, 3020308=50, 3010001=10 |
| `equipment.79` | append-parameter pair 1 ID | `s32` | 0 | 0 | 1087 | 3788 | -1..1016002; 93 distinct; top -1 (1087), 15001 (638), 15017 (422), 15002 (330) | 4020106=15001, 3020203=1016002, 3010001=1015018 |
| `equipment.80` | append-parameter pair 1 value | `s16` | 0 | 1122 | 6 | 3747 | -100..160; 73 distinct; top 0 (1122), 1 (359), 3 (277), 2 (274) | 8071503=-100, 8032801=160, 3010001=11 |
| `equipment.81` | append-parameter pair 2 ID | `s32` | 0 | 0 | 1707 | 3168 | -1..1016002; 71 distinct; top -1 (1707), 15029 (270), 15005 (241), 15006 (209) | 4020405=15001, 3020204=1016002, 3010001=1015009 |
| `equipment.82` | append-parameter pair 2 value | `s16` | 0 | 1707 | 5 | 3163 | -70..120; 53 distinct; top 0 (1707), 2 (443), 1 (383), 3 (359) | 5020406=-70, 5020104=120, 3010001=5 |
| `equipment.83` | append-parameter pair 3 ID | `s32` | 0 | 0 | 3215 | 1660 | -1..1015009; 55 distinct; top -1 (3215), 15017 (173), 15029 (162), 15009 (123) | 3010118=15001, 3010507=1015009, 3010101=1015005 |
| `equipment.84` | append-parameter pair 3 value | `s16` | 0 | 3215 | 1 | 1659 | -20..100; 36 distinct; top 0 (3215), 2 (228), 3 (217), 4 (207) | 4030711=-20, 4080502=100, 3010101=7 |
| `equipment.85` | append-parameter pair 4 ID | `s32` | 0 | 0 | 4348 | 527 | -1..16004; 36 distinct; top -1 (4348), 15031 (77), 15029 (66), 15030 (44) | 4030602=15001, 8081919=16004, 4020009=15020 |
| `equipment.86` | append-parameter pair 4 value | `s16` | 0 | 4185 | 0 | 690 | -30..9000; 62 distinct; top 0 (4185), 1 (82), 3 (51), 5 (48) | 4070402=-30, 3020505=9000, 3010001=22 |
| `equipment.87` | append-parameter pair 5 ID | `s32` | 0 | 0 | 4687 | 188 | -1..16004; 31 distinct; top -1 (4687), 15031 (35), 15033 (23), 15007 (15) | 4020402=15002, 8032828=16004, 4020009=15040 |
| `equipment.88` | append-parameter pair 5 value | `s16` | 0 | 4583 | 0 | 292 | -20..1050; 33 distinct; top 0 (4583), 5 (56), 7 (37), 10 (31) | 8013601=-20, 3020201=1050, 3010001=4 |
| `equipment.89` | append-parameter pair 6 ID | `s32` | 0 | 0 | 4828 | 47 | -1..16004; 18 distinct; top -1 (4828), 15029 (7), 15020 (5), 15022 (5) | 8013403=15009, 8071528=16004, 4020204=15010 |
| `equipment.90` | append-parameter pair 6 value | `s16` | 0 | 4785 | 0 | 90 | -30..60; 20 distinct; top 0 (4785), 3 (16), 5 (15), 10 (11) | 8032802=-30, 8071528=60, 3010101=3 |

## Parameter-ID joins

The odd equipment columns have an alternating ID/value data shape. This does not override the formula contract: columns 71-74 remain four returned condition scalars there, while columns 75-90 have the explicit combination roles shown above. Every observed non-`-1` odd-column ID resolves to the localized English name in `csv/xtx_text_paramName.csv` by one of two data-supported key rules:

The eight formula-defined ID columns 75, 77, 79, 81, 83, 85, 87, and 89 contain 11272 non-sentinel occurrences and 137 distinct IDs. Including the two data-shaped condition columns 71 and 73 yields 11620 occurrences and 141 distinct IDs across the five bands below.

| ID band | Occurrences | Distinct IDs | Join rule | Named IDs |
|---|---:|---:|---|---:|
| `15xxx` | 10711 | 62 | direct row-id | 62 |
| `16xxx` | 263 | 6 | direct row-id | 6 |
| `20xxx` | 112 | 48 | direct row-id | 48 |
| `1015xxx` | 510 | 23 | minus-1000000 | 23 |
| `1016xxx` | 24 | 2 | minus-1000000 | 2 |

The direct join is an exact row-ID match. The offset join is limited to the observed 1015xxx and 1016xxx bands and removes 1,000,000 before the same row-ID lookup. It is supported by the retail item-table audit in `xivl-captures:studies/gamerescape-tables/derived/client-column-map-notes.md`; the analyzer does not generalize it to another band. The join supplies a localized parameter label only. It does not establish value units, a parameter category, equipment eligibility, or a mapping to actor `generalParameter` indices.

### Pair sentinel audit

No requested equipment cell is blank. The pair census distinguishes the canonical `(-1, 0)` shape from residual values beside `-1`; it must not be used to invent a skip rule where the promoted consumer does not have one.

| Pair | `(-1, 0)` | `(-1, nonzero)` | `(live ID, 0)` |
|---|---:|---:|---:|
| `71/72` | 4620 | 0 | 162 |
| `73/74` | 4782 | 0 | 0 |
| `75/76` | 4555 | 0 | 77 |
| `77/78` | 3011 | 290 | 0 |
| `79/80` | 1087 | 0 | 35 |
| `81/82` | 1707 | 0 | 0 |
| `83/84` | 3215 | 0 | 0 |
| `85/86` | 4185 | 163 | 0 |
| `87/88` | 4583 | 104 | 0 |
| `89/90` | 4785 | 43 | 0 |

The client formula explicitly skips `-1` for column 75 and the six IDs in columns 79, 81, 83, 85, 87, and 89. It does not establish that skip rule for quality-gated column 77, and it returns columns 71-74 directly. Accordingly, `-1` is a proven consumer sentinel only for the seven skip-tested ID columns.

The 798-sheet inventory has these parameter-bearing names: `_zoneParam, regionParam, xtx/text_paramName, zoneGroupParam`. Only `xtx/text_paramName` is a parameter label sheet; the others are geographic parameter sheets. No inventory sheet name identifies a parameter-unit or parameter-category table. The two unit values returned by the client `desktopWidget` consumer therefore remain a native/UI boundary rather than a corpus join.

## Retail gear anchors

The three catalog IDs retained by the equipment-property correlation study are all present in both source sheets. Their tuples keep the requested columns in source order and do not assign meaning to the observed `generalParameter[18]` changes.

| Evidence anchor | Client item name | itemData 49-60 | equipment 71-90 |
|---|---|---|---|
| body capture 0x007A88D7 / row `8030423` | cotton dalmatica | `(blank, 0, blank, blank, 0, blank, blank, 0, blank, blank, 0, blank)` | `(-1, 0, -1, 0, -1, 0, 15029, 1, 15001, 27, 15029, 4, -1, 0, -1, 0, -1, 0, -1, 0)` |
| helm capture 0x007A3F58 / row `8011608` | steel sallet (green) | `(blank, 0, blank, blank, 0, blank, blank, 0, blank, blank, 0, blank)` | `(-1, 0, -1, 0, -1, 0, 15001, 4, 15001, 20, 15005, 3, -1, 0, -1, 0, -1, 0, -1, 0)` |
| weapon capture 0x003D7E3D / row `4030013` | blunt goblin gladius | `(blank, 0, blank, blank, 0, blank, blank, 0, blank, blank, 0, blank)` | `(-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0)` |

Source: `xivl-captures:studies/equipment-property-correlation/derived/evidence-map.md`. The packet study proves item/equipment-slot linkage and actor-property chronology, not a particular parameter noun.

## Grow-selector and rejected-join boundary

All four grow-selector columns (49, 52, 55, 58) and all four compatibility columns (51, 54, 57, 60) are untyped and blank on every `itemData.csv` row. The corpus therefore has no stored selector values from which to recover a domain. The formula's negative-selector-to-nil behavior is a client-consumer contract, not a sentinel observed in this extraction.

A normalized `grow` search over all 798 canonical sheet names returns 0 matches. This is a bounded sheet-inventory negative only: it does not rule out native tables behind `getGrowData` or `judgeGrowColumn`. No grow-table join can be promoted from this data corpus.

Rejected joins are: treating the offset IDs as direct `paramName` row IDs; mapping parameter IDs to actor `generalParameter` indices; assigning units or categories from numeric magnitude; and treating blank grow or compatibility cells as zero. The corpus also does not establish public field names for these numeric columns, the four condition names, HQ semantics, server authority, or equipment eligibility.
