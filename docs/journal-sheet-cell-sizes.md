# Journal text cell sizes and ComboBox declarations

Journal and quest text sheets hold text cells far larger than 256 bytes in
`ja`, `en`, `de` and `fr`. The largest is 2759 bytes.
`JournalListWidget.tpl` declares one ComboBox template, and `default.style`
and `default.skin` declare the `COM_basis` parts and skins listed below.
`JournalListWidget.form` names that template and style on its one `ComboBox`.

## Sheet sources and measure

These are `client_extraction` findings for supplied build `2012.09.19.0001`.
Neither the resources nor their decoded rows are distributed here.

| Sheet | Definition resource | Bytes | SHA-256 | Decoded bytes | Decoded SHA-256 |
| --- | --- | ---: | --- | ---: | --- |
| `xtx/journalxtxFst` | `data/0B/45/08/30.DAT` | 1739 | `f7cc05881295d3d577db4db3e846b4c18981f3fa2cc70e1a96e64d6e49176439` | 1738 | `7a8a30f537fdefbb251f26ba65f7d355b77b481b827fc86eda4430d118b36e3b` |
| `xtx/journalxtxRoc` | `data/0B/45/08/3D.DAT` | 1739 | `e40b62dc63708893a1291de93d2c8b57bd55d46b959575848937d01d2d072f7b` | 1738 | `5c291dac8b8ebee9ae85ca964bfc4dec47e5b4742ccf86a4f623a0eee42671e8` |
| `xtx/journalxtxSea` | `data/0B/45/08/17.DAT` | 1739 | `98ba224968f2287e7743971570336859fcfaf65b10e917e61992d1983094c9de` | 1738 | `40c3e3d46ee750bceade01fc0881a262b7c677b5079e165d78e3e4444461b324` |
| `xtx/journalxtxWil` | `data/0B/45/08/4A.DAT` | 1739 | `b443f70a3729513676cb8e04f72ee8d3676a137d0ca071c19b854729ded36229` | 1738 | `d023c539b4718df4c81b22b04f02adf81308ef02db5c817edd9c887304834ba6` |
| `xtx/quest` | `data/0B/45/04/59.DAT` | 5555 | `f15a895b3658ab56ca42b0d632f43e5d5b2d31506686de56ee7fba1dfb6004d6` | 5554 | `af1c39aad5632a41f5c231db2a987232a6538253928c2c5c9c582de89b239332` |

The measure follows
[xivl-tools:docs/formats/ssd-sheet.md, sheet documents, rows and strings](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/docs/formats/ssd-sheet.md#the-sheet-string-and-its-obfuscation).

1. Decode each definition through `xivl extract-resource` with the
   `scrambled-xml` reader, and require the decoded identity above.
2. For each `ja`, `en`, `de` and `fr` sheet, follow every block's named data,
   enable and offset resources. Read every row with a nonempty span, walking
   its columns in declared type order. Require each row to consume its span
   and each enabled row to have a span.
3. Count each `str` value as one text cell. Its size is the decoded body
   length without the `0xFF` obfuscation marker or the NUL terminator. Rich
   tokens count at their stored byte length and are not evaluated.

Those four languages name 96 data, enable and offset resources. Hashing their
sorted `<8-digit uppercase hex id> <lowercase SHA-256>` lines, each ended by
LF, gives SHA-256
`08da8a908ab3604b280e267cf914bedd124b3072e7bf28b6eff42412ce370d1e`.

As a second reading, `xivl extract` exported the sheets to CSV. Converting each
cell back to bytes, with escapes reversed, rich-token markers restored and
duplicate markers dropped, reproduced every largest size with its row and
column, and every count of cells over 256 bytes. The CSV merges each sheet's
languages into one row set, so it does not separate enabled rows by language.

## Largest cells

Over 256 means strictly greater than 256 bytes. That threshold is a reporting
choice. It does not identify a client buffer limit. Each journal sheet has one
text column per language. Each `xtx/quest` language has 11 text columns, which
include the shared columns 27 and 56.

| Sheet | Language | Enabled rows | Text cells | Largest bytes | At row | Column | Cells over 256 |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: |
| `xtx/journalxtxFst` | `ja` | 701 | 701 | 2759 | 404 | 0 | 430 |
| `xtx/journalxtxFst` | `en` | 701 | 701 | 1748 | 370, 371 | 1 | 394 |
| `xtx/journalxtxFst` | `de` | 701 | 701 | 2386 | 404 | 2 | 402 |
| `xtx/journalxtxFst` | `fr` | 701 | 701 | 2279 | 404 | 3 | 407 |
| `xtx/journalxtxRoc` | `ja` | 47 | 47 | 1286 | 11 | 0 | 38 |
| `xtx/journalxtxRoc` | `en` | 47 | 47 | 883 | 11 | 1 | 38 |
| `xtx/journalxtxRoc` | `de` | 47 | 47 | 1290 | 11 | 2 | 38 |
| `xtx/journalxtxRoc` | `fr` | 47 | 47 | 1070 | 23, 24 | 3 | 33 |
| `xtx/journalxtxSea` | `ja` | 493 | 493 | 1577 | 351 | 0 | 289 |
| `xtx/journalxtxSea` | `en` | 493 | 493 | 1724 | 206 | 1 | 235 |
| `xtx/journalxtxSea` | `de` | 493 | 493 | 1467 | 351 | 2 | 249 |
| `xtx/journalxtxSea` | `fr` | 494 | 494 | 1383 | 351 | 3 | 282 |
| `xtx/journalxtxWil` | `ja` | 701 | 701 | 1994 | 398 | 0 | 449 |
| `xtx/journalxtxWil` | `en` | 701 | 701 | 1725 | 323 | 1 | 402 |
| `xtx/journalxtxWil` | `de` | 701 | 701 | 1464 | 561 | 2 | 428 |
| `xtx/journalxtxWil` | `fr` | 701 | 701 | 1384 | 561 | 3 | 389 |
| `xtx/quest` | `ja` | 735 | 8085 | 2729 | 110868 | 18 | 392 |
| `xtx/quest` | `en` | 735 | 8085 | 2727 | 110868 | 19 | 402 |
| `xtx/quest` | `de` | 735 | 8085 | 2729 | 110868 | 20 | 390 |
| `xtx/quest` | `fr` | 735 | 8085 | 2727 | 110868 | 21 | 394 |

These are stored sizes. No formatted output size is measured here.

## Widget sources

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `client/sqwt/widget/JournalListWidget.tpl` | 8692 | `12f30656cf5b8945ebec43f7c7756bc47a3e67ab8fe9160d09a2f15abb8a616f` |
| Template decoded strict UTF-8 XML | 8684 | `79a72fcae798b7250e8ec8d13eb410de615458573d077c7b4795cbc6050fd0ad` |
| `client/sqwt/common/default.style` | 353783 | `632b314cb2257fcbee42d4b002989a58dfeb42e64af864c1f5356336dc233dc0` |
| Style decoded strict UTF-8 XML | 353775 | `33bb178c3b172c62eeb65e8bcaf94f701a0ec3921564e27a619516900896d9f6` |
| `client/sqwt/common/default.skin` | 141967 | `6788f2986d9cc8aeab83fcdbcf7a9115d3576ecfabf40529cc861f41f0df5640` |
| Skin decoded strict UTF-8 XML | 141959 | `929e65e9d5f191292d9b044e3e659ba115f18f6b3d8a82894046a7c75cbcad5a` |
| `client/sqwt/widget/JournalListWidget.form` | 3434 | `c72aeec944ae2072d4189cd0890bba6ca25d414d21393ee5d6eb086e017a939d` |
| Form decoded strict UTF-8 XML | 3426 | `84d3da484eb4570cfbbe16598ff367117bca9fc5521f7c37daa26850c1aebcc0` |

Each input was decoded with `xivl extract-resource` under its original
basename, using the key contract in
[xivl-tools:docs/formats/sqex.md, container and key sections](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/docs/formats/sqex.md#what-the-container-is).
All four inputs carry the signature `5351455800000000`. Re-encrypting each
decoded document with
[xivl-tools:tools/blowfish.py, Blowfish](https://github.com/XIVLegacy/xivl-tools/blob/604210657f4858fb69744a3a92c90f3369040057/tools/blowfish.py#L60)
and prepending the signature reproduced its input byte for byte. The decoded
documents were parsed with Python's `xml.etree.ElementTree`, and the raw
strings below were read without resolving references or evaluating bindings.

## Template declarations

Exactly one namespace-qualified `ControlTemplate` in the template file has
`x:Key="ControlTemplate_ComboBox"`, where `x` denotes
`http://namespace.square-enix.com/sqwt/x`. Its raw `TargetType` is
`{x:Type ComboBox}`. Its visual root is one `DockPanel`, whose direct visual
children are in this order:

| Order | Element | Raw `Name` | Selected declarations |
| ---: | --- | --- | --- |
| 1 | `ToggleButton` | `PART_DropDownButton` | `DockPanel.Dock="Right"` |
| 2 | `ToggleButton` | `PART_DropDownButton_Text` | Holds one `TextBlock` named `PART_Label` |
| 3 | `Popup` | `PART_Popup` | Holds one `ListBox` named `PART_ListBox` |

The `IsChecked` attribute of both buttons and the `IsOpen` attribute of the
popup each bind the templated parent's `IsDropDownOpen` path with
`Mode=TwoWay`. The `Text` attribute of `PART_Label` binds the templated
parent's `Text` path with `Mode=OneWay`.

The template's trigger list has two entries. An `EventTrigger` with raw
`RoutedEvent="SelectionChanged"` holds an action executing
`UILuaCommands.SelectionChanged`. A `CommandTrigger` for
`ApplicationCommands.Operate` holds an action executing
`ComboBox.OpenDropDown`.

The raw `PlacementTarget` and `MaxHeight` values on the popup each have one
more opening brace than closing braces. How the client parses them is
unresolved.

## Style and skin declarations

Each style name below occurs exactly once as a `SqwtStyle/@Name`, under a
`Widget` of the listed type. The `ComboBox` widget entries are `error`,
`COM_basis` and `COM_basis_sd`.

| Widget | Style | Part | Raw `Reference` | Raw `Style` |
| --- | --- | --- | --- | --- |
| `ComboBox` | `COM_basis` | `DownButton` | `ToggleButton` | `TOG_basis_comboDown` |
| `ComboBox` | `COM_basis` | `Background` | `Window` | `COM_basis_bg` |
| `ComboBox` | `COM_basis` | `ListBox` | `ListBox` | `LIB_basis_comboList` |
| `ToggleButton` | `TOG_basis_comboDown` | `CheckedButton` | `Button` | `BTN_basis_comboDown` |
| `ToggleButton` | `TOG_basis_comboDown` | `UncheckedButton` | `Button` | `BTN_basis_comboDown` |

The `SkinNormal` property of the `BTN_basis_comboDown` frame names skin
`BTN_basis_comboDown_N`. The `SkinNormal` property of the `COM_basis_bg` frame
names skin `COM_basis_bg1_N`.

In the skin document, `BTN_basis_comboDown_N` is a `CellSkin` with raw
`Cells="1,1"` and one `Cell` whose raw `Rectangle` is `400,860,20,20`.
`COM_basis_bg1_N` is a `CellSkin` with raw `Cells="3,3"`,
`SkinBorderThickness="2"` and nine `Cell` children. The nine rectangles are
adjacent when their fields are read as x, y, width and height. Under that
reading the `BTN_basis_comboDown_N` cell is 20 by 20.

The selected template does not name a style for its target `ComboBox`.
`JournalListWidget.form` declares one `ComboBox`, with raw
`Name="ComboBox_Category_Quest"`,
`Template="{StaticResource ControlTemplate_ComboBox}"` and
`SqwtStyle="COM_basis"`. The form's root `Window` has raw
`SqwtStyleFile="common/default.style"`, and one `ResourceDictionary` in the
form has raw `Source="widget/JournalListWidget.tpl"`.

## Open

- The native `ComboBox` and `Popup` classes.
- The placement of the `PART_DropDownButton` and `PART_DropDownButton_Text`
  parts.
- Whether `SkinBorderThickness` of the `Background` part insets the content.
- The point at which a `SelectedIndex` write raises `SelectionChanged`.
