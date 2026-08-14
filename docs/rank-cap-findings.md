# Rank, cap, and Cure column findings

Sweep date: 2026-08-14. Corpus: extraction `2012.09.19.0001`, game version
`1.23b`, 803 decoded CSV files (`xivl-client-data:manifests/manifest.json`).
CSV column numbers below are the zero-based sheet columns after the row id,
matching the repository CSV contract.

## Verdicts

### Attribute soft caps by class rank - not present

No client CSV contains a class/rank keyed matrix for these six parameters:
STR, VIT, DEX, INT, MND, and PIE. `xtx_text_paramName.csv` only supplies their
names (`xivl-client-data:csv/xtx_text_paramName.csv:rows 1-6, columns 0-1`).
`actorclass.csv` has only one populated typed field (column 5, a display-name
reference) (`xivl-client-data:csv/actorclass.csv:row 1000001, column 5`), while
`actorclass_graphic.csv` and `actorclass_mapObj.csv` are graphic/map payloads,
not rank tables. `gameCommandBasic.csv` does carry class/job, level, and
compatibility values at columns 38-40; for Cure row 27346 those values are
`23,2,6`, not attribute caps (`xivl-client-data:csv/gameCommandBasic.csv:row
27346, columns 38-40`; derivation: `docs/command-battle-params.md`, section
1). The rank-named sheets do not carry player parameter caps. Grand Company
rank data and labels live in `gcRank.csv` and `xtx_gcRank.csv`,
`memberRank.csv` carries member-rank flags, and `xtx_rankType.csv` contains
one generic `Default` text row (`xivl-client-data:csv/gcRank.csv:rows 0,11`,
`xivl-client-data:csv/memberRank.csv:rows 0,1`,
`xivl-client-data:csv/xtx_rankType.csv:row 1`).

### Attribute-to-derived-stat mapping - not present

The corpus names physical parameters but does not map them to derived combat
statistics. `xtx_text_paramName.csv` contains STR through PIE names only, and
`xtx_text_attrName.csv` names attack attributes such as slashing and piercing
(`xivl-client-data:csv/xtx_text_paramName.csv:rows 1-6`,
`xivl-client-data:csv/xtx_text_attrName.csv:rows 1-3`). The command sheet's
attribute/element fields are attack metadata: columns 108-111 are damage
attribute, weight, element, and weight, as verified by the command getter map
(`xivl-client-data:csv/gameCommand.csv:row 27346, columns 108-111 =
13,1,13,0`; `xivl-client-data:docs/command-battle-params.md`, sections 1 and
3). `compatibility.csv` is a 219-row command/item compatibility matrix, not a
parameter-to-derived-stat map: the client readers use its row key and columns
8+ for command or item compatibility percentages
(`xivl-client-data:csv/compatibility.csv:rows 1-2, columns 8-9`; derivation:
The command reader is cited at
`xivl-client-scripts:lua/scripts/command/game/gamecommandbaseclass.lua:982-995`.
The item reader is cited at
`xivl-client-scripts:lua/scripts/item/itembaseclass_common.lua:1086-1099`.
Both use extraction `2012.09.19.0001`. No searched sheet exposes a derived-stat field
or a STR/VIT/DEX/INT/MND/PIE conversion row.

### Trait point cap by rank - rank-indexed BP data present, trait label unresolved

`exp_BPCost.csv` is a positive rank-indexed table with rows 1-29 and four
unlabeled typed columns. Examples are rank 1 = `15,1,5,20`, rank 10 =
`60,2,75,65`, rank 20 = `116,3,231,122`, rank 28 = `176,4,473,184`, and
rank 29 = `184,4,-1,-1`
(`xivl-client-data:csv/exp_BPCost.csv:row ids 1,10,20,28-29, columns 0-3`).
As a separate cross-check, the hardcoded
`getExpBPCostSheetData(self, rank, column)` helper reproduces the table's rank
and selector values without reading the sheet
(`xivl-client-scripts:lua/scripts/chara/charabaseclass_parameter.lua:1467-1783`,
sha256 `748C02DBF42329DD0B942642B5FE68B35F422DB61C482954E3B00D0338F12893`,
extraction `2012.09.19.0001`). `CommonJudge.init` separately prepares the
`exp_BPCost` sheet (`xivl-client-scripts:lua/scripts/judge/commonjudge.lua:45-48`).
This proves rank-indexed BP/cost data, but the CSV headers and hardcoded helper
do not name a trait-point field or label the four selectors.
The bounded verdict is therefore positive for the rank-indexed BP table and
not sufficient to assert a trait-point cap semantic.

### Cure-related sheet column - base magnitude present; no literal Cure column

The Cure command has a client effect-block magnitude. In
`gameCommand.csv`, row 27346 has column 84 = `1000` (base magnitude), columns
108-111 = `13,1,13,0`, and column 116 = `1`
(`xivl-client-data:csv/gameCommand.csv:row 27346, columns 84,108-111,116`).
The owning derived catalog names this row `Cure` and emits `magnitude=1000`
(`xivl-client-data:derived/command_battle_params.csv:row 1101`), while rows
1387-1390 carry Cure/Cure II/III/IV magnitudes 1000/1500/2000/4000. The
command-name join is `xtx_command.csv` row 27346 (`Cure`)
(`xivl-client-data:csv/xtx_command.csv:row 27346`). The getter-verified
derivation and the Cure ladder are recorded in
`xivl-client-data:docs/command-battle-params.md:sections 3-4.1`, extraction
`2012.09.19.0001`.

There is no field literally named `cure`: `gimmickPoisonCure.csv` is a
five-column string-only gimmick text sheet (`xivl-client-data:csv/gimmickPoisonCure.csv:rows
1-2, columns 0-4`), and `status.csv`/`xtx_status.csv` carry status metadata,
not a Cure-command column (`xivl-client-data:csv/status.csv:rows 0,221000`).
The command-to-status id, duration, and chance are absent from
`gameCommand.csv`; only the base magnitude is client data
(`xivl-client-data:docs/command-battle-params.md:section 4.1`).

## Search coverage and bounded negatives

The manifest and header scan covered these candidate families and sheets:

- Rank/cap: `exp_BPCost.csv`, `gcRank.csv`, `memberRank.csv`,
  `xtx_gcRank.csv`, `xtx_rankType.csv`, and the filename false positive
  `PopulaceHamletCaptain.csv` (no player-cap fields).
- Class/job/level/skill/parameter: `actorclass.csv`, `actorclass_graphic.csv`,
  `actorclass_mapObj.csv`, `boot_skillequip.csv`, `gameCommandBasic.csv`,
  `gameCommand.csv`, `command.csv`, `debugCommand.csv`, `xtx_command.csv`,
  `xtx_command_variableemote.csv`, `xtx_command_place.csv`,
  `xtx_command_content.csv`, `xtx_command_confirm.csv`,
  `xtx__textCommand_help.csv`, `xtx__textCommand.csv`,
  `xtx__subCommand.csv`,
  `xtx_text_jobName.csv`, `xtx_text_skillName.csv`,
  `xtx_text_paramName.csv`, `xtx_text_attrName.csv`, `xtx_attributive.csv`,
  `compatibility.csv`, `xtx_compatibility.csv`,
  `regionParam.csv`, `_region.csv`, `zoneGroupParam.csv`, and `_zoneParam.csv`.
- Cure/heal/status: `gimmickPoisonCure.csv`, `gameCommand.csv`,
  `gameCommandBasic.csv`, `xtx_command.csv`, `status.csv`, `xtx_status.csv`,
  and `derived/command_battle_params.csv`.
- Other filename families included in the scan: the three
  `privateGLBattleSweep*.csv` sheets, `guildleveWarpPoint.csv`, and
  `pgHarvestPointEncounter.csv`; their headers and rows are event or point
  payloads with no rank, cap, trait, parameter-conversion, or Cure column.

No filename matched `level`, `lvl`, `trait`, or `heal`; no sheet header names a
soft cap, derived-stat conversion, or Cure field. Numeric column identities are
therefore reported by zero-based column number, with semantics only where the
getter-verified command finding or the rank-indexed BP function supplies them.
