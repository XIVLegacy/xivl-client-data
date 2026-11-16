# Character creation sheet shapes

These records cover the shapes of the four creation sheets that the
BootupManager opens, `boot_skillequip`, `boot_charaTemp`, `boot_charaLook`
and `boot_charaParts`, and the appearance window forms whose Button counts
match the value lists of `boot_charaParts`. The holders and registration of
the sheets in the executable are in
`xivl-decomp:docs/resource/character-select-status-block.md`, "Creation
sheet holders". Facts marked `STATIC` are decoded static client data
(`client_extraction`). `INFERRED` marks an interpretation that no reader
trace confirms. No reader of these sheets has been traced, so every join
below comes from the data alone.

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
membership test. Decode the forms and templates with `xivl extract-resource`
and count the `Button` and `CheckBox` elements by name.
