# Mouse-enter trigger and drag census

The installed form and template markup declares pointer hover actions in
event triggers and declares drag state on exactly two templates. This page
counts those declarations over the whole `client/sqwt` markup set.

## Input and method

These are `client_extraction` findings from the supplied retail 1.23b install,
build `2012.09.19.0001`. The set is every `.form`, `.tpl` and `.style` file
under `client/sqwt`, 620 `.form`, 482 `.tpl` and 20 `.style`, 1122 files in
all. Each is a SQEX container. Decode each with the basename as the ASCII
Blowfish key following the
[Ask extraction recipe](sqwt-ask-structure.md#reproduction-recipe). Parse the
decoded text with the standard library ElementTree and match tags by local
name. One file, `system/common/Staffroll.form`, does not parse because of an
unbound namespace prefix and is outside the counts of parsed elements. The
`.sd.` variants are counted as separate files.

## MouseEnter event triggers

There are 217 `EventTrigger` elements whose `RoutedEvent` is `MouseEnter`.
Grouped by the action elements they contain:

| Actions | Count |
| --- | ---: |
| `SoundPlayerAction` only | 111 |
| `ExecuteCommandAction` only | 49 |
| `ExecuteCommandAction` and `SoundPlayerAction` | 14 |
| `BeginStoryboard` with `DoubleAnimation` tracks only | 17 |
| `BeginStoryboard` with a discrete key frame track | 2 |
| `BeginStoryboard` and `SoundPlayerAction` | 12 |
| `BeginStoryboard`, `Setter` and `SoundPlayerAction` | 10 |
| `BeginStoryboard` and `ExecuteCommandAction` | 2 |

The 43 triggers that contain a `BeginStoryboard` are in these files, counting
each `.sd.` variant with its base:

- `system/bootup/BootupMenu.tpl`: 2
- `system/bootup/TitlePhase.{de,en,fr,ja}.tpl` and
  `system/installer/TitlePhase.tpl`: 1 each, with a `Setter`
- `system/bootup/charactercreation/`: `AppearancePhase.tpl`,
  `BirthdayPhase.tpl` (plus `.de` and `.fr`), `NamePhase.tpl` and
  `WorldSelection.tpl` 1 each, `MenuBigButton.tpl` 2
- `system/bootup/retainer/RetainerMenu.tpl`: 1
- `widget/ActionMenuWidget.tpl`: 1 storyboard-only and 1 with
  `ExecuteCommandAction`
- `widget/ConsoleIconTrayWidget.tpl`, `FellingInputWidget.tpl`,
  `FishingInputWidget.tpl`, `MiningInputWidget.tpl`: 1 each

All 10 triggers that contain a `Setter` are the `TitlePhase` files above. No
other template declares a hover `Setter` inside a `MouseEnter` trigger.

## IsMouseOver conditions

The text `Property="IsMouseOver"` occurs 66 times in 18 files:

- `common/`: `WINBasis`, `WINBasisLight`, `WINBasisWithTitle` and
  `WINBasisWithTitle_noClose`, each as `.tpl` and `.sd.tpl` (8 files)
- `common_c/`: `WINBasis.tpl`, `WINBasisLight.tpl`, `WINBasisWithTitle.tpl`
- `widget/`: `ConfigKeyboardWidget.tpl` and `.sd.tpl`,
  `ConsoleIconTrayWidget.tpl`, `HamletDefenseScoreWidget.tpl`,
  `LogWidget.sd.tpl`, `MainMenuWidget.tpl`
- `widget_c/ConfigKeyboardWidget.tpl`

In `MainMenuWidget.tpl` the condition occurs four times, each in a
`MultiTrigger` paired with `IsKeyboardFocusWithin`, covering both values of
each property.

## DragDrop declarations

`DragDrop.` appears in two files, both under `widget_c/`:

| File | Input bytes | Input SHA-256 | Decoded bytes | Decoded SHA-256 |
| --- | ---: | --- | ---: | --- |
| `widget_c/EquipWidget.tpl` | 2996 | `faa56490f0193bda368fe2d7144ceb17eae59937132c300830c28f90587f7620` | 2988 | `e0d14fec48b46e63f82f915d73974b0143bc80a541dd413bad87491307653c68` |
| `widget_c/EquipItemListWidget.tpl` | 7231 | `72703721d38710dfad448ad42bc6e7ecb044abb70f5354bd41119d4999c3b03f` | 7223 | `27dd310920978c8c218b87ddf64400724e7b38d642c47156ba13ea1c66cf9ec1` |

| Template | `DragDrop.Id` | `DragDrop.SourceCategory` | `DragDrop.DestCategory` |
| --- | ---: | ---: | ---: |
| `ControlTemplate_Button_EquipIcon` (Button) in `EquipWidget.tpl` | 2 | 2 | 1 |
| `DataTemplate_ItemList` in `EquipItemListWidget.tpl` | 1 | 1 | absent |

Each value is a `Setter` at the template's top level. The `widget/` forms and
templates, including their `.sd.` variants, declare no `DragDrop.` property.
No `Style` or `.style` file declares one. The `SkinDroppable` condition
appears in `common_c/default.style` with `Skin="NULL"`.

These are static declarations. The native arming rule for the two ids is in
`xivl-decomp:docs/input/sqwt-mouse-preview-producer.md`, and the drag event
names are in `xivl-decomp:docs/input/sqwt-scroll-and-drag-events.md`. Which
script receives a drop was not found.
