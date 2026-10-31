# Grand Company dialogue row variants

The canonical localized tables preserve these distinct text-row pairs:

| Table rows | Bounded text comparison |
| --- | --- |
| `com0l1` `34` / `58` | The English cells are identical, while the Japanese cells differ. Both versions discuss the Archon's prophecies. |
| `com0g1` `34` / `62` | Both versions describe surviving the Archon's attack. Row `34` addresses a reunion; row `62` omits that greeting. |
| `com0u1` `32` / `58` | Both versions refer to Mezaya's poetry. Row `32` offers to recite it; row `58` responds to the listener's surprise. |

These observations establish only that the localized tables contain different
text for the listed rows. A recognition or familiarity interpretation is
plausible, but the rows do not identify which condition selects them or prove
that a character had previously met the speaker. The related bytecode branch
in `xivl-decomp:docs/event/grand-company-mission-bytecode.md` records a
Boolean-`true` fade choice; it does not bind these text rows to that argument.
The historical argument producer and active branch remain unknown.

Sources: `xivl-client-data:csv/com0l1.csv` rows `34` and `58`, SHA-256
`3a70957c1099e45ce5e7e281d1e7e5ddcfc79d08d1f00a78513780d164e93457`;
`xivl-client-data:csv/com0g1.csv` rows `34` and `62`, SHA-256
`aee12f7bf80aab74fd5362a6dd3c09d6cedd209c97d99424b1111ce69fb42ac4`;
and `xivl-client-data:csv/com0u1.csv` rows `32` and `58`, SHA-256
`1101bce35ca6f91fc5536690d56d9f51c3df7a26518fe1a36f60969f46f80aa8`.
The digests are pinned in `manifests/tables.json`; all three tables are from
extraction `2012.09.19.0001`.

## Journal parameter branches

The first Grand Company quest rows in `xtx_quest` carry two parameter
branches in their journal text. Both test unary integer-parameter
expressions, written here as `$E8(n)`. The raw bytes `E8 02`, `E8 03`, and
`E8 04` encode `$E8(1)`, `$E8(2)`, and `$E8(3)`, because a compact integer
lead decodes to its value plus one.

| Quest row | Title | Journal sheet | `$E8(3)` is 1 | Otherwise | `$E8(2)` item lookup |
| --- | --- | --- | ---: | ---: | --- |
| `111401` | The Price of Integrity | `xtx/journalxtxSea` | `265` | `232` | `11000254`, Signed Agreement |
| `111601` | Breaking the Seals | `xtx/journalxtxFst` | `327` | `275` | `11000251`, Ailith's Oath |
| `111801` | Career Opportunities | `xtx/journalxtxWil` | `395` | `340` | `11000252`, Taylor's Letter |

The active-text columns, header indices `13`-`16` and `35`, hold four
`if` tokens keyed on `$E8(1)` with code `E4` and integers 0 through 3. The
branch for integer 2 nests a second `if` with payload `E0 E8 04 02`, which
compares `$E8(3)` with integer 1. Its true operand references the row in
the `$E8(3)` is 1 column, and its false operand references the row in the
Otherwise column.
Header indices `18`-`21` and `36` repeat the same nested choice under
`$E8(1)` tests with code `E0`. The tracked expression grammar retains these
binary codes without naming their comparisons. Read as equality or as a
lower bound, the nested test selects the true row for parameter value 1
and the false row for value 0.

Header indices `22`-`25` and `37` each hold one `if` with payload
`E0 E8 03 02`, which compares `$E8(2)` with integer 1. Its true operand is
an `xtx/itemName` lookup of the listed item, and its false operand is empty.
The sheet does not label these columns. Reading them as the journal reward
line is an interpretation.

In each Japanese pair, the Otherwise row introduces the speaker with a
race noun, Miqo'te, Lalafell, or Hyur, and the `$E8(3)` is 1 row names the
speaker without one. Only the Sea English cells differ. Row `232` introduces a
mysterious Miqo'te named Y'shtola, and row `265` calls her a familiar face.
The Fst and Wil English cells are identical. The inference is that
`$E8(3)` value 1 marks a player who has already met the speaker. The rows do
not identify the server state that produces either parameter, and they do
not bind these journal branches to the dialogue rows above.

The plain sheet lists in header indices `28`-`31` and `38` name Sea `266`,
Fst `328`, and Wil `396` in the third position. Neither active-text branch
selects those rows, and the available sources do not explain the
difference.

Sources: `xivl-client-data:csv/xtx_quest.csv` rows `111401`, `111601`, and
`111801`, physical lines `426`, `460`, and `494`, SHA-256
`938640466b314242916f1f8877a90154c4f4db7aa63de6223e6af4aa194e6719`
(`manifests/tables.json:6267-6271`).
`xivl-client-data:csv/xtx_journalxtxSea.csv` rows `232`, `265`, and `266`,
SHA-256 `051c2501dc9d362e7ffc1c6ec3c840ae9458c95e583fde517ba4a610297d198d`
(`manifests/tables.json:6187-6191`).
`xivl-client-data:csv/xtx_journalxtxFst.csv` rows `275`, `327`, and `328`,
SHA-256 `82dfee149d4571e83e85db585f8ae6415fe55b4273764ca0c59d37dd10367189`
(`manifests/tables.json:6171-6175`).
`xivl-client-data:csv/xtx_journalxtxWil.csv` rows `340`, `395`, and `396`,
SHA-256 `80da9c607d81f58dc7c7a9625ecd4f6cefaba32bb3448c73f85c3c8082bdd694`
(`manifests/tables.json:6195-6199`).
`xivl-client-data:csv/xtx_itemName.csv` rows `11000251`, `11000252`, and
`11000254`, SHA-256
`917c34eb0621b7d7a8261145023d0bb95cd8ca9eb52288ceb66e80d08f0d78c2`
(`manifests/tables.json:6163-6167`). All five tables are from extraction
`2012.09.19.0001`. Expression grammar:
`xivl-tools:docs/formats/ssd-sheet.md`, "Rich-string read and text-export
contract", at revision `fd4c97d89eab3bbbf657021297e3d78156c63319`.
