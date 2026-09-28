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
