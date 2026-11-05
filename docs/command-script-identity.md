# Command script identity

The static-actor catalog joins directly to command row ids. In extraction
`2012.09.19.0001`, 1,610 of the 1,611 `gameCommand.csv` rows match a
`/Command/` path in `manifests/staticactor_class_paths.json`. These matches
use 74 distinct paths. Row `0` has no matching static actor and retains an
empty `lua_class_path` in `derived/command_battle_params.csv`.

## Evidence for the join

`CommandBaseClass.getCommandId` returns `_getStaticActorID` (lines 4-11).
`GameCommandBaseClass.getGameCommandData` and `getGameCommandBasicData` use
that command id as their sheet row key (lines 11-38). The scripts therefore
connect the static-actor id to the two command sheets without a name match,
id-band inference, or an assumed numeric registry index.

The exact Lua sources are:

| Source | SHA-256 |
|---|---|
| `xivl-client-scripts:lua/scripts/command/commandbaseclass.lua` | `bf7dd5fa7a6530c0c3b683be16a252b7ffd62492bdc268f36322977dee4d3e31` |
| `xivl-client-scripts:lua/scripts/command/game/gamecommandbaseclass.lua` | `75f366ca597f77a8e4b506fa8d7b214171cfdbb8d913fa12aa685d72a0b3256b` |

Their byte identities are recorded in
`xivl-client-scripts:manifests/scripts.json`. The SAN source, decoding
procedure, and exact product hash are recorded in
[`retail_staticactor_check.json`](../manifests/retail_staticactor_check.json).
The extractor reads big-endian ids paired with NUL-terminated class paths
after XOR decoding. Its product contains 2,812 unique static-actor records.

`gameCommandBasic` column 36 is not needed for this join. Both command `26979`
and command `27199` contain `30101` there, but their static paths are
`/Command/Game/WeaponSkill/CmnAttackWeaponSkill` and
`/Command/Game/WeaponSkill/AttackWeaponSkill`, respectively. Looking up
static actor `30101` instead selects `/Command/DebugInputCommand`. Column 36
is therefore not a substitute for the command id; its meaning remains
unresolved.

## Widget-open command priority declaration

The static-actor row for `24228` maps to
`/Command/System/WidgetOpenCommand`. The supplied `command.csv` row `24228`
declares `-1` in sheet column `29`. The CSV label is `29` and
its type is `s32`. Excluding the leading row id, this is `CsvRow.values[29]`,
or CSV field index `30`, following `tools/_csv_reader.py`. The unique row
ends at CSV line `804` in the identified member.

The published `CommandBaseClass.getPriority` column29 reader is owned by
`xivl-client-scripts:docs/confirm-prompt-client-contracts.md#answers-and-command-submission`.
The `CharaBaseClass.getCommandName` system-command selector consequence is in
`xivl-client-scripts:docs/linkshell-party-command-contracts.md#shared-dispatch-and-wire-representation`.
If the selected command resolves those implementations and its sheet read
returns this row's column29 value, the published system-command path with
priority `-1` selects `commandRequest`. This declaration does not identify an actual
command object, installed sheet/provider, dynamic method or selected native
descriptor. The mapped class and row alone do not prove invocation or
accepted widget creation.

The member is pinned by [tables.json](../manifests/tables.json), row
`command.csv`: 126638 bytes, SHA-256
`14548e379a6c4f76c10a4ac53866161ebf1622ce7f1e76a760e85f0577f38848`,
extraction `2012.09.19.0001`. Its containing archive is pinned by
[private_csv_corpus.json](../manifests/private_csv_corpus.json). This selected
cell was read in memory from that authenticated member; no other row or
column value contributes to this finding. Header, row uniqueness, signed
type and field-index checks are distinct from full-corpus reproduction.

## Formula coverage

Every command row with a nonnegative parameter grow selector has a static
class path. The 21 rows use these five classes:

| Class path | Native-grow rows |
|---|---:|
| `/Command/Game/Ability/CmnAbility` | 6 |
| `/Command/Game/Magic/CmnAttackMagic` | 2 |
| `/Command/Game/Magic/CmnBadStatusMagic` | 7 |
| `/Command/Game/Magic/CmnCureMagic` | 4 |
| `/Command/Game/WeaponSkill/MonsterAttackWeaponSkill` | 2 |

The path establishes which script to inspect. It does not by itself evaluate
inherited getters, conditional cost overrides, native grow data, or the
native magnitude-combination function. Those are separate formula evidence.

## Reproduction

Use an explicitly supplied decoded CSV root whose bytes match
`manifests/tables.json`, then run:

```text
python tools/build_command_battle_params.py --csv-dir <csv-root>
python tools/build_command_battle_params.py --csv-dir <csv-root> --check
python tools/test_command_battle_params.py
python tools/validate_corpus.py --csv-dir <csv-root>
```

The generator performs a left join by command id against the repository-local
static-actor manifest, accepting only `/Command/` paths. Duplicate static ids
are an error. Missing matches stay empty. The synthetic join test deliberately
places another class at the value of column 36 and verifies that it is not
selected.
