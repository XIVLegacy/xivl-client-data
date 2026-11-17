# Boot background and map marker templates

The character creation background form, the world select help form and the
map marker templates are decoded SQEX markup in the retail client. This page
records their declarations and the caption style the quest marker templates
select.

## Source identities and decoding

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. Paths are relative to `client/sqwt/`. Neither
encrypted inputs nor decoded XML are distributed here.

| File | Input bytes | Input SHA-256 | Decoded XML bytes | Decoded XML SHA-256 |
| --- | ---: | --- | ---: | --- |
| `system/bootup/BootupBg.form` | 2329 | `e043f86b2a6b1acea804f1968773f064f889fdf4bdb7dcafb1e4ce279d8b8387` | 2321 | `b132e9be50de728fae7281290833cd09ebd076ac54e6f064eee83c1079784e9c` |
| `system/bootup/BootupBg.tpl` | 2629 | `71237e821801e69b6cbeea796803c9aae6ce52978516a49c485e71e8117db0db` | 2621 | `6bdf963738bfa42f1af17cbf63a2665c0ee1f9566541afb3a1291a8af33159c1` |
| `system/bootup/charactercreation/HelpWorldSelect.form` | 1755 | `011366ab4ed95ae73c6ffe2d18e2ff783d5945bebbedcf81becb2c4279af3231` | 1747 | `57ee4191ce5c066733acb1b648479dcf47f2771bdb2db1d56a83b6096208ec2e` |
| `common/MapMarker.tpl` | 15166 | `c9a9ddb8568e07bf67564e96328722c647a086ded15907900f73092c6706dba5` | 15158 | `68a685d900291186ba0b6472e8a6f9054459d2b2d874913725ee0fb8fe1e5555` |
| `common/default.style` | 353783 | `632b314cb2257fcbee42d4b002989a58dfeb42e64af864c1f5356336dc233dc0` | 353775 | `33bb178c3b172c62eeb65e8bcaf94f701a0ec3921564e27a619516900896d9f6` |
| `widget/MapNavigationWidget.form` | 22364 | `137c5542a8dd41fcafe85b66d8954e238b8e13d884fd6c0d89d3316c6440ef0e` | 22356 | `2012be5906707b43eadadcde937045257eed7735e9afec7a43b6b2bab5a4fa35` |
| `widget/MiniMapWidget.form` | 2943 | `83428fa59fa9d26951c1c646d40b87fbbfd9ea0b537ae30e3af4b1ff36560360` | 2935 | `7c3d9d8a0c69291d21b705c8823444fc5ab89d4ee3ae06eda80caab040e85c88` |

All inputs have the complete SQEX signature `5351455800000000`. Decode with
the basename, including case and suffix, as the ASCII Blowfish key, following
the
[Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe). The decoder
uses little-endian block halves and preserves a partial tail. Parse the
decoded text as UTF-8 XML. For every input, strict UTF-8 decoding, standard
library ElementTree parsing and byte-exact re-encryption passed.

## BootupBg form

The `BootupBg.form` root is a `Window` named `CharaMakeBase` with
`IsEnabled="False"`, `Focusable="False"` and `IsHitTestVisible="False"`. It
merges `system/bootup/BootupBg.tpl` and declares `SqwtStyleFile` as
`system/bootup/bootup.style`.

Its `Grid` holds three `Canvas` elements, each aligned right and bottom with
no size, and then a `Border` with `SqwtStyle="CharaMakeBase"`. Each `Canvas`
holds one `Label` with the template `ControlTemplate_BG`, `VisualOpacity="0"`
and `Canvas.Right="300"`. The Labels are `Label_BgLimsaLominsa`,
`Label_BgGridania` and `Label_BgUldah`, in that order. Each Label holds one
`Border` named `Border_BgLimsaLominsa`, `Border_BgGridania` or
`Border_BgUldah` with the matching `SqwtStyle` of the same name, aligned
right and bottom, `RenderTransformOrigin="1,1"` and a `ScaleTransform` with
`ScaleX="0.6"` and `ScaleY="0.6"`.

## BootupBg template

`BootupBg.tpl` holds one `ControlTemplate` keyed `ControlTemplate_BG` with
`TargetType` `Label`. Its content is a `ContentPresenter` and it declares five
`CommandTrigger` elements:

| Command | Declaration |
| --- | --- |
| `BG_FadeIn` | `ExecuteCommandAction` for `BG_FadeIn_Move` and `BG_FadeIn_Opacity`, and a `Setter` for `RenderTransform.ScaleY` with no `Value` attribute |
| `BG_FadeIn_Move` | `DoubleAnimation` on `Canvas.Right` from 200 to 380, `Duration` `0:0:3`, `FromAccelType` `SpeedUp` at 0.1 and `ToAccelType` `SlowDown` at 0.9 |
| `BG_FadeIn_Opacity` | A `BeginStoryboard` named `BeginStoryboard_BG_FadeIn_Opacity` with a `DoubleAnimation` on `VisualOpacity` from 0 to 1, `Duration` `0:0:2`, `BeginTime` 0.1 |
| `BG_FadeOut` | `DoubleAnimation` on `VisualOpacity` to 0, `Duration` `0:0:0.4`, and a `StopStoryboard` for the opacity storyboard |
| `BG_FadeOut_Decision` | `VisualOpacity` to 0 over `0:0:1`, and `DoubleAnimation` on `RenderTransform.ScaleY` and on `RenderTransform.ScaleX`, each `ToOffset` 0.06, `To` bound to `{Binding Path=From}`, `Duration` `0:0:1` and `ToAccelType` `SlowDown`, a `RenderTransformOrigin` key frame `0.7,0.8`, a `StopStoryboard` for the opacity storyboard and a `Setter` of `RenderTransform` to `ScaleTransform` |

These are static declarations. A `Setter` with no `Value` attribute names a
property and no value. Which native code posts each command and writes the
Border scale is not established by the markup.

## HelpWorldSelect form

The `HelpWorldSelect.form` root is a `Window` named `Window_HelpWorldSelect`
with `SqwtStyle="WIN_basis"`, `SqwtStyleFile` `system/bootup/bootup.style`,
`Margin="5%,5%,5%,25%"`, `MinWidth="384"` and `MaxWidth="576"`, centred
horizontally and aligned to the bottom. It merges
`system/bootup/charactercreation/HelpWorldSelect.tpl` and selects
`ControlTemplate_Window_WINBasis`. Its `Grid` named `Grid_01` has three rows,
the second and third `Auto` height. It holds:

| Element | Name | Raw attributes |
| --- | --- | --- |
| `TextBlock` | `TextBlock_Text` | `Text="@100452"`, `FontSize="16"`, centred, `Margin="16,8,16,20"` |
| `TextBlock` | `TextBlock_Text_2` | `Text="@100471"`, `FontSize="13"`, left, `Margin="16,50,16,20"` |
| `Border` | none | `SqwtStyle="BOD_basis_lineH"`, row 1 |
| `Button` | `Button_1` | `Content="@100262"`, `SqwtStyle="BTN_basis"`, `MinWidth="120"`, row 2 |

Both TextBlocks set `TextWrapping="Wrap"` and `SqwtStyle="TBL_null"`. The
phase that opens this form is in
`xivl-decomp:docs/resource/world-select-help-phase.md`.

## Map marker templates

`MapMarker.tpl` holds 17 `ControlTemplate` elements with `TargetType`
`ContentControl`, keyed `MapMarkerTemplate`, `MapMarker`, `MapMarkerUnder`,
`MapMarkerLeft`, `MapMarkerRight`, `MapMarkerPoint`, `MapMarkerSymbol`,
`MapMarkerSymbolUnder`, `MapMarkerSymbolLeft`, `MapMarkerSymbolRight`,
`MapMarkerAetheryte`, `MapMarkerAetheryteUnder`, `MapMarkerAetheryteLeft`,
`MapMarkerAetheryteRight`, `MapMarkerParty`, `MapMarkerQuest` and
`MapMarkerQuestArea`. Each template sets `Focusable` and `IsHitTestVisible` false.

`MapMarkerTemplate` holds one `ContentControl` of `Width="480"` whose
`Template` is bound to `@Template`. The templates in the table below share one caption
`TextBlock` named `TextBlock_Caption` with `Text` bound to `@Text`,
`Visibility` bound to `@Visibility`, `TextWrapping="Wrap"`, `FontSize="13"` and
`FontEdge="True"`, and one `SparkleControl` named `SparkleControl_MapMarker`
of `Width="32"` and `Height="32"` with `Sequence` bound to `@SparkleSequence`.

| Template | Layout | Caption style |
| --- | --- | --- |
| `MapMarker` | vertical `StackPanel`, caption then marker | `TBL_null` |
| `MapMarkerUnder` | vertical `StackPanel`, marker then caption | `TBL_null` |
| `MapMarkerLeft` | horizontal `StackPanel`, caption then marker, `TextAlignment="Right"` | `TBL_null` |
| `MapMarkerRight` | horizontal `StackPanel`, marker then caption, no `TextAlignment` | `TBL_null` |
| `MapMarkerSymbol` | vertical `StackPanel`, caption then marker, caption `Margin="0,0,0,4"` | `TBL_null` |
| `MapMarkerAetheryte` | as `MapMarkerSymbol` | `TBL_null` |
| `MapMarkerParty` | vertical `StackPanel`, caption then marker, the marker also binds `@Visibility` | `TBL_chat_inputParty` |
| `MapMarkerQuest` | vertical `StackPanel`, caption then marker, `TextAlignment="Center"` | `TBL_map_null` |
| `MapMarkerQuestArea` | `Grid`, marker then caption, both centred | `TBL_map_null` |

The `MapMarker`, `MapMarkerSymbol` and `MapMarkerAetheryte` families use the
Sparkle sources `common/mapMarker.le.spk`, `common/mapMarkerSymbol.le.spk`
and `common/mapMarkerAetheryte.le.spk`. `MapMarkerQuest`,
`MapMarkerQuestArea` and `MapMarkerParty` use `common/mapMarker.le.spk`. The
Under, Left and Right variants of the Symbol and Aetheryte families were not
compared beyond their key names.

## Caption style `TBL_map_null`

`common/default.style` holds `SqwtStyle` `TBL_map_null` with one `Parts`
element named `Frame`. Its `Property` rows name the skin `BOD_map_textBg` for
`SkinNormal`, `SkinHover`, `SkinActive`, `SkinDisabled` and `SkinFocused`
and the skin `NULL` for `SkinAnchored`, `SkinReserved` and `SkinDroppable`.
The font colour is `#fff3f3f3` and the font edge colour `#ff262626` for the
four active conditions. `SkinDisabled` has `#80f3f3f3` and `#801a1a1a`. The
existence and drawing of the `BOD_map_textBg` skin were not checked.

## Map readers

`MapNavigationWidget.form` declares two `RaptureSsdDataReader` elements on
`XPath="/root/marker"`:

| Name | `SheetName` | `XmlFormat` | `Row` |
| --- | --- | --- | --- |
| `ssd_marker_data` | `quest_marker` | `,Type,X,Z,,,SparkleFile,SparkleSequence,Region,Layout,Floor,Template,Text,Visibility` | absent |
| `map_marker_data` | `2Dmap_marker` | `,X,Z,,,,,Y,SparkleFile,SparkleSequence,Region,Layout,Floor,Template,Text,Visibility,,HideLayout` | absent |

Its `CustomControl` sets `GlMarkerDefaultTemplate` and
`SsdMarkerDefaultTemplate` to `MapMarkerTemplate` and its `SqwtStyleFile` is
`common/default.style`. `MiniMapWidget.form` declares two readers on
`2Dmap_marker` with `XmlFormat` `,X,Y,,,,,Z,SparkleFile,SparkleSequence,Region,Layout,Floor,Template`
for `ssd_marker_data` and
`,X,Z,,,,,Y,SparkleFile,SparkleSequence,Region,Layout,Floor,Template,,,,HideLayout`
for `map_marker_data`. Neither MiniMap reader names a `Text` or `Visibility`
column, and the MiniMap form declares no `quest_marker` reader.

## Reproduction

Decode each input with `xivl-tools:tools/blowfish.py` using the ASCII
basename key, strip the first 8 bytes before decrypting, and parse the output
as XML. Select the elements named above by tag and raw attribute, for example
the `ControlTemplate` by `x:Key` in `MapMarker.tpl` and the `SqwtStyle` by
`Name` in `default.style`. Compare input sizes and SHA-256 values with the
table above.
