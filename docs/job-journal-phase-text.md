# Job journal phase text

The pinned `xtx_journalxtxWil.csv` preserves the following English phase
instructions. They are localized client text, not server objective gates or
proof that a phase was reached in a historical session.

| Wil row | Bounded English-text observation |
| ---: | --- |
| `470` | The Warrior Sirocco exercise recommends three accompanying party members. This is phrased as a recommendation, not a cap. |
| `505` | The Warrior Audhumbla challenge recommends seven accompanying party members, again without defining a server admission rule. |
| `510` | After Curious Gorge regains control, the English text directs another conversation at the Silver Bazaar. The French text instead says to return to his cave, so the destination is not consistent across localizations. |
| `541` | The player is instructed to defeat Gluttonous Gertrude before safely using a dynamically named measuring item south of Cedarwood. The row itself does not prove item consumption or the exact use point. |
| `545` | The Prince of Pestilence is described as an obstacle to measurements near the Mun-Tuy Cellars. |
| `546` | After the Prince is defeated, the text directs the player to find a suitable location for the measurement item. This is a distinct post-kill instruction, not a kill-only completion statement. |

The item name in rows `541` and `546` is a rich-string lookup, not a plain
literal item ID in this sheet. The text does not identify a measurement actor,
combat spawn, event dispatcher, or success callback.

The same pinned Wil sheet distinguishes two Paladin encounter texts:

| Wil row | Bounded English-text observation |
| ---: | --- |
| `514` | After the last monsters are defeated, a free paladin hands over a crystal and directs the player back to Jenlyns. The text does not select either `Pld0j1` scene wrapper. |
| `527` | After the parley, the instruction names Jenlyns and his soldiers as the opposing force. Up to seven party members may accompany the player; the text labels that count recommended. |
| `531` | At the later battleground southeast of Camp Bluefog, the instruction names Jenlyns and Solkzagyl as both facing the monster cohort and asks the player to help them. The same seven-companion wording appears. |
| `532` | The post-defeat instruction sends the player back to Jenlyns in Ul'dah. |

These words distinguish participant roles and phases, but do not provide
enemy counts, allied AI, combat coordinates, a server trigger, or a return
warp. The journal's companion allowance does not itself prescribe encounter
population.

Source: `xivl-client-data:csv/xtx_journalxtxWil.csv` rows `470`, `505`, `510`, `514`, `527`,
`531`, `532`, `541`, `545`, and `546`, SHA-256
`80da9c607d81f58dc7c7a9625ecd4f6cefaba32bb3448c73f85c3c8082bdd694`
in `manifests/tables.json`.
