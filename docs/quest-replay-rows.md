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

## Man402 and Man406

The pinned table also contains these rows. Column values are literal sheet
columns after the row ID.

| Row | Scene key, sheet column 0 / CSV field 1 | Sheet columns 6/7 | Sheet columns 8-15 |
| ---: | --- | --- | --- |
| `11001801` | `man40200` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-217`, `-200`, `-200` |
| `11001802` | `man40210` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `1`, `1`, `-200` |
| `11001803` | `man40220` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-200`, `-200`, `-200` |
| `11001804` | `man40230` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-200`, `-200`, `-200` |
| `11001901` | `man40600` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-200`, `-200`, `-200` |
| `11001902` | `man40610` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-200`, `-200`, `-200` |
| `11001903` | `man40615` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-200`, `-200`, `-200` |
| `11001904` | `man40620` | `1`, `1` | all `-200` |
| `11001905` | `man40625` | `1`, `1` | all `-200` |
| `11001906` | `man40630` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-200`, `-200`, `-200` |
| `11001907` | `man40635` | `2`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-200`, `-200`, `-200` |
| `11001908` | `man40650` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-205`, `-200`, `-200` |
| `11001909` | `man40660` | `1`, `1` | `-201`, `-202`, `-203`, `-204`, `-205`, `-217`, `-200`, `-200` |

These are static row-to-key and payload values. The negative values remain
uninterpreted sentinels; the rows do not establish replay eligibility, a
server route, or historical playback. Client-side call sites for Man406 and
Man402 are indexed in `xivl-client-scripts:docs/quest-scene-replay-joins.md`;
that crosswalk does not make the sheet values runtime state.

Source: `xivl-client-data:csv/cutReplay.csv` rows `11001801`-`11001804` and
`11001901`-`11001909`, SHA-256
`2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37` in
`manifests/tables.json`.

## Additional replay row keys

These 47 rows add literal row-to-key pairs from the same pinned table.
Ranges with matching row and key ranges are paired in ascending order.

| Row IDs | Scene key, sheet column 0 / CSV field 1 |
| --- | --- |
| `11082101`-`11082109` | `rad0f300`-`rad0f308` |
| `11082201`-`11082207` | `rad0r100`-`rad0r106` |
| `11082301`-`11082304` | `rad0r400`-`rad0r403` |
| `11082401`-`11082404` | `rad0w500`-`rad0w503` |
| `11087001` | `sum6w010` |
| `11087002` | `sum6w020` |
| `11141601`, `11161601`, `11181601` | `gc010105` |
| `11141602`, `11161602`, `11181602` | `sum6a000` |
| `11141603`, `11161603`, `11181603` | `gc010110` |
| `11143304`, `11163304`, `11183304` | `gc010715` |
| `11143305`, `11163305`, `11183305` | `gc010720` |
| `11143306`, `11163306`, `11183306` | `gc010730` |
| `11143307`, `11163307`, `11183307` | `gc010740` |

These are static values from column 0. The row-to-key pairs do not establish
replay eligibility, a caller, content ownership, asset identity, or runtime
playback.

Source: `xivl-client-data:csv/cutReplay.csv` rows `11082101`-`11082109`,
`11082201`-`11082207`, `11082301`-`11082304`, `11082401`-`11082404`,
`11087001`-`11087002`, `11141601`-`11141603`, `11143304`-`11143307`,
`11161601`-`11161603`, `11163304`-`11163307`, `11181601`-`11181603`, and
`11183304`-`11183307`, SHA-256
`2553b82e1f983025e0ee23b2a8fd27e8ea44e228cda1fe3e45d743b48c584e37` in
`manifests/tables.json`.
