"""Two-source CSV mapping for the achievement seed table."""

SQL_TABLE = "achievement"
SOURCES = ["achievement.csv", "xtx_achievement.csv"]

# English title is col 8; see docs/corpus-inventory.md.
COLUMNS = [
    ("achievementId", "achievement.csv", "row_id", "u16"),
    ("name", "xtx_achievement.csv", 8, "str"),
    ("packetOffsetId", None, "iteration_index", "u16"),
    ("rewardPoints", "achievement.csv", 2, "u16"),
]
