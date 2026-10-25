# Grand Company quest identities

The retail static-actor catalog contains 102 IDs whose class paths belong to
the `Com`, `Gcg`, `Gcl` and `Gcu` scenario families. Joining those IDs directly
to `xtx_quest.csv` column 2 yields 69 named English entries and 33 literal
`\[en]` placeholders. These are retained client rows, not proof that every
entry was playable or that every resource defines a complete quest.

The 102 IDs select 92 distinct scenario resources. Five `Gcl` classes each
serve three company-specific IDs. Ten retained `Gcg`/`Gcu` resources have
no ID pointing to them in this complete SAN catalog. Resource presence and
static-actor selection must therefore remain separate.

## Shared classes

| Client class | Static actor IDs | English title family |
| --- | --- | --- |
| `Gcl101` | 111416, 111616, 111816 | It Kills with Fire |
| `Gcl104` | 111430, 111630, 111830 | In for Garuda Wakening |
| `Gcl105` | 111431, 111631, 111831 | Don't Hate the Messenger |
| `Gcl106` | 111432, 111632, 111832 | United We Stand |
| `Gcl107` | 111433, 111633, 111833 | To Kill a Raven |

Each class in this table has the prefix `/Quest/Scenario/Gcl/`. The IDs
retain their separate Limsa Lominsa, Gridania and Ul'dah title cells. They
are not three independent client implementations merely because the
corresponding `Gcg` and `Gcu` files also exist.

The unselected resources are `Gcg101`, `Gcg104`, `Gcg105`, `Gcg106`,
`Gcg107`, `Gcu101`, `Gcu104`, `Gcu105`, `Gcu106` and `Gcu107`, in their
respective scenario families. This is a bounded absence from the SAN
catalog, not proof that no other resource-loading path can address them.

## Sources and reproduction

`manifests/staticactor_class_paths.json` owns the actor-ID/class-path map.
Its complete 2,812 records were reproduced with
`tools/extract_staticactor_san.py:parse_san` from
`client/script/rq9q1797qvs.san`, 108,911 bytes, SHA-256
`bb7306461b1728493242016a16d9dd5257d7512c60e423b017de5ec7aced3d14`.
The parser checks the declared record count, record boundaries, duplicate
IDs and trailing bytes. The decoded record list equalled the catalog.

Select the four exact path prefixes `/Quest/Scenario/Com/`,
`/Quest/Scenario/Gcg/`, `/Quest/Scenario/Gcl/` and
`/Quest/Scenario/Gcu/`. Join each selected numeric ID to the row ID of
`csv/xtx_quest.csv`; derive column 2's position from its numeric header.
All selected IDs have a matching row. The 2,953,504-byte sheet has SHA-256
`938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719`,
as pinned by `manifests/tables.json`.

The resource comparison used
`xivl-client-scripts:data/quest_contracts.json`, selecting its 102
`grand-company` records. Each record's class declaration was checked against
`xivl-client-scripts:lua/registry.json`, and every selected decoded source
matched its byte length and SHA-256 in
`xivl-client-scripts:manifests/scripts.json`. The existing contract's input
hashes matched its four named manifests. No new original-bytecode analysis
is implied by this identity comparison.

The existing script contract deliberately retains a null singular
`questId`; it does not consume the SAN ownership input. This page records
the one-to-many selection separately. It does not mutate that generated
contract or reinterpret null as absence of a client actor ID.

For resource-method coverage and the client/server boundary, see
`xivl-client-scripts:docs/gc-quest-recoverability.md` and
`xivl-client-scripts:docs/quest-script-inventory.md`. IDs and title cells do
not establish event dispatch, objectives, eligibility, encounter behavior,
reward settlement or historical invocation.

## Complete selected catalog

Titles below preserve the English cells, including placeholder spelling.

| Static actor ID | English title | Client class |
| ---: | --- | --- |
| 111401 | The Price of Integrity | `/Quest/Scenario/Com/Com0l1` |
| 111402 | Testing the Waters | `/Quest/Scenario/Com/Com0l2` |
| 111403 | Seals for the Whorl | `/Quest/Scenario/Com/Com0l3` |
| 111404 | Engineering Victory | `/Quest/Scenario/Com/Com0l4` |
| 111405 | An Officer and a Wise Man | `/Quest/Scenario/Com/Com0l5` |
| 111406 | Ceruleum Shock | `/Quest/Scenario/Com/Com0l6` |
| 111407 | Till Sea Swallows All | `/Quest/Scenario/Com/Com0l7` |
| 111408 | `\[en]` | `/Quest/Scenario/Com/Com0l8` |
| 111409 | `\[en]` | `/Quest/Scenario/Com/Com0l9` |
| 111410 | Imperial Devices (Limsa Lominsa) | `/Quest/Scenario/Com/Com5l0` |
| 111411 | Into the Dark (Limsa Lominsa) | `/Quest/Scenario/Com/Com5l1` |
| 111412 | `\[en]` | `/Quest/Scenario/Com/Com5l2` |
| 111413 | `\[en]` | `/Quest/Scenario/Com/Com5l3` |
| 111414 | `\[en]` | `/Quest/Scenario/Com/Com5l4` |
| 111415 | `\[en]` | `/Quest/Scenario/Com/Com5l5` |
| 111416 | It Kills with Fire (Limsa Lominsa) | `/Quest/Scenario/Gcl/Gcl101` |
| 111417 | The Cove | `/Quest/Scenario/Gcl/Gcl301` |
| 111418 | Saving the Stead Instead | `/Quest/Scenario/Gcl/Gcl302` |
| 111419 | It's a Piece of Cake to Bake a Poison Cake | `/Quest/Scenario/Gcl/Gcl303` |
| 111420 | Kobold and the Beautiful | `/Quest/Scenario/Gcl/Gcl304` |
| 111421 | `\[en]` | `/Quest/Scenario/Gcl/Gcl501` |
| 111422 | `\[en]` | `/Quest/Scenario/Gcl/Gcl502` |
| 111423 | `\[en]` | `/Quest/Scenario/Gcl/Gcl601` |
| 111424 | `\[en]` | `/Quest/Scenario/Gcl/Gcl602` |
| 111425 | `\[en]` | `/Quest/Scenario/Gcl/Gcl603` |
| 111426 | Oil Crisis | `/Quest/Scenario/Gcl/Gcl305` |
| 111427 | Alive | `/Quest/Scenario/Gcl/Gcl102` |
| 111428 | The Weakest Link | `/Quest/Scenario/Gcl/Gcl701` |
| 111429 | Deus ex Machina | `/Quest/Scenario/Gcl/Gcl103` |
| 111430 | In for Garuda Wakening (Limsa Lominsa) | `/Quest/Scenario/Gcl/Gcl104` |
| 111431 | Don't Hate the Messenger (Limsa Lominsa) | `/Quest/Scenario/Gcl/Gcl105` |
| 111432 | United We Stand (Limsa Lominsa) | `/Quest/Scenario/Gcl/Gcl106` |
| 111433 | To Kill a Raven (Limsa Lominsa) | `/Quest/Scenario/Gcl/Gcl107` |
| 111434 | Patrol, Interrupted | `/Quest/Scenario/Gcl/Gcl702` |
| 111601 | Breaking the Seals | `/Quest/Scenario/Com/Com0g1` |
| 111602 | Why Did It Have to Be Snakes | `/Quest/Scenario/Com/Com0g2` |
| 111603 | Adder's Nest Egg | `/Quest/Scenario/Com/Com0g3` |
| 111604 | The Mail Must Get Through | `/Quest/Scenario/Com/Com0g4` |
| 111605 | Their Finest Hour | `/Quest/Scenario/Com/Com0g5` |
| 111606 | Appetite for Destruction | `/Quest/Scenario/Com/Com0g6` |
| 111607 | Serenity, Purity, Sanctity | `/Quest/Scenario/Com/Com0g7` |
| 111608 | `\[en]` | `/Quest/Scenario/Com/Com0g8` |
| 111609 | `\[en]` | `/Quest/Scenario/Com/Com0g9` |
| 111610 | Imperial Devices (Gridania) | `/Quest/Scenario/Com/Com5g0` |
| 111611 | Into the Dark (Gridania) | `/Quest/Scenario/Com/Com5g1` |
| 111612 | `\[en]` | `/Quest/Scenario/Com/Com5g2` |
| 111613 | `\[en]` | `/Quest/Scenario/Com/Com5g3` |
| 111614 | `\[en]` | `/Quest/Scenario/Com/Com5g4` |
| 111615 | `\[en]` | `/Quest/Scenario/Com/Com5g5` |
| 111616 | It Kills with Fire (Gridania) | `/Quest/Scenario/Gcl/Gcl101` |
| 111617 | Eternal Recurrence | `/Quest/Scenario/Gcg/Gcg301` |
| 111618 | The Pen Is Mightier Than the Spear | `/Quest/Scenario/Gcg/Gcg302` |
| 111619 | Woes of the Botanist | `/Quest/Scenario/Gcg/Gcg303` |
| 111620 | Gone with the Wind | `/Quest/Scenario/Gcg/Gcg304` |
| 111621 | `\[en]` | `/Quest/Scenario/Gcg/Gcg501` |
| 111622 | `\[en]` | `/Quest/Scenario/Gcg/Gcg502` |
| 111623 | `\[en]` | `/Quest/Scenario/Gcg/Gcg601` |
| 111624 | `\[en]` | `/Quest/Scenario/Gcg/Gcg602` |
| 111625 | `\[en]` | `/Quest/Scenario/Gcg/Gcg603` |
| 111626 | A Taste for Death | `/Quest/Scenario/Gcg/Gcg305` |
| 111627 | Two Vans are Better than One | `/Quest/Scenario/Gcg/Gcg102` |
| 111628 | You Don't Have the Rite | `/Quest/Scenario/Gcg/Gcg701` |
| 111629 | Shadow of the Raven | `/Quest/Scenario/Gcg/Gcg103` |
| 111630 | In for Garuda Wakening (Gridania) | `/Quest/Scenario/Gcl/Gcl104` |
| 111631 | Don't Hate the Messenger (Gridania) | `/Quest/Scenario/Gcl/Gcl105` |
| 111632 | United We Stand (Gridania) | `/Quest/Scenario/Gcl/Gcl106` |
| 111633 | To Kill a Raven (Gridania) | `/Quest/Scenario/Gcl/Gcl107` |
| 111634 | Cure for the Common Pox | `/Quest/Scenario/Gcg/Gcg702` |
| 111801 | Career Opportunities | `/Quest/Scenario/Com/Com0u1` |
| 111802 | Kindling a Flame | `/Quest/Scenario/Com/Com0u2` |
| 111803 | Burning a Hole in One's Pocket | `/Quest/Scenario/Com/Com0u3` |
| 111804 | Arms Race | `/Quest/Scenario/Com/Com0u4` |
| 111805 | Burning Man | `/Quest/Scenario/Com/Com0u5` |
| 111806 | Know Your Enemy | `/Quest/Scenario/Com/Com0u6` |
| 111807 | By Fire Reborn | `/Quest/Scenario/Com/Com0u7` |
| 111808 | `\[en]` | `/Quest/Scenario/Com/Com0u8` |
| 111809 | `\[en]` | `/Quest/Scenario/Com/Com0u9` |
| 111810 | Imperial Devices (Ul'dah) | `/Quest/Scenario/Com/Com5u0` |
| 111811 | Into the Dark (Ul'dah) | `/Quest/Scenario/Com/Com5u1` |
| 111812 | `\[en]` | `/Quest/Scenario/Com/Com5u2` |
| 111813 | `\[en]` | `/Quest/Scenario/Com/Com5u3` |
| 111814 | `\[en]` | `/Quest/Scenario/Com/Com5u4` |
| 111815 | `\[en]` | `/Quest/Scenario/Com/Com5u5` |
| 111816 | It Kills with Fire (Ul'dah) | `/Quest/Scenario/Gcl/Gcl101` |
| 111817 | Prying Eyes | `/Quest/Scenario/Gcu/Gcu301` |
| 111818 | Different Strokes | `/Quest/Scenario/Gcu/Gcu302` |
| 111819 | A Weaver and a Mummer | `/Quest/Scenario/Gcu/Gcu303` |
| 111820 | When Alchemists Cry | `/Quest/Scenario/Gcu/Gcu304` |
| 111821 | `\[en]` | `/Quest/Scenario/Gcu/Gcu501` |
| 111822 | `\[en]` | `/Quest/Scenario/Gcu/Gcu502` |
| 111823 | `\[en]` | `/Quest/Scenario/Gcu/Gcu601` |
| 111824 | `\[en]` | `/Quest/Scenario/Gcu/Gcu602` |
| 111825 | `\[en]` | `/Quest/Scenario/Gcu/Gcu603` |
| 111826 | Challenge Accepted | `/Quest/Scenario/Gcu/Gcu305` |
| 111827 | Like Father, Like Son | `/Quest/Scenario/Gcu/Gcu102` |
| 111828 | Gore a Lizard, Hurry | `/Quest/Scenario/Gcu/Gcu701` |
| 111829 | Careless Whispers | `/Quest/Scenario/Gcu/Gcu103` |
| 111830 | In for Garuda Wakening (Ul'dah) | `/Quest/Scenario/Gcl/Gcl104` |
| 111831 | Don't Hate the Messenger (Ul'dah) | `/Quest/Scenario/Gcl/Gcl105` |
| 111832 | United We Stand (Ul'dah) | `/Quest/Scenario/Gcl/Gcl106` |
| 111833 | To Kill a Raven (Ul'dah) | `/Quest/Scenario/Gcl/Gcl107` |
| 111834 | Mess with the Goat, Get the Horns | `/Quest/Scenario/Gcu/Gcu702` |
