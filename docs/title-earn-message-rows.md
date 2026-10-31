# Title award message and reward text

`populaceAchievement.csv` row 14 supplies the title-award sentence.
`xtx__text_ui.csv` row 12012 supplies a title-reward fragment used by the
achievement popup. Neither row assigns the player's selected title.

## Source identities

The decoded CSV extraction is retail FFXIV 1.23b `2012.09.19.0001`.
The named members match the byte counts and SHA-256 values in
[`manifests/tables.json`](../manifests/tables.json) at client-data revision
`f4bd2734570441a3721f460b85681435040b2724`:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `populaceAchievement.csv` | 116441 | `357e0ecc240ceec8e689da42458694d3a8b36b747f06595fbfa2ca6500f6ea49` |
| `xtx__text_ui.csv` | 1284564 | `23762a422118d99c4144a48b3495c52511b1b1b865e4fc50fdc61a973e3c6ece` |
| `achievement.csv` | 28895 | `3aecdc3005619b76c813318b12ba7e9b38588d0e3007811d43668a307a68243f` |
| `xtx_achievement.csv` | 297212 | `149f932d206dfb21dd271bd64c6028ead8ec4d3eb2adcc4258947863b05c85b5` |
| `xtx_title.csv` | 21050 | `490c6346ed541f78e50e78f087f8a4b01975bee7648359f6acd25ac5ca94f1e4` |

The archive identity is the one in
[`manifests/private_csv_corpus.json`](../manifests/private_csv_corpus.json):
70,110,686 bytes, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
Each selected ZIP member was read without extraction and compared with its
manifest identity. CSV numeric headers define the logical column labels.
The row ID is a separate first cell.

### Script identities

The decoded Lua source members match
`xivl-client-scripts:manifests/scripts.json` at revision
`0badc824adb353ca36ea41a61ee255a92a3231e2`, extraction `2012.09.19.0001`.
The source archive is declared by
`xivl-client-scripts:manifests/private_lua_corpus.json` as
`extracted/ffxiv-1.23b/client-scripts/lua.zip`, 14,385,427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
The following members were read from that archive and authenticated against
their canonical LF identities. Paths are relative to `lua/scripts/`.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `chara/npc/populace/populaceachievement.lua` | 26816 | `d2e9130ebfea08995b6c44ce7088ff07d099cfc50d8550c155daafe574aea63e` |
| `chara/player/playerbaseclass.lua` | 66466 | `6226b3fa15dfdbad279b7dba453f8a3b76fcb8b68bad6e14f5403d52987f76e4` |
| `widget/desktopwidget_connector.lua` | 660617 | `9c33f21c1f70a0056147e716d53300634efabe5b744ef6e8690114db21613a01` |
| `widget/achievementpopupwidget.lua` | 6172 | `5e9b0d2d5786c6737d0f447db598211c6d242a7dc23119d961b0b0c5e25ca3d8` |

The common `WorldMaster.say` and `DesktopWidget.showMessage` helper source,
original resource and decoded payload pins are recorded in
`xivl-client-scripts:docs/worldmaster-message-arguments.md`, Authenticated
input identities.

## Title-award sentence

`populaceAchievement.csv` row 14, English column 1, has the sentence
`You have been awarded the title [title] for completing the [achievement] achievement!`
The square-bracket names summarize its rich-string references. The cell
contains U+201C and U+201D around the title.

The achievement reference names `xtx/achievement`, uses `E8 02` for its row
and literal `09` for logical field 8. Each title alternative names
`xtx/title` and uses `E8 03` for its row. The English alternatives select
logical fields 4 and 3. The enclosing `if` condition is `E9 05`, which uses
the decoder's own vector, rather than the supplied formatter vector.
Its contextual meaning is not established here. The formatter's one-based
integer-reference rule is owned by
`xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md`, argument
reference section, VAs `0x00CB2D50` and `0x00778D50`.

The recovered `PopulaceAchievement.initForEvent` calls
`self:_loadTextDataPermanently(8000,"populaceAchievement")` at
`xivl-client-scripts:lua/scripts/chara/npc/populace/populaceachievement.lua:26-30`.
The native loader's adjusted key is conditionally `0x03A21F40`; its successful
named-sheet and receiver-lifetime conditions are recorded in
`xivl-decomp:docs/script/actor-base-text-source.md`, callback `0x006E7500`.
This is a static association, not proof that a historical client loaded it.

`PopulaceAchievement.eventReward(self,A1,A2,A3,A4)` obtains the local player
and starts `startCliantTalkTurn(2,localPlayer)` before its reward text.
The actor-specific dialogue block is conditional on `A4 == false`.
At lines 1141-1158, exactly `A2 == true` selects item row 13. Every other
value follows the row-14 branch. That branch supplies:

```text
WorldMaster.say(worldMaster, self, 14, A1, A3)
DesktopWidget.showMessage(desktopWidget, worldMaster, 40, self, 14, A1, A3)
DesktopWidget._appendMessagePool(desktopWidget, worldMaster, 40, self, 14, A1, A3)
```

The two helper bodies preserve all supplied variadic arguments and discard
results. Their original bytecode is qualified by
`xivl-client-scripts:docs/worldmaster-message-arguments.md`, Generic argument
route. Literal 40 is the supplied message category value; no category enum
name is assigned here. `finishCliantTalkTurn()` follows the selected `say`
call at lines 1160-1162. This is script call order, not observed rendering or
message dismissal order. The native message callback requests a yield, so
the helpers' lack of a Lua wait does not establish synchronous completion.

The registered native path is conditionally qualified by
`xivl-decomp:docs/script/worldmaster-message-pool.md`, callback `0x006ECED0`,
worker `0x006E8360`, WorldMaster sink `0x00772650` and source lookup
`0x007722A0`. It preserves the supplied NPC as text owner, row 14 and the
ordered tail. When A1 and A3 take the accepted integer-capture paths, they
become formatter integer arguments 1 and 2, supplying the achievement and
title row keys respectively. The source does not establish their runtime
types or values. It does not load the title from the selected-title field.

This call routes to the recipient client's desktop. It does not establish a
server broadcast audience or which clients receive an event. No inspected
source joins this NPC event's invocation to receipt of opcode `0x019E`, or
orders row 14 before or after that receipt.

## Achievement popup fragment

`PlayerBaseClass._onReceiveAchievementId` forwards its two arguments to
`desktopWidget:showAchievementPopup` at
`xivl-client-scripts:lua/scripts/chara/player/playerbaseclass.lua:2962-2972`.
`DesktopWidget.showAchievementPopup` retrieves static widget 24 and invokes
`setAchivement(A1,A2)` at `widget/desktopwidget_connector.lua:24967-24977`.
The spelling `setAchivement` is the recovered identifier.

`AchievementPopupWidget.setAchivement` saves its second argument as
`work.unlockFlag` and calls
`loadSpreadSheetDataAsync(achievementSheet,achievementId,achievementId)`
at `widget/achievementpopupwidget.lua:52-64`. In the resulting
`processSpreadSheetDataAsync` callback:

| Condition | Text supplied |
| --- | --- |
| `unlockFlag == false` | Name row 12015 with the achievement ID. If sheet column 5 is nonzero, item row 12013 takes priority. Otherwise a nonzero title in column 3 selects reward row 12012 with title ID and selector 0 or 1 from the local player's `isFemale()` result. |
| Any other `unlockFlag` value | Name row 12020 with the achievement ID, normal style, no points and no reward. |

Row 12012's English column 1 begins `Title Reward:` and carries two
`xtx/title` alternatives. It is a reward fragment assigned to
`Achievement_Maker`, row 0, attribute `reward`, with the title ID and
explicit selector as arguments. It is not a standalone success sentence or
log message. The callback then calls `updateListProperty("Achievement_Maker")`,
`sendCommand("UIFormCommands.TimerStart")` and `show()` in that order at
lines 250-260. Its `UIFormCommands.TimerFinish` handler calls `hide()` at
lines 40-49. These are recovered script operations, not measured display
durations.

The tracked native finding
`xivl-decomp:docs/script/player-achievement-titles.md`, Available-title storage
and ordering and notification ordering constraint, establishes that the
`0x019E` handler writes achievement state before its filtered Lua callback.
It does not establish the callback's second argument for each admitted ID.
The popup branch therefore remains conditional on the supplied flag.

## Availability and selected title

The established `0x019E` path inserts an admitted nonzero title into the
available-title tree without selecting it. The separate `0x019A`
initialization path constructs availability from achievement bits.
Selection writes `PlayerBase+0xE8`: the list's native setter writes locally
before building c2s `0x0134`, and incoming s2c `0x019D` writes the same field.
Those paths are owned by
`xivl-decomp:docs/script/player-achievement-titles.md`, Available-title storage
and ordering and Native request and incoming state. The text rows and popup
do not establish server award criteria, persistence, acceptance of a selected
title, or native nameplate formatting.

## Achievement display-name join

The 208 title-linked achievement IDs in
`xivl-decomp:config/achievement_title_map.json` each have an equal-ID row in
`xtx_achievement.csv`. Its English achievement name is logical column 8,
excluding the row ID. The referenced title key independently selects
`xtx_title.csv` logical columns 3 and 4 for English selector-0 and selector-1
strings. These are source-name joins; completion ordinals, predicate parents,
title eligibility and award conditions remain separate domains in the native
achievement/title maps cited above.

Sources: `csv/xtx_achievement.csv` column 8 and `csv/xtx_title.csv` columns
3/4, with the complete member identities in
[tables.json](../manifests/tables.json), extraction `2012.09.19.0001`.
