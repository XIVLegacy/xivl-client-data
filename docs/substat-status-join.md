# Finding: SubStat status-table join

The retail `0x0179` path resolves captured wire status id `0x5ADF` to status
row `223263`. The resolved status word is `0x0003681F`. SubStat kind 1 reads
value `6` from bits 12..15, and kind 2 reads value `8` from bits 8..11.

- Derived table: `derived/substat_status_crosswalk.csv`.
- Analyzer: `tools/analyze_substat_status.py`.
- Client corpus: `csv/status.csv` and `csv/xtx_status.csv`, extraction
  `2012.09.19.0001`.
- Native path: `xivl-opcodes:data/client_opcode_semantics.json#s2c-0179`.
- Status object contract:
  `xivl-client-structs:manifests/status_effect_subsystem.json` and
  `xivl-client-scripts:lua/scripts/status/statusbaseclass.lua`.

## Lookup chain

`FUN_008A3350` transforms a nonzero 16-bit wire id into the status lookup key:

```text
wire <= 0x8000: 200000 + wire
wire >  0x8000: 200000 + wire - 0x4350
```

For this capture, `200000 + 0x5ADF = 223263`. Both `status.csv` and
`xtx_status.csv` contain row `223263`; the English name for the whole status
record is `Resting`. `StatusBase.getStatusId` returns the status object's
static actor id, and `StatusBase.getStatusData` uses that id as the status-sheet
row key. The native `FUN_0075C1D0` path reads the same static actor id as its
packed 32-bit word. Therefore this joined record's word is the row id,
`223263`, or `0x0003681F`.

The analyzer fails closed when the translated row is absent or duplicated. The
two transform branches overlap, so the crosswalk records independently verified
low-branch and high-branch wire encodings. Row `223263` accepts both `0x5ADF`
and `0x9E2F`; the retained capture used `0x5ADF`.

## Bit projections

The client reader at `FUN_006F9EC0` defines the two SubStat projections:

| Projection | Expression | Captured value |
|---|---|---:|
| kind 1 | `(word >> 12) & 0xF` | 6 |
| kind 2 | `(word >> 8) & 0xF` | 8 |

The overlapping Object reader at `FUN_006F9F70` is a collision check, not a
source of SubStat names. For the same word it reads bits 8..11 as `8`, bits
14..15 as `1`, and bits 12..13 as `2`. Because these projections overlap, the
crosswalk keeps neutral numeric column names rather than assigning an exclusive
packed-field meaning.

## Naming search verdict

The complete relevant client surface supports the numeric domains but no
stable names for values 1..15. The search covered all status rows, every CSV
cell and available sheet schema or cross-sheet key, and all shipped Lua status
consumers. The only ordinary Lua SubStat consumer is the command debugger. It
accepts numeric `hand` and `state` arguments and prints the numeric result; it
does not define an enum or value table
(`xivl-client-scripts:lua/scripts/commanddebugger/commanddebuggerdev.lua`).

The following candidate mappings are rejected:

- Treating wire id `0x5ADF` as row `23263`. That row number occurs in command
  sheets and names `Ranine Stare`, but it bypasses the proven status transform.
- Treating `Resting` as the name of nibble value `6` or `8`. It names the whole
  status row, not either projection.
- Reusing historical chant labels, server terminology, wiki names, nearby
  strings, or action and cast presentation semantics. None is joined by this
  client path.
- Reusing names from the overlapping Object projections. Their shared bits
  require stronger evidence than positional overlap.

The remaining boundary is a client value table or an ordinary consumer that
compares these nibbles and gives the values stable semantics. Until one is
found, the supported result is `kind 1 = 6` and `kind 2 = 8`, with values 1..15
left unnamed.
