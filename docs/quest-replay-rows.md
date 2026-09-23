# Selected quest replay rows

The pinned `cutReplay.csv` contains three consecutive `110420` rows with
different scene keys and playback argument values:

| Row | Scene key, sheet column 0 / CSV field 1 | Sheet columns 8/9 | Sheet columns 10-15 |
| ---: | --- | --- | --- |
| `11042001` | `alc20010` | `-200`, `-200` | all `-200` |
| `11042002` | `alc20020` | `-218`, `-220` | all `-200` |
| `11042003` | `alc20030` | `-218`, `-220` | all `-200` |

These are literal static payload values, not decoded meanings for the
negative sentinels. They do not establish a retail replay-unlock state,
quest route, cutscene trigger, or runtime playback. The separate client
consumer of columns 8-15 is documented in
`xivl-client-scripts:docs/cutscene-replay-skip-contract.md`.

Source: `xivl-client-data:csv/cutReplay.csv` rows `11042001`-`11042003`,
SHA-256 `2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37`
in `manifests/tables.json`.

The same table has these eight consecutive `fsh300` rows. Column values
are literal sheet columns after the row ID.

| Row | Scene key, sheet column 0 / CSV field 1 | Sheet columns 6/7 | Sheet column 8 | Sheet columns 9-15 |
| ---: | --- | --- | --- | --- |
| `11050101` | `fsh30010` | `1`, `1` | `-200` | all `-200` |
| `11050102` | `fsh30020` | `1`, `1` | `-207` | all `-200` |
| `11050103` | `fsh30025` | `1`, `1` | `-200` | all `-200` |
| `11050104` | `fsh30030` | `1`, `1` | `-200` | all `-200` |
| `11050105` | `fsh30040` | `1`, `1` | `-200` | all `-200` |
| `11050106` | `fsh30050` | `1`, `1` | `-200` | all `-200` |
| `11050107` | `fsh30060` | `1`, `1` | `-200` | all `-200` |
| `11050108` | `fsh30070` | `1`, `1` | `-200` | all `-200` |

The next six rows name literal `fsh306` scene keys:

| Row | Scene key, sheet column 0 / CSV field 1 | Sheet columns 6/7 | Sheet column 8 | Sheet columns 9-15 |
| ---: | --- | --- | --- | --- |
| `11050201` | `fsh30610` | `1`, `1` | `-200` | all `-200` |
| `11050202` | `fsh30620` | `1`, `1` | `-200` | all `-200` |
| `11050203` | `fsh30630` | `1`, `1` | `-200` | all `-200` |
| `11050204` | `fsh30640` | `1`, `1` | `-200` | all `-200` |
| `11050205` | `fsh30650` | `1`, `1` | `-200` | all `-200` |
| `11050206` | `fsh30660` | `1`, `1` | `-200` | all `-200` |

These literal rows do not establish replay eligibility or runtime playback.
The meaning of `-207` remains unknown. The client replay consumer of sheet
columns 8-15 is documented in
`xivl-client-scripts:docs/cutscene-replay-skip-contract.md`.
The corresponding canonical Lua call sites for both families are listed in
`xivl-client-scripts:docs/quest-scene-replay-joins.md`.

Source: `xivl-client-data:csv/cutReplay.csv` rows `11050101`-`11050206`,
SHA-256 `2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37`
in `manifests/tables.json`.

The same pinned table contains these Hamlet scene keys:

| Row | Scene key, sheet column 0 / CSV field 1 |
| ---: | --- |
| `11082008` | `ham0s201` |
| `11082009` | `ham0s202` |
| `11082010` | `ham0f301` |
| `11082011` | `ham0f302` |
| `11082012` | `ham0w201` |
| `11082013` | `ham0w202` |

These literal row-to-key values do not establish unlock state, a live duty
trigger, a server route, or physical scene-asset presence.
