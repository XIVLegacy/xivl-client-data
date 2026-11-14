# Weapon class index and attach table members

Two installed resource members carry the data that places a weapon model on
a character: a class index keyed by weapon number, and a per-skeleton attach
table keyed by class tag. This page records where each member sits in client
extraction `2012.09.19.0001`, its measured layout, and the selected rows that
tie the two together.

The native readers of both members are recorded in
`xivl-decomp:docs/actor/weapon-slot-attach-and-sheathe.md`, sections "Class
tag arrays" and "Attach table lookup". The field meanings below come from
those readers. The measurements here establish only what the installed bytes
hold. They do not establish which resource a running client selects.

## Method

Python `3` standard-library reads of a contributor-supplied install whose
`game.ver` reads `2012.09.19.0001`. A resource file is a PWIB wrapper
(signature `PWIB`, big-endian first-segment offset at `+8`) whose first
segment is a `SEDB` `RES ` directory: entry count at `+0x30`, name offset at
`+0x34`, name count at `+0x38`, 16-byte entries from `+0x40` (name index,
offset, length, one unread dword), with entry and name offsets relative to
the end of the entry array. The same framing is described in
`xivl-decomp:docs/actor/locomotion-bank-census.md`, "Identity and method".
The entry named `RESOURCE_TYPE` holds one four-byte type word per member and
the entry named `RESOURCE_ID` holds 16-byte member names.

No member bytes are reproduced here. Whole-file and member SHA-256 values
identify the inputs.

## Class index member

| Installed file | Bytes | SHA-256 |
| --- | ---: | --- |
| `data/15/D9/00/00.DAT` | 4973264 | `10b8d7dc501a14a640e8338b0e17d2cc521756583fe4ed68859071d004b453e6` |
| `data/15/D9/00/01.DAT` | 1189004 | `9b1fca85933590e6e4d66a1b670408383519ef70b788a5118c3d61cc3c1df891` |

In both files the directory has three members before the two metadata
entries. Their `RESOURCE_ID` names are `InGame_Vfx`, `weponindex` and
`btlcmn`. Member 1, `weponindex`, has type word `cibp` (`0x63696270` as a
little-endian dword), entry name `chr\cib\cibw\weponindex` and length
`0x12A4`, the smallest size the native Cibp constructor admits.

| File | `weponindex` SHA-256 | Rows equal to `0xFFFFFFFF` |
| --- | --- | ---: |
| `00.DAT` | `6bf22adb5f7fce9059477653559900938ac0568ced4db3159ae7faaaa0eea123` | 865 |
| `01.DAT` | `f73fcbb61016a1b58798a82619609759f005381ed9664ec9d239e608941fb9bc` | 913 |

Layout, both files:

| Offset | Content |
| --- | --- |
| `+0x000` | one dword, zero as installed |
| `+0x004` | 256 class tags of three bytes each |
| `+0x304` | 1000 little-endian dwords, one row per weapon number |

Each row byte indexes the tag table. Byte 0 is the attach class. Bytes 1, 2
and 3 are the tags that `xivl-decomp:docs/actor/weapon-set-directories-and-battle-banks.md`
joins into the `bid`, `cid` and `pid` set directory names.

The named tags of `00.DAT`, by index: 0 `emp`, 1 `asl`, 2 `sld`, 3 `clw`,
4 `swd`, 5 `2sp`, 6 `stf`, 7 `2st`, 8 `rap`, 9 `clb`, 10 `gun`, 11 `2sw`,
12 `2ax`, 13 `2bw`, 14 `qvr`, 15 `arw`, 16 `trw`, 17 `gdt`, 18 `saw`,
19 `hmm`, 20 `ras`, 21 `ndl`, 22 `pic`, 23 `svl`, 24 `tbl`, 25 `hel`,
26 `sht`, 32 `min`, 33 `fel`, 34 `fsh`, 35 `ani`, 48 `wod`, 49 `blk`,
50 `arm`, 51 `gld`, 52 `lth`, 53 `sew`, 54 `alc`, 55 `cok`, 56 `_al`,
57 `_sr`, 64 `ccm`, 65 `ccb`, 66 `awo`, 67 `abl`, 68 `aar`, 69 `agl`,
70 `alt`, 71 `ase`, 72 `aal`, 73 `aco` and 255 `nul`. Every other index
holds its own number as three decimal digits. In `01.DAT` index 26 and
indices 64 to 73 hold digits instead of a name.

A row of `0xFFFFFFFF` selects tag 255 for all four bytes.

Rows of `00.DAT` that are not `0xFFFFFFFF`, grouped by their four tags in
byte order 0 to 3:

| Tags | Weapon numbers |
| --- | --- |
| `ccm emp emp emp` | 1 |
| `ccb emp emp emp` | 2 to 4 |
| `sld sld emp emp` | 25, 31 |
| `clw clw emp emp` | 51, 56 to 69 |
| `swd swd emp emp` | 76 to 80, 104 |
| `sht emp emp emp` | 100 |
| `2sw 2sw emp emp` | 101 to 103, 386 |
| `rap rap emp emp` | 121 |
| `2ax 2ax emp emp` | 141 to 143 |
| `2sp 2sp emp emp` | 161 to 168, 301 |
| `clb clb emp emp` | 186 |
| `2bw 2bw emp emp` | 201 to 203, 205 |
| `arw emp emp emp` | 221 |
| `qvr emp emp emp` | 226 |
| `gun gun emp emp` | 231, 232 |
| `stf stf emp emp` | 246, 281, 316, 351, 501, 551, 601, 651 |
| `2st 2st emp emp` | 261, 296 to 299, 331 to 333, 366, 525, 575, 625 |
| `gdt gdt emp emp` | 396, 901 to 903, 907, 908, 912, 914, 990 |
| `trw emp emp emp` | 406, 416 |
| `2st 2st nul emp` | 675 |
| `_al emp emp emp` | 683, 689, 719, 743, 749 |
| `_sr emp emp emp` | 684, 698, 713, 729, 744, 773, 788, 833, 848, 863, 878 |
| `tbl emp emp emp` | 728, 758, 774, 898 to 900 |
| `hel gdt emp emp` | 904 to 906, 909 to 911 |
| `gdt emp emp emp` | 913 |
| byte 0 `saw`, byte 2 `wod` | 673 |
| byte 0 `awo`, byte 2 `wod` | 674 |
| byte 0 `hmm`, byte 2 `blk`, `arm`, `gld` | 688, 703, 718 |
| byte 0 `abl`, `aar`, `agl`, byte 2 `blk`, `arm`, `gld` | 690, 704, 720 |
| byte 0 `ras`, byte 2 `lth`, `alc`, `cok` | 733, 763, 778 |
| byte 0 `alt`, `aal`, `aco`, byte 2 `lth`, `alc`, `cok` | 734, 764, 779 |
| byte 0 `ndl`, byte 2 `sew` | 748 |
| byte 0 `ase`, byte 2 `sew` | 750 |
| byte 0 `pic`, byte 3 `min` | 823 |
| byte 0 `svl`, byte 3 `fel`, `fsh`, `ani` | 838, 853, 868 |

Rows named by byte position have `emp` in the unnamed positions. Where a
row lists several tags and several weapon numbers, they pair in order.

The `01.DAT` member has fewer populated rows and differs in some of them.
For example row 1 is `asl sld emp emp` and row 396 is `trw emp emp emp`
there. Which of the two files a running client loads is not established
here.

## Attach table member

`client/chara/pc/c001/skl/0001` is 54672 bytes with SHA-256
`d90a756fc1cba6f03bb8dc102b367feb905b5e57a00d209ff4fccddaa17cd031`.
Member 0 of its directory is named `cib\ciba\pc\info_c001`, has type word
`ciba`, length 4888 (`0x1318`) and SHA-256
`82f998daaf1d598eef40fd9e4fc901f943bb164b370ecc7a4091a0fc20b03471`.
`xivl-decomp:docs/actor/ciba-pointer-source.md` records the same span and
hash.

Layout:

| Offset | Content |
| --- | --- |
| `+0x000` | one dword, zero as installed |
| `+0x004` | classes of `0x84` bytes each, `(length - 4) / 0x84` of them |

Class layout:

| Offset | Content |
| --- | --- |
| `+0x00` | three-letter tag followed by a space |
| `+0x04` | eight records of 16 bytes, index `flag + 2 * hand` |

Record layout, all fields little-endian 16-bit:

| Offset | Content |
| --- | --- |
| `+0x00` | joint index into the native name table |
| `+0x02` | scale in thousandths |
| `+0x04`, `+0x06`, `+0x08` | translation in thousandths |
| `+0x0A`, `+0x0C`, `+0x0E` | three angles in hundredths of a degree |

The six fields from `+0x04` are stored as sign and magnitude: bit 15 is the
sign and the low 15 bits the magnitude. The native initializer converts them
in place before use. The c001 member has 92 such fields with the sign bit
set.

The c001 member holds 37 classes, in order `emp asl sld clw swd rap clb gun
stf 2sw sht 2ax 2sp 2st 2bw qvr arw trw gdt saw hmm ras ndl pic svl tbl _al
_sr hel awo abl aar agl alt ase aal aco`. The largest joint index in it is
14, the last index of the native table. The `skl/0001` files of c001
through c009 each carry a 4888-byte member 0 of this type with 37 classes.
Those of c021 through c025 carry 3700 bytes and 28 classes. c010 and c999
have a different member order and were not decoded.

Selected records of the c001 `swd` class:

| Hand | Flag | Joint index and native name | Scale | Translation and angles |
| ---: | ---: | --- | ---: | --- |
| 0 | 0 | 0 `n_buki_r` | 1000 | all zero |
| 0 | 1 | 7 `j_buki_kosi_l` | 900 | nonzero |
| 1 | 0 | 1 `n_buki_l` | 1000 | all zero |
| 1 | 1 | 6 `j_buki_kosi_r` | 900 | nonzero |

The same pattern holds for the `clw`, `sld`, `2ax` and `2sp` classes of
c001: the flag 0 record of hands 0 and 1 names an `n_buki*` joint with scale 1000
and no offset, and the flag 1 record names a hip or back joint
(`j_buki2_kosi_*`, `j_buki_sebo_*`) with scale 900 and a nonzero offset. The
hands 2 and 3 records of those classes all name joint 0 with no offset.

The c001 `arw` class names joint 14, `n_gen`, in the flag 0 record of hands
0 and 1. A byte search of the whole `client/chara/pc/c001/skl/0001` file
finds the strings `n_buki_r`, `j_buki_kosi_l`, `j_buki_sebo_r` and `n_throw`
and does not find `n_gen`.

## Limits

- The joint names come from the native table, not from these members.
- The order in which the three angles compose is not established.
- The measurements cover the files named above. Other skeleton files and
  the monster and weapon trees were not read.
