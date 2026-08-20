# Quest-offer level-gating findings

Sweep date: 2026-08-15. Corpus: extraction `2012.09.19.0001`, game version
`1.23b` (`xivl-client-data:manifests/manifest.json`). CSV column numbers below
are zero-based sheet columns after the row id.

## Verdict: (a), active class or current job

Retail 1.23b quest data pairs one scalar level with an eligibility label that
restricts the class or job currently undertaking the quest. The scope varies
by row: ordinary quests can allow all classes or a discipline family, while
class and job quests name one class or job. This is active-class/current-job
level form, not highest-attained level across the character.

The strongest discriminator is the job-quest series. Quest `111201` has
column 51 = `30` and the English eligibility text `Marauder, level 30 &
Gladiator`. Quests `111202`-`111206` have column 51 = `35`, `40`, `45`, `45`,
and `50`. They pair with `Warrior, Level N & Gladiator`. The other job unlocks
repeat the form for Pugilist, Conjurer, Thaumaturge, Gladiator, Archer, and
Lancer at level 30 (`xivl-client-data:csv/quest.csv:rows 111201-111206,
111221,111241,111261,111281,111301,111321, column 51`;
`xivl-client-data:csv/xtx_quest.csv:same rows, columns 40-41`). A level held by
an unrelated class cannot satisfy those named forms. That rules out (d).

Discipline-wide rows use the same scalar but broaden the eligible current
class. `Ifrit Bleeds, We Can Kill It` has column 51 = `45` and `Disciples of
War or Magic`; `Joining the Spirit` and `Waking the Spirit` have column 51 =
`18` and respectively `Disciples of the Land` and `Disciples of the Hand
(Excluding Culinarians)` (`xivl-client-data:csv/quest.csv:rows 110627,
110813-110814, column 51`; `xivl-client-data:csv/xtx_quest.csv:same rows,
columns 40-41`). These are the discipline-scoped selector form described by
(b), but they do not encode a separate discipline-level quantity. They select
which active class may use the row's one level threshold. Named class and job
rows similarly use the selector form described by (c), without changing the
underlying level notion.

The data therefore excludes both a character-wide highest level (d) and an
absence of level data (e). A consumer implementing this form must use the
active eligible class or current job level, with the row's discipline or
named-class restriction applied where present.

## Candidate field sweep

The quest-family sheets are `quest.csv`, `_quest.csv`, `quest_marker.csv`,
`quest_new_reward.csv`, `quest_reward.csv`, `questcategory.csv`,
`xtx_quest.csv`, `xtx_questCompleteText.csv`, and
`xtx_quest_compkind.csv` (`xivl-client-data:manifests/sheet_inventory.csv:rows
13,592-596,780-782`).

Only this joined field pair carries a level plus a class/job scope:

| Sheet field | Extracted type | Observed form |
|---|---|---|
| `quest` column 51 | `s32` | Scalar level; examples range from unrestricted level 1 through named level-50 job quests. |
| `xtx_quest` columns 40-41 | `str`, `str` | Japanese and English eligibility labels: `All`, discipline families, or a named class/job plus the same level. |

The adjacent typed quest fields are columns 52-55: `s32`, `s32`, `bool`, and
`bool`. They do not form a class-level selector. Column 52 uses values such as
`101`, `201`-`203`, and `329`-`336` while the paired eligibility label can
remain unchanged; column 53 is predominantly zero; columns 54-55 are flags
(`xivl-client-data:csv/quest.csv:rows 0-1, columns 51-55`). None supplies
per-class level slots, a discipline-level array, or a highest-level flag.

`_quest.csv` has only two typed trailing integers; `quest_marker.csv` is a
marker payload; `quest_new_reward.csv` and `quest_reward.csv` are all-integer
reward payloads; `questcategory.csv` is a two-integer category table; and the
remaining `xtx` sheets contain completion/category text. None pairs a numeric
field with class, job, discipline, level, offer, unlock, or acceptance text.
No second quest-family sheet therefore supplies a competing level notion.

## Offer versus acceptance limit

The decoded sheets do not have separate offer-visible and accept-enabled
level columns. The requirement pair describes eligibility for undertaking the
quest, but static CSV alone cannot show whether the NPC hides an ineligible
quest or shows it and rejects acceptance. That presentation distinction does
not affect the FORM verdict: either behavior must evaluate the row's scalar
against the eligible active class/current job, not the character's highest
attained level.

## Trailing class in named forms

Addendum date: 2026-08-20. Question: in labels such as `Warrior, Level 45 &
Gladiator`, does the trailing class impose an eligibility requirement, or is
it presentation-only?

The named form appears on exactly 42 rows, the seven job-quest families
`111201`-`111206`, `111221`-`111226`, `111241`-`111246`, `111261`-`111266`,
`111281`-`111286`, `111301`-`111306`, and `111321`-`111326`
(`xivl-client-data:csv/xtx_quest.csv:column 41`). No named row lacks a
trailing class, and no other row carries one.

The Japanese label (column 40, same rows) is structured in two parts joined
by a slash: a prefix naming the primary class with the suffix "gentei"
("restricted to"), then a requirement clause naming the primary class, its
level, and the trailing class joined by the formal conjunction "oyobi"
("and"). The German label (column 42) joins the same three elements with a
capitalized "UND". Two conclusions follow directly from that structure:

1. The "restricted to" prefix names only the primary class. The
   active-class/current-job restriction from the verdict above therefore
   applies to the primary class alone.
2. The trailing class sits inside the requirement clause as a coordinate
   conjunct, parallel to the level term. It is a distinct requirement, not
   flavor or partner text.

No language attaches a level to the trailing class, and the candidate field
sweep above already rules out a second class-level selector in the quest
family sheets (columns 52-55 and the sibling sheets). The decoded corpus
therefore establishes THAT the trailing class is required but not at what
threshold, nor whether the requirement is a level, an unlock, or class
availability.

One bounded decompilation-consumer check was run for this addendum: the
client reverse-engineering corpus classifies `xtx_quest` as text
localization only and records no client-side gating consumer of these
columns, so no client evidence can refine the threshold. The trailing-class
threshold is UNRESOLVED. A consumer implementing the named form must apply
the primary class restriction as ruled above and fail closed on the
trailing-class requirement rather than guess a threshold.

No Ghidra or decompilation evidence was used in the original sweep; the
addendum's single consumer check is described above. No structured manifest was added:
the source rows already preserve the complete scalar and localized selector.
Converting free-form eligibility strings into an enum would exceed what
the decoded schema proves.
