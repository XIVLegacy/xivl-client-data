# Grand Company journal interaction text

The pinned client journal sheets describe three distinct Grand Company
campaign encounters. These are localized instructions and retrospective
text, not observed item use, server objective gates, or combat behavior.

| Quest title / ID | Journal row | Bounded English-text observation | Rich-string item lookup |
| --- | ---: | --- | --- |
| Alive / `111427` | Sea `318` | Secure the crash-site route and use an interaction-menu item to prevent imperial reinforcements; up to two party members may accompany the player. | `0x00a7da67` = `11000423`, Imperial Disruptor |
| Two Vans are Better than One / `111627` | Fst `385` | Secure the area after a gas attack and use an interaction-menu item to defend against specified Garlean attacks; up to two party members may accompany the player. | `0x00a7da66` = `11000422`, Mist Emitter |
| Like Father, Like Son / `111827` | Wil `449` | Fight near the cave northwest of Camp Black Brush and use an interaction-menu item to remove Garlean enhanced status; up to two party members may accompany the player. | `0x00a7da65` = `11000421`, Imperial Disruptor |

The item IDs are embedded in each row's rich-string switch/name lookup;
`xtx_itemName.csv` names them. IDs `11000421` and `11000423` share an
English name but are different catalog rows and appear in different journal
instructions. The journal does not establish their server effects or whether
an interaction was used in a historical retail session.

The quest-to-journal association is direct rather than a title guess:
`xtx_quest.csv` rows `111427`, `111627`, and `111827` contain rich-string
sheet selectors for `xtx/journalxtxSea`, `xtx/journalxtxFst`, and
`xtx/journalxtxWil`, respectively, as well as item-name lookups for
`11000423`, `11000422`, and `11000421` in columns 23-26.

Follow-up rows preserve separate narrative phases: Sea `319-320` describe
the operative defeat and return to R'ashaht Rhiki; Fst `386-389` describe
the Garlean defeat, Pfrymloef Echo, and Gridanian airship-landing report;
Wil `450-452` describe the surviving Garlean, Echo, and Ul'dahn landing.
Text order is not proof of client-method dispatch or authoritative quest state.

Sources: `csv/xtx_journalxtxSea.csv` rows `318-320` (SHA-256
`051c2501dc9d362e7ffc1c6ec3c840ae9458c95e583fde517ba4a610297d198d`),
`csv/xtx_journalxtxFst.csv` rows `385-389` (SHA-256
`82dfee149d4571e83e85db585f8ae6415fe55b4273764ca0c59d37dd10367189`),
`csv/xtx_journalxtxWil.csv` rows `449-452` (SHA-256
`80da9c607d81f58dc7c7a9625ecd4f6cefaba32bb3448c73f85c3c8082bdd694`),
`csv/xtx_itemName.csv` rows `11000421-11000423` (SHA-256
`917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2`),
and `csv/xtx_quest.csv` rows `111427`, `111627`, and `111827` (SHA-256
`938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719`)
in `manifests/tables.json`.
