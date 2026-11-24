# ItemListWidget help declarations

The installed FINAL FANTASY XIV 1.23b client declares type-1 help text on
32 elements of the item list window form. This page records the elements and
their text references. It does not resolve the text.

## Source identity and decoding

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. The path is `client/sqwt/widget/ItemListWidget.form`.
Neither the encrypted input nor the decoded XML is distributed here.

| File | Input bytes | Input SHA-256 | Decoded XML bytes | Decoded XML SHA-256 |
| --- | ---: | --- | ---: | --- |
| `widget/ItemListWidget.form` | 49304 | `65a8c82bc93664231778fe1b704b27254e03a759f4ec37fa23e6ae2f516a46be` | 49296 | `2d5d129d4028f025863c288fa0b9028e7f9222c5c0546b7e09f015b34a37622a` |

Decode with the basename as the ASCII Blowfish key, following the
[Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe). Parse the
decoded text as UTF-8 XML with the standard library ElementTree and select
every element that carries a `Help.Type` or `Help.Value0` attribute.

## Declarations

Every selected element declares `Help.Type="1"` and a literal `Help.Value0`
that is an `@` text reference. Elements are listed in document order.

| Element | Name | `Help.Value0` |
| --- | --- | --- |
| `Grid` | `Grid_Backpack` | `@71909` |
| `Grid` | `Grid_Gil` | `@71910` |
| `TabItem` | `TabItem_1` | `@71911` |
| `TabItem` | `TabItem_2` | `@71912` |
| `TabItem` | `TabItem_3` | `@71913` |
| `TabItem` | `TabItem_4` | `@71917` |
| `TabItem` | `TabItem_5` | `@71914` |
| `TabItem` | `TabItem_6` | `@71915` |
| `IconControl` | `IconControl_Equiped` | `@73950` |
| `IconControl` | `IconControl_NotEquiped` | `@73951` |
| `IconControl` | `IconControl_PolishMAX` | `@73952` |
| `IconControl` | `IconControl_Materia` | `@73953` |
| `Grid` | `Grid_ItemRare` | `@73909` |
| `Grid` | `Grid_ItemTrade` | `@73910` |
| `TextBlock` | `TextBlock_ItemStack` | `@73911` |
| `TextBlock` | `TextBlock_ItemKind` | `@73912` |
| `TextBlock` | `TextBlock_AP` | `@73908` |
| `TextBlock` | `TextBlock_ItemEquipCondition` | `@73913` |
| `WrapPanel` | `WrapPanel_MateriaSlot` | `@73934` |
| `Grid` | `Grid_Life` | `@73901` |
| `Grid` | `Grid_ItemPolish` | `@73930` |
| `Grid` | `Grid_Repair` | `@73904` |
| `Grid` | `Grid_RepairItem` | `@73902` |
| `TextBlock` | `TextBlock_ItemBazaarSingle` | `@73917` |
| `TextBlock` | `TextBlock_ItemBazaarSet` | `@73918` |
| `TextBlock` | `TextBlock_ItemBazaarSeparate` | `@73919` |
| `TextBlock` | `TextBlock_ItemBazaarBuy` | `@73920` |
| `TextBlock` | `TextBlock_ItemBazaarRepair` | `@73921` |
| `TextBlock` | `TextBlock_ItemBazaarReward` | `@73922` |
| `Grid` | `Grid_RewardItem` | `@73923` |
| `Grid` | `Grid_RewardMoney` | `@73924` |
| `Grid` | `Grid_MateriaAttachCost` | `@73924` |

`TabItem_1` through `TabItem_6` also declare `Header` values. `TabItem_1` is
`@3207`, `TabItem_2` is `@3208`, `TabItem_3` is `@3215`, `TabItem_4` is
`@3159` and `TabItem_6` is `@3212`. `TabItem_5` declares no `Header`.
`Grid_RewardMoney` and `Grid_MateriaAttachCost` share `@73924`. The elements
are static declarations. They do not establish which of them are visible for
a given list mode, and the rows of the text table are not read here.
