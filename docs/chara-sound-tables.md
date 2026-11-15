# Character and weapon sound tables

The installed `_snd` files and the voice bank hold the sound ids that the
action sound clip plays. This page records their layout, counts and selected
entries across client extraction `2012.09.19.0001`. It measures installed
bytes only. The client routines that load and index these tables are in
`xivl-decomp:docs/resource/chara-action-sound-clip.md`.

## Method

Python `3` standard-library reads of a contributor-supplied install whose
`game.ver` reads `2012.09.19.0001`. No file bytes are reproduced here. A
sound id `0xAABBCCDD` names the file `data/AA/BB/CC/DD.DAT`. The bus value of
a sound is the byte that [Sound container bus byte](sound-container-bus-byte.md)
measures in that file.

## Layout

Every file read for this page is a bare array of little-endian u32 sound ids
with no header. Its length over 4 is the id count.

| File | Bytes | Ids |
| --- | ---: | ---: |
| `client/chara/mon/m502/equ/e002/top_snd/0001` | 940 | 235 |
| `client/chara/pc/c001/equ/e001/top_snd/0000` | 600 | 150 |
| `client/chara/wep/w058/equ/e001/top_snd/0000` | 560 | 140 |
| each of the 64 files of `data/27/D9/00` | 220 | 55 |

## Directories

Every `_snd` directory below `client/chara` is named `top_snd`. There are
401 of them: 113 below `mon`, 68 below `pc` (64 of them in `c001`, 2 in
`c003`, 1 in `c006` and 1 in `c009`) and 220 below `wep`. For 347 of the
401, the file names of `top_snd` equal the file names of the `top_tex1`
directory beside it. `pc/c001/equ/e010` lists `0000` to `0013` in both, and
`wep/w076/equ/e001` lists `0000` to `0011` in both.

## Voice bank

`data/27/D9/00` holds 64 files of 55 ids each, `00.DAT` to `11.DAT` and
`5B.DAT` to `88.DAT`. Ids 1 to 4 of every file name a sound container whose
bus value is 3 (VOICE), 256 of 256.

## Selected entries

Entry `k` is the u32 at byte offset `4 * k`.

| File | Entry | Id | Bus value |
| --- | ---: | --- | ---: |
| `mon/m502/equ/e002/top_snd/0001` | 32 | `0x83DC0084` | 2 |
| `mon/m502/equ/e002/top_snd/0001` | 99 | `0x83DC0009` | 2 |
| `mon/m502/equ/e002/top_snd/0001` | 109 | `0x83DC0013` | 2 |
| `pc/c001/equ/e001/top_snd/0000` | 14 | `0x5EE00006` | 2 |
| `wep/w058/equ/e001/top_snd/0000` | 4 | `0x5DAC0009` | 2 |
| `wep/w058/equ/e001/top_snd/0000` | 74 | `0x5DAC003B` | 2 |

INFERRED. With the load and play bases of the decomp page, a monster table
loaded at entry 0 answers play group 2 index 2 with entry 32 and play group 4
indexes 4 and 14 with entries 99 and 109. A player table loaded at entry
`0x55` answers play group 4 index 4 with its entry 14. A 140-id weapon
table answers hand 0 index 4 with entry 4 and hand 1 index 4 with entry 74,
half the count further on. The `%04d` of a `top_snd` path is the texture
number of the same part, from the shared file names.
