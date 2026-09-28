# Quest 110016 journal selectors

Canonical `xtx_quest` row `110016` has the English title "Forever Taken".
Its English active-text column (header index `14`) contains five conditional
rich-text references to `xtx/journalxtxWil`. Their extended compact integer
operands are `f0 d6`, `f0 f2`, and `f0 d7` through `f0 d9`.

At `xivl-tools` revision
`be64c2842afb6b8937601fa1f1fddd2adac4ca69`, the rich-string parser decodes a
`0xf0` integer lead by reading the following byte as the low eight bits
(`src/formats/src/richstring.rs`, `decode_integer`; the expression grammar is
documented in `docs/formats/ssd-sheet.md`, "Rich-string control tokens").
The references therefore select Wil row keys `214`, `242`, and `215`-`217`.
Their English text describes the following subjects:

| Wil row | Bounded English-text observation |
| ---: | --- |
| `214` | Gather five items at Silvertear Falls for the Ashcrown Consortium; Consortium employees can explain how to obtain them. |
| `242` | Return to the Ashcrown Consortium and present the collected share to Hedyn. |
| `215` | Hand the gathered items to Hedyn and the sylphs, then report to the Waking Sands. |
| `216` | At the Waking Sands, Minfilia discusses an imperial linkpearl message and the player's role on the Path. |
| `217` | Minfilia tells the player that she intends to open talks with the beast tribes. |

The conditional references identify these text-row keys; they do not
establish which conditions were true, what the condition operators mean, or
the progression order of a historical session. The separately stored plain
`@sheet` list in column `28` names rows `251`, `242`, `215`, `252`, and `253`;
the available sources do not explain why it differs from the active-text
references, so the two lists should not be conflated. This static-data
finding does not independently associate row `110016` with a script path.

Sources: `xivl-client-data:csv/xtx_quest.csv` row `110016`, physical line
`19`, columns `14` and `28`, SHA-256
`938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719`
(`manifests/tables.json:6267-6271`); and
`xivl-client-data:csv/xtx_journalxtxWil.csv` rows `214`-`217` and `242`,
SHA-256 `80da9c607d81f58dc7c7a9625ecd4f6cefaba32bb3448c73f85c3c8082bdd694`
(`manifests/tables.json:6195-6199`). Both are from extraction
`2012.09.19.0001`. Integer decoding provenance: `xivl-tools` revision
`be64c2842afb6b8937601fa1f1fddd2adac4ca69`,
`src/formats/src/richstring.rs` and `docs/formats/ssd-sheet.md`.
