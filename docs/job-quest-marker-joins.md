# Job-quest marker and actor-class joins

The decoded `2012.09.19.0001` sheets establish four named job-quest marker
rows and their display-ID joins. `quest_marker` column 5 is a display ID;
`actorclass` column 5 maps actor-class IDs to display IDs; and
`xtx_displayName` column 1 supplies the English display name. The values
below come from `xivl-client-data:csv/quest_marker.csv`,
`xivl-client-data:csv/actorclass.csv`, and
`xivl-client-data:csv/xtx_displayName.csv` at the cited row IDs. Columns 3
and 4 are the marker's two stored floats, not a complete world transform.

| Name | Marker row | Floats, columns 3/4 | Columns 9/10 | Display ID | Actor-class rows with that display |
| --- | ---: | ---: | ---: | ---: | --- |
| Curious Gorge | `11220001` | `-1116.04`, `285.49` | `104`, `403` | `1600318` | `1060028` |
| Raya-O-Senna | `11222001` | `-1540.98`, `-1588.34` | `103`, `303` | `2700007` | `1001570` |
| Jehantel | `11225001` | `737.49`, `1025.73` | `103`, `305` | `1200133` | `1002024`, `1060039` |
| Pukno Poki | `11225002` | `1139.02`, `1012.67` | `103`, `305` | `2480005` | `1001936` |

The actor-class column is an exhaustive join over `actorclass.csv`, not a
selection made from a server spawn table. Jehantel's marker does not choose
between its two actor-class rows. The three singleton joins identify the
only matching class rows in this sheet; they still do not prove which class
was spawned for a historical quest event.

Generic destination markers cannot be turned into actor bindings by the same
method. Rows `11221002`, `11222002`, `11223301`, `11225003`, and `11226301`
all use display ID `4000257`, which joins to 87 actor-class rows. The marker
sheet supplies neither terrain height, facing, a unique spawn, nor an event
dispatcher. Its property-reference column is also not a universal row-ID
identity: row `11222501` stores `@5208/i11222301` in column 13.

Rows `11221401` and `11222401` also use display
ID `4000257`. Both store floats `(-74.51, 392.07)` in columns 3/4 and
region/area `102/201` in columns 9/10 of `quest_marker.csv`. Their distinct
row IDs and identical map point do not establish whether either refers to
the same physical Darkhold coffer, two coffers, an interaction actor, or only
a shared quest-area destination. Neither row binds an armor item to a chest.

The three CSV copies used for this join matched their pinned
`manifests/tables.json` SHA-256 values:

| Sheet | SHA-256 |
| --- | --- |
| `quest_marker.csv` | `920e93e6c1dd136ed758f22465bea3644f2bbe53a6ff46f7d938dd51e3b514be` |
| `actorclass.csv` | `3ac9f8d1812d49101f367e2a41356be96b5d64b1fc5ca29949195f50ebe1d984` |
| `xtx_displayName.csv` | `36c5dfba312695d9f4ee090dba123dfd7792feba55d88b0062c070d98abc0505` |
