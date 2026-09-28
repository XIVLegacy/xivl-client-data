"""Explicit-only actorclass mapping with placeholders for curated fields."""

SQL_TABLE = "actorclass"
SOURCE_CSV = "actorclass.csv"
INCLUDE_IN_ALL = False

COLUMNS = [
    ("id", "row_id", "u32"),
    ("classPath", "const:", "str"),
    ("displayNameId", 5, "u32"),
    ("propertyFlags", "const:0", "u32"),
    ("eventConditions", "const:NULL", "str"),
]
