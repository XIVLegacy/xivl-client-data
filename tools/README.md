# Tooling

The tools have two parts: the CSV-to-SQL promotion pipeline and maintenance
scripts. All canonical inputs and outputs stay in this repository. Generated
seed fragments are untracked.

## CSV-to-SQL promotion pipeline

`csv_to_sql.py --table <family>` or `csv_to_sql.py --all` reads `csv/` through
the declarative modules in `mappings/` and writes `build/sql/<table>.sql`.
A downstream consumer owns its DDL, server SQL, and import of these seed
fragments.

Use `csv_to_sql.py --list` to print the available mapping module names without
writing output.

`--all` excludes partial mappings that would fill curated server columns with
placeholders. Run partial mappings with `--table actor_class` or `--table
zones`.

### Mapping module contract

Each module under `mappings/` exports `SQL_TABLE`, `COLUMNS`, and either
`SOURCE_CSV` or `SOURCES`. For multiple sources, the first source defines the
output rows and order. `JOIN_KEYS` maps a lookup source to a driver source and
column. Without it, sources join by row ID. `REQUIRE_JOIN_MATCH = False`
declares an intentionally partial join. `INCLUDE_IN_ALL = False` keeps an
incomplete table mapping explicit-only.

Single-source column entries contain the SQL column, value source, and CSV
type. Multi-source entries also name the source CSV. A value source may be
`row_id`, a CSV column index, `iteration_index`, `const:N`, `const:NULL`,
`const:` for an empty string, or a resolver callable. Resolvers receive the
driver row ID and all indexed source rows. Returning `None` emits SQL `NULL`.

## Maintenance scripts

- `validate_corpus.py` is the repo gate for the tracked public boundary,
  JSON parsing, schema, checksum, referential-integrity, and docs-index checks.
- `build-manifest.ps1` rebuilds `manifests/manifest.json` and
  `manifests/tables.json` from the as-imported CSVs.
- `build_command_battle_params.py` regenerates
  `derived/command_battle_params.csv` from the `csv/gameCommand.csv` /
  `csv/gameCommandBasic.csv` / `csv/xtx_command.csv` trio. See
  `docs/command-battle-params.md` for the column map.
- `build_shop_catalogs.py` regenerates the GC seal and generic range-expanded
  shop catalogs plus `manifests/shop_catalogs.json`. Its `--check` mode verifies
  all three artifacts without writing.
- `analyze_item_graphics_candidates.py` emits full distributions, correlations,
  and packed-field profiles for the typed `weapon.csv` and `equipment.csv`
  columns considered as item-graphics candidates. An optional historical SQL
  input is used only for correlation and is never treated as retail authority.
- `verify_actor_appearance_crosswalk.py` checks the canonical names and `s32`
  types for `actorclass_graphic` columns `0x19..0x1F`, then verifies the seven
  zero packed words in rows `0x5A0700..0x5A0703`.
- `compare_sheet_inventory.py` compares `manifests/sheet_inventory.csv` with an
  explicit retail client root, checks the game/var master references and every
  named sheet document, and reports XML sheet documents carrying names outside
  the inventory.
- `build_zone_name_catalog.py` and `extract_staticactor_san.py` produce the
  zone-name and static-actor manifests from explicit client inputs.
- `verify_retail_staticactor.py` checks the fixed retail SAN product contract;
  `test_retail_staticactor.py` covers its mutation and sanitized-output cases.
- `retail_inventory_crosscheck.py` checks vendored retail item observations.

The verifier's `--input` is the artifact under test, while the separately
named tracked product is the reference result; the defaults point to the same
tracked file for the asset-free local check, and the retail workflow supplies a
generated product as `--input`.

The dependency-free checker in `_schema_check.py` validates the attestation
schema's exact subset: `type`, `const`, `enum`, `pattern`, `minLength`,
`minItems`, `uniqueItems`, `items`, `required`, `properties`, and boolean
`additionalProperties`, with the standard annotation keys `$schema`, `$id`,
`title`, and `description`. It supports object, array, string, integer,
boolean, and null types. Any other keyword or schema form raises `SchemaError`
instead of being silently ignored.

The remaining mapping helpers and shared readers are implementation details
of these entry points. See their `--help` output for flags and output paths.
