# MTB Header flag byte census

Each `SEDB` `mtb` motion in an installed motion bank has a `Header` payload
whose byte `+0x0c` carries flag bits. This page counts that byte over the
character, monster and cut motion trees. The container layout is
`xivl-decomp:docs/resource/mtb-container-framing.md`, "Header and tables" and
"Header payload". The native effect of bit 0 is
`xivl-decomp:docs/resource/mtb-fixed-motion-calculator.md`, "Layer blend mode".
On the static path described there, a set bit selects Calculate mode 1.

## Method

Python `3` standard-library reads of a contributor-supplied install whose
`game.ver` reads `2012.09.19.0001`. No file bytes are reproduced here.

The census reads every file that starts with `PWIB` below `client/cut`,
`client/chara/pc` and `client/chara/mon`. It walks the `SEDB` `RES ` directory
and its nested directories as in the
[scene file entries](cut-dataset-motion-banks.md#method). It takes every entry
whose payload starts with `SEDB` `mtb` NUL or `SEDB` `MTB `, has a version
above `0x30` and has a `SpuBinary` section. The name of a motion below is the
last backslash-separated part of its directory entry name.

A signature search over all files in the same trees also finds `SpuBinary`
motions in files that do not start with `PWIB`. They are not in the tables:
one in `client/cut` with byte 6, and five in `client/chara/pc`, three with
byte 6 and two with byte 7.

## Byte values

| Tree | `SpuBinary` motions | 6 | 7 | 14 | 15 | Bit 0 set |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cut` | 13489 | 10377 | 326 | 2782 | 4 | 330 |
| `chara/pc` | 29649 | 22815 | 677 | 256 | 5901 | 6578 |
| `chara/mon` | 6960 | 6509 | 451 | 0 | 0 | 451 |

## Names with bit 0 set

The table groups the flagged motions by name shape. "Fourth `a`" is a name
whose fourth character is `a`. "Third `x`" is a name whose third character is
`x`. No flagged motion has both.

| Tree | Fourth `a` | Third `x` | Neither |
| --- | --- | --- | --- |
| `cut` | 240: 237 `cbfa`, 3 `cbba` | 90: 86 `cbxh_hairwave*`, 4 `chxh_hairwave3` | 0 |
| `chara/pc` | 623: 449 `cbfa`, 101 `cbba`, 73 `cbna` | 5955: 5622 starting `cf`, 279 `ch`, 54 `cb` | 0 |
| `chara/mon` | 308: 166 `cbna`, 115 `cbba`, 27 `cbfa` | 138 starting `cf` | 5 starting `cbbm` |

The five `cbbm` motions are `cbbm_add_dmg_f` and `cbbm_add_dmgh_` with `b`,
`f`, `l` and `r`, in `client/chara/mon/m055/act/emp_emp/bid/base/0000`.

The name does not determine the bit. Names that start `cb`, `cf` or `ch` and
have one of the two shapes also occur with bit 0 clear:

| Tree | Fourth `a`, bit clear | Third `x`, bit clear |
| --- | ---: | ---: |
| `cut` | 1 | 15 |
| `chara/pc` | 218 | 256 |
| `chara/mon` | 26 | 487 |

Motions named `cfxm_default` show the same limit. In `chara/pc`, 90 have
byte 14 and 4 have byte 15. The 7 in `chara/mon` have byte 6.

## Two flagged motions

The curves were sampled with the reference decoder of
`xivl-decomp:docs/resource/mtb-fixed-motion-calculator.md`, "Reference decoder
and synthetic blob". Joint keys were not mapped to joint names. That page
leaves the name provider open.

| File below `client` | Bytes | SHA-256 |
| --- | ---: | --- |
| `cut/mot/c002/cbfa_talk_not` | 2480 | `4c0e13527d17b66edc1814273db8642b92c041bca6c6a282f8fec142912c2766` |
| `cut/mot/c004/cbfa_talk_not` | 2480 | `f28a7fb8f49bbdc7e2dd8de73455f6e08f1dd466bffbe323cb38a6cba9a66111` |
| `chara/pc/c001/kao/f001/fac_mdl/9999` | 179997 | `ddb1b7e50844a9f4b757ad05781df6c48557435b4027fd151ded54aa0b4024f3` |

Each `cbfa_talk_not` has byte 7. Its motion has five kind 0 quaternion
channels and no scalar channel. Every decoded key of those channels has an
absolute `w` of at least 0.9992, so each key is a small rotation from
identity.

The `cfxf_angry` motion of the third file has byte 15. It has 30 scale channels
of kinds 7 to 9. Each has one segment with a sample count of zero and `B` equal
to zero. Their `A` values lie from -0.3 to about 0.217 and include about 0.079.
The value formula `A + B*fraction` therefore gives `A` for any fraction. The
reference decoder raises on a segment with no sample, so `A` was read directly.
How the native sampler walks such a segment was not traced.

## Limits

- The counts cover installed motions. They do not show which motions a client
  session loads or plays.
- Only `Header` byte `+0x0c` was counted. Bits 1 and 2 are not interpreted
  here.
- The two flagged motions are examples. No pose was compared with client
  output.
