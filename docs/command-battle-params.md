# Finding: Battle parameter table by command (command trio decode)

This human-readable catalog describes each FFXIV 1.23b battle command within
the limits of the static client CSVs.

- Derived table: `derived/command_battle_params.csv` (1611 rows, one per
  `gameCommand.csv` id).
- Generator: `tools/build_command_battle_params.py`.
- Source data: `csv/command.csv`, `csv/gameCommand.csv`,
  `csv/gameCommandBasic.csv`, `csv/xtx_command.csv`,
  `csv/xtx_text_attrName.csv`, `csv/compatibility.csv`, extraction
  2012.09.19.0001.
- Authority for every column claim: the client's own command getter evidence
  at extraction `2012.09.19.0001`. The stable source paths are recorded
  beside the owning mappings in `tools/build_command_battle_params.py`. Getter
  names and line numbers below refer to those sources.
- Display text: `xtx_command.csv` cols 1/2 provide Japanese/English names and
  cols 22/23 provide Japanese/English descriptions. The derived table retains
  both languages so a command query carries its client explanation beside the
  numeric inputs.

This finding derives the column map from the client getters and cites the
getter and line that reads each column.

## 1. Verified column -> semantic map

Sheet column indexing: a corpus CSV's first field is the row id. Sheet column N
is `CsvRow.values[N]` (see `tools/_csv_reader.py`). All indices below are sheet
columns, matching the numbers the client getters pass to
`getGameCommandData(col)` / `getGameCommandBasicData(col)`.

### gameCommandBasic.csv (cost / level / class sheet)

| Sheet col | Meaning | Getter (gamecommandbaseclass.lua) |
|---|---|---|
| 38 | class/job (command main skill) | `getCommandMainSkill` :52 |
| 39 | command level | `getCommandLevel` :41 |
| 40 | compatibility key (row into compatibility.csv) | `getCommandCompatibilityKey` :969 |
| 76 | cast time | `getCastTime` :2041 |
| 79 | recast time | `getRecastTime` :667 |
| 114 | MP cost (raw, before `calculateCommandCost`) | `getCommandMPCost` :1947 |
| 115 | TP cost (raw) | `getCommandTPCost` :1996 |
| 36 | command-class registry id (30000-band); selects the Lua subclass | (loader-side; see section 5) |

HP cost has no sheet column: `getCommandHPCost` (:1906) returns a constant 0 in
the base class. HP cost exists only where a subclass overrides it.

### gameCommand.csv (full engine sheet)

| Sheet col | Meaning | Getter |
|---|---|---|
| 37 | caster life-state requirement category (gates alive/dead/sit) | `processCanCommandForActorStat` :73 |
| 64 | range | `getRange` :678 |
| 65 | best range | `getBestRange` :689 |
| 66 | minimum range | `getMinimumRange` :700 |
| 67 | effect range (AoE radius) | `getEffectRange` :711 |
| 68 | target life-state gate | `processCanCommandForChangeActorStat` :244 |
| 75 | action-gauge cost | `getActionGaugeCost` :2089 |
| 82 | recast-separates-hands flag | `isRecastSeparationHands` :2170 |
| 108 | damage attribute (enum) | `getCommandDamageAttribute` :1884 |
| 110 | damage element (enum) | `getCommandDamageElem` :1895 |

### The four-parameter scaling model

Each of Param1-4 is a 4-column group on a stride of 5. Verified from the param
getters:

| Param | grow col | base col | compat col | tp col | Getters |
|---|---|---|---|---|---|
| 1 | 42 | 43 | 44 | 45 | `getCommandParam1LevelAdjustGrow` :1508, `getCommandParam1` :1596 |
| 2 | 47 | 48 | 49 | 50 | `getCommandParam2LevelAdjustGrow` :1530, `getCommandParam2` :1668 |
| 3 | 52 | 53 | 54 | 55 | `getCommandParam3LevelAdjustGrow` :1552, `getCommandParam3` :1740 |
| 4 | 57 | 58 | 59 | 60 | `getCommandParam4LevelAdjustGrow` :1574, `getCommandParam4` :1812 |

`getCommandParamN` (e.g. :1596) computes:

```
base   = getGameCommandData(base_col)            # raw sheet potency
compat = getCommandCompatibilityWithAdjust(getGameCommandData(compat_col), ...)
tp     = getCommandTPPowerWithAdjust(getGameCommandData(tp_col), ...)
base   = getCommandLevelAdjust(base, ParamN_grow, lowAdj, highAdj, actor, ...)
return base * compat * tp
```

The compatibility adjustment is meaningful client-side input. The recovered
base implementation returns 1 when the raw adjustment is 0; otherwise it
interpolates from 1 toward the hand compatibility value:

```
compatibilityFactor = 1 - (1 - compatibilityByHand) * rawCompatibilityAdjust
```

The recovered base implementation of `getCommandTPPowerWithAdjust` returns 1
for every raw input. Its intermediate delta starts at `1 - 1`, so the raw TP
adjustment is multiplied by zero. A complete search of the frozen 2,671-script
Lua snapshot found calls and this base definition, but no override. The catalog
therefore preserves `pN_tp_adjust` as evidence without claiming that it scales
power in this client build.

`getCommandLevelAdjust` (:1375) resolves the grow curve as
`base * actor:getGrowData(actorLvl, growCol) / actor:getGrowData(cmdLvl, growCol)`
then applies the high/low-level fudge factors. The defaults are 0.7 high and
1.0 low (`getCommandParamN_AdjustFor{High,Low}LevelUse` :1436-1505). If the grow column
is `< 0` the param is flat and the raw base is used directly
(`getCommandParamNLevelAdjustGrow` returns nil, e.g. :1514).

## 2. What is actually populated in extraction 2012.09.19.0001

The four-param schema exists in the getters, but the data is sparse:

- **Param1, Param2, Param4 columns (42-50, 57-60) are blank across all 1611
  rows.** No potency, no grow curve.
- **Only Param3 (cols 52-55) carries data.** 1590/1611 rows have grow = -1
  (flat); 21 rows carry a real native grow-curve index (7, 23, 69, 77, 119).
  Compatibility adjustment col 54 is 1 on 806 rows and 0 on 805. Raw TP
  adjustment col 55 is 1 on 152 rows and 0 on 1459; as described above, the
  recovered base function still returns a TP factor of 1. Param3 base col 53
  is the secondary-effect / DoT magnitude:
  Bio/Bio II/III = -9/-19/-30 (grow 77 Dia = -8/-18/-28), Sacrifice I-IV =
  53/94/179/252, Ferocity/Invigorate buff tiers, etc. Negative = drain/DoT.

So the Lua-visible Param1 base (col 43) carries no potency in this snapshot.
The base magnitude does exist in the sheet, but in the native-read effect
block instead: **col 84** (section 4.1). What the corpus lacks is the scale --
how a magnitude of 950 becomes hit points -- which is the native combine step.

The per-command differentiation that *is* present lives in cast/recast/MP/TP
(gameCommandBasic), range block (64-68), damage attribute/element (108/110),
base magnitude (84), and the rest of the structured effect block at cols
84-120 (see section 4).

`derived/command_battle_params.csv` emits every raw base, grow,
compatibility-adjustment, and TP-adjustment field rather than only the
currently populated base/grow pair. This preserves the getter-shaped formula
inputs and makes future build comparisons lossless.

## 3. Decoded enums

**Damage element (col 110)** -- calibrated against named spells in xtx_command.
High confidence:

`-1` None, `5` Fire, `6` Ice, `7` Wind, `8` Earth, `9` Lightning, `10` Water,
`11` Astral, `12` Umbral, `13` Unaspected.

Evidence: Fire/Fira/Firaga/Flare = 5; Blizzard/Freeze = 6; Aero/Tornado = 7;
Stone/Quake/Stoneskin = 8; Thunder/Burst = 9; Water/Flood = 10. `11` is the
light pole (Holy/Banish) and `12` the dark pole (Dark Cloud, Sanguine Rite);
The corresponding command descriptions identify them as Astral/Umbral, the
1.x terms, and their weight is 0.33 (below) because each pole combines three
elements. `13` =
unaspected magical: Cure/Cura/Curaga/Cure II-IV, Regen, Esuna, Sacrifice, and
the void/aetherial nukes (Cataclysm, Aetherial Eruption, Voidbrume) -- all
attribute 13. The same data labels 13 "healing magic", but the void nukes show
it is broader. "Unaspected" is the safe superset.

Note the `-1` vs `13` split: `-1` means no element field at all (physical
attacks like Stone Throw, and non-damaging buffs like Dark Seal / Holy Succor
carry it), whereas `13` is a real magical element value on unaspected magic. A
naive name prefix match over-flags physical moves named "Stone.../Holy..." --
those correctly read `-1` because they are not the elemental nuke.

**Damage attribute (col 108)** -- `xtx_text_attrName.csv` directly names `1`
Slashing / `2` Piercing / `3` Blunt / `4` Projectile / `11` Sonic / `12` Breath
/ `13` Neutral. Every elemental nuke carries `13`, so the derived table uses
the more specific label `Magical`; `-1` = None. The getter returns the raw enum
without naming it, so labels are emitted in a separate `dmg_attr_label` column,
never overwriting the raw value.

**Attribute/element weights (cols 109/111)** -- the float following each enum
is the fraction that attribute/element factors into the attack. This
extraction's distribution supports that reading: col 109 is
1 on essentially all damaging attributes; col 111 is 0.33 on 38/47 Astral and
68/71 Umbral rows and 0 elsewhere -- exactly the "three elements combined"
pole semantics. Emitted as `dmg_attr_weight` / `dmg_elem_weight`. The 0-vs-1
split on single-element rows in col 111 is not yet understood.

## 4. Residual unknown columns

- **Effect block, gameCommand cols 84-120** (`effect_block_raw` in the table):
  a structured per-command payload of which cols 84 (base magnitude, section
  4.1), 108/109 (dmg attribute + weight), and 110/111 (dmg element + weight)
  are decoded. No Lua getter reads cols 84-107; the block is native-read, so
  the remaining decode path is empirical. Still unknown: cols 85/86 (floats,
  0/1), the `(s32 type, float value)` pair slots 87-94 (types 2-6; e.g.
  Blizzard carries (4, 0.5)(4, 0.25), Aero (4, .25)(5, .25)(4, .125)(5, .125)
  -- THM nukes carry type-4 only, CNJ nukes types 4+5; plausibly stat-scaling
  contributions, speculative), pair slot 99/100 (col 99 takes element-band
  values 7-12 on 26 rows -- possibly a secondary elemental rider), col 96
  (fractions 0.1/0.25/100), col 107, col 116 (multiplier 1/1.5/2/3), and col
  120 (constant 60 on 973 rows, 0 elsewhere -- present on every player action
  regardless of the status it applies, so NOT a status duration). Dumped raw
  and lossless. It is not promoted.

### 4.1 Effect block decode: base magnitude at col 84 and absent status data

**Col 84 = base magnitude (damage/heal power).** No Lua getter reads it. The
decode is empirical, pinned by tier ladders that only potency explains:
Blizzard 800 < Fire 950 < Thunder 1050 < Fira/Freeze 1200 < Firaga 1600 <
Flare/Holy 2000 < Thundaga 2150 < Burst 2200; Cure/Cura/Curaga =
1000/2000/4000; ability-heals Second Wind 1550 / Holy Succor 1500; monster
breaths 1300-1350; Stone Throw 50; non-damaging buffs 0. Emitted as
`magnitude`. The magnitude -> hit-point scale is the native combine step
(section 5). The number itself is client data.

**Status id, duration, and chance are NOT in gameCommand.csv.** An exhaustive
scan found no cell in cols 84-139 across all 1611 rows holding a status.csv-band
id (221000-253003). The command -> status link is native.
Duration is a property of the status itself, not the command:
`getStatusLifeAtSheet` (statusbaseclass.lua:820) reads statusSheet cols 47/49
with grow col 48
(`getStatusLifeLevelAdjustGrow` :495), and status power reads cols 27/28
(`getStatusPowerAtSheet` :755). Decoding `status.csv` is a separate
investigation.
- **gameCommand col 35** (s32, 8 distinct values) and **col 73** (bool):
  unmapped by any getter read. It is not emitted.
- **command.csv** is near-empty for these ids (only cols 27/29/30/31/32/33/34/35
  populated, all flags/one s32). It carries no class path or type column, so it
  contributes nothing beyond confirming the id exists.

## 5. Known gaps -- what this table cannot answer

The following are **not** in the client CSV corpus. They require runtime
observations or native-client analysis beyond this catalog:

1. **The magnitude scale.** The base magnitude per command IS client data
   (effect-block col 84, section 4.1), but the mapping from magnitude to hit
   points -- and whether the col 85/86 floats and the 87-94 stat-scaling pairs
   weight it -- is native. Retail combat-log / video magnitudes are the
   calibration source: observed damage vs col-84 value across known
   caster/target levels.
2. **The C++ combine step.** Damage roll, defense subtraction, crit multiplier,
   elemental resist multiplier, per-part damage adjust -- the Lua carries config
   only. These operators are native. Inputs the client feeds them (per this
   decode): col-84 magnitude, Param base values, `getGrowData` growth factor,
   `calcPotencial` level-adjust (`sqrt(1 + (|lvldiff|-10)*0.4)`), damage
   attribute/element + weights.
2a. **Command -> status linkage, and status apply chance.** Not in
   gameCommand.csv at all (section 4.1). The link is native and the chance is
   not client data. Which status a command applies, and at what rate, must
   come from retail observation. Status duration/power then come from status.csv
   (cols 47/49 and 27/28), not from captures.
3. **Native growth tables (`getGrowData`).** The grow-column indices (col
   42/47/52/57, and the real values 7/23/69/77/119 seen in Param3) index into
   `actor:getGrowData(level, column)`, which is a native method with no Lua body
   and no CSV table in this corpus. Resolving a scaled Param value at a given
   level therefore requires those native curves. The flat case (grow < 0) is
   fully resolvable: resolved value = raw base col 53.
4. **Command type (Attack / MagicMissile / Ability / Magic / WeaponSkill,
   1-5).** Determined by which Lua subclass a command instantiates
   (`isAttackCommand` etc. are set per-subclass; `getCommandType` in
   `battlecommandbaseclass.lua:65` dispatches on them). The id -> subclass
   binding is native (the loader reads a command-class registry id, the
   gameCommandBasic 30000-band col 36, and instantiates the matching
   `_defineClass` stub). It is not a decodable CSV column. The derived table
   ships `dmg_class` (physical/magical/none, from the damage attribute) as a
   CSV-derivable proxy, and the id band, but not the authoritative 5-way type.

## 6. Additional verified mappings

- basicSheet 114 is MP cost and 115 is TP cost. HP cost has no column.
- Col 82 is `isRecastSeparationHands`; `isRegistable` (:2160) reads no sheet
  column.
- `getCommandParam4LevelAdjustGrow` reads Param4 grow col 57 (:1574).
- The four params are cols 42-60. The 84-120 block is a separate effect payload
  that carries damage attribute at 108 and element at 110.
- `compatibility.csv` is not the param grow curve. It is the
  cross-skill effectiveness matrix keyed by basicSheet col 40, columns 8+
  indexed by skill id, value/100 (`getCommandCompatibilityData` :980). The
  param grow curves are the native `getGrowData` tables, a different axis.

## 7. Confidence

Confirmed (getter-verified): the full column map in section 1; the four-param
column layout; MP/TP/HP cost reality; col 82; Param4 grow col 57; the
compatibility.csv role. High confidence (name-calibrated from the decoded
command rows and their distributions): the element enum 5-13, attribute enum
1-4/13, and the weight columns 109/111. High confidence (empirical tier
ladders): col 84 = base magnitude. Confirmed negative (exhaustive scan): status
id/duration/chance are not in gameCommand.csv. The 87-94 pair slots are
provisional stat-scaling contributions. Out of scope / native: the
magnitude scale, grow tables, C++ combine, command -> status linkage, 5-way
command type.
