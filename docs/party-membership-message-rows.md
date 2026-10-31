# Party membership message rows

The retail 1.23b sheets contain distinct leave, oust, disband and leader-change
text. The recovered commands establish request inputs, but no inspected caller
joins these outcome rows to a request, ordered typed reply parameters, recipient
set or message type. Text addressed to "you" does not establish its delivery.

## Outcome rows

`worldMaster.csv`, English column `1` (physical field index 2), contains:

| Operation | Row / physical line | Text, using the exact control aliases below |
| --- | --- | --- |
| Leave | 30405 / 625 | You leave the party. |
| Leave | 30411 / 631 | `H Gleave` the party. |
| Leave | 30431 / 651 | `Sleave` the party. |
| Oust | 30404 / 624 | `H Gare` ousted from the party. |
| Oust | 30410 / 630 | You are ousted from the party. |
| Oust | 30428 / 648 | `Sare` ousted from the party. |
| Disband | 30401 / 621 | The party disbands. |
| Leader change | 30408 / 628 | `H Gare` promoted to party leader. |
| Leader change | 30429 / 649 | `Sare` promoted to party leader. |

The aliases are lossless substitutions for these complete source controls:

```text
H = [@head:022b37ff35020831e4eb02eb04ff04796f75ff25020821e909ff1b023117ff107874782f646973706c61794e616d6503e909020203eb04030303]
Gare = [@if:02080fe4eb02eb04ff04617265ff03697303]
Gleave = [@if:020815e4eb02eb04ff066c65617665ff076c656176657303]
Sare = [@if:02081ae4ea02eb02ff08596f7520617265ff0a022903ea020320697303]
Sleave = [@if:020820e4ea02eb02ff0a596f75206c65617665ff0e022903ea0203206c656176657303]
S = [@string:022903ea0203]
```

`H` retains a nested `xtx/displayName` reference with expression `E9 09` and
conditions containing `EB 02` / `EB 04`. `Sare` and `Sleave` retain the string
expression `EA 02` and conditional `EB 02`. These are source expressions,
not demonstrated actor IDs, names or typed network operands. In particular,
the actor-shaped and string-shaped rows are not proved to follow the request's
actor/name alternatives.

## Refusal vocabulary

These are sheet text, with no bound operation-result caller or delivery:

| Rows / physical lines | Literal meaning / controls |
| --- | --- |
| 30501 / 670; 30530 / 699 | The party cannot be disbanded. No controls. |
| 30527 / 696 | There is only one party member. No controls. |
| 30528 / 697 | Your party must disengage before you can remove party members. No controls. |
| 30529 / 698 | You are not in a party. No controls. |
| 30531 / 700 | Your party must disengage before you can leave. No controls. |
| 30536 / 705 | That person is not a party member. No controls. |
| 30537 / 706 | `H Gare` already the party leader. |
| 30538 / 707 | You have not yet joined a party. No controls. |
| 30539 / 708 | Party leader cannot be changed while engaged. No controls. |
| 30540 / 709; 30541 / 710 | Command restricted to leader / cannot be executed by leader. No controls. |
| 30549 / 717; 30552 / 720; 30554 / 722; 30558 / 726 | The party has already disbanded. No controls. |
| 30550 / 718 | The party must disengage before disbanding. No controls. |
| 30551 / 719; 30553 / 721; 30555 / 723; 30560 / 728 | Unable to disband / leave / oust / change party leader. No controls. |
| 30556 / 724 | Unable to promote. `H` cannot be found. |
| 30557 / 725 | Unable to promote. `H Gare` not a party member. |
| 30559 / 727 | You are already the party leader. No controls. |
| 30563 / 731 | `S` is already the party leader. |
| 30566 / 734 | Unable to promote. `S` could not be found. |
| 30567 / 735; 30575 / 743 | Unable to promote / oust. `S` is not a party member. |

## Request and delivery boundary

`xivl-client-scripts:docs/linkshell-party-command-contracts.md`, "Command
inputs" and "Refusals and linkshell operation meaning", owns the proven
request contract. After the command object, PartyResign 24205 and PartyBreakup
24206 supply nine explicit nils. PartyKick 24207 and PartyLeader 24208 supply
`(name,nil^8)` or `(nil^4,target,nil^4)`. The proven direct native fallback is
MapServerbound `0x012D`, event `commandRequest`; it is an outbound request,
not an outcome message. The request serializer's string/actor/nil tags do not
type the controls above.

The scoped `canFire` predicates contain no message row. Resign requires party
count other than 1; breakup additionally requires local leadership. Kick and
leader require local leadership, count other than 1, and, for the exclusive
actor/name alternatives, a non-self member. See canonical sources
`command/system/partyresigncommand.lua:11-27`,
`partybreakupcommand.lua:11-34`, `partykickcommand.lua:11-96` and
`partyleadercommand.lua:11-96` in that repository.

A whole-corpus exact-decimal-literal search of the selected outcome and refusal
IDs found no worldMaster delivery caller in the 2671 authenticated Lua members.
The lone selected outcome-number match was `30410` in
`chara/npc/debug/populacesnpccuttestman.lua:96`, a local assignment in
`debugMenuEvent`; it is not a worldMaster text-row caller. This finite literal
search does not exclude computed row selection or native/server delivery.

For each operation, the missing join is a retail producer/receiver or retained
transaction pairing its request and group transition with a source-qualified
row, ordered typed formatter values, concrete receiving client(s), and the
actual message type. A party roster update or generic SendLog/formatter
implementation alone does not supply that join. Leadership state refresh does
not prove manual promotion or automatic succession.

## Source identity

Extraction `2012.09.19.0001`; `worldMaster.csv` is 1851138 bytes, SHA-256
`2e2e2dd5cd9651388f6fa575b4229081ad0452165e78b725df0a5b5b7cf7c643`,
authenticated against [tables.json](../manifests/tables.json). The two header
records are ` ,0,1,2,3,4,5` and ` ,str,str,str,str,,str`; select by row ID.
The archive declared by [private_csv_corpus.json](../manifests/private_csv_corpus.json)
is 70110686 bytes, SHA-256
`006f9438a8cfd9277376f0ab28474500c67e4665050aa631cae64c9e6f38a5b0`.
Read the selected members with Python `zipfile` and `csv` without corpus writes.
The Lua archive is 14385427 bytes, SHA-256
`0e8f902f7a2f592fc1220d41b89a3f35ec395cfb261806d4bd590a530099ae31`.
Lua identities match `xivl-client-scripts:manifests/scripts.json` at immutable
revision `0badc824adb353ca36ea41a61ee255a92a3231e2`. Exact selected members are
`command/system/partyresigncommand.lua`, `command/system/partybreakupcommand.lua`,
`command/system/partykickcommand.lua`, `command/system/partyleadercommand.lua`,
`widget/desktopwidget_connector.lua` and
`chara/npc/debug/populacesnpccuttestman.lua`, relative to `lua/scripts/`.
The command-contract "Input identities" table owns detailed command/helper
pins; the manifest owns the debug member and full-corpus search identity.
