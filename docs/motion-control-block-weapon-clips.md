# Motion control block weapon hold records

Each motion of a character bank has a motion control block beside its
motion data. The block lists timed clip records. This page records the
measured framing of that block in client extraction `2012.09.19.0001` and
the `RaptureWeaponAutoConstClip` records of the battle draw and sheathe
motions, which name a weapon slot and a flag at a start tick.

The native consumer of the record is recorded in
`xivl-decomp:docs/actor/weapon-slot-attach-and-sheathe.md`, "Flag bit 13 and
its writers": the clip passes the record dword at `+0x14` as the weapon slot
and the dword at `+0x10` as the flag. The tick unit is the 10000 units per
frame clock of `xivl-decomp:docs/actor/animation-bank-routing.md`,
"Motion-command controller clock". The measurements here establish only
what the installed bytes hold.

## Method

Python `3` standard-library reads of a contributor-supplied install whose
`game.ver` reads `2012.09.19.0001`, with the bank directory framing of
[the class index page](weapon-class-index-and-attach-table.md#method). A
control block is a bank entry that starts with `SEDB` `MCB` NUL. Its entry
name is a backslash path whose last component is the motion name.

All 995 files under `client/chara/pc/c001/act` were read. They hold 1829
control blocks and every one parsed with the framing below. No block bytes
are reproduced here.

## Block framing

| Location | Content |
| --- | --- |
| block `+0x0E` | u16 header size, `0x30` in every block |
| block `+0x10` | u32 declared size, equal to the bank entry length in every block |
| header size | `@RST` chunk: u16 4 at `+4`, u16 count at `+6` (5 in every block), u32 offsets from `+8` |

Each `@RST` offset is relative to the `@RST` start plus `0x20` and names an
`@RES` chunk whose name is at `+8`. The five names are `motionC`, `RIDTBL`,
`Effect`, `String` and `ClipGid`, in that order, in every block.

The children of `motionC` start at its `+0x18`. They are `@ATT`, `@CPT`,
`@ACT` and `@TRK`, each with a u16 at `+4` that gives its length in units of
8 bytes, then `@BKT` with an 8-byte header, then `@BLK`.

| Chunk | Content |
| --- | --- |
| `@CPT` | u16 entry count at `+6`, 4-byte entries from `+8`: a u16 index into the `String` names and one more u16 |
| `String` | u16 offsets from `+0x18`, relative to that offset table, each to a NUL-terminated name |
| `@BLK` | u32 length in ticks at `+0x0C`, u32 record count at `+0x10`, records from `+0x18` |

Record header, 16 bytes: u16 record size, u16 class ordinal (an index into
the `@CPT` entries), u32 start tick, two u16, one u32. The payload follows.
The class name of a record is the `String` name its `@CPT` entry indexes.

Record sizes by class across the 1829 blocks: `MotionCommandClip` 16,
`RaptureWeaponAutoConstClip` 24, `RaptureWeaponAutoScaleClip` 28,
`RaptureWeaponAnimationClip` 60, `RaptureCharaActionSoundClip` 32,
`IKTargetLimitClip` 452. Each of those classes has one size throughout.

## Weapon hold records

A `RaptureWeaponAutoConstClip` record has two payload dwords: the flag at
record `+0x10` and the weapon slot at `+0x14`. The c001 tree holds 146 such
records. Their slot values are 0, 1 and 5 only.

The records of `cbbm_activ` and `cbbm_deact` in
`client/chara/pc/c001/act/<set>/bid/base/0000`, as frame (start tick over
10000), slot and flag:

| Set | Bank bytes | `cbbm_activ` length and records | `cbbm_deact` length and records |
| --- | ---: | --- | --- |
| `swd_emp` | 606880 | 400000. 10 slot 0 flag 0 | 400000. 21 slot 0 flag 1 |
| `swd_sld` | 611296 | 400000. 10 slot 0 flag 0, 16 slot 1 flag 0 | 400000. 21 slot 0 flag 1, 26 slot 1 flag 1 |
| `clb_sld` | 611296 | 400000. 10 slot 0 flag 0, 16 slot 1 flag 0 | 400000. 21 slot 0 flag 1, 26 slot 1 flag 1 |
| `2sp_emp` | 629136 | 450000. 7 slot 0 flag 0 | 350000. 25 slot 0 flag 1 |
| `2ax_emp` | 610704 | 450000. 7 slot 0 flag 0 | 350000. 25 slot 0 flag 1 |
| `2st_emp` | 610704 | 450000. 7 slot 0 flag 0 | 350000. 25 slot 0 flag 1 |
| `clw_clw` | 608448 | 480000. 11 slot 1 flag 0, 11 slot 0 flag 0 | 440000. 15 slot 0 flag 1, 18 slot 1 flag 1 |
| `stf_emp` | 582144 | 500000. 17 slot 0 flag 0 | 500000. 21 slot 0 flag 1 |
| `stf_sld` | 588960 | 500000. 16 slot 1 flag 0, 17 slot 0 flag 0 | 500000. 21 slot 0 flag 1, 30 slot 1 flag 1 |
| `2bw_emp` | 609312 | 400000. 0 slot 5 flag 1, 1 slot 0 flag 0, 21 slot 5 flag 0 | 500000. 0 slot 5 flag 1, 25 slot 0 flag 1 |
| `emp_emp` | 702992 | 450000. none | 250000. none |

Bank SHA-256 values, in table order:

- `415356f82c0d930297bb5143b3424a86811b691d21edec3b477fa923f8b65ed0`
- `a2ce2cff8abf51289c1b239e5f1ccb12f10371eaa923d99de45d4adabbf1d355`
- `c675a1d733224ab2418915e2b3e0510dc49c0dec3c2dc3f43acb07f38487277a`
- `212c8e00cea1356bb2f5b8edab92fa7569df1a72fa1795f579e68908be39d698`
- `f9aca1431ff96acb986634710c4455059cd167841ea370e0bf9d54d7474d1b40`
- `a15f27d87a5fc14cf11b59ebb23df4be30dfe460905be1570edb1163b2b59005`
- `709661da022b8e1c83dab427196ce8ef12a516a3fd5018fb0ecc0cca0d8c02bf`
- `899f51d19e6f905271150199f4cfc148822cd137462276a43444ece12c791fb7`
- `38c958874b1817403731a0acce395f99cea6072634d5dd6116fcac746628c6b1`
- `a6fee94e4b4e414323f33e9bcfa9a0ea7e942ee7039b9ec8406708e453367f79`
- `2ce7ec3844054c2ec89a21079c2820bdab588398128400c8aebab63456b3495c`

Across the whole c001 tree every `cbbm_activ` and `cbbp_u_activ` record for
slot 0 or 1 carries flag 0, and every `cbbm_deact` and `cbbp_u_deact` record
carries flag 1. The only records of those four motions that name another
slot are the slot 5 records of `2bw_emp`: flag 1 at tick 0 in all four
motions, and flag 0 at tick 210000 of `cbbm_activ` and tick 150000 of
`cbbp_u_activ`.

## Limits

- The two u16 fields and the u32 of the record header were not interpreted.
- The payloads of `RaptureWeaponAutoScaleClip` and
  `RaptureWeaponAnimationClip` were not decoded.
- Only the c001 tree was read.
