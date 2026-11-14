# Sound container bus byte

Every installed sound container holds one small record whose second byte
takes only the values of the sound driver's named buses. This page records
that byte across client extraction `2012.09.19.0001` and by sound bank. It
measures the installed bytes only. The driver routine that reads the byte
was not traced, so its role as the bus of the sound is INFERRED.

## Method

Python `3` standard-library reads of a contributor-supplied install whose
`game.ver` reads `2012.09.19.0001`. Every file below `data/` whose first
eight bytes are `SEDBSSCF` was read. There are 77694 such files, the count
`xivl sscf-census` reports as `sedbSscf` for the same install. No container
bytes are reproduced here.

The container header carries a little-endian u32 at file offset `0x50`.
`xivl-tools:docs/formats/sscf.md`, "Table header", names it the block E
offset and leaves its target unknown. Let `p` be that value. The measured
byte is the one at file offset `p + 1`.

## Values

The byte takes nine values. It is never 0, 9, 10 or above 11.

| Value | Files |
| ---: | ---: |
| 1 | 110 |
| 2 | 71026 |
| 3 | 4250 |
| 4 | 83 |
| 5 | 1100 |
| 6 | 813 |
| 7 | 137 |
| 8 | 1 |
| 11 | 174 |

The driver configuration text declares eleven bus lines in the order
`MUSIC`, `SE`, `VOICE`, `System`, `BG`, `Foot`, `PlacedNPC`,
`StringendoMUSIC`, `NULL9`, `NULL10` and `HQ`
(`xivl-decomp:docs/resource/sound-effect-triggers.md`, "Driver
configuration"). The two absent values 9 and 10 are the positions of the
two `NULL` lines.

## Values by bank

A bank is the first two path components below `data/`. The bank roles are
those of `xivl-decomp:docs/resource/sound-effect-triggers.md`, "Number
split and category table" and "Footsteps".

| Bank | Role | Values |
| --- | --- | --- |
| `data/03/5B` | category 0, markup sound numbers | 4 in 79 files, 2 in 3, 3 in 1 |
| `data/07/FE` | category 1, songs | 1 in 104 files, 4 in 4, 8 in 1 |
| `data/07/FD` | category 2 | 3 in 425 files |
| `data/5B/2D` to `data/5B/3E` | categories 3 to 20, creation voice samples | 3 in 990 files |
| `data/8A/0A` | category 21 | 3 in 1 file |
| `data/08/07` | first footstep resource | 6 in 768 files, 2 in 2 |
| `data/1A/46` | second footstep resource | 6 in 45 files |

The files that depart from the majority value of their bank:

| File | Value |
| --- | ---: |
| `data/03/5B/00/37.DAT` | 2 |
| `data/03/5B/00/38.DAT` | 2 |
| `data/03/5B/00/39.DAT` | 2 |
| `data/03/5B/00/45.DAT` | 3 |
| `data/07/FE/00/4F.DAT` | 4 |
| `data/07/FE/00/5D.DAT` | 4 |
| `data/07/FE/00/65.DAT` | 4 |
| `data/07/FE/00/6B.DAT` | 4 |
| `data/07/FE/00/61.DAT` | 8 |
| `data/08/07/00/00.DAT` | 2 |
| `data/08/07/00/01.DAT` | 2 |

The category 1 bank holds 110 files and 109 containers. Its index 0 file is
empty.

## Reading

The byte agrees with a one-based index into the bus lines of the driver
text. The majority value of each bank is the bus its role suggests:
`System` for the markup sounds, `MUSIC` for songs, `VOICE` for voice
samples and `Foot` for footsteps. Category 0 indexes 55 and 56, the files
`00/37` and `00/38`, are the two message sounds that the client plays at a
target actor position
(`xivl-decomp:docs/resource/sound-effect-triggers.md`, "Consumer
implications"), and they name 2, the `SE` line that the driver text marks
`3D`.

The values also agree with the configured volume writes of
`xivl-decomp:docs/resource/sound-effect-triggers.md`, "Configured bus
gains": `music_volume` writes buses 1 and 8, `sys_volume` bus 4,
`se_volume` buses 2, 6, 7 and 11, `voice_volume` bus 3 and
`env_sound_volume` bus 5. Those nine bus numbers are exactly the nine
values the byte takes.

This is an agreement of installed values with separately recorded bus
numbers. It is INFERRED that the driver plays a container on the bus this
byte names.

## Limits

- The driver reader of the block E record was not traced.
- The other bytes of the record were not interpreted. The first byte of
  the record is not constant across the install.
- Stream tables, codecs and the other header fields are outside this page.
