# Job-fight candidate display joins

The decoded `2012.09.19.0001` `actorclass` sheet maps the selected actor-class
IDs below to display IDs in column 5. `xtx_displayName` column 1 gives the
corresponding English label. These are static class-to-display joins, not
proof that a particular job quest spawns the class, chooses its count, or
uses it as a kill target. Source rows are
`xivl-client-data:csv/actorclass.csv` and
`xivl-client-data:csv/xtx_displayName.csv`; byte identities are pinned by
`manifests/tables.json`.

| Actor class | Display ID | English label |
| ---: | ---: | --- |
| `2201114` | `3201121` | miteling straggler |
| `2201115` | `3201122` | diremite straggler |
| `2201807` | `3201807` | wandering soldier |
| `2201808` | `3201808` | wandering mage |
| `2202611` | `3202612` | runagate imp |
| `2203001` | `3203001` | antling worker |
| `2204318` | `3204321` | wandering bogy |
| `2204511` | `3204512` | crabfisher |
| `2204610` | `3204607` | firebound wrath |
| `2206306` | `3206306` | Qiqirn shirrer |
| `2206901` | `3206901` | Ascian |
| `2207612` | `3207612` | ironshell |

In particular, the retail display label for class `2206901` is `Ascian`.
It cannot be relabeled as a quest-specific specter from a similarly named
client class file. The class file's inheritance and the actor-class row are
separate evidence until a retail binding connects them. The listed names
also do not establish combat profiles, levels, waves, placement, or a
historical encounter roster.
