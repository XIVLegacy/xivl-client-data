"""Single-CSV mapping for the guildleve seed table."""

SQL_TABLE = "guildleve"
SOURCE_CSV = "guildleve.csv"

COLUMNS = [
    ("id", "row_id", "u32"),
    ("classType", 1, "s32"),
    ("location", 2, "s32"),
    ("factionCreditRequired", 4, "s16"),
    ("level", 5, "s16"),
    ("aetheryte", 6, "s32"),
    ("plateId", 7, "s32"),
    ("borderId", 8, "s32"),
    ("objective", 17, "s32"),
    ("partyRecommended", 18, "s32"),
    ("targetLocation", 19, "s32"),
    ("authority", 20, "s32"),
    ("timeLimit", 21, "s8"),
    ("skill", 23, "s32"),
    ("favorCount", 24, "s8"),
    ("aimNum1", 39, "s8"),
    ("aimNum2", 40, "s8"),
    ("aimNum3", 41, "s8"),
    ("aimNum4", 42, "s8"),
    ("item1", 55, "s32"),
    ("item2", 56, "s32"),
    ("item3", 57, "s32"),
    ("item4", 58, "s32"),
    ("mob1", 59, "s32"),
    ("mob2", 60, "s32"),
    ("mob3", 61, "s32"),
    ("mob4", 62, "s32"),
]
