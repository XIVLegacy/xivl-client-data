# Quest 110420 journal selectors

Canonical `xtx_quest` row `110420` has the English title "Sleep, Cousin of
Death". Its English active-text column (header index `14`) contains five
conditional rich-text references to `xtx/journalxtxWil`. Column `28` repeats
the same five row selectors as plain `@sheet` references. The compact integer
operands are encoded as `f0 45` through `f0 49`.

At `xivl-tools` revision
`be64c2842afb6b8937601fa1f1fddd2adac4ca69`, the rich-string parser decodes a
`0xf0` integer lead by reading the following byte as the low eight bits
(`src/formats/src/richstring.rs`, `decode_integer`; the expression grammar is
documented in `docs/formats/ssd-sheet.md`, "Rich-string control tokens").
Therefore these operands decode to Wil row keys `69`-`73`; the following byte
in each expression is a separate expression value, not part of the row key.
This resolves the row-key ambiguity: the serialized references are not
one-based positions for rows `68`-`72`.

| Wil row | Bounded English-text observation |
| ---: | --- |
| `69` | The player obtains an ingredient from Nomomo and is directed to combine it with another material to make medicine. |
| `70` | The completed medicine is to be taken back to Nogeloix. |
| `71` | Nogeloix directs the player to bring the medicine to Damielliot and seek Healer S'lyhhia at the ward. |
| `72` | After S'lyhhia administers the medicine and speaks with Damielliot, the player is told to report back to Nogeloix. |
| `73` | Momodi discusses a group from the city guard leaving the city by chocobo. |

Rows `69`-`72` form a coherent medicine narrative, while row `73` concerns a
different topic. That content does not authorize dropping the fifth encoded
reference or reinterpreting its key. The five references are conditional; the
meanings of their operators and condition values, the active condition in any
historical session, server gates, and actual progression order remain
unverified. Localized text and field order do not establish those runtime
facts. This static-data finding does not independently associate row `110420`
with a script path.

Sources: `xivl-client-data:csv/xtx_quest.csv` row `110420`, physical line
`103`, columns `14` and `28`, SHA-256
`938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719`
(`manifests/tables.json:6267-6271`); and
`xivl-client-data:csv/xtx_journalxtxWil.csv` rows `69`-`73`, SHA-256
`80da9c607d81f58dc7c7a9625ecd4f6cefaba32bb3448c73f85c3c8082bdd694`
(`manifests/tables.json:6195-6199`). Both are from extraction
`2012.09.19.0001`. Integer decoding provenance: `xivl-tools` revision
`be64c2842afb6b8937601fa1f1fddd2adac4ca69`,
`src/formats/src/richstring.rs` and `docs/formats/ssd-sheet.md`.
