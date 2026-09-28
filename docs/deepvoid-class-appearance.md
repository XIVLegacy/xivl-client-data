# Deepvoid actor-class appearance split

The pinned decoded `actorclass.csv`, `actorclass_graphic.csv`, and
`xtx_displayName.csv` retain distinct Deepvoid actor-class rows with the
same English display text. These are static class/display/appearance joins,
not an event-spawn or dungeon-boss assignment.

| Actor class | Display ID | English text | Base | Size ordinal | Head | Body |
| ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `2102507` | `3102507` | deepvoid slave | 10037 | 7 | 5120 | 2048 |
| `2102508` | `3102507` | deepvoid slave | 10037 | 7 | 5120 | 2048 |
| `2302501` | `3202503` | deepvoid slave | 10037 | 3 | 0 | 2048 |

The two display IDs and the different size/head values prevent the shared
English name from serving as an actor identity. The `5120` head value is
the `e005` appearance selection described separately in
`xivl-decomp:docs/actor/atomos-deepvoid-presentation.md`. These rows do not
identify a retail spawn, server BNPC ID, fight profile, or enrage rule.

Sources: `xivl-client-data:csv/actorclass.csv` rows `2102507`, `2102508`,
and `2302501`; `csv/actorclass_graphic.csv` at the same row IDs;
`csv/xtx_displayName.csv` rows `3102507` and `3202503`.
The exact corpus identities in `manifests/tables.json` are SHA-256
`3ac9f8d1812d49101f367e2a41356be96b5d64b1fc5ca29949195f50ebe1d984`,
`7da8241400530885e0a28ded04a03acf2771b0580a79c1f49f46ee0861010611`,
and `36c5dfba312695d9f4ee090dba123dfd7792feba55d88b0062c070d98abc0505`
in that order.
