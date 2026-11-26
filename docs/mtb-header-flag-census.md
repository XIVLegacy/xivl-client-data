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

## Hair motions

These reads cover the motions named `cbxh_hairwave1` to `cbxh_hairwave3` and
`chxh_hairwave1` to `chxh_hairwave3`. Channels were walked with the reference
decoder above. A pair, a joint key and a kind are the blob fields of its
page. A joint key is not a skeleton row index. The base node that the name
provider adds for a pair is open there.

| Motions | Entries | Byte | Channels by pair and joint key | Last key frame |
| --- | ---: | ---: | --- | --- |
| `cut`, `cbxh_hairwave1`, `2`, `3` | 3, 9, 74 | 7 | none | no key |
| `cut`, `chxh_hairwave3` | 4 | 15 | pair 13, keys 0 to 3 | 119 |
| `chara/pc`, `chxh_hairwave1` to `3` | 279 | 15 | pair 13, a subset of keys 0 to 3, and in some entries also pair 2, keys 67, 72, 74, 76 and 83 | 118 or 119, except 3 entries with no channel |

In `chara/pc`, 96 of the 279 entries hold all four pair 13 keys, and 48 hold
key 0 only.

Each of the 86 `cbxh` blobs is 160 bytes with 17 pairs and no descriptor.
`FixedMotionCalculator` samples one descriptor per call, so these blobs give
it no row to write. Their `Header` f32 at `+0x04` is 119.0.

The four `cut` `chxh_hairwave3` entries are in the scene files `gc010715`,
`gc010720`, `gc010740` and `sum6w020`. Each has four channels under an entry
path that ends `face_pose\miga\hir\h902\bin\chxh_hairwave3`.

The `chara/pc` entries are three in each of 93
`client/chara/pc/c<NNN>/kao/h<NNN>/hir_mdl/9999` files. All channels in this
table that have keys are kind 0. The three entries with no channel are in
`c021/kao/h041`. Two of the files, `c003/kao/h004` and `c021/kao/h012`, are 6
bytes shorter than the total in their `PWIB` header. A walker that checks
that total rejects them. They were read from the `RES ` offset at `+0x08`.

### MotionClip records that name them

Every scheduler in the files below `client/cut` that contain the bytes
`hairwave` was parsed. Those files include each scheduler whose name table
can hold such a name. Each MotionClip name was resolved from `s32(D+0x10)`
with the `RIDTBL` formula of
`xivl-decomp:docs/resource/combat-motion-name-provider.md`,
"ResourceReference and serialized provider". All 147 records that resolve to
a hair name are bound to a `ProxyActor` actor record.

| Scene file | `cbxh_hairwave1` | `cbxh_hairwave2` | `cbxh_hairwave3` | `chxh_hairwave3` |
| --- | ---: | ---: | ---: | ---: |
| `gc010715` | 1 | 0 | 0 | 1 |
| `gc010720` | 0 | 0 | 8 | 1 |
| `gc010740` | 0 | 0 | 24 | 9 |
| `man0l010` | 0 | 0 | 25 | 0 |
| `man0l020` | 0 | 1 | 25 | 0 |
| `man0l040` | 0 | 0 | 1 | 0 |
| `man0u000` | 0 | 0 | 1 | 0 |
| `man2l030` | 2 | 0 | 10 | 0 |
| `man2l090` | 0 | 0 | 5 | 0 |
| `sum6w020` | 0 | 0 | 24 | 9 |

| File below `client/cut` | Bytes | SHA-256 |
| --- | ---: | --- |
| `gc010715/gc010715` | 254288 | `4430b85a480e5aec4d5a43527fbe89da31914057c93d65afea242821dd844edd` |
| `gc010720/gc010720` | 1944288 | `cf94ea0b710667db41e8ef3c22574e15bac0a92628d9906416959a6b68fce4bf` |
| `gc010740/gc010740` | 2080800 | `0efcd15e988abd4c606ed9bd0c32bdf902748c893707697ffe7ada7c9ea8ff56` |
| `sum6w020/sum6w020` | 2082032 | `3438e2049de7cabf6ef2bda67fda5bf612d05b10236d5ab803f52c768e716666` |
| `man0l010/man0l010` | 15519280 | `5b925ff3a43fa2bf6943b023a1df2de1d7325a6d6031a6fb12a6e6e5533e5cee` |
| `man0l020/man0l020` | 15089184 | `8fbfc1b7f15737c737e2292f1a7fe5dcc0487f360f1971892808bc9bc1524b6d` |

These records show authored names. They do not show which motion data the
client resolves for a record, the layer or blend it uses, or that the motion
plays. It is not established that joint keys 0 to 3 of pair 13 are hair model
joints.

## Limits

- The counts cover installed motions. They do not show which motions a client
  session loads or plays.
- Only `Header` byte `+0x0c` was counted. Bits 1 and 2 are not interpreted
  here.
- The two flagged motions are examples. No pose was compared with client
  output.
