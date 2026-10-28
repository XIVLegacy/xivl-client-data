# Party content restrictions and message rows

The recovered client party helper refuses content property 1 by returning
false. That branch supplies no refusal text row. Separate content-group
initialization/finalization callers request rows 50011/50012 through local
WorldMaster notify with literal log type 32. Those notifications do not prove
party-operation refusal, server enforcement or a departure's cause.

## Property and local guard

`xivl-client-scripts:lua/scripts/chara/charabaseclass.lua:21-49`,
`isRestrictedByContents(self,index)`, visits the list returned by
`self:_getAllGroup()` and returns true when a returned `ContentGroupBaseClass`
reports `isPropertyEnabled(index)`. This loop has no Lua membership test.
The latter method
returns `contentGroupWork.property[index]`
(`group/contentgroup/contentgroupbaseclass.lua:11-19`). Initialization declares
that property as 32 booleans (`:22-50`). The index is a Lua property index;
no wire offset or authoritative server restriction is assigned here.

`widget/desktopwidget_connector.lua:14208-14228`, `canPartyCommand`, gets the
local player and tests `isRestrictedByContents(1) == true`. True returns false;
otherwise it returns true. The complete helper has no notify, alert, message
row or formatter arguments. Its use differs by issuer:

| DesktopWidget issuer | Calls `canPartyCommand` before submission? | Source lines |
| --- | --- | --- |
| Invite by name / actor, 24203 | Yes | 14230-14303 |
| Resign, 24205 | Yes | 14307-14322 |
| Kick by name / actor, 24207 | Yes | 14326-14366 |
| Breakup, 24206 | Yes | 14370-14385 |
| Join, 24204 | No; directly calls `executePlayerCommandLocal` | 17745-17756 |
| Leader, 24208 through `executePlayerSystemCommand` | No | 13791-13978 |

Thus property 1 prevents the guarded helper submissions without emitting a
refusal row from those bodies. `executePlayerCommandLocal` itself forwards
to `executeCommand` without adding the property guard (`:13454-13477`).

The generic `executePlayerSystemCommand` route used for PartyLeader 24208
does not call `canPartyCommand` (`:13791-13978`). Its failed `canCommand` branch
calls `alertCommandError(command,0)` (`:13942-13961`); that is a separate generic
command-error path, not evidence that content property 1 blocked leadership.
The invite/join/resign/kick/breakup/leader class `canFire` bodies likewise do
not test the content property. Invite tests local leadership, party membership
and relation group 50001; join tests the local party count and target's absence
from that party (`command/system/partyinvitecommand.lua:11-83`,
`partyjoincommand.lua:11-70`). Do not extend the ordinary helper's guard into
a claim about every issuer or server handling.

The Lua invocation uses the object returned by `_getMyPlayer`, then tests the
returned group list and property values. It does not itself establish that
every returned group contains that receiver. The native qualification in
`xivl-client-structs:docs/chara-world-native-contract.md`, "Group list",
states that `_getAllGroup` callback `0x00708430` never reads its receiver.
It calls `0x00701250` with flag 0; the omitted-argument path uses identity
address `ExecuteParameters +0x0C` through `0x006C5840`. Registry enumeration
`0x006C46F0` appends records when predicate `0x006C3B30` returns nonzero.
That predicate's membership role is explicitly `INFERRED`; the association
between this native identity and the Lua local-player receiver is not proved
by the callback. The cited document's "Binary and method" section owns the
retail executable and analysis pins.

The guard does not inspect the target or another party member's
`currentContentGroup`. That separate
getter reads `charaWork.currentContentGroup`, returns nil for zero, and otherwise
calls `_getExtendedTemporaryGroup` (`chara/charabaseclass.lua:143-159`). Neither
the guarded helper nor the six scoped class predicates calls that getter or
checks remote members' content state. A remote member-in-content refusal or
server rule therefore remains unbound by this evidence.

The content restriction refresh calls `processUpdateMyPlayerRestrictionByContents`,
whose body calls only `updateMainMenuWidget` (`:6125-6135`). Content work
`_init` or `contentGroupWork/property` updates refresh it (`contentgroupbaseclass.lua:165-181`).
No inspected body binds property 1 to a specific content category, content
admission rule or server restriction writer.

## Proven notification callers

`worldMaster.csv`, English column `1`, contains these literal cells:

| Row / physical line | Text | Controls |
| --- | --- | --- |
| 50011 / 1748 | You are now bound by duty. | None |
| 50012 / 1749 | You are no longer bound by duty. | None |

`ContentGroupBaseClass.init` requests 50011 only when its explicit
`_isMember(localPlayer)` test succeeds and `_getKind()` is 30001 or 30006
(`:86-110`). `_onFinalize` requests 50012 under the same explicit
`_isMember(localPlayer)` and kind condition (`:352-376`). These lifecycle
membership tests are separate from the property guard's group-list loop.
The bytecode
qualification already published in
`xivl-client-scripts:docs/guildleve-party-continuity.md`, "Content group and
party are separate state", covers init `root/proto1`, PCs 47-66 and finalize
`root/proto6`, PCs 0-61, chunk `0xADD..0xBD1`.

The exact ordered call values, including each method receiver, are:

```text
notify(worldMaster, worldMaster, row)
showLog(desktopWidget, worldMaster, 32, worldMaster, row)
_appendLogPool(desktopWidget, worldMaster, 32, worldMaster, row)
```

There are no supplied formatter-tail values. WorldMaster is both the notify
receiver and explicit text provider. The call is made in the executing local
client when its membership condition succeeds; no party-wide server recipient
set is established. Literal 32 is the proven Lua log type, not a separately
observed wire type or an assigned human-readable enum.

`world/worldmaster_event.lua:127-140` supplies 32 and forwards the tail;
`widget/desktopwidget.lua:387-402` forwards to `_appendLogPool`.
`xivl-client-scripts:docs/worldmaster-message-arguments.md`, "Countdown log
arguments", proves open-tail forwarding and the separate log-pool native
route. Its source/provider/formatter readiness conditions still apply.
`xivl-client-structs:docs/talk-native-contract.md`, "Message and log pools",
owns registrar `0x00744020`, callback `0x006ECF80` and shared worker
`0x006E8360` with flag 0. These conditional paths do not prove rendering or
historical delivery. The init/finalize kind check does not inspect property 1,
and a party leave/kick/leader operation is not proved to cause finalization.

## Refusal-row boundary

No specific content-lock refusal row is established for invite, join, leave,
kick, breakup or leader change. The party sheet's invite/join combat refusals
are separate vocabulary:

| Operation | Row / physical line | Literal text using the exact control aliases below |
| --- | --- | --- |
| Join | 30503 / 672 | You must disengage before joining a party. No controls. |
| Invite | 30509 / 678 | Unable to invite. You are engaged in battle. No controls. |
| Invite | 30510 / 679 | Unable to invite. `P` is engaged in battle. |
| Invite | 30518 / 687 | Your party must disengage before you may invite new members. No controls. |
| Join | 30547 / 715 | Unable to join. `H` is engaged in battle. |
| Invite | 30562 / 730 | `S` must disengage from combat before inviting. |
| Join | 30570 / 738 | Unable to join. You are engaged in battle. No controls. |
| Join | 30571 / 739 | Unable to join. `HS` is engaged in battle. |

```text
P = [@head:022b48ff46020842e4eb02eb04ff05796f7572ff35020831e4eb02eb04ff04796f75ff25020821e909ff1b023117ff107874782f646973706c61794e616d6503e909020203eb0403030303]
H = [@head:022b37ff35020831e4eb02eb04ff04796f75ff25020821e909ff1b023117ff107874782f646973706c61794e616d6503e909020203eb04030303]
S = [@string:022903ea0203]
HS = [@head:022b09ff07022903ea020303]
```

These retain the `xtx/displayName` reference and `E9 09` / `EB 02` / `EB 04`
expressions in `P`/`H`, and `EA 02` in `S`/`HS`. They do not establish typed
reply parameters. Other party refusals include generic join failures 30505,
30506, 30514, 30548, disbanded-party 30545 and different-area 30574; generic
invite 30519, 30544, 30565, full-party 30561, existing invitation 30543/30564,
already-in-party 30568 and pending-invitation 30569. None is bound here to
content property 1. The leave/kick/leader/disband combat rows are 30531,
30528, 30539 and 30550, with no controls.

The finite text inspection read English column `1` of authenticated
`worldMaster.csv` and `xtx__text_ui.csv`, matching case-insensitive
`party|group|invite|invitation|join|recruit|duty|bound|content`, and inspected the
party refusal block 30501-30579 by row ID. It established no invite/join
content-lock refusal row/caller. A whole-corpus exact-decimal-literal search
for the eight combat rows above and the other selected invite/join refusals
found no match in the 2671 authenticated Lua members. These searches do not
exclude computed row selection or native/server delivery. Neither combat
wording nor a generic refusal establishes the content guard or server test.

The next discriminator is a retail caller or retained outcome transaction
joining the attempted operation and property state to a source-qualified
refusal row, its ordered typed formatter values, recipients and actual message
type. For server enforcement, the transaction must also distinguish a client
suppression from a submitted request and server refusal. No generic formatter
or group callback can substitute for that edge.

## Source identity

Extraction `2012.09.19.0001`; `worldMaster.csv` is 1851138 bytes, SHA-256
`2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643`,
authenticated against [tables.json](../manifests/tables.json). English column
`1` is physical field index 2. The archive declared by
[private_csv_corpus.json](../manifests/private_csv_corpus.json) is 70110686 bytes,
SHA-256 `006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
The Lua archive declared by `xivl-client-scripts:manifests/private_lua_corpus.json`
is 14385427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Selected member hashes match `xivl-client-scripts:manifests/scripts.json` at
immutable revision `0badc824adb353ca36ea41a61ee255a92a3231e2`.
The exact selected Lua members, relative to `lua/scripts/`, are:

- `chara/charabaseclass.lua`
- `group/contentgroup/contentgroupbaseclass.lua`
- `widget/desktopwidget_connector.lua`
- `widget/desktopwidget.lua`
- `world/worldmaster_event.lua`
- `command/system/partyinvitecommand.lua`
- `command/system/partyjoincommand.lua`
- `command/system/partyresigncommand.lua`
- `command/system/partykickcommand.lua`
- `command/system/partybreakupcommand.lua`
- `command/system/partyleadercommand.lua`

Detailed per-member source pins remain in
`xivl-client-scripts:docs/linkshell-party-command-contracts.md`, "Input identities",
`docs/guildleve-party-continuity.md`, "Original inputs and tools", and
`docs/worldmaster-message-arguments.md`, "Authenticated input identities".
Those findings also own their original-bytecode and native-input identities.
Reproduce by reading the authenticated archive members without changing the
corpus. Text scans are finite source observations, not runtime delivery checks.
