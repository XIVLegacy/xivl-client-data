# Quest-offer level-gating findings

Sweep date: 2026-08-14. Corpus: extraction `2012.09.19.0001`, game version
`1.23b` (`xivl-client-data:manifests/manifest.json`). CSV column numbers below
were zero-based sheet columns after the row id.

## Requirement fields

The quest sheet exposed one scalar `s32` level-like field at column 51. The
following fields were typed separately as `s32`, `s32`, `bool`, and `bool` at
columns 52-55 (`xivl-client-data:csv/quest.csv:rows 0-1, columns 51-55`). The
quest detail widget read columns 51-54, but its only later use of column 51
passed that value to `calcSkillPoint` while rendering reward text
(`xivl-client-scripts:lua/scripts/widget/ask/questdetailwidget.lua:584-615`,
`xivl-client-scripts:lua/scripts/widget/ask/questdetailwidget.lua:761-790`).
The condition path separately used columns 53-54 for condition/repeat and
company-rank display state (`xivl-client-scripts:lua/scripts/widget/ask/questdetailwidget.lua:454-581`).
Thus columns 52-55 did not provide a second class-level requirement matrix.

The level interpretation was corroborated by the class labels in
`xtx_quest`: the unrestricted row had `c51=1` and label `All`, while broad
discipline rows had `c51=45`/`18` and labels `Disciples of War or Magic`,
`Disciples of the Land`, and `Disciples of the Hand (Excluding Culinarians)`
(`xivl-client-data:csv/quest.csv:rows 110001, 110627, 110813-110814, column 51`,
`xivl-client-data:csv/xtx_quest.csv:rows 110001, 110627, 110813-110814, columns 40-41`).

## Cross-discipline and named-class rows

The job-quest rows paired the same scalar with an explicit named class and
level: Marauder level 30 (`111201`), Warrior levels 35, 40, 45, 45, and 50
(`111202`-`111206`), and level-30 Pugilist, Conjurer, Thaumaturge,
Gladiator, Archer, and Lancer rows with a named secondary class
(`111221`, `111241`, `111261`, `111281`, `111301`, `111321`). Their quest-sheet
values were `c51=30`, `35`, `40`, `45`, or `50`, matching the English labels
(`xivl-client-data:csv/quest.csv:rows 111201-111206, 111221-111321, column 51`,
`xivl-client-data:csv/xtx_quest.csv:rows 111201-111206, 111221-111321, columns 40-41`).

## Form verdict and limit

The extracted form was discipline-scoped for the broad labels and named-class
for the job rows. It was not an active-class or highest-attained-class matrix:
the sheet carried one scalar level and a text scope, not per-class level slots.
The client scripts exposed only a generic quest getter
(`xivl-client-scripts:lua/scripts/quest/questbaseclass.lua:17-29`); the inspected
offer/detail path did not compare that scalar with an active class, a named
class, or the player's highest attained level. The runtime choice between
active-class and highest-attained semantics therefore remained insufficient-data.

The reward-side use was consistent with a level key: `calcSkillPoint` passed its
first argument to `getSkillPointMax`, whose hardcoded tables were indexed by
level (`xivl-client-scripts:lua/scripts/chara/player/player_work.lua:675-689`,
`xivl-client-scripts:lua/scripts/chara/charabaseclass_battle.lua:1895-2027`).
That corroborated the scalar's level role but did not establish offer
eligibility semantics.
