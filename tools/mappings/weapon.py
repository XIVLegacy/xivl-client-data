"""Single-CSV mapping for the weapon seed table."""

SQL_TABLE = "weapon"
SOURCE_CSV = "weapon.csv"

COLUMNS = [
    ("catalogID", "row_id", "u32"),
    ("attack", 92, "u16"),
    ("magicAttack", 93, "u16"),
    ("craftProcessing", 94, "u16"),
    ("craftMagicProcessing", 95, "u16"),
    ("harvestPotency", 96, "u16"),
    ("harvestLimit", 97, "u16"),
    ("frequency", 98, "s8"),
    ("rate", 99, "u16"),
    ("magicRate", 100, "u16"),
    ("craftProcessControl", 101, "u16"),
    ("harvestRate", 102, "u16"),
    ("critical", 103, "u16"),
    ("magicCritical", 104, "u16"),
    ("parry", 105, "u16"),
    ("damageAttributeType1", 106, "s32"),
    ("damageAttributeValue1", 107, "float"),
    ("damageAttributeType2", 108, "s32"),
    ("damageAttributeValue2", 109, "float"),
    ("damageAttributeType3", 110, "s32"),
    ("damageAttributeValue3", 111, "float"),
    ("damagePower", 135, "s16"),
    ("damageInterval", 136, "float"),
    ("ammoVirtualDamagePower", 141, "s16"),
]
