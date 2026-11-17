# Skeleton size records and look-at IK definition records

The character skeleton file `skl/0001` of a model carries a size record
(`cibb`) and, for most models, IK definition blocks. This page records where
those sit in client extraction `2012.09.19.0001`, the measured size values and
the measured look-at definition values. The native readers are recorded in
`xivl-decomp:docs/resource/vfx-leaf-matrix-scale.md` (the size record) and
`xivl-decomp:docs/actor/look-at-ik-record-and-solver.md` (the IK record).
The measurements here establish what the installed bytes hold. They do not
establish which resource a running client selects.

## Method

Python `3` standard-library reads of a contributor-supplied install whose
`game.ver` reads `2012.09.19.0001`, under `client/chara`. A resource file is a
PWIB wrapper whose first segment is a `SEDB` `RES ` directory, with the
framing described in
[Weapon class index and attach table members](weapon-class-index-and-attach-table.md#method).
The directory entries of a skeleton are named `cib\ciba\...`, `cib\cibb\...`,
`cib\cibs\...` and the skeleton body, with the entries `RESOURCE_TYPE` and
`RESOURCE_ID` last. The IK blocks are `SEDBPHB` structures inside the skeleton
body entry. No member bytes are reproduced here. File sizes and SHA-256
values identify the inputs.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `pc/c001/skl/0001` | 54672 | `d90a756fc1cba6f03bb8dc102b367feb905b5e57a00d209ff4fccddaa17cd031` |
| `pc/c002/skl/0001` | 51280 | `527f5a0ef7453e1248ca2fd523fd5f6a1473ba23a3cf75800a073418fcfce599` |
| `pc/c003/skl/0001` | 51824 | `c24dd9910fb054095e26e980732b601ad54d3a01cabb964ef349950e990e8ef2` |
| `pc/c004/skl/0001` | 51392 | `d297880a92ac6d137be12baa1eeb3ceb94060b105731f4376731799a8f4ab5e3` |
| `pc/c005/skl/0001` | 51424 | `04416e95fdec41ccb76ddf31f7b0dc598f44f53b9ccf0011033f669f73ef8793` |
| `pc/c006/skl/0001` | 51424 | `3cd2cc48950a021f2a76543b687c70d26570b5f4f79142af411e54a08b0c354e` |
| `pc/c007/skl/0001` | 51456 | `8558b8e65e778c6239146d78071fc847c0434b2f60ad8d88308bfbd87fccbf92` |
| `pc/c008/skl/0001` | 53328 | `46d7a983e8be4215d2ea6d33cf7fa99d73ad61beda75df7c08a5c794d9826c06` |
| `pc/c009/skl/0001` | 50432 | `5a33c61b6acf8bb1ae54f2a5be2ff673e8f6c39965ce048fc86e6dcc6fb64e6f` |
| `pc/c010/skl/0001` | 50064 | `633736c748e1c53ececef77f93306ec7ea7d93d1b9034de40f02b26022bab70c` |
| `pc/c021/skl/0001` | 51280 | `4139fa3822eea5780ed12ecf7621a2478e0662d86d57ea6b773256a99318d5e7` |
| `mon/m502/skl/0001` | 15648 | `05e6f780e241329cdab0c17026f6dfc19e76e94679a63c0eb9880a8828e77c3e` |
| `mon/m001/skl/0001` | 5904 | `f60c79ed54a2220209eafb545e26731fa1378cfea5b3c13ba4b6bcdb7b3707a5` |

## Size record member

The directory holds one entry named `cib\cibb\pc\info_cNNN` (or
`cib\cibb\mon\info_mNNN`). The entry is 84 bytes, or 68 bytes in `pc/c010`. The
first byte is 1 in the 84 byte records and 0 in the 68 byte record. The signed
16-bit values at entry `+0x18` and `+0x1A` are equal in every record read:

| Skeleton | Value | Entry bytes |
| --- | ---: | ---: |
| `pc/c001` | 300 | 84 |
| `pc/c002` | 280 | 84 |
| `pc/c003` | 340 | 84 |
| `pc/c004` | 320 | 84 |
| `pc/c005` | 190 | 84 |
| `pc/c006` | 190 | 84 |
| `pc/c007` | 370 | 84 |
| `pc/c008` | 270 | 84 |
| `pc/c009` | 330 | 84 |
| `pc/c010` | 320 | 68 |
| `mon/m502` | 120 | 84 |
| `mon/m001` | 1000 | 84 |

The member SHA-256 values of the entries are `5119e83d55d97384fba85eccbf74461b2801168683f27ee744a0481211ba2401`
(`pc/c001`), `52fc14348a790db59f5a87ab6800595e4ea806c645bca7ad54c936885a47c83a`
(`pc/c010`), `270a92ccd297c3bdf7f1110bd36141d04263e588ffa19373995ecc4047f3c207`
(`mon/m502`) and `619fa38844f80acd2ecf9f8a1519374eb377fd089fb194e4e5eef97138dcd2fe`
(`mon/m001`).

The byte at entry `+3` is 0 in every record read. The native flag routine sets
its bit 7 at load for these lengths, as recorded in
`xivl-decomp:docs/actor/cibb-pointer-and-record-flag.md`, so the install bytes
alone do not show the flag.

## IK definition blocks

`pc/c001/skl/0001` holds five `SEDBPHB` blocks at file offsets `0x7D60`,
`0x8040`, `0x83C0`, `0x86B0` and `0xD1F0`. In a block, the dword at `+0x3C` is
a self-relative offset to a table of self-relative group offsets and the dword
at `+0x40` is the group count. A group holds its kind at `+0x00` (7 in every
group read), a self-relative name at `+0x04`, a self-relative member table at
`+0x18` and the member count at `+0x1C`. A member holds a self-relative name at
`+0x00` and the type byte at `+0x08`. The block at `0x86B0` has 13 groups and a
layout this page does not read.

| Block | Groups | Group, member, type |
| --- | ---: | --- |
| `0x7D60` | 1 | `t0`, `sebonemage`, 2 |
| `0x8040` | 1 | `k0`, `look_ik_001`, 2 |
| `0x83C0` | 5 | `y_hara`, `hara_fix_ik`, 8. `y_asi_l`, `asi_fix_ik_l`, 7. `y_asi_r`, `asi_fix_ik_r`, 7. `y_ude_r`, `ude_fix_ik_r`, 7. `y_ude_l`, `ude_fix_ik_l`, 7 |
| `0x86B0` | 13 | not read |
| `0xD1F0` | 1 | not read |

## Look-at definition record

The type 2 member `look_ik_001` of `pc/c001` is read here at these offsets
from the member start (floats unless noted):

| Offset | Value |
| --- | --- |
| `+0x08` | byte 2 (type) |
| `+0x0A` | byte 1 |
| `+0x14` | self-relative name `j_kao` |
| `+0x24..+0x30` | -6, 6, -10, 10 |
| `+0x34..+0x40` | -20, 20, -30, 30 |
| `+0x44..+0x50` | -50, 50, -80, 80 |
| `+0x54`, `+0x58`, `+0x5C` | 500, 10, 2500 |
| `+0x60`, `+0x64` | dwords 1, 1 |
| `+0x68`, `+0x6C` | 135, 0.3 |
| `+0x70` | self-relative name `n_hara` |
| `+0x7C` | dword 2 |
| `+0x88` | byte 31 |
| `+0x8C..+0xA4` | 0.3, 30, 90, 10, byte 1, 150, 0.7 |

The chain at `+0x0C` with count at `+0x10` holds four entries, `j_sebo_c` (delay
dword 1 at entry `+0x70`), `j_kubi`, `j_kao` and `j_kami_a`. The `j_kao` rows at
entry `+0x1C`, `+0x40`, `+0x58` and `+0x64` are (4.712, 75.6, 11.604),
(-1.111, -60.256, 0.931), (-48.415, 0, 0) and (41.537, 0, 0).

The same group `k0` and member `look_ik_001` read in `pc/c005` with the range
pair `+0x44`, `+0x48` equal to -60, 50 and in `pc/c021` with the `pc/c001`
values. `mon/m502` holds one type 2 member named `look_ik__001` with the range
pairs `+0x44..+0x50` equal to -40, 30, -45, 45 and the flag byte `+0x88` equal
to 27. Of the 48 skeletons `mon/m0*/skl/0001` read, 36 hold one type 2 member
and 12 hold none.

## Reproduction

Walk the `SEDBPHB` blocks of each file with the offsets above. Walk the `RES `
directory with the method page and take the `cibb` entry bytes. Print the
signed 16-bit values at entry `+0x18` and `+0x1A`, the byte at entry `+0` and the
entry length.
