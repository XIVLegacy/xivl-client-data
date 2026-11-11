# Boot select and error rows

These records cover the boot error type and error text sheets, the
character select string-table rows, and the status block markup of
`system/bootup/CharacterSelection.form`. Facts marked `STATIC` are decoded
static client data (`client_extraction`) or static observations of the
identified client executable. `INFERRED` marks an interpretation that no
reader or writer trace confirms. `UNKNOWN` marks a question the evidence
leaves open.

## Error type and error text sheets

Master `0x01030000` names `xtx/_text_error` at reference ordinal 31,
`_text_error_type` at ordinal 61 and `_boot_error_type` at ordinal 85.
All three definitions declare the same four blocks: begin 10000 with 10011
slots, begin 30000 with 10 slots, begin 40000 with 1 slot and begin 50000.
The last block declares 3 slots in `_boot_error_type` and 4 slots in the
other two sheets.

| Sheet | Columns | Rows | Tier |
| --- | --- | ---: | --- |
| `_boot_error_type` | `u8`, `s32`, `s32` | 57 | STATIC |
| `_text_error_type` | `u8`, `u8`, `u8` | 90 | STATIC |
| `xtx/_text_error` | one `str` per language | 90 | STATIC |

`xtx/_text_error` declares the languages `ja`, `en`, `de`, `fr` and `chs`.
Each language holds the same 90 row keys, and no row is empty. The English
string column is index param 4.

### Key sets

The 57 `_boot_error_type` keys are 10000-10006, 11000-11013, 12000-12001,
13000-13010, 14000-14001, 15000-15002, 20000-20010, 30000-30002, 40000 and
50000-50002. Every one of them also has a row in `_text_error_type` and in
every language of `xtx/_text_error`. The 33 keys present only in the two
90-row sheets are 11014-11039, 12002, 13011, 13100-13103 and 50003. STATIC.

The 10000 and 50000 enable files of `_text_error_type` and English
`xtx/_text_error` are byte-identical. The 30000 and 40000 enable files are
byte-identical across all three sheets. The `_boot_error_type` 10000 and
50000 enable files differ from the other two. STATIC.

### Stored values

| Sheet | Column 0 | Columns 1 and 2 | Tier |
| --- | --- | --- | --- |
| `_boot_error_type` | 2 at 10002, 10005, 10006, 20003 and 20005, 1 elsewhere | 0 on every row | STATIC |
| `_text_error_type` | 2 at 10002, 10005, 10006, 11034, 20003 and 20005, 1 elsewhere | column 1 is 1 at 11036 and 3 at 13102 and 13103, every other cell is 0 | STATIC |

Column 0 of `_boot_error_type` equals column 0 of `_text_error_type` at all
57 shared keys. STATIC.

The meaning of column 0 is UNKNOWN. Its six value-2 rows do not share one
text shape. Rows 20003 and 20005 end in a question, and 11034 ends with a
retry question. English rows 10002, 10005 and 10006 read
`An error has occurred.` and ask nothing. Rows 10005 and 10006 append, in
parentheses, the number token `022003e80203` and the string token
`022903ea0203`. A two-button reading of value 2 is therefore not supported
by the text alone.

### Selected English error text

The token columns use the export notation of
`xivl-tools:docs/formats/ssd-sheet.md`, Rich-string read and text-export
contract. `N1` is the newline token `02100103`. `C1` and `C2` are the number
tokens `022003e80203` and `022003e80303`. `S3` is the string token
`022903ea0403`. Those expressions retain their bytes and assign no runtime
parameter bank.

| Row | Text | Token sequence after the sentence | Tier |
| ---: | --- | --- | --- |
| 13000 | The lobby server connection has encountered an error. | none | STATIC |
| 13001 | The lobby server connection has encountered an error. | `N1` `Error Code: ` `C1` `N1` `Status: ` `C2` `N1` `S3` | STATIC |
| 13002 | The server is experiencing unusually heavy traffic. Please try again later. | `N1` `Error Code: ` `C1` `N1` `Status: ` `C2` | STATIC |
| 13003 | The server is currently unavailable. | as 13002 | STATIC |
| 13004 | That character name cannot be used. Please input another. | as 13002 | STATIC |
| 13005 | That character name is already being used. Please input another. | as 13002 | STATIC |
| 13006, 13007 | The lobby server has encountered a problem. | as 13002 | STATIC |
| 13008, 13009, 13010 | The lobby server connection has encountered a problem. | as 13001 | STATIC |
| 13011 | The server is undergoing maintenance. Please try logging in again later. | as 13001 | STATIC |
| 13100 | The lobby server connection has encountered an error. | none | STATIC |
| 20003 | Cancel FINAL FANTASY XIV installation? | none | STATIC |
| 20005 | FINAL FANTASY XIV is already installed. | `N1` `Do you wish reinstall?` | STATIC |

The `Error Code: ` and `Status: ` labels are literal text in the row. Which
values fill `C1`, `C2` and `S3` is UNKNOWN.

### Sheet names in the client executable

The executable is `ffxivgame.exe`, 15996808 bytes, SHA-256
`9341f2b4567440b310a4d494f5cc5599ca334ba51c8042247317ff466492f2e9`, image
base `0x00400000`.

- STATIC: `FUN_005705B0` stores the
  `Application::Main::Menu::ErrorDialog::ErrorDialogManager` vftable at
  offset 0 of its receiver, at `0x005705F6`. At `0x005706E6` it pushes the
  string `xtx/_text_error` at `0x00FA6188`. At `0x005706F8` it pushes the
  string `_text_error_type` at `0x00FA6198`. The class and its vftable RVA
  `0xba67e8` are catalogued in `xivl-decomp:config/ffxivgame.rtti.json`.
- STATIC: the string `xtx/_text_error` also occurs at `0x00FA9E88` and
  `0x01051220`. `FUN_00881C50` references the copy at `0x01051220`.
  References from `0x00F10356` and `0x00F10326`, outside any analyzed
  function, point at `0x00FA9E88` and at a second `_text_error_type` string
  at `0x00FA9E74`.
- STATIC: no byte string `boot_error` occurs in the loaded program image,
  as ASCII or as UTF-16LE.
- INFERRED: the `ErrorDialogManager` setup pairs `xtx/_text_error` with
  `_text_error_type`, which matches the identical key sets above.
- UNKNOWN: the reader of `_boot_error_type` and the consumer that joins it
  to `xtx/_text_error`. Its keys are a subset of the error text keys, but no
  traced reader pairs the two.

## Character select string-table rows

`system/bootup/CharacterSelectionPhase.form` is the window
`Window_CharacterSelectionPhase`. It declares the eight buttons
`Button_Chara_1` through `Button_Chara_8` with no `Content` attribute, then
three buttons with raw `Content` references. STATIC.

On this page an `@N` attribute value is read as row `N` of `xtx/_text_ui`.
That is the default table of the conditional lookup path in
[xivl-decomp:docs/resource/sqwt-plain-text-reference-lookup.md](https://github.com/XIVLegacy/xivl-decomp/blob/4081fda7ba8b8493e9b59e875bf335aa29ddb8ce/docs/resource/sqwt-plain-text-reference-lookup.md),
Default table and named language fields. The row texts are STATIC. The
resolution of each attribute to its row is INFERRED from that path.

| Element | Raw `Content` | English `xtx/_text_ui` text | Tier |
| --- | --- | --- | --- |
| `Button_CharacterDelete` | `@100216` | Delete | STATIC |
| `Button_AccountManager` | `@100215` | Accounts | STATIC |
| `Button_Back` | `@100208` | Previous | STATIC |

Neighbouring English rows in the same block read as follows. No shipped
markup in this form references them. STATIC.

| Row | English text |
| ---: | --- |
| 100205 | Select a character. |
| 100210 | New |
| 100213 | Delete |
| 100214 | Create Character |
| 100253 | Please select the character you wish to delete. |
| 100258 | * Character creation is currently under development. |

Which row, if any, captions an empty character slot is UNKNOWN.

### Name arguments by language

Rows 100225 to 100229 differ by language in whether they carry the string
token `022903ea0203`. In rows 100227, 100228 and 100229 a color token and an
edge-color token precede it wherever it occurs. STATIC.

| Row | English content | `ja` | `en` | `de` | `fr` |
| ---: | --- | --- | --- | --- | --- |
| 100225 | Logging in... | token | none | token | none |
| 100226 | Login complete. | token | none | token | none |
| 100227 | a delete confirmation question | token | token | token | token |
| 100228 | Deleting... | token | none | token | none |
| 100229 | `has been deleted.` after the token | token | token | token | none |

The `fr` row 100229 is a plain completion sentence with no token.

## CharacterSelection status block markup

`system/bootup/CharacterSelection.form` is the window
`Window_CharacterSelection`, with style file `system/bootup/bootup.style`.
Its status block sits inside `Label_Menu_Exp`. STATIC throughout this
section.

| Element | Raw attributes |
| --- | --- |
| `Label_Menu_Exp` | `Canvas.Left="-800"`, `StringData.Value0="Label_LIMSA"`, `IsEnabled="False"` |
| `Border_City` | `SqwtStyle="Border_BannerUldah"`, inside `Grid_Menu_Exp` |
| `TextBlock_Title` | `Visibility="collapsed"` |
| `TextBlock_PlayerName`, `TextBlock_PlayerName_2` | no `Text` |
| `TextBlock_Race`, `TextBlock_TRIBE` | no `Text`, siblings in one Grid |
| `TextBlock_BirthDay_2` | `Text="@100244"` |
| `TextBlock_Guardian_2` | `Text="@100245"` |
| `TextBlock_BirthDay`, `TextBlock_Guardian` | no `Text` |
| `IconControl_GuardianIcon` | `IconDatas="0"`, no `Text` |
| `IconControl_SkillCategory` | `IconDatas="83"`, no `Text` |
| `TextBlock_Skill` | no `Text` |
| `TextBlock_SkillRank` | `Text="@219/i1"`, `Visibility="Collapsed"`, sibling of `TextBlock_Skill` |
| `TextBlock_PhysicalLevel` | `Text="@220/i1"`, inside a Grid with `Visibility="Collapsed"` |
| unnamed TextBlock in `Grid_World` | `Text="@100559"` |
| `TextBlock_World` | no `Text` |
| unnamed TextBlock in `Grid_Location` | `Text="@100558"` |
| `TextBlock_Location` | no `Text` |

The referenced English `xtx/_text_ui` rows read `Nameday:` for 100244,
`Guardian:` for 100245, `World` for 100559 and `Location` for 100558. Row
219 reads `Level: ` and row 220 reads `Physical Level: `, each followed by
the one number token `022003e80203`.

The `/i1` suffix is preserved raw. Which native writer fills each
unreferenced TextBlock, and from which roster value, is UNKNOWN.

## Shipped wait dialogs

| Form | Element | Raw attribute | English text | Tier |
| --- | --- | --- | --- | --- |
| `system/bootup/Waiting.form` | `TextBlock_Text` | `Text="@100126"` | a World login queue notice that begins "This World is currently experiencing unusually heavy traffic." | STATIC |
| `system/bootup/Waiting.form` | `TextBlock_Text_2` | no `Text`, `Margin="16,80,16,8"` | none | STATIC |
| `system/bootup/Waiting.form` | `Button_Cancel` | `Content="@100128"` | Cancel Login | STATIC |
| `system/bootup/BootupDialog_NoBtn.form` | `TextBlock_Text` | no `Text`, no Button in the form | none | STATIC |

English rows 100122 and 100124 read `Connection failed.` and
`Connecting to server...`. STATIC. No shipped markup in these two forms
references them. Which form retail uses for the lobby connect and login
waits is UNKNOWN.

## Source identity and reproduction

The install labels are `game.ver` `2012.09.19.0001` and `patch.ver` `1.23b`.
Resource ID bytes `AA BB CC DD` select `data/AA/BB/CC/DD.DAT`.

| Resource | Bytes | SHA-256 |
| --- | ---: | --- |
| Master `0x01030000` | 7044 | `860023878f9ad1e98fd1baa3e3380f971f86bf1f7747043cf0c3c7459cee2eb4` |
| `_boot_error_type` definition `0x01030452` | 744 | `45ee83935df926345c5ba1d47be6ad4f377f7b342c48217a7b357b841ecca788` |
| `_text_error_type` definition `0x01030012` | 742 | `6bfba2d1ce5b2666aa065a3e96bdb3d759f0f76648d7e16002198f91659ea5f8` |
| `xtx/_text_error` definition `0x0B45008E` | 3099 | `5d1edc5123ea4de950c123ec550f02cd6e97fe0408829d9f82dc238e149e588f` |
| `xtx/_text_ui` definition `0x0B450082` | 3099 | `27e50caf3d258e8eed2d9e70bc8355e2ab67f54f2dc8bf54e6cfcdf604e5e492` |

| Sheet | Block | Kind | Resource | Bytes | SHA-256 |
| --- | ---: | --- | --- | ---: | --- |
| `_boot_error_type` | 10000 | enable | `0x01030454` | 56 | `f48d5fba3a02871c7176bb83c40b3054f850cb1bb5a8cfae7bae06932496b0f3` |
| `_boot_error_type` | 10000 | data | `0x01030453` | 450 | `9961edd594cfa2f10d5947a9e89abf3045e2f74e865c6651bd643e7b04aeb482` |
| `_boot_error_type` | 30000 | enable | `0x01030457` | 8 | `91a17162b800c2e389acb26574a41a742edd7b2fb13d8765ac59a5b43e20e804` |
| `_boot_error_type` | 30000 | data | `0x01030456` | 27 | `d79ab7cbd414e3f5f26bdd915ff67cd8e2f9b7964e0ace26dbcab76d1d120b43` |
| `_boot_error_type` | 40000 | enable | `0x0103045A` | 8 | `95b89b4180b528c69eb77bf9911e22666f81abd43c1174c40f2166ff461c47bd` |
| `_boot_error_type` | 40000 | data | `0x01030459` | 9 | `a536aa3cede6ea3c1f3e0357c3c60e0f216a8c89b853df13b29daa8f85065dfb` |
| `_boot_error_type` | 50000 | enable | `0x0103045D` | 8 | `36aea5039334883ef2e3a569724e630598e62953e36dec1fc3637a7c42f6c7e6` |
| `_boot_error_type` | 50000 | data | `0x0103045C` | 27 | `d79ab7cbd414e3f5f26bdd915ff67cd8e2f9b7964e0ace26dbcab76d1d120b43` |
| `_text_error_type` | 10000 | enable | `0x01030014` | 64 | `48c798d8c2adef2ee1c5c4837afa52fc8321821cc3292a4e9114df85c4e97181` |
| `_text_error_type` | 10000 | data | `0x01030013` | 246 | `0c530b03918f0e700e873047b5e3a79cabe569904a7a809c18976e37a8b380e9` |
| `_text_error_type` | 30000 | enable | `0x010302B2` | 8 | `91a17162b800c2e389acb26574a41a742edd7b2fb13d8765ac59a5b43e20e804` |
| `_text_error_type` | 30000 | data | `0x010302B1` | 9 | `cfd7f1c7e5c3f37b1fa6dc7079e55fb5743fa0c78eb66983d75bbde1c75b0aee` |
| `_text_error_type` | 40000 | enable | `0x010302B5` | 8 | `95b89b4180b528c69eb77bf9911e22666f81abd43c1174c40f2166ff461c47bd` |
| `_text_error_type` | 40000 | data | `0x010302B4` | 3 | `fb50dc0717ff266cf9baf82b1ce7a1c2ef6d9247859680b11a19fb7077f5f222` |
| `_text_error_type` | 50000 | enable | `0x0103032A` | 8 | `62c5779411ca2bf291f72d3f8a4769f5a30653326f37862cb6add2f27c69a4c4` |
| `_text_error_type` | 50000 | data | `0x01030329` | 12 | `58b25e5d46d5d5bd08aa156b4cc8b5db7f7ed205722692ca6888ec5d25e0ca57` |
| `xtx/_text_error` `en` | 10000 | enable | `0x0B45070D` | 64 | `48c798d8c2adef2ee1c5c4837afa52fc8321821cc3292a4e9114df85c4e97181` |
| `xtx/_text_error` `en` | 10000 | data | `0x0B45070C` | 5520 | `5e16c1d48580778cca0ea21392602db3046504d574a456bd7046a0d31b363f90` |
| `xtx/_text_error` `en` | 30000 | enable | `0x0B450794` | 8 | `91a17162b800c2e389acb26574a41a742edd7b2fb13d8765ac59a5b43e20e804` |
| `xtx/_text_error` `en` | 30000 | data | `0x0B450793` | 112 | `519bdf13ed89af297e4c386f5866e7270b8a90df733c1bb472655f62e2db7984` |
| `xtx/_text_error` `en` | 40000 | enable | `0x0B450797` | 8 | `95b89b4180b528c69eb77bf9911e22666f81abd43c1174c40f2166ff461c47bd` |
| `xtx/_text_error` `en` | 40000 | data | `0x0B450796` | 26 | `1b5430a5b11ecb3c2c5eb5c1bfd7142c2b5b3de67828c8b4f95d685625399bd4` |
| `xtx/_text_error` `en` | 50000 | enable | `0x0B450255` | 8 | `62c5779411ca2bf291f72d3f8a4769f5a30653326f37862cb6add2f27c69a4c4` |
| `xtx/_text_error` `en` | 50000 | data | `0x0B450254` | 533 | `f7cd84cfb7f779f8f985523cffde5df408439855280a9cef5d7d7281a823b5e4` |
| `xtx/_text_ui` `en` | 0 | data | `0x0B4502B5` | 71588 | `f99e738cf8762e0831f9675f37ddfea7b6072d475b3d4b0c9edeadb67bb013e0` |
| `xtx/_text_ui` `en` | 100000 | data | `0x0B4502BB` | 47069 | `227323bf982c2301c0bb062ec1698f1c226deec5f57c6c7515dd546ff20f1433` |
| `xtx/_text_ui` `ja` | 100000 | data | `0x0B4502C7` | 43011 | `2b4dd0839439a87d310e20cf113b48c8adc72c59e1bb0b92fd93de22ff742b1a` |
| `xtx/_text_ui` `de` | 100000 | data | `0x0B4502A0` | 49886 | `cf02291e96c4e2e0873227daf9ad2e95dfcfadf6a9c12642450085c330960217` |
| `xtx/_text_ui` `fr` | 100000 | data | `0x0B4502AC` | 49459 | `4c83cbe29fd74ba7f7e7315a918aaf36b8827b8d8ffced473f6c282157316155` |

Read the definitions with `decode_document` and `resource_path` in
[compare_sheet_inventory.py](../tools/compare_sheet_inventory.py). Read the
enable ranges and row spans with `read_ranges` and `row_spans` in
[build_fixed_phrase_backing_rows.py](../tools/build_fixed_phrase_backing_rows.py).
Require every enabled key to have a nonempty span and every row to consume
its span exactly under the column order of
`xivl-tools:docs/formats/ssd-sheet.md`, Rows and columns.

| Form input under `client/sqwt/` | Bytes | SHA-256 | Decoded bytes | Decoded SHA-256 |
| --- | ---: | --- | ---: | --- |
| `system/bootup/CharacterSelection.form` | 8977 | `6eb7a8613be1f6ccec3a74bd47af60dfec59c2c1e99f99988c10f25383ccaf65` | 8969 | `2a53e54c2395688b0b8520d0f9598ce7b94f65cf8cdfbc5beccb84e01340eb60` |
| `system/bootup/CharacterSelectionPhase.form` | 2507 | `94a4f819381de4b20ebb77b2e3fad4d7f2cf2370a9ab3c19940cdacc31996698` | 2499 | `95c91e6c9593c72c8f3e1465b2fc5ea85ae31913df40a3b14dccbd6196f3a054` |
| `system/bootup/Waiting.form` | 1720 | `c41493c44901b47c1a389831c9afcf8e3da5119f35d8eec6cf8b5a893ff85026` | 1712 | `72bc5361fc2956a093f10dcb18097ead82134982c055f85c7384c3e681880569` |
| `system/bootup/BootupDialog_NoBtn.form` | 1249 | `701fcbd132d65df7ededa1345479a837690756abc36a54348e08a4f56bca3c72` | 1241 | `f87499d4179264ef968fa1ce7ccbf79f805226e0f17b46044c1c9d6b36d5c20e` |

Each form carries the signature `5351455800000000`. Decrypt the remainder
with the `Blowfish` class of
[xivl-tools:tools/blowfish.py](https://github.com/XIVLegacy/xivl-tools/blob/e33378e5f2b429f49ff21a9450e787664227adca/tools/blowfish.py#L60-L125),
keyed by the ASCII basename including its suffix. Require byte-exact
re-encryption, strict UTF-8 and a parse with Python's standard-library
`xml.etree.ElementTree`. Element names are in the namespace
`http://namespace.square-enix.com/sqwt`. Attribute values are preserved raw,
with no binding, resource or default resolved. The decoded XML is not
distributed here.
