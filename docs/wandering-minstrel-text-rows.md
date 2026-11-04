# Wandering Minstrel text rows

The `2012.09.19.0001` client table `populaceBountyPresenter.csv` retains
dialogue about a level-30 blessing, the goobbue horn and a prison encounter.
These are authored text cells. They do not establish an executed level check,
item grant, player ownership flag or zone transition.

The [appearance census](../derived/actor_appearance_census.csv), row keyed by
actor class 1060027, joins display-name ID 1000436 to `wandering minstrel`.
Actor-class and display-name IDs remain separate domains; this identity join
does not establish a spawn, location or selected interaction.

## Input identity and columns

The exact table is pinned by [tables.json](../manifests/tables.json):
26592 bytes, SHA-256
`7AB1ADF5BBFBDA43851944192CC731795253993B5D0F01A2C2C040D5938CCEEA`.
The containing archive was checked against
[private_csv_corpus.json](../manifests/private_csv_corpus.json), then the
selected member's bytes, hash, header layout and row keys were checked.
This was selected-input authentication, not a new full-corpus validation.

The label row contains columns `0,1,2,3,4`, all typed `str`. There are 35
data rows with actual keys 2 through 36. The English cells below use the
column labelled `1`, the second locale cell after the row-key field. These
keys are not zero-based iteration ordinals. Embedded formatting and gender
controls remain in the source; the summaries below are not replacement text.

## Selected text meanings

| Row keys | English text supports | Boundary |
| --- | --- | --- |
| 2-5 | A prophecy, warnings about the approaching darkness, and a request to demonstrate worth. | The wording does not perform a class, level or eligibility test. |
| 6 | An instruction to speak to the minstrel again after reaching level 30 in any class for a special blessing. | This is an instruction string, not a numeric threshold field or proof of server enforcement. |
| 7-15 | A longer account of the prophecy, help received from adventurers, a vision and knowledge of taming goobbues. | Narrative knowledge does not establish an actual unlock or reward transaction. |
| 16 | Encouragement addressed to an adventurer with a horn. | The sentence is not an inventory mutation or a receipt proving that this invocation granted one. |
| 17-18 | Instructions to summon a goobbue through the micro-menu horn icon and dismount through that icon or active mode. | These describe intended use, not acquisition, an item ID, a synchronized mount flag or successful execution. |
| 19-20 | Reflection on another similar world and uncertainty about its identity. | No travel destination or duty is specified. |
| 21-22 | Two alternative introductory greetings, one recognizing a friend. | The text does not identify the caller's Boolean selector or its producer as friendship, prior reward or ownership. |
| 23 and 35 | Recognition of meaning and attribution of the words to Mezaya Thousand Eyes. | The static rows do not choose a historical encounter or script invocation. |
| 24-30 and 36 | Further verses and their interpretation through Dalamud, calamity and adventurers. | Interpretation is dialogue, not a mechanism for changing world state. |
| 31-34 | Departure, aid, rebirth and a similar-world farewell. | A request to leave prison does not identify a warp operation, destination, facing or completion result. |

The row groups describe source content rather than execution order. The
script uses some keys out of numeric order, including 35 and 36 within its
prison dialogue. Its ordered calls, exact selector and return contracts are
owned by `xivl-client-scripts:docs/wandering-minstrel-client-contract.md`.

## Script and version boundary

The client class `PopulaceBountyPresenter` requests bank 8016 under the name
`populaceBountyPresenter` in `initForEvent`. The matching named CSV and selected row keys
provide the static text join. The actual loaded native resource, receiver
and invocation remain separate from this row identity.

The retained official source
`xivl-captures:sources/lodestone-dev-patch/objects/pages/got-goobbue-2012-06-21.md`
announces an obtainability cutoff at patch 1.23a maintenance. Its announcement
tier is qualified in `xivl-captures:studies/lodestone-dev-patch/README.md`.
The continued presence of these strings in the 1.23b extraction does not
establish an active award, disprove that announced cutoff or prove that every
later interaction was absent. Original server selection, reward settlement
and historical availability require their own evidence.
