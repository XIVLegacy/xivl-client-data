"""Single-CSV mapping for the armor seed table."""

SQL_TABLE = "armor"
SOURCE_CSV = "armor.csv"

COLUMNS = [
    ("catalogID", "row_id", "u32"),
    ("defense", 116, "s16"),
    ("magicDefense", 117, "s16"),
    ("criticalDefense", 118, "s16"),
    ("evasion", 119, "s16"),
    ("magicResistance", 120, "s16"),
    ("damageDefenseType1", 121, "s32"),
    ("damageDefenseValue1", 122, "s16"),
    ("damageDefenseType2", 123, "s32"),
    ("damageDefenseValue2", 124, "s16"),
    ("damageDefenseType3", 125, "s32"),
    ("damageDefenseValue3", 126, "s16"),
    ("damageDefenseType4", 127, "s32"),
    ("damageDefenseValue4", 128, "s16"),
]
