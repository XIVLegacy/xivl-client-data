# Character creation sheet shapes

These records cover the shapes of the four creation sheets that the
BootupManager opens, `boot_skillequip`, `boot_charaTemp`, `boot_charaLook`
and `boot_charaParts`, and the appearance window forms whose Button counts
match the value lists of `boot_charaParts`. The holders and registration of
the sheets in the executable are in
`xivl-decomp:docs/resource/character-select-status-block.md`, "Creation
sheet holders". Facts marked `STATIC` are decoded static client data
(`client_extraction`). `INFERRED` marks an interpretation that no reader
trace confirms. The joins of "Joins by count and membership" come from the
data alone. The "Window table join" section tests the executable's
appearance window table against the data.

Column positions are zero-based after the row ID.

## boot_skillequip

STATIC. The sheet holds 1020 rows of 22 `s32` cells. Its first key run is
101 to 144, 44 rows. In that run the rows 102, 103, 104, 107, 108, 122,
123, 129 to 136 and 139 to 141 hold a nonzero cell 0. Every other row of
the run holds 0 in cells 0 to 7, the values 1184, 1792, 1024 and 1152 in
cells 8 to 11, and 0 in cells 12 to 21.

INFERRED. A key of the first run is 100 plus a class ID, the nonzero rows
being the classes offered at creation, and the 22 cells are seven weapon
words, six gear words and nine accessory words of the appearance record
(`xivl-decomp:docs/actor/appearance-path-decoder.md`, "Wire index to helper
field"). Which row and cells the creation preview reads is not traced.

## boot_charaTemp

STATIC. The sheet holds 15 rows keyed 1 to 15 with 18 `s32` cells, read here
as nine pairs. For row `t` the first members of pairs one to eight are the
eight consecutive keys from `6900001 + 8 * (t - 1)`, and pair nine repeats
the key of pair eight. The second member is nonzero in pairs one to four
and zero in pairs five to nine, in every row.

## boot_charaLook

STATIC. The sheet holds 60 rows of 41 `s32` cells. Its keys are exactly the
first members of pairs one to four of `boot_charaTemp`. No key of pairs five
to nine names a row. Cell 0 holds one value per tribe:

| Tribe rows | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Cell 0 | 1 | 2 | 9 | 3 | 4 | 3 | 4 | 5 | 6 | 5 | 6 | 8 | 8 | 7 | 7 |

The tribe of a look row is `(key - 6900001) / 8 + 1`.

STATIC. Cells 19 to 40 have the 22-cell layout of `boot_skillequip`. In
every row cells 19 to 25 hold 0, and cells 27 to 30 hold four nonzero
values.

## boot_charaParts

STATIC. The sheet holds 15 rows keyed 1 to 15 with 25 `str` cells. Each cell
is a comma list, and an entry may itself be a `/` list.

| Cell | Entries per row | Note |
| ---: | --- | --- |
| 0 | 16 | numbers |
| 1 | 4, 8 or 9 | numbers |
| 2 | as many as cell 1 | a number or a `/` list each |
| 3 | 32 | numbers |
| 4 | 16 | numbers |
| 5 | 4 | numbers |
| 6, 8 | 32 | ascending from 0 |
| 7 | 8 | ascending from 0 |
| 9 | 5 | `4,3,2,1,0` in every row |
| 10 | 3 | numbers |
| 11 | 2 | `1,0` or `0,1` |
| 12 to 17 | 1 to 7 | ascending from 0 |
| 18, 20 | 16 | six-digit hexadecimal colours |
| 19 | 32 | six-digit hexadecimal colours |
| 21 | 32 | `0` followed by 31 six-digit hexadecimal colours |
| 22 | 4 | six-digit hexadecimal colours |
| 23 | 8 | numbers |
| 24 | 4 | `/` lists |

STATIC. Each number of row 1 cell 5, `1,2,7,8`, names an installed face
directory `client/chara/pc/c001/kao/f<NNN>`. The install holds `f001`,
`f002`, `f005`, `f007` and `f008` there and no `f003` or `f004`.

## Appearance windows

STATIC. The window forms under `client/sqwt/system/bootup/charactercreation/`
name the Buttons `Button_CharaMake_<n>` and one `Button_CharaMake_WindowClose`.
Their counts of `Button_CharaMake_<n>`:

| Form | Buttons | Form | Buttons |
| --- | ---: | --- | ---: |
| `AppearancePhaseSizeWin` | 5 | `AppearancePhaseFaceEyeWin` | 6 |
| `AppearancePhaseVoiceWin` | 3 | `AppearancePhaseFacePupilWin` | 2 |
| `AppearancePhaseSkinColorWin` | 16 | `AppearancePhaseFacePColorWin` | 16 |
| `AppearancePhaseHairStyleWin` | 9 | `AppearancePhaseFaceNoseWin` | 6 |
| `AppearancePhaseHairVaWin` | 5 | `AppearancePhaseFaceMouthWin` | 4 |
| `AppearancePhaseHairColorWin` | 32 | `AppearancePhaseFaceContWin` | 4 |
| `AppearancePhaseHairMColorWin` | 32 | `AppearancePhaseFColorWin` | 4 |
| `AppearancePhaseFaceTypeWin` | 4 | `AppearancePhaseFTColorWin` | 4 |
| `AppearancePhaseFaceEyebroWin` | 6 | `AppearancePhaseFeatureWin` | 3 |

STATIC. The menu Buttons sit in the templates. `AppearancePhase.tpl`
declares `Button_MenuBig_1` to `_6` captioned `@100351` to `@100356`, and
`Button_MenuBig_7` (`@100260`) inside a Grid with `Visibility="collapsed"`.
`AppearancePhaseHair.tpl` declares six menu Buttons, `AppearancePhaseFace.tpl`
ten and `AppearancePhaseFeature.tpl` five after the five CheckBoxes
`CheckBox_APF_Feature1` to `5`. The last two of each of these three lists are
captioned `@100264` and `@100263`.

## Joins by count and membership

INFERRED. For every one of the 60 `boot_charaLook` rows, these cells are
members of the listed `boot_charaParts` cell of the row's tribe:

| `boot_charaLook` cell | `boot_charaParts` cell | Window with as many Buttons |
| ---: | ---: | --- |
| 1 | 9 | Size, 5 |
| 2 | 1 | Hair style, 9 |
| 5 | 5 | Face type, 4 |
| 15 | 3 | Hair colour, 32 |
| 16 | 0 | Skin colour, 16 |
| 17 | 4 | Eye colour, 16 |
| 18 | 10 | Voice, 3 |

Read with the window counts, cell 9 lists the size values in the order of
the Size window's Buttons, cell 10 the voices, cell 0 the skin tones, cell 1
the hair styles, cell 3 the hair colours, cell 4 the eye colours, cell 5
the faces and cell 11 the iris sizes, and the look cells hold a template's
value of each. Membership is a weak test for cells whose lists run from 0,
so the cells of eyebrows, eye shape, nose, mouth, features, highlights and
ears, `boot_charaParts` cells 23 and 24 and the remaining `boot_charaLook`
cells are not settled.

## Window table join

The appearance window table of the executable pairs each window with three
cells. Its entries, the `boot_charaParts` loader and the readers of each
dword are in `xivl-decomp:docs/resource/character-select-status-block.md`,
"Parts loader" and "Appearance window table". There the second dword is
passed to the tribe's `boot_charaParts` list and windows 6 and 17 store a
Button's index rather than a list entry.

STATIC. The loader reads a `/` entry as its last number plus one and the
entries of cells 18 to 22 as hexadecimal. With that reading, the first
dword of each window entry names a `boot_charaLook` cell whose value, in
all 60 look rows, is a member of the second dword's `boot_charaParts` list
for the row's tribe, or for windows 6 and 17 an index into it:

| Window | Window form | `boot_charaLook` cell | `boot_charaParts` cell | Colour cell | Rows that fit |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | `AppearancePhaseSizeWin` | 1 | 9 | | 60 |
| 1 | `AppearancePhaseVoiceWin` | 18 | 10 | | 60 |
| 2 | `AppearancePhaseSkinColorWin` | 16 | 0 | 18 | 60 |
| 3 | `AppearancePhaseHairStyleWin` | 2 | 1 | | 60 |
| 4 | `AppearancePhaseHairColorWin` | 15 | 3 | 19 | 60 |
| 5 | `AppearancePhaseHairMColorWin` | 3 | 8 | 21 | 60 |
| 6 | `AppearancePhaseHairVaWin` | 4 | 2 | | see below |
| 7 | `AppearancePhaseFacePColorWin` | 17 | 4 | 20 | 60 |
| 8 | `AppearancePhaseFaceTypeWin` | 5 | 5 | | 60 |
| 9 | `AppearancePhaseFaceEyebroWin` | 8 | 13 | | 60 |
| 10 | `AppearancePhaseFaceEyeWin` | 10 | 12 | | 60 |
| 11 | `AppearancePhaseFacePupilWin` | 9 | 11 | | 60 |
| 12 | `AppearancePhaseFaceNoseWin` | 11 | 14 | | 60 |
| 13 | `AppearancePhaseFaceMouthWin` | 13 | 15 | | 60 |
| 14 | `AppearancePhaseFeatureWin` | 14 | 17 | | 60 |
| 15 | `AppearancePhaseFaceContWin` | 12 | 16 | | 60 |
| 16 | none | 6 | 21 | | see below |
| 17 | `AppearancePhaseFColorWin`, `AppearancePhaseFTColorWin` | 7 | 22 | 22 | 60, as indices |

STATIC. Look cell 4 is 0 in every row. For 14 rows the template's hair
style has a `/` entry in cell 2, so 0 is an index below its count. For the
other 46 rows that entry is `0`, which the loader reads as a count of 0.
Look cell 6 holds values from 0 to 12. Only the 17 rows whose value is 0
are members of cell 21, whose first entry is `0`, and every value is below
the 32 entries of cell 21.

INFERRED. The seven joins of the previous section are the windows 0, 1, 2,
3, 4, 7 and 8 of this table. The table settles the cells of the other
windows: highlights cell 8, eyebrows 13, eye shape 12, iris 11, nose 14,
mouth 15, `AppearancePhaseFaceContWin` 16 and `AppearancePhaseFeatureWin`
17, and look cell 4 is a hair variation index. Window 16 has no form push,
and its look cell 6 reads as an index into cell 21. Which windows show
features and ears, and the meaning of window 16, are not settled.

## Source identity and reproduction

The install labels are `game.ver` `2012.09.19.0001` and `patch.ver` `1.23b`.
`xivl extract <game-directory>` reproduces the four sheets with the member
hashes recorded in [tables.json](../manifests/tables.json):

| CSV | Bytes | SHA-256 |
| --- | ---: | --- |
| `boot_skillequip.csv` | 69295 | `72E1861DBC07A3025FC056CBB8784E943129F40DF69C959D11C961C025486CB5` |
| `boot_charaTemp.csv` | 1626 | `8925D315DEBCD869C630BBE793A2D6B0137A982B3773EF2080CFEED17B49F0C5` |
| `boot_charaLook.csv` | 6582 | `8BD2A1241EB314053F2808BBE9CD6D5A2DA6D6A361FC4971AAFFF6843C13C4D6` |
| `boot_charaParts.csv` | 21107 | `BA3346916B246C50AF5ECAF7DDBE48E340A9FDAB5D89D56915D063F75810525C` |

Split each `boot_charaParts` cell on commas and each entry on `/` for the
membership test. For the window table join, read an entry with `/` as its
last number plus one and the entries of cells 18 to 22 as hexadecimal, take
the tribe of each `boot_charaLook` row from its key, and test each look cell
of the table against its window's list, or against the list's count for
windows 6 and 17, with the hair style's cell 2 count for window 6. Decode the forms and templates with `xivl extract-resource`
and count the `Button` and `CheckBox` elements by name.
