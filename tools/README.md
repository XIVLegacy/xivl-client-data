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
output rows and order. `JOIN_KEYS` maps a lookup source to a driver
source and column. Without it, sources join by row ID. `REQUIRE_JOIN_MATCH = False`
declares an intentionally partial join. `INCLUDE_IN_ALL = False` keeps an
incomplete table mapping explicit-only.

Single-source column entries contain the SQL column, value source, and CSV
type. Multi-source entries also name the source CSV. A value source may be
`row_id`, a CSV column index, `iteration_index`, `const:N`, `const:NULL`,
`const:` for an empty string, or a resolver callable. Resolvers receive the
driver row ID and all indexed source rows. Returning `None` emits SQL `NULL`.

## Maintenance scripts

- `validate_corpus.py` checks the tracked public boundary,
  JSON parsing, schema, checksum, referential-integrity, and docs-index checks.
- `build-manifest.ps1` rebuilds these manifests from the as-imported CSVs:
  `manifests/manifest.json` and `manifests/tables.json`.
- `build_command_battle_params.py` regenerates
  `derived/command_battle_params.csv` from the `csv/gameCommand.csv` /
  `csv/gameCommandBasic.csv` / `csv/xtx_command.csv` trio. See
  `docs/command-battle-params.md` for the column map.
- `build_shop_catalogs.py` regenerates the GC seal and generic range-expanded
  shop catalogs plus `manifests/shop_catalogs.json`. Its `--check` mode verifies
  all three artifacts without writing.
- `analyze_item_graphics_candidates.py` emits full distributions and correlations
  plus packed-field profiles for typed `weapon.csv` and `equipment.csv` columns
  considered as item-graphics candidates. An optional historical SQL
  input is used only for correlation and is never treated as retail authority.
- `verify_actor_appearance_crosswalk.py` checks the canonical names and `s32`
  types for `actorclass_graphic` columns `0x19..0x1F`, then verifies the seven
  zero packed words in rows `0x5A0700..0x5A0703`.
- `build_actor_appearance_census.py` regenerates the exhaustive nonzero-row
  census and exact per-field packed-value distributions. Its `--check` mode
  verifies both derived CSVs without writing. `test_actor_appearance_census.py`
  mutation-tests the packing, joins, source types, and deterministic rendering.
- `analyze_substat_status.py` applies the retail `0x0179` status-id transform,
  joins the status and status-text sheets, and regenerates the complete numeric
  packed-word crosswalk. Its `--check` mode verifies the derived CSV without
  writing. `test_substat_status.py` mutation-tests translation, joining, bit
  projections, failure cases, and deterministic rendering.
- `build_map_marker_resources.py` groups the complete resource/template,
  UI-class, and visibility vocabulary from `2Dmap_actor_data.csv`,
  `2Dmap_marker.csv`, and `quest_marker.csv` into a reproducible crosswalk. Its
  manifest also pins
  property-reference coverage, coordinate domains, and exact/case-folded/
  normalized searches across all 803 decoded CSVs. `test_map_marker_resources.py`
  mutation-tests width, truncation, grouping, prefix coverage, and deterministic
  rendering.
- `build_item_equipment_crosswalk.py` regenerates the canonical census for
  `itemData.csv` columns 49-60 and `equipment.csv` columns 71-90, verifies the
  supported `xtx_text_paramName.csv` joins, and retains the bounded grow-table
  negative. Its `--check` mode verifies the tracked document without writing.
  `test_item_equipment_crosswalk.py` mutation-tests source types, blank-vs-zero
  handling, parameter-key rules, row widths, retail anchors, and deterministic
  rendering.
- `compare_sheet_inventory.py` compares `manifests/sheet_inventory.csv` with an
  explicit retail client root, checks the game/var master references and every
  named sheet document, and reports XML sheet documents carrying names outside
  the inventory.
- `build_zone_name_catalog.py` and `extract_staticactor_san.py` produce the
  zone-name and static-actor manifests from explicit client inputs.
- `test_zone_name_bindings.py` mutation-tests the boundary between generated
  client bindings and curated zone-name fallbacks.
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
