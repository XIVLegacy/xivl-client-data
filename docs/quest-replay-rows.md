# Selected quest replay rows

The pinned `cutReplay.csv` contains three consecutive `110420` rows with
different scene keys and playback argument values:

| Row | Scene key, column 0 | Columns 8/9 | Columns 10-15 |
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
