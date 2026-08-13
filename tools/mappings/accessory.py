"""Single-CSV mapping for the accessory seed table."""

SQL_TABLE = "accessory"
SOURCE_CSV = "accessory.csv"

COLUMNS = [
    ("catalogID", "row_id", "u32"),
    ("power", 129, "u8"),
    ("size", 130, "u8"),
]
