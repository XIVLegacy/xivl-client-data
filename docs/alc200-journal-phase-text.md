# Alc200 journal phase-text links

The English active-text field in canonical `xtx_quest` row `110420` contains
five conditional rich-text references to `xtx_journalxtxWil`; the corresponding
completion-text field repeats the same five targets. They resolve to English
journal rows `68`-`72`:

| Wil row | Bounded English-text observation |
| ---: | --- |
| `68` | Nogeloix asks the player to obtain curative reagents from Nomomo at Camp Black Brush. |
| `69` | The player obtains an ingredient and is directed to combine it with another material to make a medicine. |
| `70` | The completed medicine is to be taken back to Nogeloix. |
| `71` | Nogeloix directs the player to bring the medicine to Damielliot and seek Healer S'lyhhia at the ward. |
| `72` | After S'lyhhia administers the medicine and speaks with Damielliot, the player is told to report back to Nogeloix. |

These are localized client text links and a narrative sequence, not proof of
server gates, runtime state values, or the order in which a historical client
session reached them. The rich-text expressions include compact operands
`0`, `5`, `7`, `10`, and `15` and operator codes `0xE4` and `0xE0`. This
finding does not assign meanings to those operands or operators, or establish
that the operands encode quest state or progression order.

Sources: `xivl-client-data:csv/xtx_quest.csv` row `110420`, physical line
`103`, SHA-256
`938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719`
(`manifests/tables.json:6267-6271`); and
`xivl-client-data:csv/xtx_journalxtxWil.csv` rows `68`-`72`, SHA-256
`80da9c607d81f58dc7c7a9625ecd4f6cefaba32bb3448c73f85c3c8082bdd694`
(`manifests/tables.json:6195-6199`). Both are from extraction
`2012.09.19.0001`.
