# NamePlateWidget primary row layout

This `client_extraction` finding adds the child order and sizes of
`Grid_NamePlate` to the
[nameplate primary-label form attributes](sqwt-nameplate-primary-label.md),
which holds the input identity, the decoded SHA-256
`de6ca8942674c3d8a8e66e442b4237b2d317dcff47cbe57caedf690505c2649f` (4040
bytes) and the reproduction recipe. The input is
`client/sqwt/system/ingame/NamePlateWidget.form`, build `2012.09.19.0001`.

## Outer grid

The window root holds one `Grid` with two `Auto` rows. Row 0 is a horizontal
`StackPanel`, `HorizontalAlignment="Center"`, with these children in order:

| Child | Declared |
| --- | --- |
| `IconControl_SecondaryRightIcon` | `IconDatas="0"`, `Width="96"`, `Height="96"`, `Collapsed` |
| `TextBlock_SecondaryLabel` | `FontSize="24"`, italic, `Margin="4,0,4,0"`, `Height="36"`, `Collapsed` |

`Grid_NamePlate` declares `Grid.Row="1"` and two `Auto` rows of its own.

## Grid_NamePlate row 0

A horizontal `StackPanel` with `Margin="40,0,40,0"` and
`HorizontalAlignment="Center"`. Its children in order:

1. `IconControl_PrimaryLeftIcon`, `IconDatas="0"`, 36 by 36, `Collapsed`.
2. A `Grid` with `SqwtDrawOrder="0.1"` holding `IconControl_PrimaryRightIcon`,
   `IconDatas="517"`, 36 by 36, `Visible`, and `TextBlock_LebelText`, the level
   text, `Margin="0,0,1,-3"`, right and bottom aligned, `Width="32"`,
   `Visible`.
3. `IconControl_SecondaryLeftIcon`, `IconDatas="0"`, 36 by 36, `Collapsed`.
4. A `Grid` holding `Label_AutoAttack` (`Height="30"`, `Collapsed`,
   `IsHitTestVisible="False"`) and `TextBlock_PrimaryLabel` (`FontSize="24"`,
   italic, `FontEdgeColor="#ff262626"`, `Margin="4,0,4,0"`, `Height="36"`).
5. `IconControl_AutoAttack`, `IconDatas="539"`, 36 by 36, `Collapsed`,
   `Focusable="False"`.

## Grid_NamePlate row 1

A centred `Grid` with two `Auto` columns: `Label_HateSignal` in column 0
(`Margin="0,0,6,0"`, `Collapsed`, template `ControlTemplate_Label_HateSignal`)
and `ProgressBar_HP` in column 1 (`Maximum="999"`, `Width="120"`, visible).

## Boundary

The form states sizes as bare numbers. The unit that maps one declared unit to
a drawn pixel and the vertical centring on the label are not stated in the
form. The tick that shows or hides the primary controls is a native contract
in [xivl-decomp:docs/actor/player-nameplate-icons.md](https://github.com/XIVLegacy/xivl-decomp/blob/main/docs/actor/player-nameplate-icons.md).
