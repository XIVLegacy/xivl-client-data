"""Single-CSV mapping for the equipment seed table."""

SQL_TABLE = "equipment"
SOURCE_CSV = "equipment.csv"

COLUMNS = [
    ("catalogID", "row_id", "u32"),
    ("equipPoint", 69, "s32"),
    ("equipTribe", 70, "s8"),
    ("paramBonusType1", 71, "s16"),
    ("paramBonusValue1", 72, "s16"),
    ("paramBonusType2", 73, "s16"),
    ("paramBonusValue2", 74, "s16"),
    ("paramBonusType3", 75, "s32"),
    ("paramBonusValue3", 76, "s16"),
    ("paramBonusType4", 77, "s32"),
    ("paramBonusValue4", 78, "s16"),
    ("paramBonusType5", 79, "s32"),
    ("paramBonusValue5", 80, "s16"),
    ("paramBonusType6", 81, "s32"),
    ("paramBonusValue6", 82, "s16"),
    ("paramBonusType7", 83, "s32"),
    ("paramBonusValue7", 84, "s16"),
    ("paramBonusType8", 85, "s32"),
    ("paramBonusValue8", 86, "s16"),
    ("paramBonusType9", 87, "s32"),
    ("paramBonusValue9", 88, "s16"),
    ("paramBonusType10", 89, "s32"),
    ("paramBonusValue10", 90, "s16"),
    ("additionalEffect", 137, "s16"),
    ("materiaBindPermission", 138, "bool"),
    ("materializeTable", 139, "s16"),
]
