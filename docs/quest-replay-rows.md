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

The same table has these eight consecutive fishing-quest rows. Column values
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

These raw rows do not establish a corresponding recovered Lua call, the
meaning of `-207`, replay eligibility, or runtime playback. The client replay
consumer of sheet columns 8-15 is documented in
`xivl-client-scripts:docs/cutscene-replay-skip-contract.md`.

Source: `xivl-client-data:csv/cutReplay.csv` rows `11050101`-`11050108`,
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
