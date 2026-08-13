"""Three-source CSV mapping for the item seed table."""

SQL_TABLE = "item"
SOURCES = ["_item.csv", "xtx_itemName.csv", "itemData.csv"]

# xtx_itemName.csv col 5 = English Title; see docs/corpus-inventory.md.
COLUMNS = [
    ("catalogID", "_item.csv", "row_id", "u32"),
    ("name", "xtx_itemName.csv", 5, "str"),
    ("category", "_item.csv", 0, "str"),
    ("maxStack", "_item.csv", 1, "s32"),
    ("isRare", "_item.csv", 2, "bool"),
    ("isExclusive", "_item.csv", 3, "bool"),
    ("durability", "itemData.csv", 33, "s32"),
    ("sellPrice", "itemData.csv", 35, "s32"),
    ("icon", "itemData.csv", 36, "s32"),
    ("kind", "itemData.csv", 40, "s32"),
    ("rarity", "itemData.csv", 41, "s32"),
    ("isUseable", "itemData.csv", 43, "s32"),
    ("mainSkill", "itemData.csv", 44, "s32"),
    ("subSkill", "itemData.csv", 45, "s32"),
    ("levelType", "itemData.csv", 46, "s32"),
    ("level", "itemData.csv", 47, "s32"),
    ("compatibility", "itemData.csv", 48, "s32"),
    ("effectMagnitude", "itemData.csv", 50, "float"),
    ("effectRate", "itemData.csv", 53, "float"),
    ("shieldBlocking", "itemData.csv", 56, "float"),
    ("effectDuration", "itemData.csv", 59, "float"),
    ("recastTime", "itemData.csv", 61, "float"),
    ("recastGroup", "itemData.csv", 63, "s8"),
    ("repairSkill", "itemData.csv", 64, "s32"),
    ("repairItem", "itemData.csv", 65, "s32"),
    ("repairItemNum", "itemData.csv", 66, "s32"),
    ("repairLevel", "itemData.csv", 67, "s32"),
    ("repairLicense", "itemData.csv", 68, "s32"),
]
