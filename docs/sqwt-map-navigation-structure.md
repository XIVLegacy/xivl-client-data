# MapNavigationWidget form and template declarations

The `widget` MapNavigationWidget form declares one `MapScreenControl`
customised for the full-screen map window. This `client_extraction` finding
covers supplied build `2012.09.19.0001`. Paths are relative to `client/sqwt/`.

## Installed inputs

| Path | Container bytes and SHA-256 | Decoded bytes and SHA-256 |
| --- | --- | --- |
| `widget/MapNavigationWidget.form` | 22364, `137c5542a8dd41fcafe85b66d8954e238b8e13d884fd6c0d89d3316c6440ef0e` | 22356, `2012be5906707b43eadadcde937045257eed7735e9afec7a43b6b2bab5a4fa35` |
| `widget/MapNavigationWidget.tpl` | 7098, `da386f16168c709a1533abe76ec55d6675533079fc34c4d8be719b60cd977483` | 7090, `5394098335ccfa4fb6577ee09d1aefbcaaed4f6a7e34332c9313f16f389cc6be` |

Use the [SQEX recipe](sqwt-ask-structure.md#reproduction-recipe) with each
original basename. Both inputs carry the signature `5351455800000000`.
`widget_c/MapNavigationWidget.form` is a different document of 13161 decoded
bytes with SHA-256
`7a7d3dda65c51759f7d5aba2a4adb0f25d0ad6a83a962c82eb6c2bdadf9d8b12`. This
page does not cover it. The decoded line numbers below are one-based.

## Map control

Line 23 of the form declares `CustomControl_MapNavigation` with
`Type="MapScreenControl"`, `Focusable="False"` and `Grid.ColumnSpan="3"` and
`Grid.RowSpan="3"`. STATIC. The attributes it declares are:

| Attribute | Value |
| --- | --- |
| `Function` | `0` |
| `FocusPointColumn` | `15` |
| `Filter` | `1` |
| `DirectionRadiusRatio`, `DirectionPositionRatio` | `1000`, `0.5` |
| `GlAreaImageId` | `0x61C10004` |
| `PrivateAreaImageId1`, `PrivateAreaImageId2` | `0x61C10001`, `0x61C10002` |
| `PrivateAreaImageWidth`, `PrivateAreaImageMeter` | `64`, `64` |
| `DefaultSparkleFile`, `DefaultSparkleSequence` | `common/mapMarker.le.spk`, `m00002` |
| `AreaName1Label`, `AreaName2Label`, `AreaName3Label` | `TextBlock_RegionName`, `AreaName2Label:TextBlock_AreaName`, `AreaName3Label:TextBlock_AreaName` |
| `MarkerCenterControlName` | `SparkleControl_MapMarker` |

The control declares no `MaskImageId`, no `Scale`, no `MaxScale` and no
`MinScale`. It declares five marker list bindings: `TypeDataSource`,
`GroupMarkerSource`, `GlMarkerSource`, `SsdMarkerSource` and
`MapMarkerSource`. Lines 19 and 20 bind `Map.ScaleUp` to `PageUp` and
`Map.ScaleDown` to `PageDown`, both repeating, with the control as command
target. The key bindings state no step size.

## Data readers

| Line | Reader key | Sheet | Declared shape |
| ---: | --- | --- | --- |
| 5 | `type_data` | `2Dmap_actor_data` | `XmlFormat="Type,SparkleFile,SparkleSequence"`, `Row="0-12"` |
| 8 | `ssd_marker_data` | `quest_marker` | `,Type,X,Z,,,SparkleFile,SparkleSequence,Region,Layout,Floor,Template,Text,Visibility` |
| 9 | `map_marker_data` | `2Dmap_marker` | `,X,Z,,,,,Y,SparkleFile,SparkleSequence,Region,Layout,Floor,Template,Text,Visibility,,HideLayout` |

`gl_marker_data` and `group_marker_data` are `SqwtXmlDataMaker` entries with
no sheet.

## Template and collapsed configuration

- `ControlTemplate_Window_MapNavigationWidget` (template line 3 onward) holds
  a `CommandTrigger` on `RaptureCommands.MoveCamera`, name `MapMove`, at line 5.
  It runs `MapScreen.Move` on `CustomControl_MapNavigation` with
  `CommandParameter` bound to `MapMove.RoutedCommandParameter`.
- Lines 53 and 54 of the template close the window on `MouseLeftButtonDown`
  by `UILuaCommands.EventMapNavigationClose`.
- Line 71 declares a `ListBoxItem` template
  `ControlTemplate_ListBoxItem_CheckBoxItem`. The form does not reference it
  by name.
- Form line 216 declares `Grid_TransparencyConfig`, `Visibility="Collapsed"`.
  Its `Slider_TransparencyConfig` at line 240 sets
  `Style="{StaticResource Style_Slider}"`. Neither this form nor this
  template defines the key `Style_Slider`.

## Reproduction

Decode both inputs by the recipe and parse with `xml.etree.ElementTree`.
Match the lines above with a one-based count over the decoded text. The
sheet names and attribute values are the literal attribute text. The sheets
themselves are not read here. The meaning of the load centre and load scale
that the control derives from `Function` and `FocusPointColumn` is in
[xivl-decomp:docs/resource/map-navigation-load-centre-and-scale.md](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/resource/map-navigation-load-centre-and-scale.md).
