# Ifrit candidate appearance boundary

The decoded `actorclass_graphic.csv` rows used in the Ifrit Bowl
investigation have three distinct appearance bases. These are raw
client-data associations by actor ID, not a retail join to an NPC
client class path or an encounter spawn rule.

| Actor IDs | Rows | Base | Head | Body |
| --- | ---: | ---: | ---: | ---: |
| `2107301..2107303`, `2207301..2207303`, `2207308..2207309`, `2207311`, `2207314` | 10 | 10852 | 0 or 2048 | 1024 |
| `2207304..2207305`, `2207310`, `2207312` | 4 | 1255 | 1024 | 0 |
| `2207306..2207307`, `2207313`, `2207315` | 4 | 10524 | 2048 | 1024 |

All 18 rows have size 2. In particular, `2207310` has base 1255,
HEAD 1024, and BODY 0; `2207314` has base 10852, HEAD 2048, and
BODY 1024. Neither row has the base-10999 appearance used by the
generic carrier candidate `1001481` (size 2, HEAD 0, BODY 1024).

Across all 7,831 `actorclass_graphic.csv` rows, 715 have base 10999;
708 of those have size 2, HEAD 0, and BODY 1024. This appearance
shape is therefore not unique to an Ifrit-related actor ID. The
m999/e001 state resources and their limits are documented in
`xivl-decomp:docs/actor/model-state-color-transitions.md`, under the
state-4/state-5 graph findings. Appearance-row similarity alone does
not establish which owner, if any, selected those resources in a
historical encounter.

The source is extraction `2012.09.19.0001`:
`manifests/tables.json` pins `actorclass_graphic.csv` at 892,164 bytes,
SHA-256 `7DA8241400530885E0A28DED04A03ACF2771B0580A79C1F49F46EE0861010611`.
The matching `actorclass.csv` rows provide display-name IDs, not NPC
class paths. The static-actor SAN and
`manifests/staticactor_class_paths.json` cover script actors but omit
NPC actor-class bindings. The candidate labels from an external
actor-class table cannot turn these appearance rows into retail-proven
`IfritHotAir`, `IfritDummy`, or `IfritAnchor` class-path joins.
